import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset
df = pd.read_csv('ppd_dataset.csv')

X = df.drop('risk_label', axis=1)
y = df['risk_label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
rf_model = RandomForestClassifier(n_estimators=200, max_depth=8, min_samples_split=10, random_state=42)
rf_model.fit(X_train, y_train)
rf_acc = accuracy_score(y_test, rf_model.predict(X_test))

# Train XGBoost
xgb_model = XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42, eval_metric='mlogloss')
xgb_model.fit(X_train, y_train)
xgb_acc = accuracy_score(y_test, xgb_model.predict(X_test))

print(f"Random Forest accuracy: {rf_acc * 100:.1f}%")
print(f"XGBoost accuracy:       {xgb_acc * 100:.1f}%")

# Pick the better model
if xgb_acc > rf_acc:
    print("\nXGBoost wins — saving XGBoost model")
    best_model = xgb_model
    cv_scores = cross_val_score(xgb_model, X, y, cv=5)
else:
    print("\nRandom Forest wins — keeping Random Forest model")
    best_model = rf_model
    cv_scores = cross_val_score(rf_model, X, y, cv=5)

print(f"Cross-validation accuracy: {cv_scores.mean() * 100:.1f}% (+/- {cv_scores.std() * 100:.1f}%)")
print("\nDetailed results:")
print(classification_report(y_test, best_model.predict(X_test), target_names=['Low Risk', 'Medium Risk', 'High Risk']))

joblib.dump(best_model, 'ppd_model.pkl')
print("Best model saved!")