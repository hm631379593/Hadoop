# coding: utf-8
from __future__ import print_function
import warnings
import itertools
import numpy as np
import statsmodels.api as sm
import datetime
import pandas as pd
import pymongo
import csv
import time

def DataToMongo(facilityname,filename):
    dict_values = []
    csv_reader = csv.reader(open(filename))
    collection=ConnectToMongo()
    for row in csv_reader:
        value=row[0].split(';')
        value1=value[0]
        value2=float(value[1].replace('"',''))
        value3=value[2].replace('"','')
        time2 = datetime.date.today()
        currentdate = time2.strftime('%Y%m%d')
        a=currentdate+value1
        timeArray = time.strptime(a, "%Y%m%d%H:%M:%S")
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # print(type(datetime.datetime.strptime(otherStyleTime,"%Y-%m-%d %H:%M:%S")))
        otherStyleTime=datetime.datetime.strptime(otherStyleTime, "%Y-%m-%d %H:%M:%S")
        dict_values.append({'time':otherStyleTime,'value':float('%.2f' % value2)})
        # print(value1,'%.2f' % value2)
        # print(dict_values)
        dict={'Equipment':facilityname,'RealtimeData':dict_values}
        # print(dict)
    collection.insert(dict)

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

def CalculateParameters(facilityname,dta):
    dta.plot(figsize=(12,8))
    # Define the p, d and q parameters to take any value between 0 and 2
    p = d = q = range(0, 2)
    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))
    # # Generate all different combinations of seasonal p, q and q triplets
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    print('Examples of parameter combinations for Seasonal ARIMA...')
    print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
    print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
    print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
    print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))
    warnings.filterwarnings("ignore") # specify to ignore warning messages
    arima={}
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(dta,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                results = mod.fit()
                arima[param, param_seasonal]=results.aic
            except:
                continue
    # print(arima)
    dict_sorted = sorted(arima.items(), key=lambda d: d[1], reverse=False)
    print(dict_sorted)
    collection=ConnectToMongo()
    collection.update({"Equipment": facilityname},
                      {"$set": {"Parameters": [dict_sorted[0][0][0],dict_sorted[0][0][1]]}})
    return dict_sorted

def ConnectToMongo():
    mongoAddress='localhost'
    mongoPort=27017
    client = pymongo.MongoClient(mongoAddress, mongoPort)
    db = client.DataSource2
    collection = db.table1
    return collection

if __name__ == '__main__':
    path = "C:\\Users\\hc\\Documents\\Tencent Files\\924520086\\FileRecv\\6.2.3.2 中间烘房传感器状态值\\20170509\\"
    filetype = '.csv'
    import os
    name = []
    for root, dirs, files in os.walk(path):
        for i in files:
            if filetype in i:
                name.append(i.replace(filetype, ''))
    # print(name)
    filename="C:\\Users\\hc\\Documents\\Tencent Files\\924520086\\FileRecv\\6.2.3.2 中间烘房传感器状态值\\20170509\\PT_TB1_LV0241.11S2_AB119_M04.AA.R2251_ActValue.csv"
    facilityname='PT_TB1_LV0241.11S2_AB119_M04.AA.R2251_ActValue'
    # for facilityname in name:
        # filename="C:\\Users\hc\\Documents\\Tencent Files\\924520086\\FileRecv\\6.2.3.2 中间烘房传感器状态值\\20170509\\PT_TB1_LV0241.11S1_HECK_ALGIY2.R2251_TK_TA_R45.csv"
        # facilityname = []
        # facilityname = filename.split('\\')
        # facilityname = facilityname[-1]
        # facilityname = facilityname.replace('.csv', '')
    print(facilityname)
    filename=path+facilityname+filetype
    DataToMongo(facilityname=facilityname,filename=filename)
    dtavalue=ObtainData(facilityname=facilityname)
    CalculateParameters(facilityname=facilityname,dta=dtavalue)