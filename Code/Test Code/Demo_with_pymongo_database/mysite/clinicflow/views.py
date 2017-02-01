from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

import pymongo
from pymongo import MongoClient #import MongoDB
client = MongoClient()
db = client.Clinic_database # create schema
settings = db.application_setting
patient = db.patient
result = db.result

def setting(request):
    if request.method =='POST':
        if request.POST.get("Change_Provider"):
            
            data = request.POST.get('Clinic_Provider')
            strings = data.split("/")
            while '' in strings:
                strings.remove('')
            old = settings.find_one({"object":"patient"})
            new ={"object":"patient", "attribute1":"Name", "attribute2":"Date", "attribute3":"Time", "provider":strings}
            settings.replace_one(old,new)
       
    
    result2 = settings.find_one({"object":"patient"})
    providers =""
    for single in result2["provider"]:
        providers=providers+single+"/"
    return render(request, 'setting.html', {"provider":providers})

def schedule(request):
    result1 = settings.find_one({"object":"patient"})
    return render(request, 'schedule.html', {"result": result1})
    
def manage(request):
    return render(request, 'manage.html')
    
def viewer(request):
    return render(request, 'viewer.html')    
    
def login(request):
    return render(request, 'login.html')      
