from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaulttags import register

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

from .ClinicCreate import *
import pymongo
from pymongo import MongoClient #import MongoDB
client = MongoClient()
db = client.Clinic_database # create schema
settings = db.application_setting #data of setting

result = db.result # temporarily store the data of simulation
schedule_list = db.schedulelist # a list of schedule, contain date and settings

@login_required
def setting(request):
    currentSettings = settings.currentSettings
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

        if request.POST.get("addProvider"): # create a new schedule based on date
            currentSettings.insert_one({"object":"provider", "name":"", "preReqs": "", "maxNum":"", "minNum":"", "varType":"", "avg":"", "dev":""})

        if request.POST.get("deleteProvider"):
            currentSettings.delete_one({"name": request.POST.get("deleteProvider").split(" ")[1]})
            
        if request.POST.get("updateClinicSettings"):
            providerNames = request.POST.getlist('providername')
            providerpreReqs = request.POST.getlist('providerpreReqs')
            providermaxNum = request.POST.getlist('providermaxNum')
            providerminNum = request.POST.getlist('providerminNum')
            providervarType = request.POST.getlist('providervarType')
            provideravg = request.POST.getlist('provideravg')
            providerdev = request.POST.getlist('providerdev')

            currentSettings.delete_many({'object': 'provider'})
            print("heree:     " + str(len(providerNames)))

            for i in range(0, len(providerNames)):
                currentSettings.insert_one({"object":"provider", "name":providerNames[i], "preReqs":providerpreReqs[i].split(","), "maxNum":providermaxNum[i], "minNum":providerminNum[i], "varType":providervarType[i], "avg":provideravg[i], "dev":providerdev[i]})

        if request.POST.get("calculateValue"):
            a=clinicCreate()

    result2 = settings.find_one({"object":"patient"}) #get settings
    providers =""
    for single in result2["provider"]:
        providers=providers+single+"/" # get teh value from database and store into template

    clinicSettings = currentSettings.find({"object":"provider"})

    return render(request, 'setting.html', {"provider":providers, "clinicSettings":clinicSettings})

@login_required
def schedulelists(request): #display the list of existed schedules based on date
    if request.method =='POST':
        if request.POST.get("DeleteSchedule"): #delete a schedule based on the date
            theDate = request.POST.get('the_date')
            schedule_list.delete_one({'Date':theDate})#delete it from schedule list
            patientdate = db[theDate+'patient']#drop the collection data of patient information of the day
            resultdate = db[theDate+'result'] #drop the collection data of simulated result of the day
            patientdate.drop()
            resultdate.drop()
    result = schedule_list.find()
    datearray=[]
    for each in result:
        datearray.append(each["Date"])# get teh date from schedule list
    datearray.sort()
    return render(request, 'schedulelists.html', {"date":datearray})

@login_required
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
            elif request.POST.get("DeletePatient"): # if delete patients
                the_select = request.POST.get('the_patient')
                patientdate.delete_one({'Name': the_select})
            elif request.FILES['uploadedfile'] and request.POST.get('Upload'):
                import csv
                import io
                paramFile = io.StringIO(request.FILES['uploadedfile'].read().decode('utf-8').strip())
                data = csv.DictReader(paramFile)
                for row in data:
                    times = row['Time'].split(':')
                    hour = int(times[0])
                    if 'pm' in times[2] or 'PM' in times[2]:
                        if hour <12:
                            hour=hour+12
                    time=str(hour)+":"+times[1]
                    one_patient={'Name':row['Name'],'Time':time}
                    providers=[]
                    for each in result1['provider']:
                        if row[each] != '':
                            providers.append(each)
                    one_patient.update({'Visit':providers})
                    patientdate.insert_one(one_patient)
            return HttpResponseRedirect("/singleschedule?date="+str(date))

        patients = patientdate.find()# display the patient reserved at that day
        for single in patients:
            patient.append(single)

    currentSettings = settings.currentSettings
    clinicSettings = currentSettings.find({"object":"provider"})

    return render(request,'singleschedule.html',{'patientinfo':patient,"information": clinicSettings})

@login_required
def passport(request):
    providers=[]
    provider_from_set = settings.currentSettings.find({"object":"provider"})
    for each in provider_from_set:
        providers.append(each['name'])
   # provider_from_set = settings.find_one({"object":"patient"}) #get settings
   # providers =provider_from_set["provider"]
    timebound1=0
    timebound2=0
    if 'timebound1' in request.GET and request.GET['timebound1']!= "":
     #   date = request.GET['timebound1'].splite('/')
     ##
     ## only work for yyyy-mm-dd format input
     ## get parameter don't take '/' as value
     ##
        date  = request.GET['timebound1'].split('-')
        #timebound1 = int(date[0])*100+int(date[1])+int(date[2])*10000
        timebound1 = int(date[1])*100+int(date[2])+int(date[0])*10000
    if 'timebound2' in request.GET and request.GET['timebound2']!= "":
      #  date = request.GET['timebound2'].splite('/')
        date  = request.GET['timebound2'].split('-')
        #timebound2 = int(date[0])*100+int(date[1])+int(date[2])*10000
        timebound2 = int(date[1])*100+int(date[2])+int(date[0])*10000
    passport = db.passport

    if request.method =='POST':

         if request.POST.get('Clean'):
            passport.delete_many({})

         elif request.POST.get("Add_Passport"):
             reason=request.POST.get('Reason')
             reasons = reason.splitlines()
             service = request.POST.get('Service')
             services = service.splitlines()
             date = request.POST.get('Date')
             sdate = date.splitlines()
             dates=[]
             for each in sdate:
                 single = each.split('/')
                 value = int(single[0])*100+int(single[1])+int(single[2])*10000
                 dates.append(value)
             #dates = date.splitlines()
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

         elif request.FILES['uploadedfile'] and request.POST.get('Upload'):
            import csv
            import io
            paramFile = io.StringIO(request.FILES['uploadedfile'].read().decode('utf-8').strip())
            data = csv.DictReader(paramFile)
            for row in data:
                one_patient = {}
                reason={'Reason':row['Reason for Visit']}
                one_patient.update(reason)
                service={'Service':row['Service']}
                one_patient.update(service)
                single=row['Date'].split('/')
                value = int(single[0])*100+int(single[1])+int(single[2])*10000
                date={'Date':value}
                one_patient.update(date)
                schedule_time={'Scheduled_Time':row['Scheduled Appointment Time']}
                one_patient.update(schedule_time)
                arrive_time={'Arrival_Time':row['Arrival Time']}
                one_patient.update(arrive_time)
                surgery_type={'Surgery_Type':row['Day Surgery/ Admitted Surgery']}
                one_patient.update(surgery_type)
                depart_time={'Departure_time':row['Departure Time']}
                one_patient.update(depart_time)
                for each in providers:
                    eachin= each+' Time In'
                    one_patient.update({each+'_Time_In':row[eachin]})
                    eachout= each+' Time Out'
                    one_patient.update({each+'_Time_Out':row[eachout]})
                    eachcomment = each+' Comments'
                    one_patient.update({each+'_Comment':row[eachcomment]})
                passport.insert_one(one_patient)

         if timebound1 !=0 and timebound2 != 0:
             time11=timebound1%100
             timebound1 = int(timebound1/100)
             time12 = timebound1%100
             timebound1 =int(timebound1/100)
             time1 = str(timebound1)+'-'+str(time12)+'-'+str(time11)
             time21=timebound2%100
             timebound2 = int(timebound2/100)
             time22 = timebound2%100
             timebound2 =int(timebound2/100)
             time2 = str(timebound2)+'-'+str(time22)+'-'+str(time21)
             return HttpResponseRedirect("/passport?timebound1="+str(time1)+"&timebound2="+str(time2))
         elif timebound1 !=0 and timebound2==0 :
             time11=timebound1%100
             timebound1 = int(timebound1/100)
             time12 = timebound1%100
             timebound1 =int(timebound1/100)
             time1 = str(timebound1)+'-'+str(time12)+'-'+str(time11)
             return HttpResponseRedirect("/passport?timebound1="+str(time1))
         elif timebound1 ==0 and timebound2 !=0:
             time21=timebound2%100
             timebound2 = int(timebound2/100)
             time22 = timebound2%100
             timebound2 =int(timebound2/100)
             time2 = str(timebound2)+'-'+str(time22)+'-'+str(time21)
             return HttpResponseRedirect("/passport?timebound2="+str(time2))
         else:
             return  HttpResponseRedirect("/passport")
    if timebound1 !=0 and timebound2 !=0:
        if timebound2 < timebound1:
            passports = passport.find({'Date': {'$gte': timebound2, '$lte':timebound1}})
        elif timebound1 < timebound2:
            passports = passport.find({'Date': {'$gte': timebound1, '$lte':timebound2}})
        else:
            passports = passport.find({'Date':timebound1})
    elif timebound1 !=0 and timebound2==0 :
        passports = passport.find({'Date':timebound1})
    elif timebound1 ==0 and timebound2 !=0:
        passports = passport.find({'Date':timebound2})
    else:
        passports = passport.find()

    return render(request,'passport.html',{'passport':passports, 'providers':providers})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_date(date):
    day = date%100
    date = int(date/100)
    month = date%100
    date = int(date/100)
    newdate =  str(date)+'/'+str(month)+'/'+str(day)
    return newdate

def schedule(request): #sample of changing setting
    if not request.user.is_staff:
        raise PermissionDenied
    else:
        result1 = settings.find_one({"object":"patient"})
        return render(request, 'schedule.html', {"result": result1})

def manage(request):
    return render(request, 'manage.html')

def viewer(request):
    return render(request, 'viewer.html')

def login(request):
    # if request.method =='POST': #if post/submit
    #     if request.POST.get("Change_Provider"):
    #         data = request.POST.get('Clinic_Provider') # change clinic setting
    #         strings = data.split("/")
    #         while '' in strings:
    #             strings.remove('')

    return render(request, 'login.html')

def forbidden(request):
    return render(request, '403.html')

def page_not_found(request):
    return render(request, '404.html')
