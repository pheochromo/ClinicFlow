# -*- coding: utf-8 -*-
"""
Loads the clinic data
@author: karl_
"""
import os
from .ClinicStation import *

import pymongo
from pymongo import MongoClient #import MongoDB
client = MongoClient()
db = client.Clinic_database
settings = db.application_setting



class Clinic:
    def __init__(self):
        client = MongoClient()
        db = client.Clinic_database
        settings = db.application_setting
        currentSettings = settings.currentSettings
        self.stations = []
        clinicSettings = currentSettings.find({"object":"provider"})

        for provider in clinicSettings:
            print(provider["name"])
            print("___")
            temp = ClinicStation(provider["name"], provider["preReqs"], provider["maxNum"], provider["minNum"], provider["varType"], provider["avg"],  provider["dev"])
            self.stations.append(temp)


#Test Harness
def main():
   file = "ClinicFile1.txt"
   newClinic = Clinic(file)
   for station in newClinic.stations:
       print(station.name, station.prerequesites, station.maximum, station.minimum,station.varianceType, station.mean, station.var)

if __name__ == "__main__": main()


## ability to add constraints to optimization schedules
