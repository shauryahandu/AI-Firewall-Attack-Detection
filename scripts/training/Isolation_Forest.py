import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import IsolationForest

# =====================================
# LOAD DATA
# =====================================

df = pd.read_parquet(
    "processed/master_network_attacks_v1.parquet"
)

# Keep only benign traffic
df = df[df["attack_type"] == "BENIGN"].copy()

print("Benign Samples:", len(df))

# =====================================
# CLEANUP
# =====================================

if "Flow Bytes/s" in df.columns:
    df["Flow Bytes/s"] = df["Flow Bytes/s"].fillna(0)

X = df.drop(
    columns=[
        "Label",
        "attack_type"
    ]
)

# =====================================
# MEMORY OPTIMIZATION
# =====================================

for col in X.select_dtypes(include=["float64"]).columns:
    X[col] = X[col].astype("float32")

for col in X.select_dtypes(include=["int64"]).columns:
    X[col] = pd.to_numeric(
        X[col],
        downcast="integer"
    )

print("Shape:", X.shape)

# =====================================
# ISOLATION FOREST
# =====================================

iso = IsolationForest(
    n_estimators=300,
    contamination=0.01,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

iso.fit(X)

# =====================================
# SAVE MODEL
# =====================================

joblib.dump(
    iso,
    "firewall_isolation_forest.pkl"
)

print("Saved: firewall_isolation_forest.pkl")

attacks = pd.read_parquet(
    "processed/master_network_attacks_v1.parquet"
)

attacks = attacks[
    attacks["attack_type"] != "BENIGN"
]

X_attack = attacks.drop(
    columns=[
        "Label",
        "attack_type"
    ]
)

scores = iso.predict(X_attack)

anomaly_rate = (
    (scores == -1).sum()
    / len(scores)
)

print(
    f"Attack Detection Rate: "
    f"{anomaly_rate:.4f}"
)

import numpy as np
import pandas as pd

# Reload attack traffic
attacks = pd.read_parquet(
    "processed/master_network_attacks_v1.parquet"
)

attacks = attacks[
    attacks["attack_type"] != "BENIGN"
].copy()

if "Flow Bytes/s" in attacks.columns:
    attacks["Flow Bytes/s"] = attacks["Flow Bytes/s"].fillna(0)

X_attack = attacks.drop(
    columns=["Label", "attack_type"]
)

# Same dtype conversions used during training
for col in X_attack.select_dtypes(include=["float64"]).columns:
    X_attack[col] = X_attack[col].astype("float32")

for col in X_attack.select_dtypes(include=["int64"]).columns:
    X_attack[col] = pd.to_numeric(
        X_attack[col],
        downcast="integer"
    )

scores = iso.decision_function(X_attack)

print("Min:", scores.min())
print("Max:", scores.max())
print("Mean:", scores.mean())

for p in [1, 5, 10, 20, 30]:
    threshold = np.percentile(scores, p)
    detected = (scores < threshold).mean()

    print(
        f"Threshold {p}% -> Detection Rate: {detected:.4f}"
    )