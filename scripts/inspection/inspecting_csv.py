import pandas as pd

df = pd.read_csv("processed/master_network_attacks_v1.csv")

print(df.shape)

print("\nMissing values:")
print(df.isnull().sum().sort_values(ascending=False).head(20))
print("\nDtypes:")
print(df.dtypes.value_counts())