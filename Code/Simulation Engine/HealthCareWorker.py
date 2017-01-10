# -*- coding: utf-8 -*-
"""
@author: karl_
"""
class HealthCareWorker:
    def __init__(self,newName,breakTimes,workStation):
        self.name = newName
        self.type = "Nurse" #distinguish between types of workers
        self.scheduledTime = 0 # when they are scheduled to start
        self.breaks = breakTimes
        self.station = workStation
    
    def schedule(self, time):
        self.scheduledTime = time
        
    def changeStation(self,newLoc):
        self.station = newLoc
        
    def __repr__(self):
        return "<Worker name:%s station:%d>" % (self.name, self.station)

    def __str__(self):
        return "Worker %s, works at %d" % (self.name, self.station)
