import time

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("z4-year").getOrCreate()

df = spark.read.parquet("hdfs:///taxi")

t0 = time.time()
print("partitions:", df.rdd.getNumPartitions())
print(f"time partitions: {time.time() - t0:.2f}s")

t0 = time.time()
rows = df.count()
print("rows:", rows)
print(f"time count: {time.time() - t0:.2f}s")

t0 = time.time()
mean_distance = df.agg(
    F.avg("trip_distance").alias("avg")
).first()["avg"]

print(f"mean distance: {mean_distance:.4f}")
print(f"time avg: {time.time() - t0:.2f}s")

t0 = time.time()

zones = (
    df.groupBy("PULocationID")
      .agg(
          F.avg("trip_distance").alias("avg"),
          F.count("*").alias("trips")
      )
)

for row in zones.collect():
    print(
        f"{row['PULocationID']}\t"
        f"{row['avg']:.4f}\t"
        f"{row['trips']}"
    )

print(f"time by zone: {time.time() - t0:.2f}s")

spark.stop()