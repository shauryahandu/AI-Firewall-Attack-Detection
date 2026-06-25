# ============================================================
# EVALUATE DENOISING AUTOENCODER
# ============================================================

import json
import joblib
import numpy as np
import pandas as pd

from tensorflow.keras.models import load_model

# ============================================================
# LOAD MODEL
# ============================================================

MODEL_PATH = "models/autoencoder/denoising_autoencoder1.keras"
SCALER_PATH = "models/autoencoder/scaler2.pkl"
THRESHOLD_PATH = "models/autoencoder/threshold2.json"

print("Loading Denoising Autoencoder...")

model = load_model(MODEL_PATH)

scaler = joblib.load(SCALER_PATH)

with open(THRESHOLD_PATH, "r") as f:
    threshold = json.load(f)["threshold"]

print("Threshold:", threshold)

# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = "data/processed/master_network_attacks_v1.parquet"

print("\nLoading dataset...")

df = pd.read_parquet(DATA_PATH)

print("Shape:", df.shape)

# ============================================================
# SAVE LABELS
# ============================================================

labels = df["attack_type"].copy()

# ============================================================
# FEATURE MATRIX
# ============================================================

drop_cols = []

for col in ["Label", "attack_type"]:
    if col in df.columns:
        drop_cols.append(col)

X = df.drop(columns=drop_cols)

# ============================================================
# SAME PREPROCESSING AS TRAINING
# ============================================================

bad_cols = [
    "Fwd Header Length",
    "Fwd Header Length.1",
    "Bwd Header Length"
]

X = X.drop(
    columns=[c for c in bad_cols if c in X.columns]
)

X = X.replace(
    [np.inf, -np.inf],
    np.nan
)

X = X.fillna(
    X.median(numeric_only=True)
)

X = X.clip(lower=0)

X = np.log1p(X)

# ============================================================
# SCALE
# ============================================================

X_scaled = scaler.transform(X)

print("Scaled Shape:", X_scaled.shape)

# ============================================================
# RECONSTRUCTION
# ============================================================

print("\nRunning Denoising Autoencoder...")

recon = model.predict(
    X_scaled,
    batch_size=8192,
    verbose=1
)

mse = np.mean(
    np.square(X_scaled - recon),
    axis=1
)

# ============================================================
# ANOMALY FLAGS
# ============================================================

anomaly = mse > threshold

# ============================================================
# CLASS-WISE RESULTS
# ============================================================

results = []

for attack in sorted(labels.unique()):

    mask = labels == attack

    total = mask.sum()

    detected = anomaly[mask].sum()

    detection_rate = detected / total

    mean_error = mse[mask].mean()

    results.append([
        attack,
        total,
        detected,
        detection_rate,
        mean_error
    ])

results_df = pd.DataFrame(
    results,
    columns=[
        "Attack",
        "Samples",
        "Detected",
        "DetectionRate",
        "MeanError"
    ]
)

results_df = results_df.sort_values(
    by="DetectionRate",
    ascending=False
)

# ============================================================
# PRINT RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("DENOISING AUTOENCODER RESULTS")
print("=" * 70)

print(results_df)

# ============================================================
# SAVE RESULTS
# ============================================================

SAVE_PATH = (
    "models/autoencoder/"
    "denoising_autoencoder_evaluation.csv"
)

results_df.to_csv(
    SAVE_PATH,
    index=False
)

print("\nSaved:")
print(SAVE_PATH)

# ============================================================
# SUMMARY
# ============================================================

print("\nTop Detection Rates")

print(
    results_df[
        ["Attack", "DetectionRate"]
    ]
)