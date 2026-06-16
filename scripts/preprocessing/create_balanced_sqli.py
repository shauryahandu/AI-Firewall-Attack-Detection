import pandas as pd

df = pd.read_csv(
    r"processed/sqli_binary.csv"
)

normal = df[df["attack_type"] == "Normal"]
sqli = df[df["attack_type"] == "SQLi"]

# Downsample SQLi
sqli = sqli.sample(
    n=len(normal),
    random_state=42
)

balanced = pd.concat(
    [normal, sqli],
    ignore_index=True
)

print(balanced["attack_type"].value_counts())

balanced.to_csv(
    r"processed/sqli_balanced.csv",
    index=False
)

print("Saved!")