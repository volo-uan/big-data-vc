from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("z2-median").getOrCreate()

df = spark.read.parquet(
    "hdfs:///taxi/yellow_tripdata_2024-01.parquet"
)

result = (
    df.groupBy("PULocationID")
      .agg(
          F.median("trip_distance").alias("median"),
          F.count("*").alias("trips"),
          F.percentile_approx("trip_distance", 0.5).alias("approx")
      )
)

for row in result.collect():
    print(
        f"{row['PULocationID']}\t"
        f"{row['median']:.3f}\t"
        f"{row['trips']}\t"
        f"{row['approx']:.3f}"
    )

spark.stop()