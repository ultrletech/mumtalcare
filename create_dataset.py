import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000

age = np.random.randint(16, 45, n)
marital_status = np.random.choice([0, 1], n, p=[0.3, 0.7])  # 0=single, 1=partnered
partner_support = np.random.choice([0, 1, 2, 3], n, p=[0.15, 0.25, 0.35, 0.25])  # 0=none to 3=strong
planned_pregnancy = np.random.choice([0, 1], n, p=[0.4, 0.6])  # 0=unplanned, 1=planned
prior_mental_health = np.random.choice([0, 1], n, p=[0.75, 0.25])  # 0=no, 1=yes
prev_pregnancy_loss = np.random.choice([0, 1], n, p=[0.7, 0.3])  # 0=no, 1=yes
low_birth_weight = np.random.choice([0, 1], n, p=[0.8, 0.2])  # 0=normal, 1=low
self_reported_mood = np.random.choice([0, 1, 2, 3], n, p=[0.1, 0.3, 0.35, 0.25])  # 0=very low to 3=good
sleep_quality = np.random.choice([0, 1, 2], n, p=[0.2, 0.45, 0.35])  # 0=very poor to 2=okay
weeks_postpartum = np.random.choice([0, 1, 2, 3], n, p=[0.25, 0.35, 0.25, 0.15])  # 0=0-2wks to 3=12+wks

# Calculate risk score based on known clinical factors
risk_score = (
    (age < 20).astype(int) * 2 +
    (marital_status == 0).astype(int) * 2 +
    (partner_support < 2).astype(int) * 2 +
    (planned_pregnancy == 0).astype(int) * 1 +
    prior_mental_health * 3 +
    prev_pregnancy_loss * 1 +
    low_birth_weight * 1 +
    (self_reported_mood < 2).astype(int) * 2 +
    (sleep_quality < 1).astype(int) * 1 +
    (weeks_postpartum < 2).astype(int) * 1
)

# Convert score to risk label
def score_to_label(s):
    if s <= 3:
        return 0  # Low
    elif s <= 6:
        return 1  # Medium
    else:
        return 2  # High

risk_label = np.array([score_to_label(s) for s in risk_score])

df = pd.DataFrame({
    'age': age,
    'marital_status': marital_status,
    'partner_support': partner_support,
    'planned_pregnancy': planned_pregnancy,
    'prior_mental_health': prior_mental_health,
    'prev_pregnancy_loss': prev_pregnancy_loss,
    'low_birth_weight': low_birth_weight,
    'self_reported_mood': self_reported_mood,
    'sleep_quality': sleep_quality,
    'weeks_postpartum': weeks_postpartum,
    'risk_label': risk_label
})

df.to_csv('ppd_dataset.csv', index=False)
print("Dataset created successfully!")
print(df['risk_label'].value_counts())