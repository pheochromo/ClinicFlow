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

result = db.result # temporarily store the data of simulation
schedule_list = db.schedulelist # a list of schedule, contain date and settings

class PatientSchedule:
    def __init__(self,date):
        self.patients = []
        self.arrivalVariance = "uniform"
        self.date = date

        arrSettings = db.settings.find({"name":"Arrivals"})
        if arrSettings.count() > 0:
            arrMean = arrSettings.ArrMean
            arrVar = arrSettings.ArrStd
        else:
            arrMean = 5
            arrVar = 1

        patientdate = db[date+"patient"]
        patients = patientdate.find()

        for patient in patients:
            temptime = patient["Time"].split(":")
            hrs = temptime[0]
            mins = temptime[1]
            appttime = 60*int(hrs)+int(mins)
            print("appt time: " + str(appttime))
            print("arrmean, var:" +str(arrMean) + str(arrVar))
            arrTime = (appttime-480) + int(float(arrMean))+ NP.random.randint(-1 * float(arrVar)/2,float(arrVar)/2);
            print("arrTime: " + str(arrTime))
            temp = Patient(patient["Name"], patient["Visit"])
            temp.assignTime(arrTime)
            self.patients.append(temp)


    # def schedule(self,fileName):
    #     for line in arrivalFile:
    #         data = line.split()
    #         if(data[0] == 'Arrivals'):
    #             arrMean = data[5]
    #             arrVar = data[6]

        # for element in self.patients:
            # arrTime = int(round(counter*15 + NP.random.normal(arrMean,arrVar)))
        #     self.patients[counter-1].assignTime(arrTime) ##schedule a patient every 15 minutes
        #     counter += 1
        # arrivalFile.close()

    def loadSchedule(self):
        print("loading schedule \n")

# Test Harness
#def main():
#    file = "TestPatients.txt"
#    newSchedule = PatientSchedule(file)
#    newSchedule.schedule("NewClinicFile.txt")
#    for person in newSchedule.patients:
#        print(person.name, person.arrivalTime, person.stations)


#if __name__ == "__main__": main()


## ability to add constraints to optimization schedules
##
