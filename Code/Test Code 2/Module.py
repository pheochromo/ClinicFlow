from Person import Person

class Module:
    def __init__(self,name,time,people,req):
        self.location = name
        self.completionTime = time ## can use this for randomness
        self.staffCount = people
        self.currentStaff = 0
        self.requirements = req
        
    ##method to serve the patient
    def serve(self,patient):
        patient.serviceTime -=1
        if patient.serviceTime == 0:
            patient.completionTime += self.completionTime
            patient.location.append(self.location)
            patient.serviceTime = -1
            print ('Location {0} has finished serving {1}'.format(self.location,patient.name))
        else :
            print ('Location {0} is still serving {1}'.format(self.location,patient.name))
  

