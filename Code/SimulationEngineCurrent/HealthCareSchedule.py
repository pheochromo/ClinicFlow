# -*- coding: utf-8 -*-
"""
HealthCareSchedule reads in the health care worker file and creates a health care schedule object
that contains the workers information for the simulation
"""
from HealthCareWorker import HealthCareWorker

class HealthCareSchedule:
    def __init__(self,fileName):
        healthFile = open(fileName,mode ='r')
        self.healthcare = []
        for line in healthFile:
            data = line.split()
            temp = HealthCareWorker(data[0], data[1].split(','), data[2])
            self.healthcare.append(temp)
        
        healthFile.close()

    #scheudles the workers based on their start time
    def schedule(self,startTime,endTime):
        counter = 0
        for element in self.healthcare:
            #self.healthcare
            element.breaks.append(str(endTime - startTime))
            counter += 1
            
# Test Harness
#def main():
#    file = "Worker1.txt"
#    newSchedule = HealthCareSchedule(file)
#    newSchedule.schedule(0,100)
#    for worker in newSchedule.healthcare:
#        print(worker.name,worker.type, worker.scheduledTime, worker.breaks, worker.station)
#    
#if __name__ == "__main__": main()