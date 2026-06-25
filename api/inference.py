# ============================================================
# FIREWALL IDS V1.0
# inference.py
# ============================================================

from pathlib import Path
import json

import pandas as pd
from catboost import CatBoostClassifier


# ============================================================
# PATHS
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = ROOT_DIR / "models" / "catboost"

BINARY_MODEL_PATH = (
    MODEL_DIR / "firewall_binary_ids_catboost.cbm"
)

MULTICLASS_MODEL_PATH = (
    MODEL_DIR / "firewall_multiclass_catboost.cbm"
)

FEATURE_PATH = MODEL_DIR / "features.json"


# ============================================================
# LOAD FEATURES
# ============================================================

with open(FEATURE_PATH) as f:
    FEATURE_NAMES = json.load(f)

print(f"Loaded {len(FEATURE_NAMES)} features")


# ============================================================
# LOAD MODELS
# ============================================================

print("Loading binary model...")

binary_model = CatBoostClassifier()
binary_model.load_model(str(BINARY_MODEL_PATH))

print("Loading multiclass model...")

multiclass_model = CatBoostClassifier()
multiclass_model.load_model(str(MULTICLASS_MODEL_PATH))

print("Firewall IDS V1.0 ready.")


# ============================================================
# CONFIG
# ============================================================

BINARY_THRESHOLD = 0.50


# ============================================================
# SINGLE PREDICTION
# ============================================================

def predict_single(flow: dict):

    df = pd.DataFrame([flow])

    # Ensure exact training order
    df = df.reindex(
        columns=FEATURE_NAMES,
        fill_value=0
    )

    # ------------------------
    # Binary Model
    # ------------------------

    binary_probs = binary_model.predict_proba(df)[0]

    benign_prob = float(binary_probs[0])
    attack_prob = float(binary_probs[1])

    if attack_prob < BINARY_THRESHOLD:

        return {

            "prediction": "BENIGN",

            "binary_confidence":
                benign_prob,

            "multiclass_confidence":
                None
        }

    # ------------------------
    # Multiclass Model
    # ------------------------

    multi_probs = multiclass_model.predict_proba(df)[0]

    idx = multi_probs.argmax()

    prediction = multiclass_model.classes_[idx]

    return {

        "prediction":
            str(prediction),

        "binary_confidence":
            attack_prob,

        "multiclass_confidence":
            float(multi_probs[idx]),

        "all_probabilities": {

            str(cls): float(prob)

            for cls, prob in zip(
                multiclass_model.classes_,
                multi_probs
            )
        }
    }


# ============================================================
# BATCH PREDICTION
# ============================================================

def predict_batch(df: pd.DataFrame):

    df = df.reindex(
        columns=FEATURE_NAMES,
        fill_value=0
    )

    binary_probs = binary_model.predict_proba(df)

    multi_probs = multiclass_model.predict_proba(df)

    results = []

    for i in range(len(df)):

        attack_prob = float(binary_probs[i][1])

        if attack_prob < BINARY_THRESHOLD:

            results.append({

                "prediction": "BENIGN",

                "binary_confidence":
                    float(binary_probs[i][0]),

                "multiclass_confidence":
                    None
            })

            continue

        idx = multi_probs[i].argmax()

        results.append({

            "prediction":
                str(multiclass_model.classes_[idx]),

            "binary_confidence":
                attack_prob,

            "multiclass_confidence":
                float(multi_probs[i][idx])
        })

    return pd.DataFrame(results)