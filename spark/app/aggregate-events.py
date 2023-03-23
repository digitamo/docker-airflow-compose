import os
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import collect_list, map_from_entries, struct, col, max
from pyspark.sql import Window

EVENTS_S3_URI = os.environ.get("EVENTS_S3_URI")
S3_ENDPOINT = os.environ.get("S3_ENDPOINT")
S3_KEY = os.environ.get("S3_KEY")
OUTPUT_BUCKET = "s3://output/"


def create_spark_session():
    def configure_spark():
        conf = SparkConf().setAppName("AggregateUserEvents").setMaster("local[*]")

        spark_context = SparkContext(conf=conf)

        hadoop_config = spark_context._jsc.hadoopConfiguration()
        hadoop_config.set("fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        hadoop_config.set("fs.s3a.access.key", "mock")
        hadoop_config.set("fs.s3a.secret.key", "mock")
        hadoop_config.set("fs.s3a.path.style.access", "true")
        hadoop_config.set("fs.s3a.endpoint", S3_ENDPOINT)

        return spark_context

    spark_context = configure_spark()
    return SparkSession(spark_context)


spark = create_spark_session()
events_df = spark.read.csv(EVENTS_S3_URI, header=True).repartition("id")

window = Window.partitionBy("id", "name")
events_df = (
    events_df.withColumn("max_timestamp", max("timestamp").over(window))
    .where(col("timestamp") == col("max_timestamp"))
    .drop("max_timestamp")
    .groupBy("id")
    .agg(map_from_entries(collect_list(struct("name", "value"))).alias("settings"))
)

output_path = OUTPUT_BUCKET + S3_KEY
events_df.write.partitionBy("id").mode("overwrite").parquet(output_path)
