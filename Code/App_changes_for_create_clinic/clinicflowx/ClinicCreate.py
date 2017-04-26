# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 09:36:41 2017

@author: karl_

use: conda install -c anaconda openpyxl=2.4.1
to set up openpyxl to read xlsx file

use: conda install -c anaconda pandas=0.19.2
to set up panda to do data analysis
"""
import datetime
import numpy as np
import pandas as pd
import itertools as it
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pymongo
from pymongo import MongoClient #import MongoDB
client = MongoClient()
db = client.Clinic_database # create schema

settings = db.application_setting
currentSettings= settings.currentSettings
providers=[]
provider_from_set = currentSettings.find({"object":"provider"})
for each in provider_from_set:
    providers.append(each['name'])
    
result = db.result # temporarily store the data of simulation
schedule_list = db.schedulelist # a list of schedule, contain date and settings
passport = db.passport
def clinicCreate():
    fileName = "newClinicFile.txt"
    passportInfo = passport.find()
    header = ['Scheduled_Time','Arrival_Time','Departure_time']
    for each in providers:
        header.append(each+'_Time_In')
        header.append(each+'_Time_Out')
    data=[]
    i=0
    for row in passportInfo:
        eachpassport=[]
        for each in header:
            eachpassport.append(row[each])
        i=i+1
        data.append(eachpassport)
    therow= len(data[0])
    length=i
   
    arr2 = np.empty_like(data,dtype=float)
    totalTime = 24.0*60.0
    for i in range(0,length):
        for j in range(0,therow):
            temp = data[i][j]
            temp1 = temp.split(':')
            if temp != '' and len(temp1)>=2 :
                hour = int(temp1[0])
                minute = int(temp1[1])
                if 'pm' in temp1[2] or 'PM' in temp1[2]:
                        if hour <12:
                            hour=hour+12
                temp2 = (60*hour +minute)/totalTime #convert the times into a scale from 0 to 1
                arr2[i][j] =float(temp2)
            else:
                arr2[i][j] = np.nan
    
    df = pd.DataFrame(arr2,columns = header)
    
    apTime = df.ix[:,'Scheduled_Time':'Arrival_Time'] ## select scheduled arrivaltime and given arrival time
    apTime = apTime.dropna(how='any') ##remove Nan from this selection
    apDiff = pd.DataFrame() # create a dataframe for the differences
    for row in apTime.iterrows():
        apDiff = apDiff.append(pd.DataFrame([float(row[1][1]) - float(row[1][0])]), ignore_index=True)
    apMean = apDiff.mean()[0]*60*24 # mean of distribution
    apStd = apDiff.std()[0]*60*24
    f = open(fileName, 'w') 
    ## create the information for arrivals
    f.write('Arrivals' + ' ' + 'Arrivals'  + ' ' +  '1' + ' ' + '1' + ' ' + 'uniform' + ' ' + repr(apMean) + ' ' + repr(apStd) + '\n')
    
    settings = {"name":"Arrivals", "Num":1, "Distribution":"uniform", "ArrMean": apMean, "ArrStd":apStd}
    db.settings.delete_many({})
    db.settings.insert_one(settings)
    previousDests = []
    #handle creating the information for each of the clinic modules
    for i in range(3,therow,2):   
        sectionName = header[i][:-8]  
        sectionName = ''.join(sectionName.split())  
        secTime = df.ix[:,header[i]:header[i+1]] ## 
        secTime = secTime.dropna(how='any') ##remove Nan from this selection
        secDiff = pd.DataFrame() # create a dataframe for the differences
        for row in secTime.iterrows():
            secDiff = secDiff.append(pd.DataFrame([float(row[1][1]) - float(row[1][0])]), ignore_index=True)
        secMean = secDiff.mean()[0]*60*24 # mean of distribution
        secStd = secDiff.std()[0] *60*24 # std of distribution * sqrt(60*24)
        previousDests.append(sectionName) #','.join(previousDests), replace the section name to create prerequisites; for no prerequesites use sectionName 
        provider_from_set = currentSettings.find({"object":"provider"})
        for each in provider_from_set:
            print(each['name'])
            if sectionName == each['name']:
                temp = {"object": "provider", "name":each['name'], "preReqs":each['preReqs'], "maxNum":each['maxNum'], "minNum":each['minNum'], "varType":each['varType'], "avg":secMean, "dev":secStd}
                print(temp)
                currentSettings.replace_one(each,temp)

#==============================================================================
#         tempData = ClinicMerge(sectionName,'ClinicData1.txt')       
#         tempString = ''
#         if(tempData[4] == '2'):
#             tempString = tempData[0] + ' ' + tempData[1] + ' ' + tempData[2] + ' ' + tempData[3] + ' ' + 'normal'
#         else:
#             tempString = tempData[0] + ' ' + tempData[1] + ' ' + tempData[2] + ' ' + tempData[3] + ' ' + 'exponential'
#         f.write(tempString + ' ' + repr(secMean) + ' ' + repr(secStd))
#         if(i != length - 2):
#             f.write('\n')
#==============================================================================
    f.close()
    return fileName
## There needs to be another file that contains the qualitative data and that needs to be merged with the data file created here

def main():
   a=clinicCreate()
   f=open(a,'r')
   for line in f:
       print(line)
   f.close()
if __name__ == "__main__": main()