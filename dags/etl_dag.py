from datetime import datetime, timedelta
import os, sql
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'natalia_m',
    'start_date': datetime(2019, 11, 7),
    'retries': 3,
    'retry_delay': timedelta(minutes=3)
}

dag = DAG('sparkify_etl_task2',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@daily' #'0 * * * *'
        )

start_operator = DummyOperator(task_id='Start_ETL',  dag=dag)

# Load and transfor JSON data from S3 to staging table

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='stage_events_task',
    dag=dag,
    table="staging_events",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-dend",
    s3_key="log_data/",
    file_type="json",
    json_path="s3://udacity-dend/log_json_path.json"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='stage_songs_task',
    dag=dag,
    table="staging_songs",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-dend",
    s3_key="song_data/",
    file_type="json",
    json_path="auto"
)

# Load from staging to Redshift

load_songplays_table = LoadFactOperator(
    task_id='load_songplays_fact_table_task',
    dag=dag,
    redshift_conn_id="redshift",
    table="songplays",
    sql_source=SqlQueries.songplay_table_insert 
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='load_user_dim_table_task',
    dag=dag,
    redshift_conn_id="redshift",
    table='users',
    sql_source=SqlQueries.user_table_insert
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='load_song_dim_table_task',
    dag=dag,
    redshift_conn_id="redshift",
    table='songs',
    sql_source=SqlQueries.song_table_insert
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='load_artist_dim_table_task',
    dag=dag,
    redshift_conn_id="redshift",
    table='artists',
    sql_source=SqlQueries.artist_table_insert
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='load_time_dim_table_task',
    dag=dag,
    redshift_conn_id="redshift",
    table='time',
    sql_source=SqlQueries.time_table_insert
)

# Run quality check 
quality_checks = DataQualityOperator(
    task_id='data_quality_checks_task',
    dag=dag,
    all_tables=['songplays','users','songs','artists','time'],
    redshift_conn_id = 'redshift',
)

end_operator = DummyOperator(task_id='End_of_ETL',  dag=dag)

#####
start_operator >> stage_events_to_redshift
start_operator >> stage_songs_to_redshift

# From staging to fact and dim tables
stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table
stage_events_to_redshift >> load_user_dimension_table 
stage_songs_to_redshift >> load_song_dimension_table 
stage_songs_to_redshift >> load_artist_dimension_table 
load_songplays_table >> load_time_dimension_table 

load_songplays_table >> quality_checks
load_user_dimension_table >> quality_checks
load_song_dimension_table  >> quality_checks   
load_artist_dimension_table >> quality_checks
load_time_dimension_table >> quality_checks

quality_checks >> end_operator