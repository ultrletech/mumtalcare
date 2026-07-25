## Mumtal Care
AI-Powered Postpartum Depression Risk Screening Tool for Ghana's Community Health Nurses and Officers

## Live Demo
https://mumtalcare.streamlit.app

## Offline Version
See the `/offline-app` folder for the PWA version that works with zero internet.

## Problem
25% of Ghanaian new mothers are at risk of postpartum depression. Ghana's 
Community Health Nurses and Officers conduct postnatal visits but have no 
AI tool to identify at-risk mothers.

## Solution
Mumtal Care is a web-based AI screening tool that assesses 10 clinically 
validated risk factors and outputs Low/Medium/High PPD risk with recommended 
clinical actions in under 2 minutes, along with the key contributing factors behind each result.

## Tech Stack
- Python, XGBoost, scikit-learn, pandas
- Streamlit (web app)
- ONNX Runtime Web (offline PWA)

## Dataset
1,000-record synthetic dataset (not real patient data), generated via weighted random sampling and calibrated against Ghana's GDHS 2022-2023 national statistics
Grounded in 5 published Ghanaian clinical studies
Real-world accuracy has not yet been validated on actual patient data. Reported model metrics (93% test accuracy, 89.4% cross-validation) reflect performance on this synthetic dataset, not clinical performance
Real patient data validation, through a hospital partnership under formal ethics approval, is the planned next step before any clinical deployment

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `streamlit run app.py`

## Built By
Andrew Sam — KNUST, Kumasi, Ghana
Ghana AI Innovation Challenge 2026
