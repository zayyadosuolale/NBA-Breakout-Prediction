# NBA Breakout Prediction

## Project Overview

Can an NBA player's breakout season be predicted before it happens?

This project develops an end-to-end data analytics and machine learning pipeline to predict future NBA breakout players using historical player performance data. Five seasons of traditional and advanced NBA statistics were collected, cleaned, and integrated into a relational MySQL database before being analyzed in Python.Rather than relying solely on a player's current performance, this project focuses on year-over-year improvement by engineering delta features that measure changes in production, efficiency, and overall player value. These features were used to construct a custom Breakout Score, which identifies the top 20% of player improvements in each season and serves as the target variable for supervised machine learning.

Multiple classification models were trained and evaluated using historical player data. The final model was then validated against the completed 2025–26 NBA season by comparing preseason predictions with actual player outcomes, providing an out-of-sample assessment of the model's predictive performance.

## Problem Statement

NBA organizations, analysts, and fans often attempt to identify players who are poised for a breakout season before it occurs. While many evaluations focus on a player's current statistics, predicting future improvement is considerably more challenging because player development is influenced by multiple factors, including increased opportunity, efficiency, usage, and overall impact. The objective of this project was to develop a machine learning pipeline capable of identifying players with the greatest likelihood of experiencing a breakout season using only information available prior to that season. To accomplish this, historical NBA player statistics were transformed into predictive features representing year-over-year improvement rather than raw performance alone.

A custom Breakout Score was developed to quantify player improvement across multiple dimensions of performance. This score was then used to create a binary classification problem, allowing supervised machine learning models to predict whether an eligible player would break out during the following NBA season. The final objective was not only to generate preseason predictions, but also to evaluate how well those predictions generalized by comparing them with the completed 2025–26 NBA season.
