# train.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_and_save_model():
    # Load dataset
    data = pd.read_csv("C:\\Users\\shere\\Documents\\diseaseprediction\\data\\Training.csv")

    # Drop unnecessary columns (like unnamed index)
    if "Unnamed: 133" in data.columns:
        data = data.drop("Unnamed: 133", axis=1)

    # Features (symptoms)
    X = data.drop("prognosis", axis=1)
    # Target (disease name)
    y = data["prognosis"]

    # Split into training & validation
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model (Random Forest)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate accuracy
    accuracy = model.score(X_val, y_val)
    print(f"Validation Accuracy: {accuracy:.2f}")

    # Save model
    joblib.dump(model, "../models/disease_model.joblib")
    print("✅ Model saved as ../models/disease_model.joblib")

if __name__ == "__main__":
    train_and_save_model()
