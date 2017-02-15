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

    def schedule(self):
        counter = 0
        for element in self.patients:
            self.patients[counter].assignTime(counter*10 + NP.random.poisson(5,1)) ##schedule a patient every 15 minutes
            counter += 1
    
    def loadSchedule(self):
        print("loading schedule \n")
        
# Test Harness
#def main():
#    file = "TestPatients.txt"
#    newSchedule = PatientSchedule(file)
#   newSchedule.schedule()
#    for person in newSchedule.patients:
#        print(person.name, person.arrivalTime[0], person.stations)

    
#if __name__ == "__main__": main()


## ability to add constraints to optimization schedules
##