"""List 5, Z0: the same January in pandas and in Spark on your laptop, without a cluster.

  uv run python src/z0_local.py local[*] 60
The second argument keeps the program (and Spark UI on localhost:4040) alive for that many seconds.
"""
import sys
import time

import pandas as pd
from pyspark.sql import SparkSession

PATH = "data/yellow_tripdata_2024-01.parquet"
master = sys.argv[1] if len(sys.argv) > 1 else "local[*]"

t0 = time.time()
pdf = pd.read_parquet(PATH)
print("pandas: trips over 50 miles:", len(pdf[pdf.trip_distance > 50]))
print(pdf[pdf.total_amount > 0][["trip_distance", "total_amount"]].describe())
print(f"pandas: {time.time() - t0:.1f} s")

t0 = time.time()
spark = SparkSession.builder.master(master).appName("z0-local").getOrCreate()
df = spark.read.parquet(PATH)
print(
    "spark: trips over 50 miles:",
    df.where(df.trip_distance > 50).count(),
)

df.select("trip_distance", "total_amount") \
    .filter(df.total_amount > 0) \
    .summary() \
    .show()

print(f"spark {master}: {time.time() - t0:.1f} s, partitions: {df.rdd.getNumPartitions()}")
time.sleep(float(sys.argv[2]) if len(sys.argv) > 2 else 0)
spark.stop()
