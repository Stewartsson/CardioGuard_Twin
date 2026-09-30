import pandas as pd
import numpy as np
import datetime
import os

def generate_synthetic_data(num_patients=500):
    print(f"Generating synthetic EHR and Wearable data for {num_patients} patients...")
    np.random.seed(42)
    
    # 1. Generate Static EHR Data
    patient_ids = [f"PT_{i:04d}" for i in range(num_patients)]
    
    # 20% of patients will have a "high risk" profile for silent ischemia
    is_high_risk = np.random.choice([0, 1], size=num_patients, p=[0.8, 0.2])
    
    ehr_data = {
        'patient_id': patient_ids,
        'age': np.where(is_high_risk == 1, np.random.randint(35, 60, num_patients), np.random.randint(20, 60, num_patients)),
        'cholesterol_ldl': np.where(is_high_risk == 1, np.random.normal(160, 20, num_patients), np.random.normal(110, 20, num_num_patients := num_patients)),
        'systolic_bp': np.where(is_high_risk == 1, np.random.normal(145, 15, num_patients), np.random.normal(120, 10, num_patients)),
        'smoker': np.where(is_high_risk == 1, np.random.choice([0, 1], size=num_patients, p=[0.3, 0.7]), np.random.choice([0, 1], size=num_patients, p=[0.8, 0.2])),
        'family_history_cvd': np.where(is_high_risk == 1, np.random.choice([0, 1], size=num_patients, p=[0.4, 0.6]), np.random.choice([0, 1], size=num_patients, p=[0.8, 0.2])),
        'target_event_in_24h': is_high_risk # This is what we want to predict
    }
    
    df_ehr = pd.DataFrame(ehr_data)
    
    # 2. Generate Dynamic Wearable Time-Series Data (Last 7 days, 1 reading per hour)
    sensor_records = []
    base_time = datetime.datetime.now() - datetime.timedelta(days=7)
    
    for i, row in df_ehr.iterrows():
        pid = row['patient_id']
        risk = row['target_event_in_24h']
        
        for hour in range(7 * 24):
            timestamp = base_time + datetime.timedelta(hours=hour)
            
            # If high risk and in the last 24 hours, simulate physiological crash
            in_crash_window = risk == 1 and hour >= (6 * 24)
            
            if in_crash_window:
                hr = np.random.normal(95, 10)     # Elevated resting heart rate
                hrv = np.random.normal(25, 5)     # Severely depressed HRV
                spo2 = np.random.normal(92, 2)    # Slight hypoxia
            else:
                hr = np.random.normal(70, 8)      # Normal HR
                hrv = np.random.normal(60, 15)    # Normal HRV
                spo2 = np.random.normal(98, 1)    # Normal SpO2
                
            sensor_records.append({
                'patient_id': pid,
                'timestamp': timestamp,
                'heart_rate': max(40, min(hr, 180)),
                'hrv_ms': max(10, min(hrv, 120)),
                'spo2_percent': max(80, min(spo2, 100))
            })
            
    df_sensor = pd.DataFrame(sensor_records)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df_ehr.to_csv('data/ehr_static_data.csv', index=False)
    df_sensor.to_csv('data/sensor_dynamic_data.csv', index=False)
    
    print("[SUCCESS] Successfully generated data/ehr_static_data.csv")
    print("[SUCCESS] Successfully generated data/sensor_dynamic_data.csv")

if __name__ == "__main__":
    generate_synthetic_data()
