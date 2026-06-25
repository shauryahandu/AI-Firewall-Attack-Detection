import pandas as pd
import numpy as np

from catboost import CatBoostClassifier

# ============================================================
# LOAD MODEL
# ============================================================

MODEL_PATH = r"models/catboost/firewall_binary_ids_catboost.cbm"

model = CatBoostClassifier()

model.load_model(MODEL_PATH)

print("Model loaded.")

# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = r"data/processed/master_network_attacks_v1.parquet"

df = pd.read_parquet(DATA_PATH)

print("Dataset:", df.shape)

# ============================================================
# LABELS
# ============================================================

attack_labels = df["attack_type"].values

# ============================================================
# FEATURES
# ============================================================

X = df.drop(
    columns=[
        c for c in [
            "Label",
            "attack_type",
            "binary_label"
        ]
        if c in df.columns
    ]
)

X = X.replace(
    [np.inf, -np.inf],
    np.nan
)

X = X.fillna(0)

# ============================================================
# CHUNKED PREDICTION
# ============================================================

chunk_size = 100000

predictions = []

for start in range(0, len(X), chunk_size):

    end = min(start + chunk_size, len(X))

    print(
        f"Predicting rows "
        f"{start:,} -> {end:,}"
    )

    pred_chunk = model.predict(
        X.iloc[start:end]
    )

    predictions.extend(
        pred_chunk.astype(int).flatten()
    )

predictions = np.array(predictions)

# ============================================================
# RESULTS
# ============================================================

results = []

for attack in sorted(np.unique(attack_labels)):

    mask = attack_labels == attack

    total = mask.sum()

    detected = predictions[mask].sum()

    rate = detected / total

    results.append([
        attack,
        total,
        detected,
        rate
    ])

results_df = pd.DataFrame(
    results,
    columns=[
        "Attack",
        "Samples",
        "Detected",
        "DetectionRate"
    ]
)

results_df = results_df.sort_values(
    "DetectionRate",
    ascending=False
)

print()
print("="*70)
print("BINARY CATBOOST RESULTS")
print("="*70)

print(results_df)

results_df.to_csv(
    "binary_catboost_detection_rates.csv",
    index=False
)

print(
    "\nSaved: "
    "binary_catboost_detection_rates.csv"
)