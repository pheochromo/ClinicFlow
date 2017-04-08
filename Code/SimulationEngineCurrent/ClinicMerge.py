# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 10:55:28 2017

@author: karl_
"""


def ClinicMerge(module,dataFile):
    clinicFile = open(dataFile,mode ='r')
    returnString = ""
    for line in clinicFile:
        data = line.split()
        if(data[0] == module):
            returnString = data
                #temp = ClinicStation(data[0], data[1].split(','),data[2],data[3],data[4],data[5],data[6])
                #self.stations.append(temp)
    clinicFile.close()
    return returnString
    
    