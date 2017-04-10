# -*- coding: utf-8 -*-
"""
@author: karl_
"""

import simpy
from .Clinic import *
from .HealthCareSchedule import *
from .HealthCareWorker import *
from .PatientSchedule import *
from random import randint

import pymongo
from pymongo import MongoClient #import MongoDB
client = MongoClient()
db = client.Clinic_database # create schema
settings = db.application_setting #data of setting

result = db.result # temporarily store the data of simulation
schedule_list = db.schedulelist # a list of schedule, contain date and settings

startTime = (8*60)
endTime = (17*60)

patientCount = 0
patientCompleted = 0


def Simulation(env,clinic,workerSchedule,patientSchedule,outfile):
    global patientCount; global patientCompleted;
    resources = [simpy.PriorityResource(env,1) for _ in range(len(clinic.stations))]
    patientCount = len(patientSchedule.patients)
    patientCompleted = 0
    for i in range(len(workerSchedule.healthcare)):
        env.process(workerRun(env,workerSchedule.healthcare[i],clinic,resources))
    for i in range(len(patientSchedule.patients)):
        env.process(patientRun(env,patientSchedule.patients[i],clinic,resources, patientSchedule))
    env.run(until=(endTime-startTime)+1)

    #Clinic Statistics From Simulation Run
    # Average Time in Clinic
    averageClinicTime = 0
    for person in patientSchedule.patients:
        averageClinicTime = averageClinicTime + person.completionTime
    averageClinicTime = averageClinicTime / (len(patientSchedule.patients))

    averageDownTime = 0
    for person in patientSchedule.patients:
        averageDownTime = averageDownTime + (person.completionTime - person.timeInService)
    averageDownTime = averageDownTime / (len(patientSchedule.patients))
    #write statistics to file
    f = open(outfile, 'a')
    f.write('Average Time in Clinic: %d  Average Idle Time for a patient: %d \n' % (averageClinicTime,averageDownTime))
    clinicStats = {"Name":"clinicStats", "averageClinicTime":averageClinicTime, "averageDownTime":averageDownTime}
    db[patientSchedule.date+"result"].insert_one(clinicStats)
    f.close()


    #NEED TO Give patient requests priority over worker breaks, so that if they occur at the same time the worker stays

def workerRun(env,worker,clinic,resources):
    global patientCount; global patientCompleted;
    yield env.timeout(worker.scheduledTime)
    print('%s arriving at %s' % (worker.name, prettyTime(startTime,env.now)))
    while(patientCompleted < patientCount):
        found = False
        for i in range(0,len(resources)):
            if (clinic.stations[i].name in worker.station):
                with resources[i].request(priority=0) as req:
                    yield req
                    if (clinic.stations[i].maximum > clinic.stations[i].count):
                        found = True
                        print('%s starting work at %s %s' % (worker.name,clinic.stations[i].name, prettyTime(startTime,int(env.now))))
                        # add to database
                        clinic.stations[i].activate()
                        resources[i].release(req)
                        yield env.timeout(worker.breakTime(env.now))
                        with resources[i].request(priority=0) as req2:
                            yield req2
                            clinic.stations[i].deactivate()
                            resources[i].release(req2)
                            if(patientCompleted == patientCount):
                                break
                            print('%s leaving work at %s %s' % (worker.name,clinic.stations[i].name, prettyTime(startTime,int(env.now))))
                            yield env.timeout(15) #break is 10 minutes
        if(found == False):
            yield env.timeout(5) # each recheck station period is 5 minutes
    print('%s going home at %s' % (worker.name, prettyTime(startTime,env.now)))
#Use the following to rewrite this and fix it
#http://simpy.readthedocs.io/en/latest/simpy_intro/process_interaction.html
#http://simpy.readthedocs.io/en/latest/topical_guides/process_interaction.html

def patientRun(env, patient,clinic,resources, patientSchedule):
    global patientCount; global patientCompleted;
    yield env.timeout(patient.arrivalTime)
    print('%s arriving at %s' % (patient.name, prettyTime(startTime,env.now)))
    while(len(patient.locations) > 0 ):
        for i in range(0,len(resources)):
            if (clinic.stations[i].name in patient.locations) :
                with resources[i].request(priority=1) as req:
                    if(clinic.stations[i].active == True) and (len(set(patient.locations) - set(clinic.stations[i].prerequesites)) == (len(patient.locations) -1)):
                        yield req
                        temptime = prettyTime(startTime,int(env.now))
                        print('%s starting service at %s %s' % (patient.name,clinic.stations[i].name, temptime))
                        timedat = {"Name":"stationDuration", "stationName":clinic.stations[i].name, "patientName":patient.name, "startTime":temptime}
                        serviceTime = clinic.stations[i].getRandomness()
                        patient.addServiceTime(serviceTime)
                        yield env.timeout(serviceTime)
                        waitTime = randint(1,5)

                        #patient.addServiceTime(serviceTime)
                        #yield env.timeout(waitTime) #time to allow provider to prepare for next person, return to clinic
                        resources[i].release(req)
                        temptime = prettyTime(startTime,int(env.now))
                        print('%s leaving service at %s %s' % (patient.name,clinic.stations[i].name, prettyTime(startTime,int(env.now))))
                        timedat.update({"endTime":temptime})
                        db[patientSchedule.date+"result"].insert_one(timedat)
                        patient.addLocation(clinic.stations[i].name) # Patient completed a location
                        if(patient.locations == []): # check if patient is finished
                            patient.completed(int(env.now) - patient.arrivalTime) #record when the patient finished
                            patientCompleted = patientCompleted + 1
                        yield env.timeout(waitTime) #time to allow provider to prepare for next person, return to clinic
        yield env.timeout(randint(1,3))



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
    # fileName = patientFile
    patientSchedule = PatientSchedule(patientFile)
    # if(patientScheduleFile == "generated"):
    # patientSchedule.schedule(clinicFile)

    Simulation(env,thisClinic,workerSchedule,patientSchedule,outFile)

def prettyTime(startTime,timestep):
    h, m = divmod(timestep, 60)
    sh,sm = divmod(startTime, 60)
    return "%d:%02d" % (h + sh, m + sm)
