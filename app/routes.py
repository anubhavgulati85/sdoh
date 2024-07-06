# app/routes.py

from flask import Blueprint,render_template, request, redirect, url_for, jsonify
#from app import app, db
from app.models import db,User
from app.utils import extract_sdoh_keywords
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/submit', methods=['POST'])
def submit():
    #data = request.json 
    ##df = pd.DataFrame(data, index=[0])

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    gender = request.form['gender']
    state = request.form['state']
    clinical_notes = request.form['clinical_notes']

    #new_user = User(first_name=first_name, last_name=last_name, gender=gender, state=state, clinical_notes=clinical_notes)
    #db.session.add(new_user)
    #db.session.commit()

    # Extract SDOH keywords
    sdoh_keywords = extract_sdoh_keywords(clinical_notes)

    # Load the pre-trained model and scaler
    model = joblib.load('./app/rf_model.pkl')
    scaler = joblib.load('./app/scaler.pkl')
    
    #label_encoders_d = LabelEncoder()
    label_encoders_d = joblib.load('./app/disease_encoder.pkl')

  
    data=[[1,1,0,1,2,0,1,0,1,1,0,1]]
    df = pd.DataFrame(data,columns=['age','gender','income_level','employment_status','education_level',
                                'housing_status','neighborhood_safety','access_to_healthcare','social_support',
                                'physical_activity_level','dietary_habits','smoking_status'])

  
    # Predict using the loaded model
    prediction = model.predict(df)
    
    print(prediction)
    # Decode the prediction
    prediction = label_encoders_d.inverse_transform(prediction)

    return render_template('success.html', first_name=first_name, sdoh_keywords=sdoh_keywords, prediction=prediction)


    
@bp.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get the data from the request
    df = pd.DataFrame(data, index=[0])
    # Load the pre-trained model and scaler
    model = joblib.load('./app/rf_model.pkl')
    scaler = joblib.load('./app/scaler.pkl')
    label_encoders_d = joblib.load('./app/label_encoders_disease.pkl')
    label_encoders_g = joblib.load('./app/label_encoders_gender.pkl')
    sdoh_keywords = extract_sdoh_keywords(data['clinicalNotes'])
    
    print(type(label_encoders_g))
    # Preprocess the data (e.g., scaling, encoding)
    df[['age']] = scaler.transform(df[['age']])
    #for column in label_encoders.keys():
    df['new_gender'] = label_encoders_g.transform(df['gender'])
    
    # Predict using the loaded model
    prediction = model.predict(df)
    
    # Decode the prediction
    prediction = label_encoders['disease'].inverse_transform(prediction)
    
    return jsonify({'prediction': prediction[0]})
    #return render_template('success.html', sdoh_keywords=sdoh_keywords)
    