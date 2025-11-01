import streamlit as st
import pandas as pd
import joblib
import sqlite3
import datetime
import os

# Load trained model
model = joblib.load("disease_model.joblib")

# Load dataset to get symptoms
data = pd.read_csv("../data/Training.csv")
if "Unnamed: 133" in data.columns:
    data = data.drop("Unnamed: 133", axis=1)

symptoms_list = list(data.columns)
symptoms_list.remove("prognosis")

# --- Database Setup ---
conn = sqlite3.connect("patients.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    duration TEXT,
    symptoms TEXT,
    predicted_disease TEXT,
    doctor_recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()

# --- Streamlit UI ---
st.title("🩺 Smart Disease Prediction System - Patient Portal")
st.write("Fill in your details and select symptoms to predict your possible disease.")

# --- Patient Info Section ---
st.subheader("👤 Patient Information")
name = st.text_input("Full Name")
age = st.number_input("Age", min_value=1, max_value=120, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
duration = st.slider("Duration of Symptoms (in days)", 1, 60, 7)

# --- Symptom Selection ---
st.subheader("🤒 Select Symptoms")
selected_symptoms = st.multiselect("Choose symptoms:", symptoms_list)

# --- Predict Button ---
if st.button("🔍 Predict"):
    if not selected_symptoms:
        st.warning("⚠️ Please select at least one symptom.")
    else:
        # Prepare input for model
        input_data = [0] * len(symptoms_list)
        for symptom in selected_symptoms:
            index = symptoms_list.index(symptom)
            input_data[index] = 1
        input_df = pd.DataFrame([input_data], columns=symptoms_list)

        # Prediction
        prediction = model.predict(input_df)[0]
        probas = model.predict_proba(input_df)[0]

        # Top 3 predictions
        top3_idx = probas.argsort()[-3:][::-1]
        top3_diseases = [(model.classes_[i], probas[i]) for i in top3_idx]

        # Show result
        st.success(f"✅ Predicted Disease for **{name}**: **{prediction}**")

        st.write("📊 Top Possible Diseases:")
        for dis, p in top3_diseases:
            st.write(f"- {dis} ({p*100:.2f}%)")

        # Save patient record to SQLite database
        conn = sqlite3.connect("patients.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patients (name, age, gender, duration, symptoms, predicted_disease, doctor_recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            age,
            gender,
            f"{duration} days",
            ", ".join(selected_symptoms),
            prediction,
            None   # doctor will fill later
        ))
        conn.commit()

        # Fetch latest doctor recommendation for this patient
        cursor.execute(
            "SELECT doctor_recommendation FROM patients WHERE name=? ORDER BY id DESC LIMIT 1", 
            (name,)
        )
        rec = cursor.fetchone()
        conn.close()

        if rec and rec[0]:
            st.info(f"💊 Doctor's Recommendation: {rec[0]}")
        else:
            st.warning("⏳ Doctor has not yet added a recommendation.")

# To run the app, use the following command in the terminal:
# streamlit run app_streamlit.py --server.port 8501
