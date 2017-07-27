# coding: utf-8
from __future__ import print_function
import datetime
import time
import numpy as np
import statsmodels.api as sm
import pandas as pd
import pymongo
import matplotlib.pyplot as plt


def ObtainData(facilityname):
    collection=ConnectToMongo()
    data=collection.find({"Equipment" : facilityname})
    for n in data:
        values=n['RealtimeData']
        dtavalue=[]
        time=[]
        for i in values:
            d = i['time']
            time.append(d)
            dtavalue.append(i['value'])
    dtavalue=np.array(dtavalue,dtype=np.float)
    dtavalue=pd.Series(dtavalue)
    dtavalue.index=pd.Index(time)
    return dtavalue

def DealWithData(facilityname,dta):
    collection=ConnectToMongo()
    bson=collection.find_one({"Equipment": facilityname})
    dict_sorted=bson['Parameters']
    print(tuple(dict_sorted[1]))
    mod = sm.tsa.statespace.SARIMAX(dta,order=tuple(dict_sorted[0]),
    seasonal_order=tuple(dict_sorted[1]),
    enforce_stationarity=False,
    enforce_invertibility=False,freq='s')
    results = mod.fit()
    nowdata=findFacilityLastTimestamp(facilityname)
    lengthdata=len(bson['RealtimeData'])
    # print(lengthdata)
    # print(type(nowdata))
    # print(type(dta))
    # print(pd.to_datetime(nowdata))
    pred = results.get_prediction(start=nowdata,end=lengthdata+4,dynamic=False)
    print(pred.predicted_mean)
    pred_ci = pred.conf_int()
    # list2=[]
    # list1=[]
    # for i in pred.predicted_mean.values:
    #     a=float('%.2f' % i)
    #     list2.append(a)
    # nowdata=nowdata-datetime.timedelta(seconds=1)
    # for i in pred.predicted_mean.index:
    #     # print(i)
    #     # print(type(i))
    #     nowdata=nowdata+ datetime.timedelta(seconds=1)
    #     # print(nowdata)
    #     # print(type(nowdata))
    #     list1.append(nowdata)
    # data=pd.Series(list2)
    # data.index=pd.Index(list1)
    print(dta)
    ax = dta['2017-06-19 00:00:16':'2017-06-19 23:05:25'].plot(label='observed')
    # dta.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, color='b')
    # ax1=dta['2017-06-19 23:05:18':'2017-06-19 23:59:28']
    dta.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)
    plt.show()
    print(list1,list2)
    return list1,list2

def PredictDataToMongo(facilityname,list1,list2):
    collection=ConnectToMongo()
    dict_data = {}
    predictdata = []
    length=len(list1)
    for n in range(length):
        dict_data['time']=list1[n]
        dict_data['value']=list2[n]
        predictdata.append(dict_data.copy())
    collection.update({"Equipment": facilityname}, {"$set": {"PredictData":predictdata}})

def findFacilityLastTimestamp(facilityname):
    collection=ConnectToMongo()
    data = collection.find_one({"Equipment": facilityname})
    if(data):
        rs=data['RealtimeData'][-1]['time']
    return rs

def ConnectToMongo():
    mongoAddress='localhost'
    mongoPort=27017
    client = pymongo.MongoClient(mongoAddress, mongoPort)
    db = client.DataSource
    collection = db.table1
    return collection

if __name__ == '__main__':
    # while True:
    #     path = "C:\\Users\\hc\\Documents\\Tencent Files\\924520086\\FileRecv\\6.2.3.2 中间烘房传感器状态值\\20170509\\"
    #     filetype = '.csv'
    #     import os
    #     name = []
    #     for root, dirs, files in os.walk(path):
    #         for i in files:
    #             if filetype in i:
    #                 name.append(i.replace(filetype, ''))
        # print(name)
    facilityname='PT_TB1_LV0241.11S1_HECK_ALGIY2.R2251_LG_TA_R25'
        # for facilityname in name:
        #     filename = path + facilityname + filetype
        #     print(facilityname)
    mongoAddress = 'localhost'
    mongoPort = 27017
    dtavalue = ObtainData(facilityname=facilityname )
    list1, list2 = DealWithData(facilityname=facilityname,dta=dtavalue)
    PredictDataToMongo(facilityname, list1, list2)
        # time.sleep(180)