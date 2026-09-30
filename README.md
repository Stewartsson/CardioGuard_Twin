# CardioGuard Twin: Predicting Silent Ischemia

## Team Details
*   **Team Name:** [Your Team Name]
*   **Team Leader:** [Your Name]
*   **Leader Email:** [Your Email]
*   **Leader Phone:** [Your Phone Number]

## College/Incubator Information
*   **Institution:** [Your College/University Name]
*   **Program/Department:** [e.g., Dept of Computer Science / Bio-Medical Engineering]

## Project Title
**CardioGuard Twin:** A Predictive Digital Twin for Early Detection of Silent Ischemia in Young Adults.

## Problem Statement
Cardiovascular diseases (CVD) are striking the Indian population at increasingly younger ages, particularly among urban professionals. A significant portion of acute myocardial infarctions (heart attacks) are preceded by "silent ischemia"—periods of reduced blood flow to the heart lacking classic symptoms like chest pain. Traditional episodic check-ups fail to catch these sudden physiological crashes.

## Healthcare Use Case
We built a Digital Twin Proof-of-Concept (PoC) that continuously monitors a virtual patient. By fusing static Electronic Health Records (EHR) with dynamic, time-series data from consumer wearables (like smartwatches tracking Heart Rate Variability and SpO2), our algorithmic model predicts an impending severe cardiac event (Silent Ischemia) 24 hours before it happens. This allows doctors to intervene proactively rather than reactively.

## Technical Stack
*   **Backend & Data Processing:** Python, Pandas, NumPy
*   **Machine Learning:** Scikit-learn (Random Forest Classifier for Sensor-EHR data fusion)
*   **Synthetic Data Generation:** Custom Python simulator mimicking distributions from Synthea and MIMIC-IV
*   **API / Model Serving:** FastAPI (Planned for Phase 2)
*   **Frontend Dashboard:** React.js / Next.js (Planned for Phase 2)

## AI/ML Model or Framework Details
Our solution utilizes a **Late-Fusion Ensemble approach**:
1.  **Data Ingestion:** We ingest synthetic static EHR data (age, LDL cholesterol, blood pressure) and dynamic wearable data (hourly HR, HRV, SpO2).
2.  **Feature Extraction:** The system extracts 24-hour physiological trends (e.g., HRV depression, SpO2 dips during sleep) from the dynamic stream.
3.  **Predictive Engine:** A Scikit-learn Random Forest Classifier evaluates the fused feature set to calculate a probability score of an acute ischemic event within the next 24 hours. The model achieves high accuracy by recognizing the toxic combination of chronic risk factors and acute physiological stressors.

## Demo Video
*(Link to 15-20 min Unlisted YouTube video explaining and demonstrating the prototype will be added here prior to final submission).*

## Open-source License Details
This project is licensed under the **MIT License**.

## Architecture Diagram & Presentation
*   **Architecture Diagram:** `CardioGuard_Architecture.pdf` (Included in repository root)
*   **Presentation:** `CardioGuard_Presentation.pdf` (Included in repository root)

---
*Note: All files and links in this repository are publicly accessible without additional permissions.*
