# Python Workflow

This folder contains the Python scripts used throughout the NBA Breakout Prediction project.

## Data_Cleaning

Scripts used to clean the raw Basketball Reference datasets before importing them into MySQL.

Tasks include:
- Standardize column names
- Remove repeated header rows
- Clean player names
- Add season labels
- Convert numeric columns
- Export cleaned CSV files

## Machine_Learning

This folder will contain the Python scripts used to build and evaluate the predictive model.

Workflow:
- Connect Python to MySQL
- Load the master NBA dataset
- Perform correlation analysis
- Engineer breakout features
- Create the composite breakout label
- Train machine learning models
- Evaluate model performance
- Analyze feature importance
