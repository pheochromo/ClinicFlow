from Module import Module

class Clinic:
    def __init__(self,fileName):
        clinicFile = open(fileName,mode ='r')
        self.stations = []
        for line in clinicFile:
            data = line.split()
            temp = Module(data[0],float(data[1]),data[2],data[3].split(','))
            self.stations.append(temp)

        clinicFile.close()


# Test Harness
#def main():
#    file = "Clinic1.txt"
#    newClinic = Clinic(file)
#    for station in newClinic.stations:
#        print(station.location, station.completionTime,station.requirements)

    
#if __name__ == "__main__": main()
