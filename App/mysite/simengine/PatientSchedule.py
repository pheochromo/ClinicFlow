# -*- coding: utf-8 -*-
"""

@author: karl_
"""
import os
from .Patient import *
import numpy as NP

import pymongo
from pymongo import MongoClient #import MongoDB
client = MongoClient()
db = client.Clinic_database # create schema
settings = db.application_setting #data of setting

result = db.result # temporarily store the data of simulation
schedule_list = db.schedulelist # a list of schedule, contain date and settings

class PatientSchedule:
    def __init__(self,date):
        self.patients = []
        self.arrivalVariance = "uniform"
        self.arrivalAvg = 0
        self.arrivalVar = 0

        patientdate = db[date+"patient"]
        patients = patientdate.find()
        counter = 0
        for single in patients:
            print("\n\n\n"+','.join(single["Visit"])+"\n")
            temp = Patient(single["Name"], single["Visit"])
            temptime = single["Time"].split(":")
            hrs = temptime[0]
            mins = temptime[1]
            appttime = 60*int(hrs)+int(mins)
            temp.assignTime(appttime-60*8 + NP.random.poisson(5,1))
            self.patients.append(temp)
            counter += 1

        # for line in patientFile:
        #     data = line.split()
        #     temp = Patient(data[0], data[1].split(','))
        #     self.patients.append(temp)

    # def schedule(self):
    #     counter = 0
    #     for element in self.patients:
    #         self.patients[counter].assignTime(counter*10 + NP.random.poisson(5,1)) ##schedule a patient every 15 minutes
    #         counter += 1

    # def loadSchedule(self):
    #     print("loading schedule \n")

# Test Harness
#def main():
#    file = "TestPatients.txt"
#    newSchedule = PatientSchedule(file)
#   newSchedule.schedule()
#    for person in newSchedule.patients:
#        print(person.name, person.arrivalTime[0], person.stations)


#if __name__ == "__main__": main()


## ability to add constraints to optimization schedules
