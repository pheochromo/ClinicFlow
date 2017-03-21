# -*- coding: utf-8 -*-
"""
@author: karl_
"""
from SimulationEngine import SimulationEngine
from ClinicCreate import clinicCreate

def main():
    clinicFile = clinicCreate() ## create the clinic file
    for i in range(0,2):
        print(" \nNow running Simulation %d \n"%(i+1))
        SimulationEngine(clinicFile,"Worker1.txt","TestPatients.txt","generated","generated","outFile1.txt")
   
if __name__ == '__main__': main()
