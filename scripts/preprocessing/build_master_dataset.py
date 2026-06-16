import pandas as pd

all_dfs = []

# ==========================
# SQLiV2
# ==========================

print("Loading SQLiV2...")

df = pd.read_csv(
    r"raw\web\sqliv2.csv",
    encoding="utf-16"
)

df = df.rename(columns={"Sentence": "payload"})

df = df[["payload"]]

df = df.dropna()

df["attack_type"] = "SQLi"

all_dfs.append(df)

# ==========================
# SQLiV3
# ==========================

print("Loading SQLiV3...")

df = pd.read_csv(
    r"raw\web\SQLiV3.csv"
)

df = df[["Sentence"]]

df = df.rename(
    columns={
        "Sentence": "payload"
    }
)

df = df.dropna()

df["attack_type"] = "SQLi"

all_dfs.append(df)

# ==========================
# XSS DATASET
# ==========================

print("Loading XSS...")

df = pd.read_csv(
    r"raw\web\XSS_dataset.csv"
)

df = df[["Sentence", "Label"]]

df = df.rename(
    columns={
        "Sentence": "payload"
    }
)

df["attack_type"] = df["Label"].map(
    {
        0: "Normal",
        1: "XSS"
    }
)

df = df[
    ["payload", "attack_type"]
]

all_dfs.append(df)

# ==========================
# PAYLOAD TRAIN
# ==========================

print("Loading payload_train...")

df = pd.read_csv(
    r"raw\web\payload_train.csv"
)

df = df[
    ["payload", "attack_type"]
]

label_map = {
    "norm": "Normal",
    "sqli": "SQLi",
    "xss": "XSS",
    "path-traversal": "PathTraversal",
    "cmdi": "CommandInjection"
}

df["attack_type"] = (
    df["attack_type"]
    .map(label_map)
)

all_dfs.append(df)

# ==========================
# COMBINE
# ==========================

print("Combining...")

master_df = pd.concat(
    all_dfs,
    ignore_index=True
)

master_df = master_df.dropna()

master_df["payload"] = (
    master_df["payload"]
    .astype(str)
    .str.strip()
)

master_df = master_df[
    master_df["payload"] != ""
]

master_df = master_df.drop_duplicates()

# ==========================
# SAVE
# ==========================

output_path = (
    r"processed\master_web_attacks_v1.csv"
)

master_df.to_csv(
    output_path,
    index=False
)

print("\nSaved!")

print(master_df.shape)

print(master_df["attack_type"].value_counts())

df = pd.read_csv("processed/master_web_attacks_v1.csv")

# Keep only Normal and SQLi
df = df[df["attack_type"].isin(["Normal", "SQLi"])]

print(df["attack_type"].value_counts())

df.to_csv(
    "processed/sqli_binary.csv",
    index=False
)