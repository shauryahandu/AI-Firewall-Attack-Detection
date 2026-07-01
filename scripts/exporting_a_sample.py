import pandas as pd

df = pd.read_parquet(
    "data/processed/master_network_attacks_v1.parquet"
)

samples = pd.concat([
    df[df["Label"] == "BENIGN"].head(3),
    df[df["Label"] == "DDoS"].head(3),
    df[df["Label"] == "PortScan"].head(3),
    df[df["Label"] == "Bot"].head(3),
])

samples = samples.drop(
    columns=["Label", "attack_type"],
    errors="ignore"
)

samples.to_csv(
    "mixed_demo.csv",
    index=False
)

print("Saved mixed_demo.csv")