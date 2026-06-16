from autogluon.tabular import TabularPredictor
import pandas as pd

df = pd.read_csv("processed/master_network_attacks_v1.csv")

# Binary target
df["is_attack"] = (df["attack_type"] != "BENIGN").astype(int)

# Fill the only missing feature
df["Flow Bytes/s"] = df["Flow Bytes/s"].fillna(0)

# Remove target columns
DROP_COLS = [
    "Label",
    "attack_type"
]

train_df = df.drop(columns=DROP_COLS)

predictor_binary = TabularPredictor(
    label="is_attack",
    eval_metric="roc_auc",
    path="models/binary_ids"
)

predictor_binary.fit(
    train_df,
    presets="best_quality",
    time_limit=14400,   # 4 hours
    verbosity=4         # Maximum useful logging
)

leaderboard = predictor_binary.leaderboard(silent=True)

print(
    leaderboard[
        ["model", "score_val"]
    ].head(20)
)

fi = predictor_binary.feature_importance(train_df)

print(fi.head(30))

predictor_binary.save()