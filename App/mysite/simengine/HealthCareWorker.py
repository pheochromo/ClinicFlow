# -*- coding: utf-8 -*-
"""
@author: karl_
"""
class HealthCareWorker:
    def __init__(self,newName,breakTimes,workStation):
        self.name = newName
        self.type = "Nurse" #distinguish between types of workers
        self.breaks = breakTimes
        self.scheduledTime =  int(self.breaks[0])  # when they are scheduled to start
        self.station = workStation.split(",")
        self.breakCount = 0
    def schedule(self, time):
        self.scheduledTime = time
        
    def changeStation(self,newLoc):
        self.station = newLoc
        
    def breakTime(self,currentTime):
        self.breakCount = self.breakCount + 1
        if(self.breakCount < len(self.breaks)):
            return (int(self.breaks[self.breakCount]))
        else:
            return self.breaks[-1]
            
    def __repr__(self):
        return "<Worker name:%s station:%d>" % (self.name, self.station)

    def __str__(self):
        return "Worker %s, works at %d" % (self.name, self.station)
