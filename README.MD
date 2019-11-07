# Airflow Pipeline  

> Nov 5, 2019
> DEND Project 5 
> Author: Natalia Meleshkina

## Project Overview

In this project I introduce automated ETL pipeline with Apache Airflow for Streaming startup Sparkify. Source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Data

Sparkify's data are stored on Amazon S3

1.Song dataset consists of JSON files and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID.

- Song data: `s3://udacity-dend/song_data`

2.Log dataset. Contains app activity logs from streaming app. The log files in the dataset are partitioned by year and month.

- Log data: `s3://udacity-dend/log_data`

Log data JSON path: `s3://udacity-dend/log_json_path.json`

## Project Steps

To accomplish this task we are going to implement Airflow DAG with following tasks:

- prepare Redshift schema by creating all requered tables for staging, facts and dimention tables
- extract data from S3 to staging
- load data to fact and dimention tables

## Project Files

- 
