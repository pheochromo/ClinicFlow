# -*- coding: utf-8 -*-
"""

@author: karl_
"""
import os
from .HealthCareWorker import *
import numpy as NP   # not working properly

class HealthCareSchedule:
    def __init__(self,fileName):

        file_name = os.path.join(os.path.dirname(__file__), fileName)
        healthFile = open(file_name,mode ='r')
        self.healthcare = []
        for line in healthFile:
            data = line.split()
            temp = HealthCareWorker(data[0], data[1].split(','), data[2])
            self.healthcare.append(temp)

        healthFile.close()

    def schedule(self,startTime,endTime):
        counter = 0
        for element in self.healthcare:
            #self.healthcare
            element.breaks.append(str(endTime - startTime))
            counter += 1

    def loadSchedule(self):
        print("loading schedule \n")

# Test Harness
#def main():
#    file = "Worker1.txt"
#    newSchedule = HealthCareSchedule(file)
#   newSchedule.schedule()
#    for worker in newSchedule.healthcare:
#        print(worker.name,worker.type, worker.scheduledTime, worker.breaks, worker.station)

#if __name__ == "__main__": main()
