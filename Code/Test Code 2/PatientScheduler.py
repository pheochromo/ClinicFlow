from Person import Person
import numpy as NP   # not working properly

class PatientScheduler:
    def __init__(self,fileName):
        patientFile = open(fileName,mode ='r')
        self.patients = []
        for line in patientFile:
            data = line.split()
            temp = Person(data[0], data[1].split(','))
            self.patients.append(temp)
        
        patientFile.close()

    def schedule(self):
        counter = 0
        for element in self.patients:
            self.patients[counter].assignTime(counter*10 + NP.random.poisson(5,1)) ##schedule a patient every 15 minutes
            counter += 1
    
# Test Harness
#def main():
#    file = "TestPatients.txt"
#    newSchedule = PatientScheduler(file)
#    newSchedule.schedule()
#    for person in newSchedule.patients:
#        print(person.name, person.arrivalTime, person.modules)

    
#if __name__ == "__main__": main()


## ability to add constraints to optimization schedules
##