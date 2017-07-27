from kafka import KafkaProducer
producer =  KafkaProducer(bootstrap_servers='ambari-node5.cloud.sinocbd.com:6667,ambari-node0.cloud.sinocbd.com:6667,ambari-node2.cloud.sinocbd.com:6667')
producer.send("test3", "asdasdas".encode('utf-8'))
producer.flush()