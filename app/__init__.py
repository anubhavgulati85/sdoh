# app/__init__.py

from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object('config')
    db.init_app(app)
    #db = SQLAlchemy(app)
    from app.routes import bp
    app.register_blueprint(bp)
    

    # Load the trained model and scaler
    model = joblib.load('./app/rf_model.pkl')
    scaler = joblib.load('./app/scaler.pkl')

    # Load the label encoders
    label_encoders_hc = joblib.load('./app/label_encoders_access_to_healthcare.pkl')
    label_encoders_ac = joblib.load('./app/label_encoders_alcohol_consumption.pkl')
    label_encoders_dh = joblib.load('./app/label_encoders_dietary_habits.pkl')
    label_encoders_d = joblib.load('./app/label_encoders_disease.pkl')
    label_encoders_el = joblib.load('./app/label_encoders_education_level.pkl')
    label_encoders_es = joblib.load('./app/label_encoders_employment_status.pkl')
    label_encoders_g = joblib.load('./app/label_encoders_gender.pkl')
    label_encoders_ehs = joblib.load('./app/label_encoders_housing_status.pkl')
    label_encoders_eil = joblib.load('./app/label_encoders_income_level.pkl')
    label_encoders_mhs = joblib.load('./app/label_encoders_mental_health_status.pkl')
    label_encoders_ns = joblib.load('./app/label_encoders_neighborhood_safety.pkl')
    label_encoders_pa = joblib.load('./app/label_encoders_physical_activity_level.pkl')
    label_encoders_sst = joblib.load('./app/label_encoders_smoking_status.pkl')
    label_encoders_ss = joblib.load('./app/label_encoders_social_support.pkl')

    return app


if __name__ == '__main__':
    app.run(debug=True)
