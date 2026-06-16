import pandas as pd
from autogluon.tabular import TabularPredictor

df = pd.read_csv(
    r"processed/sqli_balanced.csv"
)

predictor = TabularPredictor(
    label="attack_type",
    eval_metric="balanced_accuracy"
)

predictor.fit(
    train_data=df,
    presets="best_quality",
    time_limit=3600
)

print("Training Complete")