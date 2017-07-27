import sys
import os
os.environ["SPARK_HOME"]="/usr/hdp/2.5.0.0-1245/spark"
sys.path.append("/usr/hdp/2.5.0.0-1245/spark/python")
from pyspark.ml.clustering import KMeans
from pyspark.mllib.linalg import Vectors
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
conf = SparkConf().setAppName("appName").setMaster("local")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
data = [(Vectors.dense([0.0, 0.0]),), (Vectors.dense([1.0, 1.0]),),(Vectors.dense([9.0, 8.0]),), (Vectors.dense([8.0, 9.0]),)]
df = sqlContext.createDataFrame(data, ["features"])
kmeans = KMeans(k=2, seed=1)
model = kmeans.fit(df)
centers = model.clusterCenters()
print('***************************')
print(len(centers))
transformed = model.transform(df).select("features", "prediction")
rows = transformed.collect()
rows[0].prediction == rows[1].prediction
print('**************************')
print(rows[0])
rows[2].prediction == rows[3].prediction
print('***************************')
print(rows[2])