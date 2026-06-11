import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.model_selection import train_test_split

df = pd.read_csv(
    "processed/sqli_binary.csv"
)

train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    stratify=df["attack_type"],
    random_state=42
)

train_df.to_csv(
    "processed/sqli_train.csv",
    index=False
)

test_df.to_csv(
    "processed/sqli_test.csv",
    index=False
)

predictor = TabularPredictor(
    label="attack_type",
    eval_metric="precision"
)

predictor.fit(
    train_data=train_df,
    presets="best_quality",
    time_limit=3600
)

print("Training Complete")

eval_metric="precision"