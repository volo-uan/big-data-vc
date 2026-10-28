import sys
import pandas as pd

path = "/data/yellow_tripdata_2024-01.csv"

if len(sys.argv) > 1:
    n = int(sys.argv[1])
    df = pd.read_csv(path, nrows=n)
else:
    df = pd.read_csv(path)

print("rows:", len(df))
print("memory:", df.memory_usage(deep=True).sum())