from pathlib import Path
from catboost import CatBoostClassifier
import json

ROOT_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    ROOT_DIR
    / "models"
    / "catboost"
    / "firewall_multiclass_catboost.cbm"
)

model = CatBoostClassifier()
model.load_model(str(MODEL_PATH))

with open(
    ROOT_DIR / "models" / "catboost" / "features.json",
    "w"
) as f:

    json.dump(
        model.feature_names_,
        f,
        indent=4
    )

print("Saved features.json")