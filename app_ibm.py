import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import random
import json
import requests
app = Flask(__name__)


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "jqja7xuBXX5cTYoUhTtd_g3PTUQppwhOF0IzQSeixeBl"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)
#model = joblib.load("engine_model.sav")


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/m_predict',methods=['GET','POST'])
def mpred():
    return render_template('Manual_predict.html')
@app.route('/s_predict',methods=['GET','POST'])
def spred():
    return render_template('Sensor_predict.html')

@app.route('/y_predict',methods=['GET','POST'])
def y_predict():
    x_test = [[int(x) for x in request.form.values()]]
    
    
    print(x_test)
  #  a = model.predict(x_test)
    payload_scoring = {"input_data": [{"field": [['_id','cycles_per_minute','set1','set2','sen3','sen4','sen5','sen6','sen7','sen8','sen9','sen10','set11','set12','set13','set14','set15','set16','set17','set18','set19','set20','sen21','trajectory']], "values": x_test}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5e26a1e2-6568-4f87-b290-73928dbc8ea2/predictions?version=2022-03-06', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions = response_scoring.json()

    print("Scoring response")
    predictions=response_scoring.json()
#print(predictions)
    pred=predictions['predictions'][0]['values'][0][0]
    print(pred)
    #pred = a[0]
    if(pred == 0):
        pred = "No failure expected within 30 days."
    else:
        pred = "Maintenance Required!! Expected a failure within 30 days."
    
    return render_template('Manual_predict.html', prediction_text=pred)



#@app.route('/sy_predict',methods=['GET','POST'])
#def sy_predict():
 #   inp1=[]
  #  inp1.append(random.randint(0,100)) #id
   # inp1.append(random.randint(0,365)) #cycle
    #for i in range(0,24):
     #   inp1.append(random.uniform(0,1))
        #inp1.append(random.randint(0,365)) #ttf
    #pred=model.predict([inp1])
    #payload_scoring = {"input_data": [{"field": [['_id','cycles_per_minute','set1','set2','set3','sen1','sen2','sen3','sen4','sen5','sen6','sen7','sen8','sen9','sen10','set11','set12','set13','set14','set15','set16','set17','set18','set19','set20','sen21','trajectory']], "values": [inp1]}]}

    #response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/0d1c2b4a-e6e5-41af-8ce8-596283a95dbb/predictions?version=2022-03-05', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    #print("Scoring response")
    #print(response_scoring.json())
    #predictions = response_scoring.json()

    #print("Scoring response")
    #predictions=response_scoring.json()
#print(predictions)
    #pred=predictions['predictions'][0]['values'][0][0]
    #print(pred)
  
    #if(pred == 0):
     #   pred = "No failure expected within 30 days."
    #else:
     #   pred = "Maintenance Required!! Expected a failure within 30 days."
    #return render_template('Sensor_predict.html', prediction_text=pred,data=inp1)

if __name__ == '__main__':
    app.run(debug=False)
