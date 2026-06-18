import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset
df = pd.read_csv('ppd_dataset.csv')

# Separate inputs (X) from the answer we want to predict (y)
X = df.drop('risk_label', axis=1)
y = df['risk_label']

# Split into training data (80%) and testing data (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train a Random Forest model — more powerful than Logistic Regression
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    min_samples_split=10,
    random_state=42
)
model.fit(X_train, y_train)

# Test accuracy on unseen data
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test set accuracy: {accuracy * 100:.1f}%")

# Cross-validation - tests the model 5 different ways for a more reliable score
cv_scores = cross_val_score(model, X, y, cv=5)
print(f"Cross-validation accuracy: {cv_scores.mean() * 100:.1f}% (+/- {cv_scores.std() * 100:.1f}%)")

print("\nDetailed results:")
print(classification_report(y_test, y_pred, target_names=['Low Risk', 'Medium Risk', 'High Risk']))

# Show which factors matter most to the model
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nTop risk factors (by importance):")
print(importances.head(5))

# Save the trained model
joblib.dump(model, 'ppd_model.pkl')
print("\nModel saved successfully!")