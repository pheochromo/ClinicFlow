# -*- coding: utf-8 -*-
"""
@author: karl_
"""
from SimulationEngine import SimulationEngine


def main():
    for i in range(0,2):
        print(" \nNow running Simulation %d \n"%(i+1))
        SimulationEngine("ClinicFile1.txt","Worker1.txt","TestPatients.txt","generated","generated","outFile1.txt")
   
if __name__ == '__main__': main()
