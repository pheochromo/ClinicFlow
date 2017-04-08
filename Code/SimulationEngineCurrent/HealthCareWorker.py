# -*- coding: utf-8 -*-
"""
HealthCareWorker is a class that represents a worker in the simulation. 
It manages all of the workers data, and schedules all of their breaks.


"""
class HealthCareWorker:
    # the constructor for HealthCareWorker
    def __init__(self,newName,breakTimes,workStation):
        self.name = newName
        self.type = "Nurse" #distinguish between types of workers
        self.breaks = breakTimes
        self.scheduledTime =  int(self.breaks[0])  # when they are scheduled to start
        self.station = workStation.split(",")
        self.breakCount = 0
    # schedules the worker's arrival time
    def schedule(self, time):
        self.scheduledTime = time
        
    #represents a change of their current station
    def changeStation(self,newLoc):
        self.station = newLoc
        
    #gets the next break time for the worker
    def breakTime(self,currentTime):
        self.breakCount = self.breakCount + 1
        if(self.breakCount < len(self.breaks)):
            return (int(self.breaks[self.breakCount]))
        else:
            return self.breaks[-1]
        
    #defines the representation of the HealthCareWorker    
    def __repr__(self):
        return "<Worker name:%s station:%d>" % (self.name, self.station)
    #defines the string representation of the HealthCareWorker
    def __str__(self):
        return "Worker %s, works at %d" % (self.name, self.station)
