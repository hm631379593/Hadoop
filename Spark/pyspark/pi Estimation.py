import sys
import os
os.environ["SPARK_HOME"]="/usr/hdp/2.5.0.0-1245/spark2"
sys.path.append("/usr/hdp/2.5.0.0-1245/spark2/python")
from pyspark.ml.clustering import KMeans
from pyspark.mllib.linalg import Vectors
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from numpy import random
def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

# conf = SparkConf().setAppName("appName").setMaster("local")
conf = SparkConf().setAppName("appName")
sc = SparkContext(conf=conf)
count = sc.parallelize(xrange(0, 10000000)).filter(inside).count()
print("Pi is roughly %f" % (4.0 * count / 10000000))