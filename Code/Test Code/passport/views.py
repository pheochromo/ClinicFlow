from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaulttags import register

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

        patients = patientdate.find()# display the patient reserved at that day
        for single in patients:
            patient.append(single)

    return render(request,'singleschedule.html',{'patientinfo':patient,"information": result1})

def passport(request):
    provider_from_set = settings.find_one({"object":"patient"}) #get settings
    providers =provider_from_set["provider"]
    
    passport = db.passport
    if request.method =='POST':
         if request.POST.get("Add_Passport"):
             reason=request.POST.get('Reason')
             reasons = reason.splitlines()
             service = request.POST.get('Service')
             services = service.splitlines()
             date = request.POST.get('Date')
             dates = date.splitlines()
             schedule_time = request.POST.get('Scheduled_Time')
             schedule_times = schedule_time.splitlines()
             arrive_time = request.POST.get('Arrival_Time')
             arrive_times = arrive_time.splitlines()
             surgery_type = request.POST.get('Surgery_Type')
             surgery_types = surgery_type.splitlines()
             depart_time = request.POST.get('Departure_time')
             depart_times = depart_time.splitlines()
             sections=[]
             for each in providers:
                 time_in = request.POST.get(each+'_Time_In')
                 time_ins = time_in.splitlines()
                 time_out = request.POST.get(each+'_Time_Out')
                 time_outs = time_out.splitlines()
                 comment = request.POST.get(each+'_Comment')
                 comments = comment.splitlines()
                 sections.append([each,time_ins,time_outs, comments])
             lables =[]
             if len(reasons) > 0 and len(reasons) == len(dates):
                 lables.append(['Reason',reasons])
             if len(services) > 0 and len(services) == len(dates):
                 lables.append(['Service',services])
             lables.append(['Date',dates])
             if len(schedule_times) > 0 and len(schedule_times) == len(dates):
                 lables.append(['Scheduled_Time',schedule_times])
             if len(arrive_times) > 0 and len(arrive_times) == len(dates):
                 lables.append(['Arrival_Time',arrive_times])
             if len(surgery_types) > 0 and len(surgery_types) == len(dates):
                 lables.append(['Surgery_Type',surgery_types])
             if len(depart_times) > 0 and len(depart_times) == len(dates):
                 lables.append(['Departure_time',depart_times])
             for each in sections:
                 if len(each[1]) > 0 and len(each[1]) == len(dates):
                     lables.append([each[0]+'_Time_In',each[1]])
                 if len(each[2]) > 0 and len(each[2]) == len(dates):
                     lables.append([each[0]+'_Time_Out',each[2]])
                 if len(each[3]) > 0 and len(each[3]) == len(dates):
                     lables.append([each[0]+'_Comment',each[3]])
             i =0
             for day in dates:
                 one_patient = {}
                 for title in lables:
                     one_patient.update({title[0]:title[1][i]})
                 passport.insert(one_patient)
                 i=i+1
#==============================================================================
#              if len(reasons) == len(services):
#                  i=0
#                  for line in reasons:
#                      one_patient={'Reason':line, 'Service': services[i]}
#                      passport.insert_one(one_patient)
#                      i=i+1
#==============================================================================
         return  redirect("/passport")
    passports = passport.find()


    return render(request,'passport.html',{'passport':passports, 'providers':providers})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def schedule(request): #sample of changing setting
    result1 = settings.find_one({"object":"patient"})
    return render(request, 'schedule.html', {"result": result1})

def manage(request):
    return render(request, 'manage.html')

def viewer(request):
    return render(request, 'viewer.html')

def login(request):
    return render(request, 'login.html')
