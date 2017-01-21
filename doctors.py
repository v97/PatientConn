import json
import pymongo


#TODO



def docAvailability():
    hours = {}


def listDoctor(name, specialty, description, availability):
    doctor = {}
    doctor['name'] = name
    doctor['specialty'] = specialty
    doctor['description'] = description
    doctor['reviews'] = []
    return doctor

def newDocReview(stars, comments, patientName, patient=0):
    review = {}
    review['stars'] = stars
    review['comments'] = comments
    review['patient'] = patientName
    return review

def prescribeDrUgS(patient, drugName, dosage, freq, freqUnit, start, end, comments):

#TODO

   dRuGs = patients.addInstanceMedi(dosage, freq, freqUnit, start, end, comments)
   #pull patient data from DB
   if drugName in patient.Medications:
       # add instance of drugName
   else:
       # add new medication of drugName


#TODO
def setAppointment(time, patientName):


def approveAppointment(times):
