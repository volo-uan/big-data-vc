"""List 5, Z0: the first Spark program on the cluster - count the January trips."""
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("z0-count").getOrCreate()
df = spark.read.parquet("hdfs://namenode:9000/taxi/yellow_tripdata_2024-01.parquet")
print("rows:", df.count(), " partitions:", df.rdd.getNumPartitions())
spark.stop()
