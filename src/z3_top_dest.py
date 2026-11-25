from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("z3-top-dest").getOrCreate()

df = spark.read.parquet(
    "hdfs:///taxi/yellow_tripdata_2024-01.parquet"
)

pairs = (
    df.groupBy("PULocationID", "DOLocationID")
      .count()
)

result = (
    pairs.groupBy("PULocationID")
         .agg(
             F.max_by("DOLocationID", "count").alias("top_dest"),
             F.max("count").alias("trips"),
         )
)

# Plan wykonania
result.explain()

for row in result.collect():
    print(
        f"{row['PULocationID']}\t"
        f"{row['top_dest']}\t"
        f"{row['trips']}"
    )

spark.stop()