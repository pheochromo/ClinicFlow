# -*- coding: utf-8 -*-
"""
@author: karl_
"""

import simpy
from Clinic import Clinic
from HealthCareSchedule import HealthCareSchedule
from HealthCareWorker import HealthCareWorker
from PatientSchedule import PatientSchedule
from random import randint

startTime = (6*60)          #start time of simulation
workerStartTime = (8*60)    #start time when workers arrive
endTime = (20*60)           #end time of simulation

patientCount = 0            #check to see how many patients there have been
patientCompleted = 0        #check to see how many patients have completed the clinic

"""
Simulation is the function that runs the simulation

It takes a simulation environment 'env', a clinic array 'clinic',a 'workerSchedule', a 'patientSchedule',
and a fileName that will store the output data.

Simulation starts the patient and worker threads in the simulation environment. It also calculates the
simulation statistics and prints them to the outfile. 

"""
def Simulation(env,clinic,workerSchedule,patientSchedule,outfile):
    global patientCount; global patientCompleted;
    resources = [simpy.PriorityResource(env,1) for _ in range(len(clinic.stations))] #generate the clinic modules as simulation resources
    patientCount = len(patientSchedule.patients)
    patientCompleted = 0
    #start the patient threads
    for i in range(len(workerSchedule.healthcare)):
        env.process(workerRun(env,workerSchedule.healthcare[i],clinic,resources))
    #start the worker threads
    for i in range(len(patientSchedule.patients)):
        env.process(patientRun(env,patientSchedule.patients[i],clinic,resources))
    env.run(until=(endTime-startTime)+1)
    
    #Clinic Statistics From Simulation Run
    # Average Time in Clinic
    averageClinicTime = 0
    for person in patientSchedule.patients:
        averageClinicTime = averageClinicTime + person.completionTime
    averageClinicTime = averageClinicTime / (len(patientSchedule.patients))
    
    #Average Time spent waiting in clinic 
    averageDownTime = 0
    for person in patientSchedule.patients:
        averageDownTime = averageDownTime + (person.completionTime - person.timeInService)
    averageDownTime = averageDownTime / (len(patientSchedule.patients))
    #write statistics to file
    f = open(outfile, 'a')
    f.write('Average Time in Clinic: %d  Average Idle Time for a patient: %d \n' % (averageClinicTime,averageDownTime))
    f.close()
        
"""
workerRun is the function that handles the actions of the worker threads in the simulation

It takes as input: a simulation environment, a worker thread, an clinic object and an array of 
simulation resources that represent the in the clinic

"""
def workerRun(env,worker,clinic,resources):
    global patientCount; global patientCompleted;
    yield env.timeout(worker.scheduledTime + (workerStartTime - startTime)) ##start the worker at their start time
    print('%s arriving at %s' % (worker.name, prettyTime(startTime,env.now))) 
    while(patientCompleted < patientCount): #while there are still patients to see
        found = False
        for i in range(0,len(resources)):
            if (clinic.stations[i].name in worker.station):
                with resources[i].request(priority=0) as req:
                    yield req
                    if (clinic.stations[i].maximum > clinic.stations[i].count): #if there is room for the worker at the station
                        found = True
                        print('%s starting work at %s %s' % (worker.name,clinic.stations[i].name, prettyTime(startTime,int(env.now))))
                        clinic.stations[i].activate()
                        resources[i].release(req)
                        yield env.timeout(worker.breakTime(env.now)) ## wait for the next break
                        with resources[i].request(priority=0) as req2:
                            yield req2 
                            clinic.stations[i].deactivate()
                            resources[i].release(req2)
                            if(patientCompleted == patientCount): ## if the station has seen every patient
                                break
                            print('%s leaving work at %s %s' % (worker.name,clinic.stations[i].name, prettyTime(startTime,int(env.now))))
                            yield env.timeout(15) #break is 10 minutes
        if(found == False): ## if the provider can not find an available station, they wait 5 units and try again
            yield env.timeout(5) # each recheck station period is 5 minutes
    print('%s going home at %s' % (worker.name, prettyTime(startTime,env.now)))       

    
"""
patientRun is a function that handles the actions of the patient in the simulation.

It takes as input: a simulation environment, a patient thread, an clinic object and an array of 
simulation resources that represent the in the clinic

"""
def patientRun(env, patient,clinic,resources):
    global patientCount; global patientCompleted;
    yield env.timeout(patient.arrivalTime + (workerStartTime - startTime)) ## start the patient at their scheudled start time
    print('%s arriving at %s' % (patient.name, prettyTime(startTime,env.now)))
    while(len(patient.locations) > 0 ): ## while the patient still has stations to go to
        for i in range(0,len(resources)):
            if (clinic.stations[i].name in patient.locations) :
                with resources[i].request(priority=1) as req: ## request the station
                    if(clinic.stations[i].active == True) and (len(set(patient.locations) - set(clinic.stations[i].prerequesites)) == (len(patient.locations) -1)):
                     #if(len(set(patient.locations) - set(clinic.stations[i].prerequesites)) == (len(patient.locations) -1)):
                        yield req
                        if(clinic.stations[i].active == False): ##if there is no one at the station
                            break
                        print('%s starting service at %s %s' % (patient.name,clinic.stations[i].name, prettyTime(startTime,int(env.now))))
                        serviceTime = clinic.stations[i].getRandomness()
                        patient.addServiceTime(serviceTime)
                        yield env.timeout(serviceTime)
                        waitTime = randint(1,5)
                        resources[i].release(req)
                        print('%s leaving service at %s %s' % (patient.name,clinic.stations[i].name, prettyTime(startTime,int(env.now))))
                        patient.addLocation(clinic.stations[i].name) # Patient completed a location
                        if(patient.locations == []): # check if patient is finished
                            patient.completed(int(env.now) - patient.arrivalTime) #record when the patient finished
                            patientCompleted = patientCompleted + 1
                        
                        yield env.timeout(waitTime) #time to allow provider to prepare for next person, return to clinic
        yield env.timeout(randint(1,3))
        
    
"""
SimulationEngine is the function that handles the input from outside of the module, and
passes that information to Simulation, to run the simulation.

It takes as input 4 file names, the clinic information file, the employee file, the patient file and the outfile

"""
def SimulationEngine(clinicFile,employeeFile,patientFile,outFile):
    env = simpy.Environment()
    #load clinic information
    fileName = clinicFile
    thisClinic = Clinic(fileName)
    
    #load worker information
    fileName = employeeFile
    workerSchedule = HealthCareSchedule(fileName)
    workerSchedule.schedule(startTime,endTime)
    
    #load patient information
    fileName = patientFile
    patientSchedule = PatientSchedule(fileName)
    patientSchedule.schedule(clinicFile)
    
    Simulation(env,thisClinic,workerSchedule,patientSchedule,outFile)

def prettyTime(startTime,timestep):
    h, m = divmod(timestep, 60)
    sh,sm = divmod(startTime, 60)
    return "%d:%02d" % (h + sh, m + sm)