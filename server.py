from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import time
import datetime

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'users'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'
client = MongoClient('mongodb://localhost:27017/')
patients = (client.users)["patients"]

def newPatientJSON(name, DOB, male, symptoms):
    patient = {}
    patient['name'] = name
    patient['allergies'] = []
    patient['DOB'] = DOB
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
	id = patients.insert(newPatientJSON(request.form["name"], request.form["DOB"], request.form["male"], symptoms))
	return str(id)

@app.route('/updatePatient/', methods = ['POST'])
def updatePatient():
	patients.update({"_id": ObjectId(request.form["id"])}, request.form["patient"], upsert=True)
	return "True"

@app.route('/updateNutrition/', methods = ['POST'])
def updateNutrition():
	patient = patients.find({"_id": ObjectId(id)}).next()
	patient["prescription"]["nutrition"].append(request.form["nutrition"])
	patients.update({"_id": ObjectId(request.form["id"])}, patient, upsert=True)
	return "True"

@app.route('/updateExercise/', methods = ['POST'])
def updateExercise():
	patient = patients.find({"_id": ObjectId(id)}).next()
	patient["prescription"]["exercise"] = request.form["exercise"]
	patients.update({"_id": ObjectId(request.form["id"])}, patient, upsert=True)
	return "True"

@app.route('/updateSleep/', methods = ['POST'])
def updateSleep():
	patient = patients.find({"_id": ObjectId(request.form["id"])}).next()
	if not ("prescription" in patient):
		patient["prescription"] = {}
	patient["prescription"]["sleep"] = request.form["sleep"]
	patients.update({"_id": ObjectId(request.form["id"])}, patient)
	return "True"

def TEMP_ADD(name, DOB, male, symptoms = None):
	if symptoms is None:
		symptoms = {}
	id = patients.insert(newPatientJSON(name, DOB, male, symptoms))
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
	return "True"

@app.route('/symptomOngoing/<id>/<symptom>')
def symptomOngoing(id, symptom):
    patient = patients.find({"_id": ObjectId(id)}).next()
    if symptom in patient["symptoms"] == False:
        return "False"
    return str((patient["symptoms"][symptom]["instances"][-1]["end"] is None) == False)

@app.route('/endOngoingSymptom/<symptom>/<end>')
def endOngoingSymptom(id, symptom, end):
	patient = patients.find({"_id": ObjectId(id)}).next()
	patient["symptoms"][symptom]["instances"][-1]["end"] = end
	patients.update({"_id": ObjectId(id)}, patient, upsert=True)
	return "True"

@app.route('/drugsToTakeWithin/<id>/<minutes>')    
def drugsToTakeWithin(id, minutes):
	drugsToTake = []
	patient = patients.find({"_id": ObjectId(id)}).next()
	now = datetime.datetime.now()
	for d in patient["prescription"]["medication"]["drug"]:
		date = patient["prescription"]["medication"][d][-1]["end"].split("/")
		if ((date[0] == now.strftime("%d")) and (date[1] == now.strftime("%m")) and (date[2] == now.strftime("%y")) and (daysOfWeek[now.weekday()])):
			times = patient["prescription"]["medication"][drug][-1]["times"]
			for time in times:
				diff = time - (60*now.strftime("%H") + now.strftime("%M"))
				if((diff >= 0) and (diff <= minutes)):
					drugs.append(d)
					break
	return str(drugsToTake)

@app.route('/addMedicine/', methods = ['POST'])
def addMedicine():
    patient = patients.find({"_id": ObjectId(request.form["id"])}).next()
    instance = {"dosage": request.args["dosage"], "daysOfWeek": request.args["daysOfWeek"], "times": request.args["times"], "start": request.args["start"], "end": request.args["end"], "comments": request.args["comments"]}
    #instance = {"dosage": request.args["dosage"]}
    patient["prescription"]["medication"][drug] = patient["prescription"]["medication"].get("drug", []) + [instance]
    patients.updateOne({"_id": ObjectId(id)}, patient)
	#return "e"
	#patients.update({"_id": ObjectId(id)}, )


@app.route('/getMedication/<id>')
def getMedication(id):
    patient = patients.find({"_id": ObjectId(id)}).next()
    return str(patient["medication"])

@app.route('/getNutrition/<id>')
def getNutrition(id):
    patient = patients.find({"_id": ObjectId(id)}).next()
    return str(patient["nutrition"])

@app.route('/getPatient/<id>')
def getPatient(id):
	return str(patients.find({"_id": ObjectId(id)}).next())

@app.route('/getPatients/')
def getPatients():
	return str([docs for docs in patients.find({})])

@app.route('/clear/')
def clear():
	patients.delete_many({})
	return "True"

@app.route('/')
def index():
    return str(time.time())

#addSymptomInstance(id, "Jew", True, 10, 1, "21/01/2017")
#endOngoingSymptom(id, "Jew", "22/01/2026")
app.run(host="0.0.0.0", port=80)
