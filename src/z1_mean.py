import sys
import time

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

fmt = sys.argv[1]  # csv | parquet
sleep_time = float(sys.argv[2]) if len(sys.argv) > 2 else 0

spark = SparkSession.builder.appName("z1-mean").getOrCreate()

if fmt == "csv":
    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("hdfs:///csv/yellow_tripdata_2024-01.csv")
    )
elif fmt == "parquet":
    df = spark.read.parquet(
        "hdfs:///taxi/yellow_tripdata_2024-01.parquet"
    )
else:
    raise ValueError("argument must be csv or parquet")

result = (
    df.groupBy("PULocationID")
      .agg(
          F.avg("trip_distance").alias("mean_distance"),
          F.count("trip_distance").alias("trips")
      )
)

for row in result.collect():
    print(
        f"{row['PULocationID']}\t"
        f"{row['mean_distance']:.4f}\t"
        f"{row['trips']}"
    )

time.sleep(sleep_time)
spark.stop()