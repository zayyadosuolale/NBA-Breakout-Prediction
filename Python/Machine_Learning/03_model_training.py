# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 16:13:11 2026

@author: zayya
"""
### Imports ###
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
)
#-------------------------------------------------------------------

### Loading Engineered Data Sets ###
df_m1 = pd.read_csv("feature_engineered_data.csv")
#df_m1.sort_values(by= 'breakout_score', ascending = False).head(10)

#-------------------------------------------------------------------

### Create next-season prediction target ###
df_m1 = df_m1.sort_values(['player', 'season']).reset_index(drop=True)
df_m1['breakout_next_season'] = df_m1.groupby('player')['breakout'].shift(-1)
'''
print(df_m1[df_m1['player'] == 'Anthony Edwards']
      [['player', 'season', 'breakout', 'breakout_next_season']]
      )
'''
#-------------------------------------------------------------------

### Building Modeling Season Dataset ###
training_df = df_m1.dropna(subset=['breakout_next_season']).copy()
training_df['breakout_next_season'] = (training_df['breakout_next_season'].astype(int))
prediction_2025_26 = df_m1[(df_m1['season'] == '2024-25') &
                           (df_m1['breakout_next_season'].isna())
                           ].copy()
print("Training data shape:", training_df.shape) #this is the training data-train model
print("2025-26 prediction data shape:", prediction_2025_26.shape) #this is what is fed into the model
print(
    training_df['breakout_next_season']
    .value_counts()
)
#Features used to predict next seasons breakout
model_features = [
    # Player information
    'age',
    'games_played',
    'minutes_per_game',
    # Current season production
    'points_per_game',
    'rebounds_per_game',
    'assists_per_game',
    # Advanced metrics
    'per',
    'usage_pct',
    'true_shooting_pct',
    'Box_PlusMinus',
    'win_shares',
    'value_over_replacement',
    # Year-over-year improvement
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
model_df = training_df.dropna(subset = model_features).copy()
print(training_df['breakout_next_season'].value_counts())
print(model_df['breakout_next_season'].value_counts())
X = model_df[model_features] #extracts from model df the features needed to predict breakout
Y = model_df['breakout_next_season']
#-------------------------------------------------------------------

### Train/Test Split ###
X_train, X_test, y_train, y_test = train_test_split(
    X,
    Y,
    test_size=0.20,
    random_state=42,
    stratify= Y
)
print("Training set:", X_train.shape)
print("Testing set:", X_test.shape)
print("\nTraining labels:")
print(y_train.value_counts())
print("\nTesting labels:")
print(y_test.value_counts())
#-------------------------------------------------------------------

### Logistic Regression Baseline ###
log_reg = LogisticRegression(
    random_state = 42,
    max_iter = 1000,
    class_weight="balanced"
    )
log_reg.fit(X_train, y_train)
y_pred = log_reg.predict(X_test)
y_prob = log_reg.predict_proba(X_test)[:,1]
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
#"Logistic Regression was used as a baseline model. 
#Due to the nonlinear nature of player development and the class imbalance in breakout seasons,
#its predictive performance was limited. 
#A Random Forest classifier was then trained to better capture complex interaction across player seasons
#-------------------------------------------------------------------

### Random Forest Baseline ###
rf1 = RandomForestClassifier(
    n_estimators = 200,
    random_state = 42,
    class_weight="balanced",
    max_depth=8
    )
rf1.fit(X_train, y_train)
r_pred = rf1.predict(X_test)
r_prob = rf1.predict_proba(X_test)[:,1]
print("Accuracy:", accuracy_score(y_test, r_pred))
print("Precision:", precision_score(y_test, r_pred))
print("Recall:", recall_score(y_test, r_pred))
print("F1 Score:", f1_score(y_test, r_pred))
print("ROC-AUC:", roc_auc_score(y_test, r_prob))

### Debugging ###
'''
feature_importance = pd.DataFrame({
    'Feature': model_features,
    'Importance': rf1.feature_importances_
}).sort_values('Importance', ascending=False)

print(feature_importance)

prob_df = pd.DataFrame({
    "Actual": y_test,
    "Probability": r_prob
})
print(prob_df.sort_values("Probability", ascending=False))
print(training_df.isna().sum().sort_values(ascending=False))

'''
### Cross Validation ###
#Random_Forest
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42)
scoring = {
    'accuracy': 'accuracy',
    'precision': 'precision',
    'recall': 'recall',
    'f1': 'f1',
    'roc_auc': 'roc_auc'}
rf_cv_results = cross_validate(
    rf1,
    X,
    Y,
    cv=cv,
    scoring=scoring)
print("\nRandom Forest Cross-Validation Results:")
for metric in scoring:
    scores = rf_cv_results[f'test_{metric}']
    print(
        f"{metric}: "
        f"{scores.mean():.3f} "
        f"(+/- {scores.std():.3f})")
#Logistic_Regression
log_cv_results = cross_validate(
    log_reg,
    X,
    Y,
    cv=cv,
    scoring=scoring)
print("\nLogistic Regression Cross-Validation Results:")
for metric in scoring:
    scores = log_cv_results[f'test_{metric}']
    print(
        f"{metric}: "
        f"{scores.mean():.3f} "
        f"(+/- {scores.std():.3f})")
#-------------------------------------------------------------------

### Hyperparameter Tuning ###
#Random Forest
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [4, 6, 8, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'class_weight': ['balanced', 'balanced_subsample']
}
grid_search = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_grid=param_grid,
    scoring='roc_auc',
    cv=cv,
    n_jobs=-1
)
grid_search.fit(X, Y)
print("\n Best parameters:")
print(grid_search.best_params_)
print("Best cross-validated ROC-AUC:")
print(grid_search.best_score_)

#Logistic Regression
param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear']
}
grid_search_lr = GridSearchCV(
    estimator=log_reg,
    param_grid=param_grid,
    cv=cv,
    scoring='roc_auc',
    n_jobs=-1
)
grid_search_lr.fit(X, Y)
print("Best Parameters:")
print(grid_search_lr.best_params_)
print("Best Cross-Validated ROC-AUC:")
print(grid_search_lr.best_score_)
best_log_reg = grid_search_lr.best_estimator_
best_rf = grid_search.best_estimator_
# Logistic Regression outperformed Random Forest during cross-validation
# and was selected as the final model.
#-------------------------------------------------------------------

### Final Model ###
final_model = best_log_reg
final_model.fit(X,Y)
#-------------------------------------------------------------------

### Prediction 25-26 ###
prediction_model_df = prediction_2025_26.dropna(subset=model_features).copy()
X_2025_26 = prediction_model_df[model_features]
prediction_model_df['breakout_probability'] = (final_model.predict_proba(X_2025_26)[:, 1])
final_predictions = prediction_model_df[
    [
        'player',
        'team',
        'age',
        'season',
        'breakout_probability'
    ]].sort_values('breakout_probability',ascending=False)
print("\n The top 20 players predicted for 25- 26 are ")
print(final_predictions.head(20))
final_predictions.to_csv("2025_26_breakout_predictions.csv",index=False)
#-------------------------------------------------------------------

### Feature Direction
coef_df = pd.DataFrame({'feature': model_features,'coefficient': final_model.coef_[0]})
coef_df = coef_df.sort_values('coefficient', ascending=False)
print(coef_df)
coef_df.to_csv("feature_importance.csv",index=False)
