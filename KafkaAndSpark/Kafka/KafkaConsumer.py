from kafka import KafkaConsumer
class KafkaPython:

    consumer = None
    TOPIC   = 'test3'
    #kkfhost = "ambari.cloud.sinocbd.com:6667,ambari-node2.cloud.sinocbd.com:6667,ambari-node5.cloud.sinocbd.com:6667"
    kkfhost = "ambari-node0.cloud.sinocbd.com:6667"
    server = topic =  None

    def __init__(self):
        print("begin kafka-python")
        self.server = self.kkfhost
        self.topic  = self.TOPIC

    def __del__(self):
        print("end")

    def getConnect(self):
            self.consumer = KafkaConsumer(self.topic, bootstrap_servers = self.server)

    def beginConsumer(self):
        for oneLog in self.consumer:
            print(oneLog.value.decode())


    def disConnect(self):
        self.consumer.close()


if __name__ == '__main__':

	kp = KafkaPython()
	kp.getConnect()
	kp.beginConsumer()