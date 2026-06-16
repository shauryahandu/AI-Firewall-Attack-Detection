import pandas as pd
import glob
import os

files = glob.glob(r"raw/network/*.csv")

for file in files:
    try:
        df = pd.read_csv(file, nrows=5)
        print("\n", os.path.basename(file))

        full_df = pd.read_csv(file, usecols=[" Label"])
        print(full_df[" Label"].value_counts())

    except Exception as e:
        print(file, e)