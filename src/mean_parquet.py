import pandas as pd

df = pd.read_parquet("/data/yellow_tripdata_2024-01.parquet")

print("rows:", len(df))
print("memory:", df.memory_usage(deep=True).sum())
print("mean:", df["trip_distance"].mean())