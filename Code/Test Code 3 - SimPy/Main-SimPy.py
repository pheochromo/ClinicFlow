# -*- coding: utf-8 -*-
"""

@author: Karl
"""

import simpy
import random
import numpy

env = simpy.Environment()

resources = [simpy.Resource(env, 1) for _ in range(6)]
resourceTimes = [1,2,3,4,5,6]
resourceReqs = numpy.matrix([[1,2],[1],[1],[1]])

def patient(env, name, resourceRequirements, arrival_time):

    yield env.timeout(arrival_time)

    print('%s arriving at %d' % (name, env.now))
    for i in range(0,len(resources)):
        if i in resourceRequirements:
            with resources[i].request() as req:
                yield req
                print('%s starting service at %d %s' % (name,i, env.now))
                yield env.timeout(resourceTimes[i]+random.randint(0,3)) # apply randomness to service times
                print('%s leaving service at %d %s' % (name,i, env.now))
    

def main():
    fileName = "TestPatients2.txt"
    patientFile = open(fileName,mode ='r')
    j = 0
    for line in patientFile:
        data = line.split()
        temp = [data[0], data[1].split(',')]
        resourceReqs[0,j] = list(map(int, temp[1]))
        j += 1
    patientFile.close()
       
        
    print(resourceReqs[0,2])
    for i in range(4):
        env.process(patient(env, 'Patient %d' % i, resourceReqs[0,i], i*random.randint(1,10)))
    
    env.run(until=100)

if __name__ == '__main__': main()