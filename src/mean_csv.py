import pandas as pd

df = pd.read_csv("/data/yellow_tripdata_2024-01.csv")

print("rows:", len(df))
print("mean:", df["trip_distance"].mean())