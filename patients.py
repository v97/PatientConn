import json
import pymongo

# all

# x = registerUserJSON("Brian", 69, True, [])

def registerUserJSON(name, age, gender, symptoms):
    user_data = {}
    user_data['name'] = name
    user_data['age'] = age
    user_data['gender'] = gender
    user_data['symptoms'] = []
    user_data['appointments'] = []
    prescription = {}
    prescription['medication'] = []
    prescription['nutrition'] = []
    sleep = {}
    sleep['hours'] = 9
    sleep['comments'] = []
    prescription['sleep'] = sleep
    user_data['prescriptions'] = prescription
    return json.dumps(user_data)

def addSymptom(name, date, scale):
    user_symptom = {}
    user_symptom['name'] = name
    user_symptom['frequency'] = 1
    instances = [addInstanceSymptom(date, scale)]
    user_symptom['instances'] = instances
    user_symptom['ongoing'] = True
    return json.dumps(user_symptom)

def endSymptom():


def addInstanceSymptom(date, scale):
    instance = {}
    instance['startdate'] = date
    instance['enddate'] = False
    instance['scale'] = scale
    return instance

def getDate(date):
    temp = date.split('-')
    date = {}
    date['M'] = int(temp[0])
    date['D'] = int(temp[1])
    date['Y'] = int('20' + temp[2]) if temp[2] < 100 else int(temp[2])
    return date

def addInstanceMedi(dosage, freq, freqUnit, start, end, comments):
    instance = {}
    instance['dosage'] = dosage
    instance['frequency'] = freq
    instance['freqUnit'] = freqUnit
    instance['start'] = start
    instance['end'] = end
    instance['comments'] = comments

    return instance

def addMedication(drug, instances, dosage, freq, freqUnit, start, end, comments):
    medication = {}
    medication['drug'] = drug
    medication['ongoing'] = True
    instances = [addInstanceMedi(dosage, freq, freqUnit, start, end, comments)]
    medication['instances'] = instances

def endSymptom(name, date, symptom):


