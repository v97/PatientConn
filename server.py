from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'test_database'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_database'
client = MongoClient('mongodb://localhost:27017/')
patients = (client.test_database)["patients"]

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

@app.route('/addPatient/', [methods = 'POST'])
def addPatient(name, age, male, symptoms = None):
	#<name>/<age>/<male>/<symptoms>
	a = request.form()
	#if symptoms is None:
	#	symptoms = {}
	#id = patients.insert(newPatientJSON(name, age, male, symptoms))
	print(a)
	return "134"

@app.route('/addSymptomInstance')
def addSymptomInstance(id, symptom, freq, severity, start, end = None):
    patient = patients.find({"_id": id}).next()
    instance = {"start": start, "end": end, "freq": freq, "severity": severity}
    if symptom in patient["symptoms"]:
        patient["symptoms"][symptom]["instances"].append(instance)
    else:
        patient["symptoms"][symptom] = {"instances": [instance]}
    patients.update({"_id": id}, patient, upsert=True)

@app.route('/endOngoingSymptom/<symptom>/<end>')
def endOngoingSymptom(id, symptom, end):
	patient = patients.find({"_id": id}).next()
	patient["symptoms"][symptom]["instances"][-1]["end"] = end
	patients.update({"_id": id}, patient, upsert=True)

def symptomOngoing(id, symptom):
    patient = patients.find({"_id": id}).next()
    if symptom in patient["symptoms"] == False:
        return False
    return (patient["symptoms"][symptom]["instances"][-1]["end"] is None) == False
    
def getDate(date):
    temp = date.split('-')
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

def endOngoingMedicine(drug, end):
    patient = patients.find({"_id": id})
    patient["prescription"]["medication"][drug][-1]["end"] = end
    patients.update({"_id": id}, patient, upsert=True)

def medicineOngoing(id, drug):
    patient = patients.find({"_id": id}).next()
    if drug in patient["prescription"]["medication"] == False:
        return False
    return (patient["prescription"]["medication"][drug][-1]["end"] is None) == False

def getMedication():
    patient = patients.find({"_id": id})
    patient["medication"]
    patients.update({"_id": id}, patient, upsert=True)

patients.delete_many({})
id = addPatient("Vikram", 19, True)	
print(id)

@app.route('/getPatient/<id>')
def getPatient(id):
	return str(patients.find({"_id": ObjectId(id)}).next())

#addSymptomInstance(id, "Jew", True, 10, 1, "21/01/2017")
#endOngoingSymptom(id, "Jew", "22/01/2026")
app.run()
