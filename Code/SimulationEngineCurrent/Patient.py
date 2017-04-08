# -*- coding: utf-8 -*-
"""
Patient is a class that represents a patient in the simulation. 
It manages their arrival times, and it keeps track of the patients statistics

"""
class Patient:
    #constructor for the patient class
    def __init__(self,newName,mods):
        self.name = newName
        self.scheduledTime = 0 # when they are scheduled to arrive
        self.arrivalTime = 0 # when they arrived
        self.stations= mods
        self.locations = mods ## have arrays of where they have been, and where they need to go
        self.completionTime = -1 # when they left
        self.timeInService = 0
    
    #schedule the patients arrival time
    def schedule(self, time):
        self.scheduledTime = time
    
    #schedule the patients assigned arrival time
    def assignTime(self,time):
        self.arrivalTime = time 
        
    #called when a patient completes a station
    def addLocation(self,newLoc):
        self.locations.remove(newLoc)
    
    #called when the patient has completed the clinic
    def completed(self, time):
        self.completionTime = time
        
    #records the time spent in service
    def addServiceTime(self,time):
        self.timeInService = self.timeInService + time
        
    #defines the repr representation of the patient
    def __repr__(self):
        return "<Person name:%s arrivalTime:%d>" % (self.name, self.scheduledTime)
    #defines the string representation of the patient
    def __str__(self):
        return "Person %s, scheduled to arrive at %d" % (self.name, self.scheduledTime)
        
            
    
            
            
            
