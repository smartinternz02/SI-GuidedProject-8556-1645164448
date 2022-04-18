from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import pickle
import requests


model=pickle.load(open('PCASSS_model.pkl','rb'))
app=Flask(__name__)
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "HkOydNLfzniWDo6QaNwNX1274Y5tJ05-xyxPq-Owbv-e"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/')
def home():
    return render_template('demo.html')

@app.route('/predict',methods=["POST"])
def predict1():
   
    input_features=[float(x) for x in request.form.values()]
    features_value=[np.array(input_features)]
    payload_scoring = {"input_data": 
			[{"field": [['id','cycle','setting1', 'setting2', 'setting3', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11',
                   's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21','ttf']], "values": [(input_features)]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7488912b-b6aa-4b62-a92b-8273bfcc6da6/predictions?version=2021-12-03', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    pred= response_scoring.json()
    print(pred)
    output=pred['predictions'][0] ['values'][0][0]
    print(output)
    '''features_name=[''id','cycle','setting1', 'setting2', 'setting3', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11',
                   's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21','ttf']
    df=pd.DataFrame(features_value,columns=features_name)
    output=model.predict(df)
    print(output)'''
    
    return render_template('result1.html',prediction_text=output)

if __name__ == "__main__" :
        app.run(debug=False)
