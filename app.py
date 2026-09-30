from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="CardioGuard Digital Twin API")

# Enable CORS so our frontend HTML can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained machine learning model
MODEL_PATH = "models/cardio_twin_model.pkl"
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
else:
    model = None
    print("Warning: Model not found. Did you run train_model.py?")

# Define the expected incoming data structure
class PatientData(BaseModel):
    age: int
    cholesterol_ldl: float
    systolic_bp: float
    smoker: int
    family_history_cvd: int
    hr_mean: float
    hr_max: float
    hrv_mean: float
    hrv_min: float
    spo2_mean: float
    spo2_min: float

from fastapi.responses import FileResponse

@app.get("/")
def read_root():
    return FileResponse("dashboard/index.html")

@app.post("/predict")
def predict_risk(data: PatientData):
    if model is None:
        return {"error": "Model not loaded"}

    # Convert the incoming JSON payload into a Pandas DataFrame
    input_data = pd.DataFrame([data.model_dump()])
    
    # Get the probability of a cardiac event (Class 1)
    risk_prob = model.predict_proba(input_data)[0][1]
    
    # Threshold for critical alert
    is_high_risk = bool(risk_prob > 0.75)
    
    return {
        "risk_score_percentage": round(risk_prob * 100, 2),
        "alert_status": "CRITICAL RISK: SILENT ISCHEMIA IMMINENT (Next 24h)" if is_high_risk else "STABLE: NO IMMEDIATE RISK",
        "is_high_risk": is_high_risk
    }
