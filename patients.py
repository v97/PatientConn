from flask import Flask
from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client.test_database
patients = db.test_collection
patients.delete_many({})
#print([doc for doc in patients.find({"age" : 19})])

def newPatientJSON(name, age, male, symptoms):
    patient = {}
    patient['name'] = name
    patient['allergies'] = []
    patient['age'] = age
    patient['male'] = male
    patient['symptoms'] = symptoms
    patient['appointments'] = []
    prescription = {}
    prescription['medication'] = {}
    prescription['nutrition'] = []
    sleep = {}
    sleep['hours'] = 8
    sleep['comments'] = []
    prescription['sleep'] = sleep
    patient['prescriptions'] = prescription
    return patient

def addPatient(name, age, male, symptoms = None):
    if symptoms is None:
        symptoms = {}
    id = patients.insert(newPatientJSON(name, age, male, symptoms))
    return id

def addSymptomInstance(id, symptom, freq, severity, start, end = None):
    patient = patients.find({"_id": id}).next()
    instance = {"start": start, "end": end, "freq": freq, "severity": severity}
    if symptom in patient["symptoms"]:
        patient["symptoms"][symptom]["instances"].append(instance)
    else:
        patient["symptoms"][symptom] = {"instances": [instance]}
    patients.update({"_id": id}, patient, upsert=True)

def endOngoingSymptom(id, symptom, end):
    patient = patients.find({"_id": id}).next()
    patient["symptoms"][symptom]["instances"][-1]["end"] = end

def symptomOngoing(id, symptom):
    patient = patients.find({"_id": id}).next()
    if symptom in patient["symptoms"] == False:
        return False
    return (patient["symptoms"][symptom]["instances"][-1]["end"] is None) == False
    
def getDate(d):
    temp = d.split('-')
    date = {}
    date['M'] = int(temp[0])
    date['D'] = int(temp[1])
    date['Y'] = int('20' + temp[2]) if temp[2] < 100 else int(temp[2])
    return date

def addMedicine(drug, dosage, freq, comments, start, end):
    patient = patients.find({"_id": id})
    instance = {"dosage": dosage, "freq": freq, "start": start, "end": end, "comments": comments}
    patient["prescription"]["medication"][drug] = patient["prescription"]["medication"].get("drug", []) + [instance]
    patients.update({"_id": id}, patient, upsert=True)

def sendOngoingMedicine(drug, end):
    patient = patients.find({"_id": id})
    patient["prescription"]["medication"][drug][-1]["end"] = end
    patients.update({"_id": id}, patient, upsert=True)

def getMedication():
    patient = patients.find({"_id": id})
    patient["medication"]
    patients.update({"_id": id}, patient, upsert=True)
#
#id = addPatient("Vikram", 19, True)
#addSymptomInstance(id, "Jew", True, 10, 1, "21/01/2017")
#endOngoingSymptom(id, "Jew", "22/01/2026")
#
#print(patients.find({"_id": id}).next())
