from Person import Person
from Module import Module
#import unittest

def main():
    ## create patient schedule
    patientList = []
    personA = Person('A',0)
    patientList.append(personA)
    personB = Person('B',4)
    patientList.append(personB)
    personC = Person('C',10)
    patientList.append(personC)

    ## module schedule (from a file)
    moduleList = []
    module1 = Module(0,2)
    moduleList.append(module1)
    module2 = Module(1,3)
    moduleList.append(module2)
    
    moduleCount = len(moduleList)

    ## need a nursing scheduler as nurses could be different than modules.

    ## intialize simulation parameters
    counter = 0
    completed = 0

    ## simulation loop
    
    while completed < len(patientList):
        print('Time Step: {0}'.format(counter))
        for mod in moduleList:
            for pat in patientList:
                if pat.location == mod.location and pat.serviceTime > 0:
                    mod.serve(pat)
                    break
                if pat.location == mod.location and pat.serviceTime == -1:
                    # This should be a method in the module class.
                    print('Location {0} now serving Patient {1}'.format(mod.location,pat.name))
                    pat.serviceTime = mod.completionTime
                    break

        completed = 0
        # condition to check if all patients have completed the clinic (Can we close?)
        for pat in patientList:
            if pat.location == moduleCount:
                
                completed += 1
        counter +=1


# program for post simulation data analysis

# use unittest for unit testing like JUnit
if __name__ == "__main__": main()
