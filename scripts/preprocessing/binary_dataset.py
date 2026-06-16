import pandas as pd

df = pd.read_csv("processed/master_network_attacks_v1.csv")

df["is_attack"] = (df["attack_type"] != "BENIGN").astype(int)

print(df["is_attack"].value_counts())