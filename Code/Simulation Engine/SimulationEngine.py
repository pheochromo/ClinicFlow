# -*- coding: utf-8 -*-
"""
@author: karl_
"""

import simpy
from Clinic import Clinic
from HealthCareSchedule import HealthCareSchedule
from HealthCareWorker import HealthCareWorker
from PatientSchedule import PatientSchedule


def Simulation(env,clinic,workerSchedule,patientSchedule,outfile):
    resources = [simpy.Resource(env,1) for _ in range(len(clinic.stations))]
    for i in range(len(workerSchedule.healthcare)):
        env.process(workerRun(env,workerSchedule.healthcare[i],clinic,resources))
    for i in range(len(patientSchedule.patients)):
        env.process(patientRun(env,patientSchedule.patients[i],clinic,resources))
    env.run(until=100)
    
    #Clinic Statistics From Simulation Run
    # Average Time in Clinic
    averageClinicTime = 0
    for person in patientSchedule.patients:
        averageClinicTime = averageClinicTime + person.completionTime
    averageClinicTime = averageClinicTime / (len(patientSchedule.patients))
    
    #write statistics to file
    f = open(outfile, 'a')
    f.write('Average Time in Clinic: %d \n' % (averageClinicTime))
    f.close()
    
    
def workerRun(env,worker,clinic,resources):
    yield env.timeout(worker.scheduledTime)
    print('%s arriving at %d' % (worker.name, env.now))
    for i in range(0,len(resources)):
        if worker.station == clinic.stations[i].name:
            with resources[i].request() as req:
                yield req
                print('%s starting work at %s %s' % (worker.name,clinic.stations[i].name, int(env.now)))
                clinic.stations[i].activate()
                yield env.timeout(0)          
                #need to have breaks and leaving / how to end it?

def patientRun(env, patient,clinic,resources):
    yield env.timeout(patient.arrivalTime)
    print('%s arriving at %d' % (patient.name, env.now))
    for i in range(0,len(resources)):
        if (clinic.stations[i].name in patient.stations) and (clinic.stations[i].active == True):
            with resources[i].request() as req:
                yield req
                print('%s starting service at %d %s' % (patient.name,i, int(env.now)))
                yield env.timeout(clinic.stations[i].getRandomness())
                print('%s leaving service at %d %s' % (patient.name,i, int(env.now)))
                patient.addLocation(clinic.stations[i].name) # Patient completed a location
    if(patient.stations == patient.location): # check if patient is finished
        patient.completed(int(env.now) - patient.arrivalTime) #record when the patient finished
    
    

def SimulationEngine(clinicFile,employeeFile,patientFile,employeeScheduleFile,patientScheduleFile,outFile):
    env = simpy.Environment()
    #load clinic information
    fileName = clinicFile
    thisClinic = Clinic(fileName)
    
    #load worker information
    fileName = employeeFile
    workerSchedule = HealthCareSchedule(fileName)
    if(employeeScheduleFile == "generated"):
        workerSchedule.schedule()
    else:
        workerSchedule.loadSchedule(employeeScheduleFile)
    
    #load patient information
    fileName = patientFile
    patientSchedule = PatientSchedule(fileName)
    if(patientScheduleFile == "generated"):  
        patientSchedule.schedule()
    else:
        patientSchedule.loadSchedule(patientScheduleFile)
    
    Simulation(env,thisClinic,workerSchedule,patientSchedule,outFile)

