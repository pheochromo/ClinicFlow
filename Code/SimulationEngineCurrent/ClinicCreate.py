# -*- coding: utf-8 -*-
"""
ClinicCreate creates the clinic file using information from the database, 
and information from a user defined clinic file.

use: conda install -c anaconda openpyxl=2.4.1 
to set up openpyxl to read xlsx file

use: conda install -c anaconda pandas=0.19.2 
to set up panda to do data analysis
"""
import math
import datetime
import numpy as np
import pandas as pd
import itertools as it
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from ClinicMerge import ClinicMerge

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
        apDiff = apDiff.append(pd.DataFrame([row[1][1] - row[1][0]]), ignore_index=True)
    apMean = apDiff.mean()[0]*60*24 # mean of distribution
    apStd = apDiff.std()[0]*60*24
    f = open(fileName, 'w') 
    ## create the information for arrivals
    f.write('Arrivals' + ' ' + 'Arrivals'  + ' ' +  '1' + ' ' + '1' + ' ' + 'uniform' + ' ' + repr(apMean) + ' ' + repr(apStd) + '\n')
    previousDests = []
    #handle creating the information for each of the clinic modules
    for i in range(3,len(headerNames),2):
        sectionName = headerNames[i][:-7]  
        sectionName = ''.join(sectionName.split())  
        secTime = df.ix[:,headerNames[i]:headerNames[i+1]] ## 
        secTime = secTime.dropna(how='any') ##remove Nan from this selection
        secDiff = pd.DataFrame() # create a dataframe for the differences
        for row in secTime.iterrows():
            secDiff = secDiff.append(pd.DataFrame([row[1][1] - row[1][0]]), ignore_index=True)
        secMean = secDiff.mean()[0]*60*24 # mean of distribution
        secStd = secDiff.std()[0] *60*24 # std of distribution * sqrt(60*24)
        previousDests.append(sectionName) #','.join(previousDests), replace the section name to create prerequisites; for no prerequesites use sectionName 
        tempData = ClinicMerge(sectionName,'ClinicData1.txt')
        tempString = ''
        if(tempData[4] == '2'):
            tempString = tempData[0] + ' ' + tempData[1] + ' ' + tempData[2] + ' ' + tempData[3] + ' ' + 'normal'
        else:
            tempString = tempData[0] + ' ' + tempData[1] + ' ' + tempData[2] + ' ' + tempData[3] + ' ' + 'exponential'
        f.write(tempString + ' ' + repr(secMean) + ' ' + repr(secStd))
        if(i != len(headerNames) - 2):
            f.write('\n')
    f.close()
    return fileName
    
## There needs to be another file that contains the qualitative data and that needs to be merged with the data file created here

 #Test Harness
#def main():
#   newClinic = clinicCreate()
#   f = open(newClinic, 'r')
 #  for line in f:
#       print(line)
#   f.close()
#if __name__ == "__main__": main()