#from Person import Person
#from Module import Module
from PatientScheduler import PatientScheduler
from Clinic import Clinic
import numpy as np
#import unittest

def main():
    ## module schedule 
    #input_file = input("Enter the name of the Clinic File: ")
    input_file = "Clinic1.txt"
    c1 = Clinic(input_file)
    moduleList = c1.stations
    
    ## create patient schedule
    #input_file = input("Enter the name of the Patient File: ")
    input_file = "TestPatients.txt"
    pSch = PatientScheduler(input_file)
    pSch.schedule()
    patientList = pSch.patients
    ## need a nursing scheduler as nurses could be different than modules.

    ## intialize simulation parameters
    counter = 0 #what is the time step
    completed = 0 # how many patients are done?
    
    clinicArray = [] # array to store the current patients in the clinic
    clinicTimer = [] # array to store the amount of time each patient spent in the clinic

    ## simulation loop
    ## Discrete event simulation: looped based on next event rather than time steps
    while completed  < len(patientList):
        print('Time Step: {0}'.format(counter))
        # if person arrives, add them to waiting room
        for pat in patientList:
            if pat.arrivalTime == counter:
                pat.location.append('0')
                clinicArray.append([pat, moduleList[0].location])
        # for each module check if working on a patient, if so continue
        for mod in moduleList:
            for pat in clinicArray:
                if mod.location == pat[1]:
                    if pat[0].serviceTime > 0 and pat[0].location.__contains__(mod.location) == False:
                        mod.serve(pat[0])
                        break
                        # do nothing, and wait for the patient to leave
            # modules check for a new patient
            for pat in clinicArray:
                if pat[0].location.__contains__(mod.location) == False and pat[0].modules.__contains__(mod.location) == True and pat[0].serviceTime  < 0:
                    pat[0].serviceTime = mod.completionTime
                    clinicArray.append([pat[0], mod.location])
                    clinicArray.remove(pat)
                    print('Location {0} now serving Patient {1}'.format(mod.location,pat[0].name))
                    break
        
        # check to see if we can finish a patient
        for pat in clinicArray:
            if set(pat[0].location) == set(pat[0].modules):
                print('Patient {0} has left the building'.format(pat[0].name))
                clinicTimer.append(counter - pat[0].arrivalTime)
                clinicArray.remove(pat)
                completed+=1
        counter +=1

# program for post simulation data analysis
    print("\nBasic Analysis Statistics:")
    print('Clinic took {0} steps to complete'.format(counter)) 
    print("Amount of time spent in clinic:",clinicTimer)
# use unittest for unit testing like JUnit
if __name__ == "__main__": main()
