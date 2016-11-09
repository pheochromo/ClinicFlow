# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 12:44:44 2016

@author: Karl
"""
from Person import Person
import numpy as NP   # not working properly

class HealthCareScheduler:
    def __init__(self,fileName):
        healthFile = open(fileName,mode ='r')
        self.healthcare = []
        for line in healthFile:
            data = line.split()
            #temp = Person(data[0], data[1].split(','))
            self.healthcare.append(temp)
        
        healthFile.close()

    def schedule(self):
        counter = 0
        for element in self.healthcare:
            #self.healthcare
            counter += 1

