import csv
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import pymongo
import pandas as pd
import time

def DataIntoMongo(Equipment,ExcelData):
    collection=ConnectToMongo()
    collection.update({"Equipment":Equipment},{'$pushAll':{'RealtimeData': ExcelData}})

def ReadExcelData(filename,Equipment):
    rs=[]
    data = csv.reader(open(filename))
    mtime=findFacilityLastTimestamp(Equipment)
    for row in data:
        value = row[0].split(';')
        value1 = value[0]
        value2 = float(value[1].replace('"', ''))
        value3 = value[2].replace('"', '')
        nowdata = datetime.datetime.now()
        nowdata = nowdata.strftime('%Y-%m-%d %H:%M:%S')
        nowdata = datetime.datetime.strptime(nowdata, "%Y-%m-%d %H:%M:%S")
        exceldatastr=nowdata.date().strftime('%Y-%m-%d')+" "+value1
        exceldata = datetime.datetime.strptime(exceldatastr, "%Y-%m-%d %H:%M:%S")

        if((nowdata>mtime)&(exceldata<nowdata))&(exceldata>mtime):
            timeandvalue={'time':exceldata,'value':float('%.2f' % value2)}
            # print(timeandvalue)
            rs.append(timeandvalue)
    return rs

def findFacilityLastTimestamp(Equipment):
    collection=ConnectToMongo()
    data = collection.find_one({"Equipment": Equipment})
    if(data):
        rs=data['RealtimeData'][-1]['time']
    return rs

def createEquipmentData(facilityname):
    EquipmentName = facilityname
    filename = 'C:\\Users\\hc\\Documents\\Tencent Files\\924520086\\FileRecv\\6.2.3.2 中间烘房传感器状态值\\20170509\\' + EquipmentName + '.csv'
    rs = []
    rs = ReadExcelData(filename, EquipmentName)
    DataIntoMongo(EquipmentName, rs)
def ConnectToMongo():
    mongoAddress='localhost'
    mongoPort=27017
    client = pymongo.MongoClient(mongoAddress, mongoPort)
    db = client.DataSource2
    collection = db.table1
    return collection

if __name__ == '__main__':
    while True:
        path = "C:\\Users\\hc\\Documents\\Tencent Files\\924520086\\FileRecv\\6.2.3.2 中间烘房传感器状态值\\20170509\\"
        filetype = '.csv'
        import os
        name = []
        for root, dirs, files in os.walk(path):
            for i in files:
                if filetype in i:
                    name.append(i.replace(filetype, ''))
        for facilityname in name:
            print(facilityname)
        # facilityname='PT_TB1_LV0241.11S1_HECK_ALGIY2.R2251_TK_Y56'
        # filename = path + facilityname + filetype
            createEquipmentData(facilityname)
        time.sleep(120)