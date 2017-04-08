# -*- coding: utf-8 -*-
"""
ClinicStation is a class that represents a station (module) in the clinic.

"""
import random
import numpy as np

class ClinicStation:
    def __init__(self,newName,prereqs,newMax,newMin,varType,avg,dev):
        self.name = newName
        self.prerequesites = prereqs
        self.minimum = int(newMin)
        self.maximum = int(newMax)
        self.count = 0
        self.varianceType = varType
        self.mean = float(avg)
        self.var = float(dev)
        self.active = False
    
    # activate (Start) the clinic module
    def activate(self):
        if(self.count < self.maximum):
            self.count = self.count + 1
            if(self.count >= self.minimum):
                self.active = True
            else:
                self.active= False
        
        #else:
            #throw error message, as station is already full
    #deactivate / turn off the station
    def deactivate(self):
        if(self.count > 0):
            self.count = self.count - 1
            if(self.count < self.minimum):
                self.active = False
    
    # get a random wait time from the station
    def getRandomness(self):
        if(self.varianceType == "uniform"):
            return (self.mean +random.randint(0,self.var))
        if(self.varianceType == "normal"):
            return abs(int(round(np.random.normal(self.mean,self.var))))
        if(self.varianceType == "exponential"):
            return int(round( np.random.exponential(self.mean)))
        else:
            return 0
     
    #how to represent the station as a repr
    def __repr__(self):
        return "<Station name:%s size: %d and is %s>" % (self.name, self.maximum,self.active)
    # how to represent the station as a string
    def __str__(self):
        return "Station %s, has size %d and is %s"  % (self.name, self.maximum,self.active)
    
    
            
    
            
        
        
        
        