import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import random

#import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
'''API_KEY = "yRrxWYCduJe9oe664g4jPMnAK7oEXdcycNCMXbaFuYov"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
'''

app = Flask(__name__)
model = joblib.load("engine_model.sav")


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/m_predict',methods=['POST'])
def mpred():
    return render_template('Manual_predict.html')
@app.route('/s_predict',methods=['POST'])
def spred():
    return render_template('Sensor_predict.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    x_test = [[int(x) for x in request.form.values()]]
    
    
    print(x_test)
    a = model.predict(x_test)
    pred = a[0]
    if(pred == 0):
        pred = "No failure expected within 30 days."
    else:
        pred = "Maintenance Required!! Expected a failure within 30 days."
    
    return render_template('Manual_predict.html', prediction_text=pred)



#@app.route('/sy_predict',methods=['POST'])
#def sy_predict():
    #inp1=[]
    #inp1.append(random.randint(0,100)) #id
    #inp1.append(random.randint(0,365)) #cycle
    #for i in range(0,24):
     #   inp1.append(random.uniform(0,1))
        #inp1.append(random.randint(0,365)) #ttf
    #pred=model.predict([inp1])
    
  
   # if(pred == 0):
    #    pred = "No failure expected within 30 days."
    #else:
     #   pred = "Maintenance Required!! Expected a failure within 30 days."
    #return render_template('Sensor_predict.html', prediction_text=pred,data=inp1)

if __name__ == '__main__':
    app.run(debug=False)
