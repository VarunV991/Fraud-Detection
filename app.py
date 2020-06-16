import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler,OneHotEncoder
import os
from flask import Flask, request, jsonify, render_template, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from sklearn.externals import joblib 

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS =False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
scaler = joblib.load('scale.pkl')
model_last = joblib.load('fraud_RF1.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "Unsuccessful"
    file = request.files['file']
    if file.filename == '':
        return "Unsuccessful"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return predict(filename)
    
    return "Unsuccessful"

def predict(filename):
    path = 'uploads/'+filename
    trans_df = pd.read_csv(path)
    original = trans_df
    trans_df = trans_df.drop(['nameOrig','nameDest'],1)
    trans_df["errorBalanceOrg"] = trans_df.newbalanceOrig + trans_df.amount - trans_df.oldbalanceOrg
    trans_df["errorBalanceDest"] = trans_df.oldbalanceDest + trans_df.amount - trans_df.newbalanceDest
    dataset = pd.get_dummies(trans_df,prefix='type')
    
    scaler.transform(dataset)
    
    predictions = model_last.predict(dataset)
    original['isFraud'] = pd.DataFrame(data=predictions,columns=['isFraud'])
    fraud = original[original['isFraud']==1]
    fraud.to_csv('predict_files/fraud.csv',index=False)
    return send_file('predict_files/fraud.csv',as_attachment=True)

@app.route('/train',methods=['POST'])
def train():
    if 'file' not in request.files:
        return "Unsuccessful"
    file = request.files['file']
    if file.filename == '':
        return "Unsuccessful"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('train_upload', filename))
        return train_model(filename)

    
    return "Unsuccessful"

def train_model(filename):
    path = "train_upload/"+filename
    trans_df = pd.read_csv(path)
    original = trans_df
    trans_df = trans_df.drop(['nameOrig','nameDest'],1)
    trans_df["errorBalanceOrg"] = trans_df.newbalanceOrig + trans_df.amount - trans_df.oldbalanceOrg
    trans_df["errorBalanceDest"] = trans_df.oldbalanceDest + trans_df.amount - trans_df.newbalanceDest
    dataset = pd.get_dummies(trans_df,prefix='type')
    X_train = dataset.drop('isFraud',1)
    y_train = dataset.isFraud
    scaler.transform(X_train)
    model_last.fit(X_train,y_train)
    joblib.dump(model_last,'fraud_RF1.pkl')
    return "Successful"

if __name__ == '__main__':
   app.run(debug = True)
    