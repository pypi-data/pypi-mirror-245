# Databricks notebook source
# MAGIC %md
# MAGIC #### Main Anomaly Detector for DQS **`(Data Quality Service)`** <br>

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ##### Setup

# COMMAND ----------

_run_params = dict(dbutils.notebook.entry_point.getCurrentBindings())

# COMMAND ----------

# DBTITLE 1,Install required Packages
!/databricks/python/bin/pip install --upgrade pip
!/databricks/python/bin/pip install --upgrade numpy
!/databricks/python/bin/pip install plotly kaleido nbformat numpy prophet==1.1.1 slack-sdk pillow holidays==0.24 # Recent release of holidays==0.25 breaks prophet=1.1.1 & 1.1.2

# COMMAND ----------

import numpy as np
import logging, os, ast
import pandas as pd
from prophet import Prophet
from slack_sdk import WebClient
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

# COMMAND ----------

# MAGIC %md
# MAGIC ###### Get Parameters

# COMMAND ----------

DATASET = _run_params['metric_source_table']
PERIOD_TYPE = _run_params.get('period_type', 'DAILY')

_top_n_measure_ops = ast.literal_eval(_run_params.get('top_n_measure_ops', "['sum']"))
_top_n_measures = ast.literal_eval(_run_params.get('top_n_measures', "[]"))
TOP_N_MEASURES = ['num_count'] + [f"{ops}_{measure}" for ops in _top_n_measure_ops for measure in _top_n_measures]
TOP_N_DIMENSIONS = ast.literal_eval(_run_params.get('top_n_dimensions', "['__na__']"))
TOP_N_EXTENDED_MEASURES = TOP_N_MEASURES

if ast.literal_eval(_run_params.get('include_null_counts', "True")):
    TOP_N_EXTENDED_MEASURES = TOP_N_EXTENDED_MEASURES + [f"count_null_{dim}" for dim in TOP_N_DIMENSIONS]
if ast.literal_eval(_run_params.get('include_dist_counts', "True")):
    TOP_N_EXTENDED_MEASURES = TOP_N_EXTENDED_MEASURES + [f"num_dist_{dim}" for dim in TOP_N_DIMENSIONS]

END_PERIOD = _run_params.get('end_period', (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))
START_PERIOD = (datetime.strptime(END_PERIOD, '%Y-%m-%d') - timedelta(days=int(_run_params.get('ml_lookback_days', 700)))).strftime('%Y-%m-%d')
NUM_FORECAST_PERIODS = int(_run_params.get('num_forcast_periods', 7))

DQS_DIR = _run_params.get('dqs_dir', '/dbfs/dmeci/data_quality_framework/')
IMAGE_DIR = f'{DQS_DIR}images/'
NUM_IMAGES_PER_PAGE = int(_run_params.get('num_images_per_page', 2))

LINE_COLORS = ['68, 46, 209', '212, 57, 101', '181, 70, 22', '81, 176, 77', '31, 119, 180']
BAND_COLORS = ['173, 167, 209', '212, 165, 178', '209, 165, 146', '161, 199, 159', '137, 172, 196']

NUM_TOP_CONTRIBUTORS = int(_run_params.get('num_top_contributors', 3))
NUM_DATE_ALERTS_PER_KEY_MEASURE = int(_run_params.get('num_date_alerts_per_key_measure', 2))
NUM_LATEST_DATES_TO_EXCLUDE = int(_run_params.get('num_latest_dates_to_exclude', 2))

MEASURES_NUM_LATEST_DATES_TO_EXCLUDE = {}
for _measure in ast.literal_eval(_run_params.get('measures_num_latest_dates_to_exclude', "[]")): MEASURES_NUM_LATEST_DATES_TO_EXCLUDE[_measure['measure']] = _measure['num_latest_dates_to_exclude']

NUM_DAYS_IGNORE_ANOMS_OLDER_THAN =int( _run_params.get('num_days_ignore_anoms_older_than', 60))

PROPHET_PARAMS = ast.literal_eval(_run_params.get('prophet_params', """{
    'daily_seasonality': False, 
    'yearly_seasonality': True, 
    'weekly_seasonality': True, 
    'seasonality_mode': 'multiplicative', 
    'interval_width': 0.97, 
    'changepoint_range': 0.9
}"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ###### Get Outliers & Ignores

# COMMAND ----------

# Get Outlier Periods
OUTLIER_PERIODS = spark.sql("""
  SELECT DISTINCT outlier_date
  FROM ccea_prod.dq_outliers
  WHERE metric_source_table = '{metric_source_table}'
""".format(metric_source_table=DATASET)).toPandas()['outlier_date'].values.tolist()

OUTLIER_PERIODS

# COMMAND ----------

# Get Ignore Periods
IGNORE_PERIODS = spark.sql("""
  SELECT DISTINCT ignore_date
  FROM ccea_prod.dq_ignores
  WHERE metric_source_table = '{metric_source_table}'
""".format(metric_source_table=DATASET)).toPandas()['ignore_date'].values.tolist()

IGNORE_PERIODS

# COMMAND ----------

# MAGIC %md
# MAGIC ###### Get Date DF, Measures, & Dimensions

# COMMAND ----------

# DBTITLE 0,Get Date DF
if PERIOD_TYPE == 'DAILY':

    date_df = spark.sql("""

        SELECT 
            date_date AS date,
            fiscal_yr_and_wk_desc,
            fiscal_yr_and_qtr_desc,
            RANK() OVER (PARTITION BY fiscal_yr_and_qtr_desc ORDER BY date_date) AS qtr_index,
            fiscal_yr,
            RANK() OVER (PARTITION BY fiscal_yr ORDER BY date_date) AS yr_index
        FROM ids_coredata.dim_date
        WHERE date_date BETWEEN '{start_period}' AND '{end_period}' 
        ORDER BY 1

    """.format(start_period=START_PERIOD, end_period=END_PERIOD)).toPandas()

elif  PERIOD_TYPE == 'FISCAL_WK':

    date_df = spark.sql("""

        WITH wk_data AS (
        SELECT DISTINCT
            TO_DATE(fiscal_wk_ending_date) AS date,
            fiscal_yr_and_wk_desc,
            fiscal_yr_and_qtr_desc,
            fiscal_yr
        FROM ids_coredata.dim_date
        WHERE fiscal_yr BETWEEN YEAR('{start_period}') AND YEAR('{end_period}')
        ORDER BY 1
        ), indexed AS (
        SELECT
            date,
            fiscal_yr_and_wk_desc,
            fiscal_yr_and_qtr_desc,
            RANK() OVER (PARTITION BY fiscal_yr_and_qtr_desc ORDER BY fiscal_yr_and_wk_desc) AS qtr_index,
            fiscal_yr,
            RANK() OVER (PARTITION BY fiscal_yr ORDER BY fiscal_yr_and_wk_desc) AS yr_index
        FROM wk_data
        )
        SELECT date, fiscal_yr_and_wk_desc, fiscal_yr_and_qtr_desc, qtr_index, fiscal_yr, yr_index
        FROM indexed
        WHERE date BETWEEN '{start_period}' AND DATE_ADD('{end_period}', {forecast_period} * 7)

    """.format(start_period=START_PERIOD, end_period=END_PERIOD, forecast_period=NUM_FORECAST_PERIODS)).toPandas()

date_df = date_df.rename(columns={'date': 'ds'});
date_df['ds'] = pd.to_datetime(date_df['ds'])

date_df.head(15)

# COMMAND ----------

extended_measures = ', '.join([f"'{measure}'" for measure in TOP_N_EXTENDED_MEASURES])
measures = ', '.join([f"'{measure}'" for measure in TOP_N_MEASURES if not (measure.startswith('count_null_') or measure.startswith('num_dist_'))])
print(extended_measures)
print(measures)

# COMMAND ----------

dimensions_df = spark.sql("""

    WITH base_metrics AS (

      SELECT
        metric_calc_period AS date,
        MAP_KEYS(metric_dimensions)[0] AS dimension_key,
        MAP_VALUES(metric_dimensions)[0] AS dimension_value,
        metric_name,
        metric_value
      FROM ccea_prod.dq_metrics
      WHERE metric_calc_period BETWEEN '{start_period}' AND '{end_period}' 
           AND metric_source_table = '{dataset}' 
           AND metric_name IN ({measures})
           AND SIZE(metric_dimensions) = 1

    ), pivoted_metrics AS (

      SELECT *
      FROM base_metrics
      PIVOT (
        SUM(metric_value) AS metric_value
        FOR metric_name IN ({measures})
      )

    )

    SELECT *
    FROM pivoted_metrics
    WHERE dimension_key IN ({dimensions})
    ORDER BY date

""".format(start_period=START_PERIOD, end_period=END_PERIOD, dataset=DATASET, measures=extended_measures, dimensions=', '.join([f"'{dimension}'" for dimension in TOP_N_DIMENSIONS]))).toPandas();

dimensions_df = dimensions_df.drop(['num_dist___na__','count_null___na__'], axis=1, errors='ignore')
dimensions_df = dimensions_df.rename(columns={'date': 'ds'});
dimensions_df['ds'] = pd.to_datetime(dimensions_df['ds'])

dimensions_df.head(10)

# COMMAND ----------

dim_df = date_df
dim_keys = []
for dim_key, df in dimensions_df.groupby('dimension_key'):
    dim_keys.append(dim_key)
    for dim_value, df in df.groupby('dimension_value'):
        data = df.drop(columns=['dimension_key', 'dimension_value'])
        data.columns = ['ds'] + [f'{dim_key}:{dim_value}|' + col for col in data.columns if col != 'ds']
        data = date_df[['ds']].merge(data, on='ds', how='left').fillna(0)
        dim_df = dim_df.merge(data, on='ds', how='left')

dim_df.tail()

# COMMAND ----------

measures_df = spark.sql("""

    WITH base_metrics AS (

      SELECT
        metric_calc_period AS date,
        metric_name,
        metric_value
      FROM ccea_prod.dq_metrics
      WHERE metric_calc_period BETWEEN '{start_period}' AND '{end_period}' 
           AND metric_source_table = '{dataset}' 
           AND metric_name IN ({measures})
           AND metric_dimensions IS NULL

    ), pivoted_metrics AS (

      SELECT *
      FROM base_metrics
      PIVOT (
        SUM(metric_value) AS metric_value
        FOR metric_name IN ({measures})
      )

    )

    SELECT *
    FROM pivoted_metrics
    ORDER BY date

""".format(start_period=START_PERIOD, end_period=END_PERIOD, dataset=DATASET, measures=extended_measures)).toPandas();

measures_df = measures_df.drop(['num_dist___na__','count_null___na__'], axis=1, errors='ignore')
measures_df = measures_df.rename(columns={'date': 'ds'});
measures_df['ds'] = pd.to_datetime(measures_df['ds'])

measures_df.head(10)

# COMMAND ----------

extended_measures_metrics = [metric for metric in measures_df.columns]
measures_metrics = [metric for metric in measures_df.columns if not (metric.startswith('count_null_') or metric.startswith('num_dist_'))]
measures_metrics.remove('ds')
extended_measures_metrics.remove('ds')
measures_metrics

# COMMAND ----------

dimensions_metrics = list(dim_df.columns)
dimensions_metrics.remove('ds')
dimensions_metrics.remove('fiscal_yr_and_wk_desc')
dimensions_metrics.remove('fiscal_yr_and_qtr_desc')
dimensions_metrics.remove('fiscal_yr')
dimensions_metrics.remove('qtr_index')
dimensions_metrics.remove('yr_index')
dimensions_metrics

# COMMAND ----------

# MAGIC %md
# MAGIC ###### Get top N contributors by dimension per measure

# COMMAND ----------

_all_df = measures_df.merge(dim_df, on='ds', how='left')
top_dimensions_metrics = []

for measure in measures_metrics:
    for _dim in dimensions_metrics:
        if _dim.split('|')[1] == measure:
            _all_df['cont_' + _dim] = _all_df[_dim]/_all_df[measure]

    for dim_key in dim_keys:
        last_entry = _all_df.tail(1)[['cont_' + dim_metric for dim_metric in dimensions_metrics if dim_metric.split('|')[1] == measure and dim_metric.split(':')[0] == dim_key]].T
        last_entry = last_entry.sort_values(last_entry.columns[0], ascending=False)
        top_dimensions_metrics = top_dimensions_metrics + [_dim[5:] for _dim in last_entry.index.values[:NUM_TOP_CONTRIBUTORS]]

top_dimensions_metrics

# COMMAND ----------

# MAGIC %md
# MAGIC ###### Merge Dimensions & Measures + WoW Changes

# COMMAND ----------

all_df = measures_df.merge(dim_df[(['ds', 'fiscal_yr_and_wk_desc', 'fiscal_yr_and_qtr_desc', 'fiscal_yr', 'qtr_index', 'yr_index']) + dimensions_metrics], on='ds', how='right')

all_df.tail(10)

# COMMAND ----------

metrics = list(all_df.columns)
metrics.remove('ds')
#if PERIOD_TYPE == 'FISCAL_WK': 
metrics.remove('fiscal_yr_and_wk_desc')
metrics.remove('fiscal_yr_and_qtr_desc')
metrics.remove('fiscal_yr')
metrics.remove('qtr_index')
metrics.remove('yr_index')

pct_change_df = all_df[metrics].pct_change(periods=7 if PERIOD_TYPE == 'DAILY' else 1)
pct_change_df.columns = ['wow_' + col for col in pct_change_df.columns]

#if PERIOD_TYPE == 'FISCAL_WK': 

for metric in metrics:
    pct_change_df['qoq_' + metric] = all_df.groupby(['qtr_index'])[metric].apply(lambda x:(x.pct_change()))
    pct_change_df['yoy_' + metric] = all_df.groupby(['yr_index'])[metric].apply(lambda x:(x.pct_change()))

all_df = pd.concat([all_df, pct_change_df], axis=1)

pct_change_metrics = pct_change_df.columns.tolist()

all_df.tail(10)

# COMMAND ----------

# DBTITLE 1,Exclude Next Week for Outliers
_outliers_following_week = [(pd.to_datetime(date) + pd.DateOffset(days= 7 if PERIOD_TYPE == 'DAILY' else 1)).strftime('%Y-%m-%d') for date in OUTLIER_PERIODS]
for metric in pct_change_metrics:
    all_df.loc[all_df['ds'].isin(_outliers_following_week), metric] = None

all_df

# COMMAND ----------

# MAGIC %md
# MAGIC ##### ML Training and Fitting

# COMMAND ----------

res_all_df = all_df[(['ds'] if PERIOD_TYPE == 'DAILY' else ['ds', 'fiscal_yr_and_wk_desc']) + pct_change_metrics]

for metric in extended_measures_metrics + top_dimensions_metrics:

    data = all_df[['ds', metric]].rename(columns={metric: 'y'}).copy()

    # Exclude outliers from training data
    data.loc[data['ds'].isin(OUTLIER_PERIODS), metric] = None

    # Train model
    m = Prophet(**PROPHET_PARAMS)
    m.fit(data if PERIOD_TYPE == 'DAILY' else data[:-NUM_FORECAST_PERIODS])
    to_pred = (data).reset_index().drop(columns=['index'])
    _future = m.make_future_dataframe(NUM_FORECAST_PERIODS, include_history=True)
    to_pred = to_pred.merge(_future, on='ds', how='outer')
    _pred = m.predict(to_pred)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    data = data.merge(_pred, on='ds', how='outer')
    data['isAnomaly'] = data['y'].gt(data['yhat_upper']) | data['y'].lt(data['yhat_lower'])
    
    data.columns = ['ds', metric] + [f"{metric}:{col}" for col in data.columns if col not in ['ds', 'y']]

    res_all_df = res_all_df.merge(data, on='ds', how='outer')

    if PERIOD_TYPE == 'FISCAL_WK': res_all_df = res_all_df[res_all_df['fiscal_yr_and_wk_desc'].notnull()]

res_all_df.tail(15)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Generate Highlights

# COMMAND ----------

highlights = []

_max_anom_date = (datetime.today() - timedelta(days=NUM_DAYS_IGNORE_ANOMS_OLDER_THAN)).strftime('%Y-%m-%d')

data = res_all_df[(-90 - NUM_FORECAST_PERIODS): -1 * NUM_FORECAST_PERIODS - NUM_LATEST_DATES_TO_EXCLUDE]

for measure in extended_measures_metrics:

    data.loc[data['ds'].isin(OUTLIER_PERIODS), measure] = None
    data.loc[data['ds'].isin(IGNORE_PERIODS), measure] = None
    _measure_data = data[['ds', measure, 'wow_' + measure, 'qoq_' + measure, 'yoy_' + measure, measure + ':isAnomaly']]
    _measure_anom = _measure_data[_measure_data[measure + ':isAnomaly']].dropna()

    _measure_dt = {'measure': measure, 'dates': []}

    _max_measure_anom_date = (datetime.strptime(END_PERIOD, '%Y-%m-%d') - timedelta(days=MEASURES_NUM_LATEST_DATES_TO_EXCLUDE.get(measure.split('_', 1)[1], 0))).strftime('%Y-%m-%d')

    for dimension in top_dimensions_metrics:
        if dimension.split('|')[1] == measure:
            _dim_data = res_all_df[['ds', dimension, 'wow_' + dimension, 'qoq_' + dimension, 'yoy_' + dimension, dimension + ':isAnomaly']]
            _dim_anom = _dim_data[_dim_data[dimension + ':isAnomaly']].dropna()
            _measure_anom = _measure_anom.merge(_dim_anom, on='ds', how='left')
    
    for index, row in _measure_anom.iterrows():

        if row['ds'].strftime('%Y-%m-%d') < _max_anom_date or row['ds'].strftime('%Y-%m-%d') > _max_measure_anom_date:
            continue

        _tmp = {'ds': row['ds'].strftime('%Y-%m-%d'), 'wow_measure': row['wow_' + measure] * 100, 'qoq_measure': row['qoq_' + measure] * 100, 'yoy_measure': row['yoy_' + measure] * 100, 'dimensional_breakdown': []}

        for dimension in top_dimensions_metrics:
            if dimension.split('|')[1] == measure and not pd.isnull(row[dimension + ':isAnomaly']) and row[dimension + ':isAnomaly']:

                _tmp['dimensional_breakdown'].append({'dimension': dimension, 'wow_dimension': row['wow_' + dimension] * 100, 'qoq_dimension': row['qoq_' + dimension] * 100, 'yoy_dimension': row['yoy_' + dimension] * 100})

        _measure_dt['dates'].append(_tmp)

    highlights.append(_measure_dt)

highlights

# COMMAND ----------

highlight_msg = ''
highlight_msg_blocks = []

anom_extended_measures_metrics = []
anom_top_dimensions_metrics = []

for highlight in highlights:

    if len(highlight['dates']) > 0:

        anom_extended_measures_metrics.append(highlight['measure'])

        _msg = f"*{highlight['measure'].upper()}*\n"
        
        highlight_msg_blocks.append({
            "type": "section", 
            "text": {
                "type": "mrkdwn", 
                "text": f"*{highlight['measure'].upper()}*"
            }
        })

        for date in sorted(highlight['dates'], key=lambda d: d['ds'], reverse=True)[:NUM_DATE_ALERTS_PER_KEY_MEASURE]:

            tmp_msg = f"On *{date['ds']}*, there was a *{abs(date['wow_measure']):.1f}%* WoW _{'drop' if date['wow_measure'] < 0 else 'rise'}_ ({abs(date['qoq_measure']):.1f}% QoQ {'drop' if date['qoq_measure'] < 0 else 'rise'}, {abs(date['yoy_measure']):.1f}% YoY {'drop' if date['yoy_measure'] < 0 else 'rise'}) in {highlight['measure']}"

            _msg = _msg + f"On *{date['ds']}*, there was a *{abs(date['wow_measure']):.1f}%* WoW _{'drop' if date['wow_measure'] < 0 else 'rise'}_ ({abs(date['qoq_measure']):.1f}% QoQ {'drop' if date['qoq_measure'] < 0 else 'rise'}, {abs(date['yoy_measure']):.1f}% YoY {'drop' if date['yoy_measure'] < 0 else 'rise'}) in {highlight['measure']}"

            if(len(date['dimensional_breakdown']) > 0):
                _msg = _msg + ' mainly due to a:\n'
                _msg = _msg + ''.join(f">{abs(dim_brk['wow_dimension']):.1f}% WoW {'drop' if dim_brk['wow_dimension'] < 0 else 'rise'} ({abs(dim_brk['qoq_dimension']):.1f}% QoQ {'drop' if dim_brk['qoq_dimension'] < 0 else 'rise'}, {abs(dim_brk['yoy_dimension']):.1f}% YoY {'drop' if dim_brk['yoy_dimension'] < 0 else 'rise'}) in {' = '.join(dim_brk['dimension'].split('|')[0].split(':'))}\n" for dim_brk in sorted(date['dimensional_breakdown'], key=lambda d: (d['dimension'].split('|')[0].split(':')[0], abs(d['wow_dimension'])), reverse=True))

                tmp_msg = tmp_msg + ' mainly due to a:\n'
                tmp_msg = tmp_msg + ''.join(f">{abs(dim_brk['wow_dimension']):.1f}% WoW {'drop' if dim_brk['wow_dimension'] < 0 else 'rise'} ({abs(dim_brk['qoq_dimension']):.1f}% QoQ {'drop' if dim_brk['qoq_dimension'] < 0 else 'rise'}, {abs(dim_brk['yoy_dimension']):.1f}% YoY {'drop' if dim_brk['yoy_dimension'] < 0 else 'rise'}) in {' = '.join(dim_brk['dimension'].split('|')[0].split(':'))}\n" for dim_brk in sorted(date['dimensional_breakdown'], key=lambda d: (d['dimension'].split('|')[0].split(':')[0], abs(d['wow_dimension'])), reverse=True))

                for d in date['dimensional_breakdown']:
                    anom_top_dimensions_metrics.append(d['dimension'])

            else:
                _msg = _msg + '.\n'
                tmp_msg = tmp_msg + '.'

            _msg = _msg + '\n'        
            highlight_msg_blocks.append({
                "type": "section", 
                "text": {
                    "type": "mrkdwn", 
                    "text": tmp_msg
                }
            })
            highlight_msg_blocks.append({
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action",
                    "multiline": False,
                    "dispatch_action_config": {
                        "trigger_actions_on": [
                            "on_enter_pressed"
                        ]
                    },
                    "placeholder": {
                        "type": "plain_text",
                        "text": f"Fill in the reason for this anomaly on {highlight['measure'].upper()} for {date['ds']} if it is known",
                        "emoji": True
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": " ",
                    "emoji": True
                }
            })

            highlight_msg_blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Known Anomaly"
                        },
                        "style": "primary",
                        "value": "click_me_123"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Ignore Anomaly"
                        },
                        "confirm": {
                            "title": {
                                "type": "plain_text",
                                "text": "Are you sure?"
                            },
                            "text": {
                                "type": "mrkdwn",
                                "text": "Once ignored, you will no longer receive alerts about this anomaly"
                            },
                            "confirm": {
                                "type": "plain_text",
                                "text": "Yes, Ignore"
                            },
                            "deny": {
                                "type": "plain_text",
                                "text": "Stop, I've changed my mind!"
                            }
                        },
                        "value": "click_me_123"
                    }
                ]
            },)

        _msg = _msg + '\n'
        highlight_msg = highlight_msg + _msg

        highlight_msg_blocks.append({
			"type": "divider"
		})

print(highlight_msg)
print(highlight_msg_blocks)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Plotting and Alerting

# COMMAND ----------

# Split in groups of NUM_IMAGES_PER_PAGE
measures_metric_gps = [anom_extended_measures_metrics[i:i + NUM_IMAGES_PER_PAGE] for i in range(0, len(extended_measures_metrics), NUM_IMAGES_PER_PAGE)]
dimensions_metric_gps = [anom_top_dimensions_metrics[i:i + NUM_IMAGES_PER_PAGE] for i in range(0, len(anom_top_dimensions_metrics), NUM_IMAGES_PER_PAGE)]

measures_metric_gps = [gp for gp in measures_metric_gps if len(gp) > 0]
dimensions_metric_gps = [gp for gp in dimensions_metric_gps if len(gp) > 0]
metric_gps = measures_metric_gps + dimensions_metric_gps
metric_gps

# COMMAND ----------

if len(metric_gps) < 1:
    dbutils.notebook.exit("SUCCESS")

# COMMAND ----------

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
from random import *
import plotly.io as pio

pyLogo = Image.open(DQS_DIR + 'logo_on_transparent_bg.png')

for _gp in metric_gps:

    fig = make_subplots(
            rows=len(_gp), cols=1, 
            specs=[[{"secondary_y": True}]] * len(_gp), 
            subplot_titles=[f"<span style='font-size: 13px; color: black'><i>{DATASET}</i> - <b> {metric.split('|')[1] + '</b> | ' + ' = '.join(metric.split('|')[0].split(':')) if len(metric.split('|')) > 1 else metric + '</b>'}</span>" for metric in _gp], 
            shared_xaxes=False,
            vertical_spacing=0.1
    )

    _row = 1
    _col = 1

    for id, metric in enumerate(_gp):

        data = res_all_df[(-90 - NUM_FORECAST_PERIODS): -1 * NUM_FORECAST_PERIODS]  
        _data = data[data[metric + ':isAnomaly']].reset_index()
        _anom_data = _data[~_data['ds'].isin(OUTLIER_PERIODS)]
        _outlier_data = _data[_data['ds'].isin(OUTLIER_PERIODS)]
        _forecast_data = res_all_df[-1 * NUM_FORECAST_PERIODS - 1:]

        color_idx = randint(0, len(LINE_COLORS) - 1)

        ## Actual and Expected

        fig.add_trace(
            go.Scatter(
                name='Actual',
                x=data['ds'] if PERIOD_TYPE == 'DAILY' else data['fiscal_yr_and_wk_desc'],
                y=data[metric],
                mode='lines',
                line=dict(color=f"rgb({LINE_COLORS[color_idx]})", width=1),
                line_shape='spline',
                showlegend=True, #if _row < 2 else False,
                legendgroup=id #'anomaly'
            ),
            row=_row, col=_col
        )

        fig.add_trace(
            go.Scatter(
                name='Expected',
                x=res_all_df[-90:]['ds'] if PERIOD_TYPE == 'DAILY' else res_all_df[-90:]['fiscal_yr_and_wk_desc'],
                y=res_all_df[-90:][metric + ':yhat'],
                mode='lines',
                line=dict(color=f"rgba({LINE_COLORS[(color_idx + 1) % len(LINE_COLORS)]}, 0.6)", width=1, dash='dot'),
                line_shape='spline',
                showlegend=True, #if _row < 2 else False
                legendgroup=id
            ),
            row=_row, col=_col
        )

        ## WoW / QoQ / YoY % Change

        fig.add_trace(
            go.Scatter(
                name='%△ WoW',
                x=data['ds'] if PERIOD_TYPE == 'DAILY' else data['fiscal_yr_and_wk_desc'],
                y=data['wow_' + metric],
                mode='lines',
                line=dict(color=f"rgba({LINE_COLORS[(color_idx + 2) % len(LINE_COLORS)]}, 0.45)", width=1, dash='dash'),
                showlegend=True,
                line_shape='linear',
                legendgroup=id
            ),
            secondary_y=True,
            row=_row, col=_col
        )

        fig.add_trace(
            go.Scatter(
                name='%△ QoQ',
                x=data['ds'] if PERIOD_TYPE == 'DAILY' else data['fiscal_yr_and_wk_desc'],
                y=data['qoq_' + metric],
                mode='lines',
                line=dict(color=f"rgba({LINE_COLORS[(color_idx + 3) % len(LINE_COLORS)]}, 0.45)", width=1, dash='dash'),
                showlegend=True,
                line_shape='linear',
                legendgroup=id
            ),
            secondary_y=True,
            row=_row, col=_col
        )

        fig.add_trace(
            go.Scatter(
                name='%△ YoY',
                x=data['ds'] if PERIOD_TYPE == 'DAILY' else data['fiscal_yr_and_wk_desc'],
                y=data['yoy_' + metric],
                mode='lines',
                line=dict(color=f"rgba({LINE_COLORS[(color_idx + 4) % len(LINE_COLORS)]}, 0.45)", width=1, dash='dash'),
                showlegend=True,
                line_shape='linear',
                legendgroup=id
            ),
            secondary_y=True,
            row=_row, col=_col
        )

        ## Upper and Lower Bound

        fig.add_trace(
            go.Scatter(
                name=metric + ':yhat_upper',
                x=data['ds'] if PERIOD_TYPE == 'DAILY' else data['fiscal_yr_and_wk_desc'],
                y=data[metric + ':yhat_upper'],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False,
                line_shape='spline',
                legendgroup=id
            ),
            row=_row, col=_col
        )

        fig.add_trace(
            go.Scatter(
                name=metric + ':yhat_lower',
                x=data['ds'] if PERIOD_TYPE == 'DAILY' else data['fiscal_yr_and_wk_desc'],
                y=data[metric + ':yhat_lower'],
                marker=dict(color="#444"),
                line=dict(width=0),
                mode='lines',
                fillcolor=f"rgba({BAND_COLORS[color_idx]}, 0.35)",
                fill='tonexty',
                showlegend=False,
                line_shape='spline',
                legendgroup=id
            ),
            row=_row, col=_col
        )

        ## Anomalies and Known Outliers

        fig.add_trace(
            go.Scatter(
                name="Anomaly",
                x=_anom_data["ds"] if PERIOD_TYPE == 'DAILY' else _anom_data['fiscal_yr_and_wk_desc'],
                y=_anom_data[metric],
                marker=dict(color="#8F1A18"),
                text=_anom_data["ds"].dt.date if PERIOD_TYPE == 'DAILY' else _anom_data['fiscal_yr_and_wk_desc'],
                mode='markers+text',
                textposition="bottom center",
                showlegend=True, #if _row < 2 else False,
                legendgroup=id #legendgroup='anomaly'
            ),
            row=_row, col=_col
        )

        fig.add_trace(
            go.Scatter(
                name="Known Outlier",
                x=_outlier_data["ds"] if PERIOD_TYPE == 'DAILY' else _outlier_data['fiscal_yr_and_wk_desc'],
                y=_outlier_data[metric],
                marker=dict(color="#4725f5"),
                text=_outlier_data["ds"].dt.date if PERIOD_TYPE == 'DAILY' else _outlier_data['fiscal_yr_and_wk_desc'],
                mode='markers+text',
                textposition="bottom center",
                showlegend=True, #if _row < 2 else False,
                legendgroup=id #legendgroup='outlier'
            ),
            row=_row, col=_col
        )

        ## Forecast
        fig.add_trace(
            go.Scatter(
                name=metric + ':yhat_upper',
                x=_forecast_data['ds'] if PERIOD_TYPE == 'DAILY' else _forecast_data['fiscal_yr_and_wk_desc'],
                y=_forecast_data[metric + ':yhat_upper'],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False,
                line_shape='spline',
                legendgroup=id
            ),
            row=_row, col=_col
        )

        fig.add_trace(
            go.Scatter(
                name='Forecast',
                x=_forecast_data['ds'] if PERIOD_TYPE == 'DAILY' else _forecast_data['fiscal_yr_and_wk_desc'],
                y=_forecast_data[metric + ':yhat_lower'],
                marker=dict(color="#444"),
                line=dict(width=0),
                mode='lines',
                fillpattern=dict(fgcolor=f"rgba({BAND_COLORS[color_idx]}, 0.45)", fillmode='replace', shape='/'),
                fillcolor=f"rgba({BAND_COLORS[color_idx]}, 0.45)",
                fill='tonexty',
                showlegend=True,
                legendgroup=id, #legendgroup='forecast',
                line_shape='spline'
            ),
            row=_row, col=_col
        )


        _row = _row + 1

    fig.for_each_xaxis(lambda x: x.update(showgrid=True, linewidth=0, gridwidth=0, gridcolor='rgba(36, 41, 46, 0.07)', griddash='solid', nticks=25, color='rgb(36, 41, 46)', tickfont=dict(size=12, family='Adobe Clean'), minor=dict(ticklen=0, gridcolor="rgba(36, 41, 46, 0.07)", showgrid=True), type='date' if PERIOD_TYPE == 'DAILY' else 'category', tickangle=-45 if PERIOD_TYPE != 'DAILY' else 0))
    fig.for_each_yaxis(lambda y: y.update(showgrid=True, linewidth=0, gridwidth=0, gridcolor='rgba(36, 41, 46, 0.07)', griddash='solid', title_standoff=10, color='rgb(36, 41, 46)', tickfont=dict(size=12, family='Adobe Clean')))

    fig.layout.images = [dict(
        source=pyLogo,
        xref="paper", yref="paper",
        x=1.04, y=-0.005,
        sizex=0.085, sizey=0.085,
        xanchor="center", yanchor="bottom",
        layer='above'
      )]

    fig.update_layout(
        font_family='Adobe Clean',
        hovermode="x",
        yaxis2={'tickformat': '.0%', 'showgrid': False},
        yaxis4={'tickformat': '.0%', 'showgrid': False},
        paper_bgcolor='rgb(244, 245, 245)',
        plot_bgcolor='rgb(244, 245, 245)',
        showlegend=True,
        legend_traceorder="grouped",
        legend_tracegroupgap = 300,
        margin=go.layout.Margin(l=25, r=25, b=25, t=25),
        width=1700, height=400 * len(_gp)
    )

    fig.show()

    pio.write_image(fig, IMAGE_DIR + DATASET + '-'.join([val.replace('/', '_') for val in _gp]) + '.jpg', format='jpg', scale=2.5, width=1700)


# COMMAND ----------

# DBTITLE 1,Alert via Slack
SLACK_BOT_TOKEN = _run_params.get('slack_bot_token', 'xoxb-259334933125-2780256816183-FEkYMrM3e7uzFaaotxpZRsoa')
SLACK_CHANNEL_ID = _run_params.get('slack_channel_id', 'C0568U1MA4W')

client = WebClient(SLACK_BOT_TOKEN, timeout=300)

highlight_msg_blocks.append({
    "type": "context",
    "elements": [
        {
            "type": "mrkdwn",
            "text": "Generated by the <https://wiki.corp.adobe.com/display/CCEA/Implementation|*DQS Anomaly Detector*>"
        }
    ]
})

message = f'Data Quality Check complete for *{DATASET}*. Please review the summary below for _key measure_ checks and follow the thread for _key dimensional_ breakdowns.\n\n A more detailed analysis can be performed <https://dmeci.corp.ethos53-prod-or2.prod.ethos.corp.adobe.com/d/9HE7If1Vz/dqs-data-quality-service?orgId=1&var-metric_source_table={DATASET}|here>.\n\n {highlight_msg} \n' #<@U022RPJT7K9>

thread_message = 'Attached are dimensional breakdowns of the data quality checks.'

for _gp in measures_metric_gps:
    metric_file = IMAGE_DIR + DATASET + '-'.join(_gp) + '.jpg'
    upload = client.files_upload_v2(file=metric_file)
    message = message + "<" + upload["file"]["permalink"] + "| >"

for _gp in dimensions_metric_gps:
    metric_file = IMAGE_DIR + DATASET + '-'.join([val.replace('/', '_') for val in _gp]) + '.jpg'
    upload = client.files_upload_v2(file=metric_file)
    thread_message = thread_message + "<" + upload["file"]["permalink"] + "| >"

highlight_msg_blocks = [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": message
        }
    },
    {
        "type": "divider"
    }
] + highlight_msg_blocks

_parent_msg = client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=message) #, blocks=highlight_msg_blocks)
_thread_msg = client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=thread_message, thread_ts=_parent_msg['ts'])
