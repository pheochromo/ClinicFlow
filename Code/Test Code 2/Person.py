class Person:
        def __init__(self,newName,mods):
            self.name = newName
            self.arrivalTime = 0 # when they arrived
            self.modules = mods
            self.location = [] ## have arrays of where they have been, and where they need to go
            self.serviceTime = -1 # what time they are currently in service
            self.completionTime = -1 # when they left

        def assignTime(self,time):
                self.arrivalTime = time 

        def addLocation(self,newLoc):
                self.location.append(newLoc)

        def __repr__(self):
                return "<Person name:%s arrivalTime:%d>" % (self.name, self.arrivalTime)

        def __str__(self):
                return "Person %s, arrives at %d" % (self.name, self.arrivalTime)





