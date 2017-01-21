import pymongo as pm
import patients.py

uri = 'mongodb://bjluk:pcjt5ebFS1e3Ww305Ck9nG7tlW' \
      'pNCoEbJRieI3PwsUWEqNrZOp2aeucUSuIfIiMzUrDf' \
      'zK3WfL7q1BR4b4lGBg==@bjluk.documents.azure' \
      '.com:10250/?ssl=true&ssl_cert_reqs=CERT_NONE'
client = pm.MongoClient(uri)

usersCollection = client['Users']
patientsCollection = usersCollection['Patients']


print(client.database_names())