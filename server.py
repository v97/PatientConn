from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import time

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'users'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'
client = MongoClient('mongodb://localhost:27017/')
patients = (client.users)["patients"]

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

@app.route('/addPatient/', methods = ['POST'])
def addPatient():
	symptoms = request.form["symptoms"]
	if symptoms is None:
		symptoms = {}
	id = patients.insert(newPatientJSON(request.form["name"], request.form["age"], request.form["male"], symptoms))
	return str(id)

@app.route('/updatePatient/', methods = ['POST'])
def updatePatient():
	patients.update({"_id": ObjectId(request.form["id"])}, request.form["patient"], upsert=True)
	return True

@app.route('/updateNutrition/', methods = ['POST'])
def updateNutrition():
	patient = patients.find({"_id": ObjectId(id)}).next()
	patient["prescription"]["nutrition"] = request.form["nutrition"]
	patients.update({"_id": ObjectId(request.form["id"])}, patient, upsert=True)
	return True

@app.route('/updateExercise/', methods = ['POST'])
def updateExercise():
	patient = patients.find({"_id": ObjectId(id)}).next()
	patient["prescription"]["exercise"] = request.form["exercise"]
	patients.update({"_id": ObjectId(request.form["id"])}, patient, upsert=True)
	return True

@app.route('/updateSleep/', methods = ['POST'])
def updateSleep():
	patient = patients.find({"_id": ObjectId(id)}).next()
	patient["prescription"]["sleep"] = request.form["sleep"]
	patients.update({"_id": ObjectId(request.form["id"])}, patient, upsert=True)
	return True

def TEMP_ADD(name, age, male, symptoms = None):
	if symptoms is None:
		symptoms = {}
	id = patients.insert(newPatientJSON(name, age, male, symptoms))
	return str(id)

@app.route('/addSymptomInstance/<id>/<symptom>/<freq>/<severity>/<start>/<end>/')
def addSymptomInstance(id, symptom, freq, severity, start, end):
    patient = patients.find({"_id": ObjectId(id)}).next()
    instance = {"start": start, "end": end, "freq": freq, "severity": severity}
    if symptom in patient["symptoms"]:
        patient["symptoms"][symptom]["instances"].append(instance)
    else:
        patient["symptoms"][symptom] = {"instances": [instance]}
    patients.update({"_id": ObjectId(id)}, patient, upsert=True)

@app.route('/symptomOngoing/<id>/<symptom>')
def symptomOngoing(id, symptom):
    patient = patients.find({"_id": ObjectId(id)}).next()
    if symptom in patient["symptoms"] == False:
        return False
    return (patient["symptoms"][symptom]["instances"][-1]["end"] is None) == False

@app.route('/endOngoingSymptom/<symptom>/<end>')
def endOngoingSymptom(id, symptom, end):
	patient = patients.find({"_id": ObjectId(id)}).next()
	patient["symptoms"][symptom]["instances"][-1]["end"] = end
	patients.update({"_id": ObjectId(id)}, patient, upsert=True)
    
def getDate(date):
    temp = date.split('-')
    date = {}
    date['M'] = int(temp[0])
    date['D'] = int(temp[1])
    date['Y'] = int('20' + temp[2]) if temp[2] < 100 else int(temp[2])
    return date

@app.route('/addMedicine/<drug>/<dosage>/<freq>/<comments>/<start>/<end>')
def addMedicine(drug, dosage, freq, comments, start, end):
	patient = patients.find({"_id": ObjectId(id)}).next()
	instance = {"dosage": dosage, "freq": freq, "start": start, "end": end, "comments": comments}
	patient["prescription"]["medication"][drug] = patient["prescription"]["medication"].get("drug", []) + [instance]
	patients.update({"_id": ObjectId(id)}, patient, upsert=True)
	return True

@app.route('/endOngoingMedicine/<id>/<drug>/<end>')
def endOngoingMedicine(id, drug, end):
	patient = patients.find({"_id": ObjectId(id)}).next()
	patient["prescription"]["medication"][drug][-1]["end"] = end
	patients.update({"_id": ObjectId(id)}, patient, upsert=True)
	return True

@app.route('/medicineOngoing/<id>/<drug>')
def medicineOngoing(id, drug):
    patient = patients.find({"_id": ObjectId(id)}).next()
    if drug in patient["prescription"]["medication"] == False:
        return False
    return (patient["prescription"]["medication"][drug][-1]["end"] is None) == False

@app.route('/getMedication/<id>')
def getMedication(id):
    patient = patients.find({"_id": ObjectId(id)}).next()
    return patient["medication"]

@app.route('/getNutrition/<id>')
def getNutrition(id):
    patient = patients.find({"_id": ObjectId(id)}).next()
    return patient["nutrition"]

@app.route('/getPatient/<id>')
def getPatient(id):
	return str(patients.find({"_id": ObjectId(id)}).next())

@app.route('/getPatients/')
def getPatients():
	return str([docs for docs in patients.find({})])

@app.route('/clear/')
def clear():
	patients.delete_many({})
	return True

@app.route('/')
def index():
    return str(time.time())

#addSymptomInstance(id, "Jew", True, 10, 1, "21/01/2017")
#endOngoingSymptom(id, "Jew", "22/01/2026")
app.run(host="0.0.0.0", port=80)
