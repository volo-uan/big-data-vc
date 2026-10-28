import pandas as pd

df = pd.read_parquet("/data/yellow_tripdata_2024-01.parquet")

res = (
    df.groupby(
        ["PULocationID", "DOLocationID"]
    )["trip_distance"]
    .agg(["count", "mean"])
)

print("groups:", len(res))

print(
    res.sort_values(
        "count",
        ascending=False
    ).head(3)
)
