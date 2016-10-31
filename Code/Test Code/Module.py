from Person import Person

class Module:
    def __init__(self,name,time):
        self.location = name
        self.completionTime = time
        ## include an array of requirements *where they need to have been
        

    ##method to serve the patient
    ## could include a randomization element?
    def serve(self,patient):
        patient.serviceTime -=1
        if patient.serviceTime == 0:
            patient.completionTime += self.completionTime
            patient.location += 1
            patient.serviceTime = -1
            print ('Location {0} has finished serving {1}'.format(self.location,patient.name))
        else :
            print ('Location {0} is still serving {1}'.format(self.location,patient.name))
  

