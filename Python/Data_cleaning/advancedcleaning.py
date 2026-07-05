# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 09:30:17 2026

@author: zayya
"""

import pandas as pd
import unicodedata

# ---------- SETTINGS ----------
input_file = "24-25Advanced.csv"   # change filename
output_file = "45-25.csv"
season = "2024-25"

# ---------- READ FILE ----------
df = pd.read_csv(input_file, encoding="utf-8-sig")

# ---------- CLEAN COLUMN NAMES ----------
df.columns = (
    df.columns
    .str.strip()
    .str.replace("%", "_pct", regex=False)
    .str.replace("+/-", "plus_minus", regex=False)
    .str.replace("/", "_", regex=False)
    .str.replace(" ", "_", regex=False)
)

print("Columns:", df.columns.tolist())

# ---------- REMOVE REPEATED HEADER ROWS ----------
if "Player" in df.columns:
    df = df[df["Player"] != "Player"]

# ---------- REMOVE FULLY BLANK ROWS ----------
df = df.dropna(how="all")

# ---------- REMOVE UNNEEDED COLUMNS ----------
df = df.drop(columns=["Awards", "Player_additional"], errors="ignore")

# ---------- CLEAN PLAYER NAMES ----------
def clean_name(name):
    if pd.isna(name):
        return name
    name = str(name).strip()
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("utf-8")
    return name

df["Player"] = df["Player"].apply(clean_name)

# ---------- ADD SEASON ----------
df["Season"] = season

# ---------- CLEAN TEAM / POSITION ----------
if "Team" in df.columns:
    df["Team"] = df["Team"].astype(str).str.strip()

if "Pos" in df.columns:
    df["Pos"] = df["Pos"].astype(str).str.strip()



# ---------- CONVERT NUMERIC COLUMNS ----------
non_numeric_cols = ["Player", "Team", "Pos", "Season"]

for col in df.columns:
    if col not in non_numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")


df = df.fillna(0)

# ---------- SAVE CLEAN FILE ----------
df.to_csv(output_file, index=False, encoding="utf-8")

print("Cleaning complete.")
print("Rows, Columns:", df.shape)
print(df.head())
print(df.tail())