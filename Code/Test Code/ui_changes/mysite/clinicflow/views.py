from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

import pymongo
from pymongo import MongoClient #import MongoDB
client = MongoClient()
db = client.Clinic_database # create schema
settings = db.application_setting #data of setting

result = db.result # temporarily store the data of simulation
schedule_list = db.schedulelist # a list of schedule, contain date and settings

def setting(request):
    if request.method =='POST': #if post/submit
        if request.POST.get("Change_Provider"):
            
            data = request.POST.get('Clinic_Provider') # change clinic setting
            strings = data.split("/")
            while '' in strings:
                strings.remove('')
            old = settings.find_one({"object":"patient"})
            new ={"object":"patient", "attribute1":"Name", "attribute2":"Date", "attribute3":"Time", "provider":strings}
            settings.replace_one(old,new) # replace the change in database
        if request.POST.get("Create_Schedule"): # create a new schedule based on date
            datedate = request.POST.get('Schedule_Date')
            patientsetting = settings.find_one({"object":"patient"})
            schedule = {"Date":datedate, "setting1": patientsetting} # store in schedule list
            schedule_list.update_one({"Date":datedate}, {'$set':schedule},upsert=True) #prevent duplicate
    
    result2 = settings.find_one({"object":"patient"}) #get settings 
    providers =""
    for single in result2["provider"]:
        providers=providers+single+"/" # get teh value from database and store into template
    return render(request, 'setting.html', {"provider":providers})
    
def schedulelists(request): #display the list of existed schedules based on date
    if request.method =='POST':
        if request.POST.get("DeleteSchedule"): #delete a schedule based on the date
            theDate = request.POST.get('the_date')
            schedule_list.delete_one({'Date':theDate})#delete it from schedule list
            patientdate = db[theDate+'patient']#drop the collection data of patient information of the day
            resultdate = db[theDate+'result'] #drop the collectioni data of simulated result of the day
            patientdate.drop()
            resultdate.drop()
    result = schedule_list.find()
    datearray=[]
    for each in result:
        datearray.append(each["Date"])# get teh date from schedule list
    datearray.sort()
    return render(request, 'schedulelists.html', {"date":datearray})    

    
def singleschedule(request):
    date=''
    patient =[]
    result1 ={}
    if 'date' in request.GET and request.GET['date'] != "": #determine the date of the schedule
        date = request.GET['date']
        patientdate = db[date+'patient'] # create the data collection for patient at that day
        resultdate = db[date+'result'] # create simulation result collection for that day
        result = schedule_list.find_one({'Date':date})
        result1 = result['setting1']
        
        if request.method =='POST':
            if request.POST.get("AddPatient"):# if add patients
                name = request.POST.get('Name')
                time = request.POST.get('Time')
                providers = request.POST.getlist('Providers')
                one_patient = {'Name':name,'Time':time,'Visit':providers}
                patientdate.insert_one(one_patient)
            if request.POST.get("DeletePatient"): # if delete patients
                the_select = request.POST.get('the_patient')
                patientdate.delete_one({'Name': the_select})
        
        patients =patientdate.find()# display the patient reserved at that day
        for single in patients:
            patient.append(single)
    
    return render(request,'singleschedule.html',{'patientinfo':patient,"information": result1})
    
def schedule(request): #sample of changing setting
    result1 = settings.find_one({"object":"patient"})
    return render(request, 'schedule.html', {"result": result1})
    
def manage(request):
    return render(request, 'manage.html')
    
def viewer(request):
    return render(request, 'viewer.html')    
    
def login(request):
    return render(request, 'login.html')      
