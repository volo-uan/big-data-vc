import pandas as pd

csv_df = pd.read_csv(
    "/data/yellow_tripdata_2024-01.csv",
    nrows=200_000
)

parquet_df = pd.read_parquet(
    "/data/yellow_tripdata_2024-01.parquet"
).head(200_000)

print("CSV")
print(csv_df.dtypes)
print()
print(csv_df.memory_usage(deep=True))

print("\n" + "=" * 50 + "\n")

print("PARQUET")
print(parquet_df.dtypes)
print()
print(parquet_df.memory_usage(deep=True))