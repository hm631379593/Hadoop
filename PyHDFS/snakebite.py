import webhdfspy
import pandas as pd
webHDFS = webhdfspy.WebHDFSClient("host6.cloud.sinocbd.com", 50070,username='root')
data=pd.DataFrame(webHDFS.listdir('/'))
print(data)
pathlist=data['pathSuffix']
for i in pathlist:
    path="/"+pathlist
    # print(path)
    # print(webHDFS.listdir(path))