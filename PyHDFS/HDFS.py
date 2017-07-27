from hdfs.client import Client
client = Client("http://host6.cloud.sinocbd.com:50070/")  # 50070: Hadoop默认namenode
dir(client)
# 其中用到的方法有：
# walk() 类似os.walk，返回值也是包含(路径，目录名，文件名)元素的数组，每层迭代。
# read() 类似file.read，官方文档的说法是client.read必须在with块里使用：
# path=[]
# for i in client.walk('/tempfiles/temp',depth=1):
#     for item in i:
#      path.append(item)
#      print(item)
# print(path)
with client.read('/tempfiles/1.csv', encoding='gbk') as fs:
    content = fs.read()
    print(content)