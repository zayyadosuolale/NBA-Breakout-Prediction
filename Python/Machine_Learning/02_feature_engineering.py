# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 16:06:06 2026

@author: zayya
"""
####### IMPORT ##############
from dotenv import load_dotenv
import os
load_dotenv()
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys
from sqlalchemy import create_engine
import pandas as pd
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)
query = """
SELECT *
FROM nba_master_all
WHERE minutes_per_game >= 12
and age <= 24
and games_played >= 20
;
"""
####### Building the change in data ##############
df = pd.read_sql(query, engine)
df_1 = df.sort_values(['player' ,'season' ]).reset_index(drop=True)
#print("First 5 rows: ")
#print(df_1.head())
columns = [
    'points_per_game',
    'rebounds_per_game',
    'assists_per_game',
    'per',
    'usage_pct',
    'true_shooting_pct',
    'Box_PlusMinus',
    'win_shares',
    'value_over_replacement'
]
for i in columns:
    df_1['delta_' + i] = df_1.groupby('player')[i].diff()
'''
for i in columns:
    print(df_1[df_1['player'] == 'Anthony Edwards'] 
          [['player', 'season',  i, 'delta_' + i ]])
'''
####### Choosing how to build breakout score ##############
delta_statistics= (df_1[['delta_points_per_game',
      'delta_rebounds_per_game',
      'delta_assists_per_game',
      'delta_per',
      'delta_usage_pct',
      'delta_true_shooting_pct',
      'delta_Box_PlusMinus',
      'delta_win_shares',
      'delta_value_over_replacement'
]].describe())

###Brings out the means and standrad deviations to see how important each statistics is
#for example how valuable a change in ppg than is to asts or per for example
#allows for account when building the breakout score
#A high standard deviation only tells us that the metric varies more across players.
corr_df_1 = df_1[
[
'delta_points_per_game',
      'delta_rebounds_per_game',
      'delta_assists_per_game',
      'delta_per',
      'delta_usage_pct',
      'delta_true_shooting_pct',
      'delta_Box_PlusMinus',
      'delta_win_shares',
      'delta_value_over_replacement'
]
]
corr_matrix = corr_df_1.corr()
plt.figure(figsize = (10,8))
sns.heatmap(corr_matrix, annot = True, fmt = ".2f", cmap = "coolwarm", center = 0)
plt.title("Correlation Matrix of NBA Player-Season Delta Statistics")
plt.tight_layout()
plt.show() 
##Heatmap what statistcis are correlated just so we dont have to account for both in the breakout score
# no point incuding win shares and vorp or per and bpm

##In conclusion I will include delta ppg delta per delta usgpct delta winshares and delta true shooting
#So breakout score can be defined as avg (zscore(of delta(ppg+ per+ usgpct+ws+ts)))

### Breakout Score Calculation ####
breakout_features = [
    'delta_points_per_game',
    'delta_per',
    'delta_usage_pct',
    'delta_true_shooting_pct',
    'delta_win_shares'
    ]
for i in breakout_features:
    df_1['z_' + i] = (df_1[i]- df_1[i].mean())/ (df_1[i].std())
zscore_features = [
    'z_delta_points_per_game',
    'z_delta_per',
    'z_delta_usage_pct',
    'z_delta_true_shooting_pct',
    'z_delta_win_shares'
    ]
df_1['breakout_score'] = round(df_1[zscore_features].mean(axis=1), 2)
'''
print(
    df_1[df_1['player'] == 'Tyrese Maxey']
    [['player', 'season',  'breakout_score']]
)
'''
#For example, A score of 1.11 means his combined improvement (after standardizing the five metrics) 
#for that season was 1.11 standard deviations above the average player-season improvement.
#df_1[['player', 'season' , 'breakout_score']]\
 #   .sort_values('breakout_score', ascending= False).head(30)

#A breakout will be defined as one where the breakout score resides in top 20% of all eligible player seasons

threshold = df_1['breakout_score'].quantile(0.80)
df_1['breakout'] = (df_1['breakout_score'] >= threshold).astype(int)
'''
print(
    df_1[df_1['player'] == 'Tyrese Maxey']
    [['player', 'season',  'breakout_score', 'breakout']]
)

print(
       df_1[df_1['player'] == 'Anthony Edwards']
       [['player', 'season', 'breakout_score', 'breakout']])
'''
print(threshold)
print(
    df_1[df_1['breakout'] == 1]
    [['player', 'season', 'breakout_score', 'breakout']]
    .sort_values(by='breakout_score', ascending=False)
)
df_1.to_csv("feature_engineered_data.csv", index=False)
##Continued to the training model