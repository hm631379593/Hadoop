#encoding='utf-8'
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
    # sconf.set('spark.streaming.blockInterval','100')
    sconf.set('spark.cores.max' , 8)
    sc=SparkContext(appName='KafkaWordCount',conf=sconf)
    ssc=StreamingContext(sc,2)
    numStreams = 3
    kafkaStreams = [KafkaUtils.createStream(ssc,"ambari-node5.cloud.sinocbd.com:6667","streaming_test_group",{"spark_streaming_test_topic":1}) for _ in range (numStreams)]
    unifiedStream = ssc.union(*kafkaStreams)
    print unifiedStream
    result=unifiedStream.map(lambda x:(x[0],1)).reduceByKey(lambda x, y: x + y)
    result.pprint()
    ssc.start()             # Start the computation
    ssc.awaitTermination()  # Wait for the computation to terminate

if __name__ == '__main__':
    start()