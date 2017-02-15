# -*- coding: utf-8 -*-
"""
@author: karl_
"""

import simpy
from Clinic import Clinic
from HealthCareSchedule import HealthCareSchedule
from HealthCareWorker import HealthCareWorker
from PatientSchedule import PatientSchedule

startTime = (8*60)
endTime = (17*60)

def Simulation(env,clinic,workerSchedule,patientSchedule,outfile):
    resources = [simpy.PriorityResource(env,1) for _ in range(len(clinic.stations))]
    for i in range(len(workerSchedule.healthcare)):
        env.process(workerRun(env,workerSchedule.healthcare[i],clinic,resources))
    for i in range(len(patientSchedule.patients)):
        env.process(patientRun(env,patientSchedule.patients[i],clinic,resources))
    env.run(until=(endTime-startTime)+1)
    
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
    
    
    #NEED TO Give patient requests priority over worker breaks, so that if they occur at the same time the worker stays
    
def workerRun(env,worker,clinic,resources):
    yield env.timeout(worker.scheduledTime)
    print('%s arriving at %s' % (worker.name, prettyTime(startTime,env.now)))
    while(True):
        for i in range(0,len(resources)):
            if worker.station == clinic.stations[i].name:
                with resources[i].request(priority=0) as req:
                    yield req
                    print('%s starting work at %s %s' % (worker.name,clinic.stations[i].name, prettyTime(startTime,int(env.now))))
                    clinic.stations[i].activate()
                    resources[i].release(req)
                    yield env.timeout(worker.breakTime(env.now))
                    with resources[i].request(priority=0) as req2:
                        yield req2
                        clinic.stations[i].deactivate()
                        resources[i].release(req2)
                        print('%s leaving work at %s %s' % (worker.name,clinic.stations[i].name, prettyTime(startTime,int(env.now))))
                        yield env.timeout(15) # each break period is 15 minutes
                
#Use the following to rewrite this and fix it
#http://simpy.readthedocs.io/en/latest/simpy_intro/process_interaction.html
#http://simpy.readthedocs.io/en/latest/topical_guides/process_interaction.html

def patientRun(env, patient,clinic,resources):
    yield env.timeout(patient.arrivalTime)
    print('%s arriving at %s' % (patient.name, prettyTime(startTime,env.now)))
    for i in range(0,len(resources)):
        if (clinic.stations[i].name in patient.stations) and (clinic.stations[i].active == True):
            with resources[i].request(priority=1) as req:
                yield req
                print('%s starting service at %s %s' % (patient.name,clinic.stations[i].name, prettyTime(startTime,int(env.now))))
                yield env.timeout(clinic.stations[i].getRandomness())
                resources[i].release(req)
                print('%s leaving service at %s %s' % (patient.name,clinic.stations[i].name, prettyTime(startTime,int(env.now))))
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
        workerSchedule.schedule(startTime,endTime)
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

def prettyTime(startTime,timestep):
    h, m = divmod(timestep, 60)
    sh,sm = divmod(startTime, 60)
    return "%d:%02d" % (h + sh, m + sm)