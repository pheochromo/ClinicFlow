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

def clinicCreate():
    fileName = "newClinicFile.txt"
    ## The following two lines should be changed to allow for data access from a database file
    wb2 = load_workbook('PreOpModified2017.xlsx') #change to database file
    sheet1 = wb2['Sheet1'] # get the first sheet 
    length = len(sheet1['A'])
    
    # process the sheet into a readable format
    headers = sheet1[1]
    headerNames = []
    for x in headers:
        headerNames.append(x.value)
    data = sheet1[2:length]
    arr = np.asarray(data)
    arr2 = np.empty_like(arr)
    totalTime = 24.0*60.0
    for i in range(0,length-1):
        for j in range(0,len(data[1])):
            temp = arr[i][j].value
            if isinstance(temp, datetime.time):
                temp2 = (60*temp.hour +temp.minute)/totalTime #convert the times into a scale from 0 to 1
                arr2[i][j] = temp2
            else:
                arr2[i][j] = np.nan
    
    df = pd.DataFrame(arr2,columns = headerNames)
    
    apTime = df.ix[:,'Scheduled Appointment Time':'Arrival Time'] ## select scheduled arrivaltime and given arrival time
    apTime = apTime.dropna(how='any') ##remove Nan from this selection
    apDiff = pd.DataFrame() # create a dataframe for the differences
    for row in apTime.iterrows():
        #print(row[1][0] - row[1][1])
        apDiff = apDiff.append(pd.DataFrame([row[1][1] - row[1][0]]), ignore_index=True)
    
    apMean = apDiff.mean()[0]*60 # mean of distribution
    apStd = apDiff.std()[0] *60# std of distribution
    
    f = open(fileName, 'w') 
    ## read in other data from another database
    f.write('Arrivals' + ' ' + 'Arrivals' + ' ' + '1' + ' ' +  '1' + ' ' + 'normal' + ' ' + repr(apMean) + ' ' + repr(apStd) + '\n')
    previousDests = []
    for i in range(3,len(headerNames),2):
        sectionName = headerNames[i][:-7]  
        sectionName = ''.join(sectionName.split())  
        secTime = df.ix[:,headerNames[i]:headerNames[i+1]] ## 
        secTime = secTime.dropna(how='any') ##remove Nan from this selection
        secDiff = pd.DataFrame() # create a dataframe for the differences
        for row in secTime.iterrows():
            secDiff = secDiff.append(pd.DataFrame([row[1][1] - row[1][0]]), ignore_index=True)
    
        secMean = secDiff.mean()[0]*60 # mean of distribution
        secStd = secDiff.std()[0] *60# std of distribution
        previousDests.append(sectionName) #','.join(previousDests), replace the section name to create prerequisites; for no prerequesites use sectionName 
        f.write(sectionName + ' ' + sectionName + ' ' + '2' + ' ' +  '1' + ' ' + 'exponential' + ' ' + repr(secMean) + ' ' + repr(secStd))
        if(i != len(headerNames) - 2):
            f.write('\n')
    f.close()
    return fileName
    
## There needs to be another file that contains the qualitative data and that needs to be merged with the data file created here
