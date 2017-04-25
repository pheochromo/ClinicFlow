from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import json

from .SimulationEngine import *

from pprint import pprint

import os
import pymongo
from pymongo import MongoClient #import MongoDB
client = MongoClient()
db = client.Clinic_database # create schema
settings = db.application_setting #data of setting

result = db.result # temporarily store the data of simulation
schedule_list = db.schedulelist # a list of schedule, contain date and settings

def simulation(request): #display the list of existed schedules based on date
    result = schedule_list.find()
    datearray=[]
    for each in result:
        datearray.append(each["Date"])# get teh date from schedule list
    datearray.sort()
    return render(request, 'simulation.html', {"date":datearray})

def simengine(request):
    date = ''
    patient = ""
    result1 = {}
    if 'date' in request.GET and request.GET['date'] != "": #determine the date of the schedule
        date = request.GET['date']
        patientdate = db[date+'patient'] # create the data collection for patient at that day
        resultdate = db[date+'result'] # create simulation result collection for that day
        # result = schedule_list.find_one({'Date':date})
        # result1 = result['setting1']

    # print("\n\n\n" + patient)
    # file_name = os.path.join(os.path.dirname(__file__), "TestPatients.txt")
    # f = open(file_name, "w")
    # f.write(patient)
    # f.flush()
    # f.close
    #f = open("TestPatients.txt", "w")
    #f.write(patient)
    #f.close()
    db[date+'result'].delete_many({})
    mysim = SimulationEngine("Worker1.txt", date, "generated", "generated", "outFile1.txt")

    stats = db[date+'result'].find_one({"Name":"clinicStats"})
    # test = db[date+'result'].find_one({"Name":"stationDuration"})
    # print(str(test))
    durationList = []
    durations = db[date+'result'].find({"Name":"stationDuration"})
    for duration in durations:
        temptime1 = duration['startTime'].split(":")
        temptime2 = duration['endTime'].split(":")
        durationList.append([duration['patientName'], duration['stationName'], [0,0,0,temptime1[0], temptime1[1], 0], [0,0,0,temptime2[0], temptime2[1],0]])
        json_list = json.dumps(durationList)



    return render(request,'result.html',{"averageClinicTime":stats['averageClinicTime'], "averageDownTime": stats['averageDownTime'], "durations":json_list})
