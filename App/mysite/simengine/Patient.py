# -*- coding: utf-8 -*-
"""
@author: karl_
"""
class Patient:
    def __init__(self,newName,mods):
        self.name = newName
        self.scheduledTime = 0 # when they are scheduled to arrive
        self.arrivalTime = 0 # when they arrived
        self.stations= mods
        self.location = [] ## have arrays of where they have been, and where they need to go
        self.completionTime = -1 # when they left
    
    def schedule(self, time):
        self.scheduledTime = time
        
    def assignTime(self,time):
        self.arrivalTime = time 

    def addLocation(self,newLoc):
        self.location.append(newLoc)
        
    def completed(self, time):
        self.completionTime = time

    def __repr__(self):
        return "<Person name:%s arrivalTime:%d>" % (self.name, self.scheduledTime)

    def __str__(self):
        return "Person %s, scheduled to arrive at %d" % (self.name, self.scheduledTime)
        
            
    
            
            
            
