import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset we just created
df = pd.read_csv('ppd_dataset.csv')

# Separate inputs (X) from the answer we want to predict (y)
X = df.drop('risk_label', axis=1)
y = df['risk_label']

# Split into training data (80%) and testing data (20%)
# The model learns from training data, then we test it on data it has never seen
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Test how accurate it is
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy * 100:.1f}%")
print("\nDetailed results:")
print(classification_report(y_test, y_pred, target_names=['Low Risk', 'Medium Risk', 'High Risk']))

# Save the trained model so our app can use it
joblib.dump(model, 'ppd_model.pkl')
print("Model saved successfully!")