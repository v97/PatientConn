import pymongo as pm
import patients.py
import doctors.py

collection = 'Users'
dbpatients = 'Patients'
dbdoctor = 'Doctor'

def readCSV(filename):
    d = []
    file = open(filename, encoding='utf-8')
    data = file.read()
    lines = data.split('\n')
    for line in lines:
        d.append(line.split(','))
    return d
