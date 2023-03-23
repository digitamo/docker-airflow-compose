import os
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

EVENTS_S3_KEY = os.environ.get("EVENTS_S3_KEY")
S3_ENDPOINT = os.environ.get("S3_ENDPOINT")


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


print("EVENTS_S3_KEY >> ", EVENTS_S3_KEY)
print("S3_ENDPOINT >> ", S3_ENDPOINT)

spark = create_spark_session()
events_df = spark.read.csv(EVENTS_S3_KEY, header=True)
events_df.show()
