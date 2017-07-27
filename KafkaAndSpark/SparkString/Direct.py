import sys
import os
os.environ["SPARK_HOME"]="/usr/hdp/2.5.0.0-1245/spark"
sys.path.append("/usr/hdp/2.5.0.0-1245/spark/python")
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
def start():
    sconf=SparkConf()
    sconf.set('spark.cores.max' , 8)
    sc=SparkContext(appName='KafkaDirectWordCount',conf=sconf)
    ssc=StreamingContext(sc,2)
    brokers='ambari-node5.cloud.sinocbd.com:6667,ambari-node0.cloud.sinocbd.com:6667,ambari-node2.cloud.sinocbd.com:6667'
    topic='test3'
    kafkaStreams = KafkaUtils.createDirectStream(ssc,[topic],kafkaParams={"metadata.broker.list": brokers})
    result=kafkaStreams.map(lambda x:(x[0],1)).reduceByKey(lambda x, y: x + y)
    kafkaStreams.transform(storeOffsetRanges).foreachRDD(printOffsetRanges)
    result.pprint()
    ssc.start()
    ssc.awaitTermination()
offsetRanges = []
def storeOffsetRanges(rdd):
    global offsetRanges
    offsetRanges = rdd.offsetRanges()
    return rdd
def printOffsetRanges(rdd):
    for o in offsetRanges:
        print "%s %s %s %s %s" % (o.topic, o.partition, o.fromOffset, o.untilOffset,o.untilOffset-o.fromOffset)
if __name__ == '__main__':
    start()