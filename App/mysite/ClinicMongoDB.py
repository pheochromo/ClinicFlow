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
samplepatient = {"name":"John", "provider":["blood","xray"]}
patient.create_index("name")
settings.create_index("object")
patient.insert_one(samplepatient)
setting_of_patient ={"object":"patient", "attribute1":"Name", "attribute2":"Date", "attribute3":"Time", "provider":["Registration","RNInterview","LaboratoryECG","LaboratoryBloodwork","Anesthesiologist","X-Ray"]}
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
