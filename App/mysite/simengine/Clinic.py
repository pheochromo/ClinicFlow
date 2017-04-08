# -*- coding: utf-8 -*-
"""
Loads the clinic data
@author: karl_
"""
import os
from .ClinicStation import *

class Clinic:
   def __init__(self,fileName):

        # test
        file_name = os.path.join(os.path.dirname(__file__), fileName)

        clinicFile = open(file_name,mode ='r')
        self.stations = []
        for line in clinicFile:
            data = line.split()
            temp = ClinicStation(data[0], data[1].split(','),data[2],data[3],data[4],data[5],data[6])
            self.stations.append(temp)
        clinicFile.close()




#Test Harness
#def main():
#   file = "ClinicFile1.txt"
#    newClinic = Clinic(file)
#    for station in newClinic.stations:
#        print(station.name, station.prerequesites, station.maximum, station.minimum,station.varianceType, station.mean, station.var)

#if __name__ == "__main__": main()


## ability to add constraints to optimization schedules