# -*- coding: utf-8 -*-
"""
PatientSchedule reads in the patient information from a file and creates a patient
schedule object that contains all of the patients for the simulation. 
"""
from Patient import Patient
import numpy as NP   

class PatientSchedule:
    #constructor for the patient schedule
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
    
    #schedules the patients, they should arrive every 15 minutes
    def schedule(self,fileName):
        counter = 0
        arrivalFile = open(fileName,mode ='r')
        arrMean = 5 #default value 
        arrVar = 1 #default value
        for line in arrivalFile:
            data = line.split()
            if(data[0] == 'Arrivals'):
                arrMean = data[5]
                arrVar = data[6]
        
        for element in self.patients:
            arrTime = (counter* 15) + int(float(arrMean))+ NP.random.randint(-1 * float(arrVar)/2,float(arrVar)/2);
            self.patients[counter].assignTime(arrTime) ##schedule a patient every 15 minutes
            counter += 1
        arrivalFile.close()
        
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