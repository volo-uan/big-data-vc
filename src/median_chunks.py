from collections import Counter
import pandas as pd

freq = Counter()

for chunk in pd.read_csv(
    "/data/yellow_tripdata_2024-01.csv",
    chunksize=1_000_000,
    usecols=["trip_distance"]
):
    freq.update(chunk["trip_distance"])

total = sum(freq.values())

left = (total - 1) // 2
right = total // 2

count = 0
m1 = None
m2 = None

for value in sorted(freq):
    count += freq[value]

    if m1 is None and count > left:
        m1 = value

    if m2 is None and count > right:
        m2 = value
        break

median = (m1 + m2) / 2

print("median =", median)
print("state_size =", len(freq))