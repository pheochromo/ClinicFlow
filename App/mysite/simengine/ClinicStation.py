# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 09:24:24 2017

@author: karl_
"""
import random
import numpy as np

class ClinicStation:
    def __init__(self,newName,prereqs,newMax,newMin,varType,avg,dev):
        self.name = newName
        self.prerequesites = prereqs
        self.maximum = int(newMax)
        self.minimum = int(newMin)
        self.count = 0
        self.varianceType = varType
        self.mean = float(avg)
        self.var = float(dev)
        self.active = False

    def activate(self):
        if(self.count < self.maximum):
            self.count = self.count + 1
            if(self.count >= self.minimum):
                self.active = True
            else:
                self.active= False

        #else:
            #throw error message, as station is already full
    def deactivate(self):
        if(self.count > 0):
            self.count = self.count - 1
            if(self.count < self.minimum):
                self.active = False

    def getRandomness(self):
        if(self.varianceType == "uniform"):
            return (self.mean +random.randint(0,self.var))
        if(self.varianceType == "normal"):
            return int(round(random.normal(self.mean,self.var)))
        if(self.varianceType == "exponential"):
            return int(round( np.random.exponential(self.mean)))
        else:
            return 0

    def __repr__(self):
        return "<Station name:%s size: %d and is %s>" % (self.name, self.maximum,self.active)

    def __str__(self):
        return "Station %s, has size %d and is %s"  % (self.name, self.maximum,self.active)









