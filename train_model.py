import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

def train_digital_twin_model():
    print("Loading datasets...")
    # Load data
    df_ehr = pd.read_csv('data/ehr_static_data.csv')
    df_sensor = pd.read_csv('data/sensor_dynamic_data.csv')
    
    print("Extracting features from time-series sensor data (Digital Twin processing)...")
    # Feature Engineering: Extract 24-hour trends from the dynamic data
    # In a real app, this would be a rolling window. We'll simplify for the PoC.
    
    # Filter to only the last 24 hours of data for feature extraction
    latest_time = pd.to_datetime(df_sensor['timestamp']).max()
    cutoff_time = latest_time - pd.Timedelta(hours=24)
    df_sensor['timestamp'] = pd.to_datetime(df_sensor['timestamp'])
    recent_sensor_data = df_sensor[df_sensor['timestamp'] >= cutoff_time]
    
    # Aggregate wearable data per patient
    sensor_features = recent_sensor_data.groupby('patient_id').agg({
        'heart_rate': ['mean', 'max'],
        'hrv_ms': ['mean', 'min'],
        'spo2_percent': ['mean', 'min']
    }).reset_index()
    
    # Flatten multi-level columns
    sensor_features.columns = ['patient_id', 'hr_mean', 'hr_max', 'hrv_mean', 'hrv_min', 'spo2_mean', 'spo2_min']
    
    print("Fusing Static EHR and Dynamic Wearable Streams...")
    # Merge Static (EHR) and Dynamic (Sensor) streams
    fused_data = pd.merge(df_ehr, sensor_features, on='patient_id')
    
    # Prepare X (features) and y (target)
    features = ['age', 'cholesterol_ldl', 'systolic_bp', 'smoker', 'family_history_cvd', 
                'hr_mean', 'hr_max', 'hrv_mean', 'hrv_min', 'spo2_mean', 'spo2_min']
    
    X = fused_data[features]
    y = fused_data['target_event_in_24h']
    
    # Split for training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training the Digital Twin Predictive Model (Random Forest)...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    print("\n--- Model Evaluation ---")
    print(f"Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")
    print(classification_report(y_test, predictions))
    
    # Save the model
    os.makedirs('models', exist_ok=True)
    with open('models/cardio_twin_model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    print("\n[SUCCESS] Model saved to models/cardio_twin_model.pkl")
    print("The Digital Twin is now ready to make predictions on real-time data!")

if __name__ == "__main__":
    train_digital_twin_model()
