import random
import os

from pyspark import SparkContext, SparkConf


NUM_SAMPLES = int(os.environ.get("NUM_SAMPLES"))


def get_spark_context():
    conf = SparkConf().setAppName("Example job").setMaster("local[*]")
    spark_context = SparkContext(conf=conf)

    return spark_context


"""
    This code estimates π by "throwing darts" at a circle. 
    We pick random points in the unit square ((0, 0) to (1,1)) and see how many fall in the unit circle. 
    The fraction should be π / 4, so we use this to get our estimate.
    """


def inside(p):
    x, y = random.random(), random.random()
    return x * x + y * y < 1


spark_context = get_spark_context()
count = spark_context.parallelize(range(0, NUM_SAMPLES)).filter(inside).count()
print("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))
