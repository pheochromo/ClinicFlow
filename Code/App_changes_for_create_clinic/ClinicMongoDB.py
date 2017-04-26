# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 13:44:57 2017

@author: weilin
"""
import pymongo
from pymongo import MongoClient #import MongoDB
client = MongoClient()
databaseName = "Clinic_database"
db = client.Clinic_database # create schema

settings = db.application_setting
patient = db.patient
result = db.result
settings.delete_many({})
patient.delete_many({})
result.delete_many({})
# samplepatient = {"name":"John", "provider":["blood","xray"]}
patient.create_index("name")
settings.create_index("object")
# patient.insert_one(samplepatient)
setting_of_patient ={"object":"patient", "attribute1":"Name", "attribute2":"Date", "attribute3":"Time", "provider":["Registration","RNInterview","LaboratoryECG","LaboratoryBloodwork","Anesthesiologist","X-Ray"]}


# Add first default clinic settings
default1 = settings.default1
default1.delete_many({})
currentSettings = settings.currentSettings
currentSettings.delete_many({})

temp = {"object": "provider", "name":"Registration", "preReqs":["Registration"], "maxNum":1, "minNum":1, "varType":"exponential", "avg":5, "dev":2}
default1.insert_one(temp)
currentSettings.insert_one(temp)

temp = {"object": "provider", "name":"RNInterview", "preReqs":["Registration", "RNInterview"], "maxNum":1, "minNum":1, "varType":"exponential", "avg":10, "dev":10}
default1.insert_one(temp)
currentSettings.insert_one(temp)

temp = {"object": "provider", "name":"LaboratoryECG", "preReqs":["Registration", "RNInterview", "LaboratoryECG"], "maxNum":1, "minNum":1, "varType":"exponential", "avg":5, "dev":5}
default1.insert_one(temp)
currentSettings.insert_one(temp)

temp = {"object": "provider", "name":"LaboratoryBloodwork", "preReqs":["Registration", "RNInterview", "LaboratoryBloodwork"], "maxNum":1, "minNum":1, "varType":"exponential", "avg":5, "dev":5}
default1.insert_one(temp)
currentSettings.insert_one(temp)

temp = {"object": "provider", "name":"Anesthesiologist", "preReqs":["Registration", "RNInterview", "Anesthesiologist"], "maxNum":1, "minNum":1, "varType":"normal", "avg":20, "dev":10}
default1.insert_one(temp)
currentSettings.insert_one(temp)

temp = {"object": "provider", "name":"X-Ray", "preReqs":["Registration","RNInterview","LaboratoryECG","LaboratoryBloodwork","X-Ray"], "maxNum":1, "minNum":1, "varType":"normal", "avg":20, "dev":20}
default1.insert_one(temp)
currentSettings.insert_one(temp)



settings.insert_one(setting_of_patient)
result = patient.find()
print("results:")
for single in result:
    print (single["name"])
    print (single["provider"])

result1 = settings.find_one({"object":"patient"})
print(result1["attribute1"])

providers =""
for e in result1["provider"]:
    print(e)
    providers = providers+e+"/"
    #providers=providers+result1["provider"][e]+"/"
print(providers)

#==============================================================================
# strings = providers.split("/")
# while '' in strings:
#     strings.remove('')
# print("new:::!!")
# print (strings)
# setting_of_patient ={"object":"patient", "attribute1":"Name", "attribute2":"Date", "attribute3":"Time", "provider":strings}
# settings.save(setting_of_patient)
# result1 = settings.find_one({"object":"patient"})
# providers =""
# for e in result1["provider"]:
#     print(e)
#     providers = providers+e+"/"
#==============================================================================
