# SQL

## Overview

This folder contains the SQL scripts used to clean, merge, and analyze NBA player statistics from the 2020–21 through 2024–25 seasons.

The final output is a unified master table (`nba_master_all`) that serves as the data source for the Python machine learning pipeline.

## Workflow

1. Clean individual season datasets.
2. Standardize column names.
3. Create season master tables.
4. Merge all seasons into one master table.
5. Perform exploratory data analysis (EDA).

## Exploratory Data Analysis

The SQL EDA focused on four major areas:

- League-wide trends across seasons
- League leaders in traditional and advanced metrics
- Young player analysis (Age ≤ 24)
- Statistical distributions by age and position

Additional analyses included:
- Rotation-player filtering (12+ MPG)
- Games played thresholds
- Usage and scoring distributions
- Efficiency leaderboards
- Experience distribution for young players

## Technologies Used

- MySQL
- SQL Window Functions
- Subqueries
- Joins
- Groupby
- Case statements
- Data Cleaning
- Exploratory Data Analysis (EDA)

## Files

1. 01_cleaning_2020_21.sql
2. 02_cleaning_2021_22.sql
3. 03_cleaning_2022_23.sql
4. 04_cleaning_2023_24.sql
5. 05_cleaning_2024_25.sql
6. 06_dummycleanforallseasons.sql
7. 07_create_master_table
8. 08_renamecolumns
9. 09_nba_eda.sql

## Key Insights

- League leaders : Jokic consistently ranked among the league leaders in advanced metrics such as BPM, PER, Win Shares, and VORP, illustrating why advanced statistics capture overall impact better than points alone.
- Scoring trends: League scoring remained high across the five-season dataset
- Advanced metrics: League leaders in advanced statistics such as BPM, PER, Win Shares, and VORP remained relatively consistent across seasons, with elite players such as Giannis and Jokic consistently ranking near the top.
- Age distribution : Young players were defined as players under the age of 24. They averaged around 2.4 seasons in the dataset
- Position differences: Guards generally exhibited higher usage rates and scoring volume, while centers led in rebounding and efficiency-related metrics.
- Data quality: Applying minimum games played and minutes-per-game thresholds removed small-sample performances, producing more reliable league leaderboards and comparisons.
- Project direction: These findings informed the feature engineering stage, where year-over-year improvements in advanced metrics are used to define and predict breakout players.
