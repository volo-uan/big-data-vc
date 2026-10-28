import pandas as pd

path = "/data/yellow_tripdata_2024-01.csv"

means = []
total_sum = 0
total_count = 0

for i, chunk in enumerate(
    pd.read_csv(path, chunksize=1_000_000)
):
    mean = chunk["trip_distance"].mean()
    median = chunk["trip_distance"].median()

    print(
        f"chunk {i+1}: rows={len(chunk)} "
        f"mean={mean:.4f} median={median:.2f}"
    )

    means.append(mean)
    total_sum += chunk["trip_distance"].sum()
    total_count += len(chunk)

print()
print("mean_of_means =", sum(means) / len(means))
print("global_mean   =", total_sum / total_count)