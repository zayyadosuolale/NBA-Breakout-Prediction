# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 18:00:00 2026

@author: zayya
"""
####### IMPORT ##############
from dotenv import load_dotenv
import os
load_dotenv()
from sqlalchemy import create_engine
import pandas as pd
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)
query = """
SELECT *
FROM nba_master_all_3
WHERE minutes_per_game >= 12
  AND age <= 24
  AND games_played >= 20
  AND player IN (
      SELECT player
      FROM nba_master_all_3
      GROUP BY player
      HAVING
          SUM(CASE WHEN season = '2024-25' THEN 1 ELSE 0 END) = 1
      AND SUM(CASE WHEN season = '2025-26' THEN 1 ELSE 0 END) = 1
);
"""
# Included only players with both 2024-25 and 2025-26 seasons, since
# year-over-year deltas are required to calculate the actual 2025-26 Breakout Score.
# -------------------------------------------------------------------

### Loading Engineered Data Sets ###
break_pred = pd.read_csv("2025_26_breakout_predictions.csv")
break_pred.sort_values(by= 'breakout_probability', ascending = False).head(10)
# -------------------------------------------------------------------

#######  Data for Season 25-26 ##############
df_4 = pd.read_sql(query, engine)
df_4 = df_4.sort_values(['player' ,'season' ]).reset_index(drop=True)
#print("First 5 rows: ")
#print(df_4.head())
#print(df_4[df_4['player'] == 'Anthony Edwards'][['player', 'season', 'points_per_game']])
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
    df_4['delta_' + i] = df_4.groupby('player')[i].diff()
'''
for i in columns:
    print(df_4[df_4['player'] == 'Anthony Edwards'] 
          [['player', 'season',  i, 'delta_' + i ]])
'''
### Breakout Score Calculation for 25-26 season ####
breakout_features = [
    'delta_points_per_game',
    'delta_per',
    'delta_usage_pct',
    'delta_true_shooting_pct',
    'delta_win_shares'
    ]
# -------------------------------------------------------------------

### Isolate completed 2025-26 season ###
actual_2025_26 = df_4[df_4['season'] == '2025-26'].copy()
print("Eligible 2025-26 players:", actual_2025_26.shape[0])
# Calculate z-scores relative only to the 2025-26 player population
for feature in breakout_features:
    actual_2025_26['z_' + feature] = (actual_2025_26[feature] - actual_2025_26[feature].mean()) / actual_2025_26[feature].std()
zscore_features = [
    'z_delta_points_per_game',
    'z_delta_per',
    'z_delta_usage_pct',
    'z_delta_true_shooting_pct',
    'z_delta_win_shares'
]
actual_2025_26['breakout_score'] = (actual_2025_26[zscore_features].mean(axis=1).round(2))

# Define actual breakouts as the top 20% of 2025-26 scores
threshold_2025_26 = actual_2025_26['breakout_score'].quantile(0.80)
actual_2025_26['actual_breakout'] = (actual_2025_26['breakout_score'] >= threshold_2025_26).astype(int)
print("\n2025-26 Breakout Threshold:", round(threshold_2025_26,2))
print("\nActual 2025-26 Breakouts:")
print(actual_2025_26[actual_2025_26['actual_breakout'] == 1]
      [
        [
            'player',
            'team',
            'breakout_score',
            'actual_breakout'
        ]
    ].sort_values('breakout_score',ascending=False))
# -------------------------------------------------------------------

### Merge Predictions With Actual Results ###
prediction_df = break_pred.merge(actual_2025_26[['player', 'season', 'breakout_score', 'actual_breakout']]
                                 ,on = 'player', how ='inner')
print('Matched players :: ' , prediction_df.shape[0])
print('Original players ::' , break_pred.shape[0])
'''
print(prediction_df
       [[
         'player',
         'breakout_probability',
         'breakout_score',
         'actual_breakout']].sort_values('breakout_probability', ascending = False).head(20))
'''
prediction_df['predicted_breakout'] = (prediction_df['breakout_probability'] >= 0.50
).astype(int)
print("\nProbability Range:", round(prediction_df['breakout_probability'].min(),2),
    "to",
    round(prediction_df['breakout_probability'].max(),2)
)
print("\nPredicted Class Counts:")
print(prediction_df['predicted_breakout'].value_counts())
'''
print(prediction_df[prediction_df['player'] == 'Anthony Edwards']
                    [['player',  'predicted_breakout','actual_breakout']])
'''
# -------------------------------------------------------------------

### Out-of-Sample 2025-26 Validation ###
y_actual = prediction_df['actual_breakout']
y_predicted = prediction_df['predicted_breakout']
y_probability = prediction_df['breakout_probability']
print("\n2025-26 Final Validation Results:")
print("Accuracy:",round(accuracy_score(y_actual, y_predicted), 3))
print("Precision:",round(precision_score(y_actual,y_predicted,zero_division=0),3))
print("Recall:", round(recall_score(y_actual, y_predicted, zero_division=0),3))
print("F1 score:", round(f1_score(y_actual, y_predicted, zero_division=0),3))
print("ROC - AUC:", round(roc_auc_score(y_actual, y_probability),3))
print("\nConfusion Matrix:")
print(confusion_matrix(y_actual, y_predicted))
print("\nClassification Report:")
print(classification_report(y_actual,y_predicted,zero_division=0))
# -------------------------------------------------------------------

### Top-20 Prediction Evaluation ###
top_20 = prediction_df.sort_values('breakout_probability',ascending=False).head(20)
top_20_hits = top_20['actual_breakout'].sum()
top_20_precision = top_20_hits / len(top_20)
print("\nTop-20 Predicted Candidates:")
print(top_20[['player','breakout_probability', 'breakout_score','actual_breakout']])
print(
    f"\nActual breakouts among top 20: "
    f"{top_20_hits} out of {len(top_20)}"
)
print("\nOut of the top 20 these were the players that were correctly predicted")
print(top_20[ (top_20['actual_breakout'] == 1) & (top_20['predicted_breakout'] == 1) ]
      [['player']])
print(
    "Top-20 Precision:",
    round(top_20_precision, 3)
)
# -------------------------------------------------------------------

### Final Save ###
prediction_df = prediction_df.sort_values('breakout_probability',ascending=False)
prediction_df.to_csv( "2025_26_prediction_validation.csv",index=False)

#-------------------------------- END ---------------------------------------


