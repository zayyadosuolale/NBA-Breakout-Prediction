# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 12:52:52 2026

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
;
"""
####### GENERAL DESCRIPTION ##############
df = pd.read_sql(query, engine)
print("First 5 rows: ")
print(df.head())
print("Last 5 rows: ")
print(df.tail())
print()
print("Shape is " + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns' )
x = str(df.duplicated().sum())
print("There are " + str(df.duplicated().sum()) + ' duplicate rows ')

####### PART 1 HISTOGRAMS ##############

#Histogram 1: Points Per Game
#To examine the distribution of scoring across player-seasons
plt.figure(figsize=(8,5))
plt.hist(df['points_per_game'])
plt.title(" Distribution of Points Per Game")
plt.xlabel("Points per Game")
plt.ylabel("Number of Players")
plt.show()

#Histogram 2: Ages
#To examine the distribution of ages across player-seasons
plt.figure(figsize=(8,5))
plt.hist(df['age'])
plt.title(" Distribution of Player-Season Ages")
plt.xlabel("Ages")
plt.ylabel("Number of Players")
plt.show()

#Histogram 3: Rebounds Per Game
#To examine the distribution of rebounds across player-seasons
plt.figure(figsize=(8,5))
plt.hist(df['rebounds_per_game'])
plt.title(" Distribution of Rebounds Per Game")
plt.xlabel("Rebounds")
plt.ylabel("Number of Players")
plt.show()

#Histogram 4: Assists Per Game
#To examine the distribution of assists across player-seasons
plt.figure(figsize=(8,5))
plt.hist(df['assists_per_game'])
plt.title(" Distribution of Assists Per Game")
plt.xlabel("Assists")
plt.ylabel("Number of Players")
plt.show()

#Histogram 5:'PER' Per Game
#To examine the distribution of 'PER' across player-seasons
plt.figure(figsize=(8,5))
plt.hist(df['per'])
plt.title(" Distribution of PER")
plt.xlabel("PER")
plt.ylabel("Number of Players")
plt.show()

#Histogram 6:Usage_pct
#To examine the distribution of usage across player-seasons
plt.figure(figsize=(8,5))
plt.hist(df['usage_pct'])
plt.title(" Distribution of Usage")
plt.xlabel("Usage Percent")
plt.ylabel("Number of Players")
plt.show()

#Histogram 7: True Shooting
#To examine the distribution of true shooting across player-seasons
plt.figure(figsize=(8,5))
plt.hist(df['true_shooting_pct'])
plt.title(" Distribution of True Shooting")
plt.xlabel("True Shooting Percent")
plt.ylabel("Number of Players")
plt.show()

#Histogram 8: BPM Per Game
#To examine the distribution of Box Plus Minus across player-seasons
plt.figure(figsize=(8,5))
plt.hist(df['Box_PlusMinus'])
plt.title(" Distribution of Box Plus Minus")
plt.xlabel("BPM")
plt.ylabel("Number of Players")
plt.show()

#Histogram 9: Win Shares
#To examine the distribution of Win Shares across player-seasons
plt.figure(figsize=(8,5))
plt.hist(df['win_shares'])
plt.title(" Distribution of Win Shares")
plt.xlabel("Win Shares")
plt.ylabel("Number of Players")
plt.show()

#Histogram 10: VORP Per Game
#To examine the distribution of VORP across player-seasons
plt.figure(figsize=(8,5))
plt.hist(df['value_over_replacement'])
plt.title(" Distribution of VORP")
plt.xlabel("VORP")
plt.ylabel("Number of Players")
plt.show()

####### PART 2 BOX PLOTS ##############

#Boxplot 1 : Points Per Game
# Visualize the distribution, median, spread, and potential outliers in points per game.
plt.figure(figsize=(8,5))
plt.boxplot(df['points_per_game'])
plt.title("Points Per Game ")
plt.ylabel("Points Per Game")
plt.show()

#Boxplot 2 : PER
# Visualize the distribution, median, spread, and potential outliers in PER.
plt.figure(figsize=(8,5))
plt.boxplot(df['per'])
plt.title("PER")
plt.ylabel("PER")
plt.show()

#Boxplot 3 : USAGE %
# Visualize the distribution, median, spread, and potential outliers in USAGE %.
plt.figure(figsize=(8,5))
plt.boxplot(df['usage_pct'])
plt.title("USAGE %")
plt.ylabel("USAGE %")
plt.show()

#Boxplot 4 : BPM
# Visualize the distribution, median, spread, and potential outliers in BPM.
plt.figure(figsize=(8,5))
plt.boxplot(df['Box_PlusMinus'])
plt.title("BOX PLUS MINUS ")
plt.ylabel("BOX PLUS MINUS ")
plt.show()

#Boxplot 5 : Win Shares
# Visualize the distribution, median, spread, and potential outliers in Win Shares.
plt.figure(figsize=(8,5))
plt.boxplot(df['win_shares'])
plt.title("WIN SHARES ")
plt.ylabel("WIN SHARES")
plt.show()

#Boxplot 6 : VORP
# Visualize the distribution, median, spread, and potential outliers in VORP.
plt.figure(figsize=(8,5))
plt.boxplot(df['value_over_replacement'])
plt.title("VORP")
plt.ylabel('VORP')
plt.show()

####### PART 3 SCATTER PLOTS ##############

#Scatterplot 1 : USAGE% VS PPG
#To determine whether players with higher usage percentages tend to score more points per game.
plt.figure(figsize = (8,5))
plt.scatter(df['usage_pct'], df['points_per_game'])
m, b = np.polyfit(df['usage_pct'], df['points_per_game'], 1)
plt.plot(
    df["usage_pct"],
    m * df["usage_pct"] + b,
    color="red",
    linewidth=2
)
plt.title('USAGE_PCT vs Points Per Game')
plt.xlabel('Usage Percentage')
plt.ylabel('Points Per Game')
plt.show()

#Scatterplot 2 : AGE VS PPG
#To determine whether as players age they tend to score more points per game.
plt.figure(figsize = (8,5))
plt.scatter(df['age'], df['points_per_game'])
m, b = np.polyfit(df['age'], df['points_per_game'], 1)
plt.plot(
    df['age'],
    m * df['age'] + b,
    color="red",
    linewidth=2
)
plt.title('AGE vs Points Per Game')
plt.xlabel('AGE')
plt.ylabel('Points Per Game')
plt.show()

#Scatterplot 3 : PER VS BPM
#To determine whether advanced metrics such as PER and BPM agree with each other.
plt.figure(figsize = (8,5))
plt.scatter(df['per'], df['Box_PlusMinus'])
m, b = np.polyfit(df['per'], df['Box_PlusMinus'], 1)
plt.plot(
    df['per'],
    m * df['per'] + b,
    color="red",
    linewidth=2
)
plt.title('PER vs BoxPlusMinus ')
plt.xlabel('PER')
plt.ylabel('BoxPlusMinus')
plt.show()

#Scatterplot 4 : BPM VS Win Shares
#To determine whether player impact stats such as BPM leads to more wins.
plt.figure(figsize = (8,5))
plt.scatter(df['Box_PlusMinus'], df['win_shares'])
m, b = np.polyfit(df['Box_PlusMinus'], df['win_shares'], 1)
plt.plot(
    df['Box_PlusMinus'],
    m * df['Box_PlusMinus'] + b,
    color="red",
    linewidth=2
)
plt.title('BoxPlusMinus vs Win Shares ')
plt.xlabel('BoxPlusMinus')
plt.ylabel('Win Shares')
plt.show()

#Scatterplot 5 : TS VS PPG
##To determine whether players with higher true shooting percentages tend to score more points per game.
plt.figure(figsize = (8,5))
plt.scatter(df['true_shooting_pct'], df['points_per_game'])
m, b = np.polyfit(df['true_shooting_pct'], df['points_per_game'], 1)
plt.plot(
    df['true_shooting_pct'],
    m * df['true_shooting_pct'] + b,
    color="red",
    linewidth=2
)
plt.title('True Shooting vs Points Per Game')
plt.xlabel('True Shooting')
plt.ylabel('Points Per Game')
plt.show()

#Scatterplot 6 : USG VS APG
##To determine whether players with higher usage percentages tend to have more assists per game.
plt.figure(figsize = (8,5))
plt.scatter(df['usage_pct'], df['assists_per_game'])
m, b = np.polyfit(df['usage_pct'], df['assists_per_game'], 1)
plt.plot(
    df['usage_pct'],
    m * df['usage_pct'] + b,
    color="red",
    linewidth=2
)
plt.title('USAGE_PCT vs Assists Per Game')
plt.xlabel('Usage Percentage')
plt.ylabel('Assists Per Game')
plt.show()

####### PART 4 CORRELATION ANALYSIS ##############

corr_df = df[
[
 'age' ,
 'points_per_game',
 'assists_per_game',
 'rebounds_per_game',
 'per',
 'usage_pct' ,
 'true_shooting_pct',
 'Box_PlusMinus',
 'win_shares',
 'value_over_replacement'
]
]
corr_matrix = corr_df.corr()
plt.figure(figsize = (10,8))
sns.heatmap(corr_matrix, annot = True, fmt = ".2f", cmap = "coolwarm", center = 0)
plt.title("Correlation Matrix of NBA Player-Season Statistics")
plt.tight_layout()
plt.show() 

#### Key Findings ::
#Usage percentage strongly correlates with scoring
#PER, BPM , Win Shares, and VORP are very highly correlated showing that 
#advanced metrics often capture overlapping measures of player impact.
#Age has little correlation with scoring within the under-25 player sample -
#suggesting that age cannot be used as a sole productor of offensive production

    