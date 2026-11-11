import pandas as pd

print("Loading parquet...")

df = pd.read_parquet("/data/yellow_tripdata_2024-01.parquet")

ref = (
    df.groupby("PULocationID")["trip_distance"]
    .agg(["count", "mean", "median"])
    .reset_index()
)

ref["PULocationID"] = ref["PULocationID"].astype(str)

mean_df = pd.read_csv(
    "/out/z1-mean.tsv",
    sep="\t",
    names=["PULocationID", "mean_cluster", "count_cluster"],
)

median_df = pd.read_csv(
    "/out/z3-median.tsv",
    sep="\t",
    names=[
        "PULocationID",
        "median_cluster",
        "count_median",
        "distinct_values",
    ],
)

avg_df = pd.read_csv(
    "/out/z2-avg.tsv",
    sep="\t",
    names=["PULocationID", "avg_combiner", "count_avg"],
)

mean_df["PULocationID"] = mean_df["PULocationID"].astype(str)
median_df["PULocationID"] = median_df["PULocationID"].astype(str)
avg_df["PULocationID"] = avg_df["PULocationID"].astype(str)

ref = ref.merge(mean_df, on="PULocationID")
ref = ref.merge(median_df, on="PULocationID")
ref = ref.merge(avg_df, on="PULocationID")

print()
print("Zones parquet:", len(ref))
print("Zones cluster:", len(mean_df))

count_ok = (ref["count"] == ref["count_cluster"]).all()

print("Counts equal:", count_ok)

max_mean_diff = (
    ref["mean"] - ref["mean_cluster"]
).abs().max()

print("Max mean difference:", max_mean_diff)

different_medians = (
    (ref["median"] - ref["median_cluster"]).abs() > 0.0001
).sum()

print("Different medians:", different_medians)

wrong = ref[
    (ref["mean"] - ref["avg_combiner"]).abs() > 0.01
].copy()

wrong["error"] = (
    ref["mean"] - ref["avg_combiner"]
).abs()

wrong = wrong.sort_values(
    "error",
    ascending=False
)

print()
print("z2-avg zones > 0.01:", len(wrong))

print()
print("Top 10 errors:")

print(
    wrong[
        [
            "PULocationID",
            "count",
            "mean",
            "avg_combiner",
            "error",
        ]
    ]
    .head(10)
    .to_string(index=False)
)