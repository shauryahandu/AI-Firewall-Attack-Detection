from autogluon.tabular import TabularPredictor
import pandas as pd

# Load dataset
df = pd.read_csv(
    r"processed/master_web_attacks_v1.csv"
)

print(df.shape)

# Train model
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
print(predictor.leaderboard(silent=True))