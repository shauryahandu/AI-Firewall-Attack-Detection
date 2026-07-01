import shap
import pandas as pd
from catboost import CatBoostClassifier


MODEL_PATH = (
    "models/catboost/"
    "firewall_binary_ids_catboost.cbm"
)


binary_model = CatBoostClassifier()

binary_model.load_model(
    MODEL_PATH
)


explainer = shap.TreeExplainer(
    binary_model
)


def get_shap_values(
    df: pd.DataFrame
):

    shap_values = explainer.shap_values(
        df
    )

    return shap_values


def get_top_features(
    df: pd.DataFrame,
    top_k: int = 10
):

    shap_values = get_shap_values(df)

    importance = pd.DataFrame({

        "feature": df.columns,

        "shap_value": [
            abs(x)
            for x in shap_values[0]
        ]
    })

    importance = importance.sort_values(
        "shap_value",
        ascending=False
    )

    return importance.head(top_k)