import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

df = pd.read_csv(
    r"processed/sqli_binary.csv"
)

_, test_df = train_test_split(
    df,
    test_size=0.2,
    stratify=df["attack_type"],
    random_state=42
)

predictor = TabularPredictor.load(
    r".\AutogluonModels\ag-20260609_090955"
)

preds = predictor.predict(test_df)

print(
    classification_report(
        test_df["attack_type"],
        preds,
        digits=4
    )
)
