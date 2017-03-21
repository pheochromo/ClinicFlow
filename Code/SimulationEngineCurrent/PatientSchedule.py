# -*- coding: utf-8 -*-
"""

@author: karl_
"""
from Patient import Patient
import numpy as NP   

class PatientSchedule:
    def __init__(self,fileName):
        patientFile = open(fileName,mode ='r')
        self.patients = []
        self.arrivalVariance = "uniform"
        self.arrivalAvg = 0
        self.arrivalVar = 0

        for line in patientFile:
            data = line.split()
            temp = Patient(data[0], data[1].split(','))
            self.patients.append(temp)
        
        patientFile.close()

    def schedule(self,fileName):
        counter = 1
        arrivalFile = open(fileName,mode ='r')
        arrMean = 5
        arrVar = 1
        for line in arrivalFile:
            data = line.split()
            if(data[0] == 'Arrivals'):
                arrMean = data[5]
                arrVar = data[6]
        
        for element in self.patients:
            arrTime = int(round(counter*15 + NP.random.normal(arrMean,arrVar)))
            self.patients[counter-1].assignTime(arrTime) ##schedule a patient every 15 minutes
            counter += 1
        arrivalFile.close()
    
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