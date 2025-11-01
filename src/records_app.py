# records_app.py
import streamlit as st
import pandas as pd
import sqlite3

st.title("👩‍⚕️ Doctor Portal - Patient Records")
st.write("View patient records and add treatment recommendations.")

# Connect to SQLite database
conn = sqlite3.connect("patients.db")
cursor = conn.cursor()

# Fetch patient records
df = pd.read_sql_query("SELECT * FROM patients", conn)

if df.empty:
    st.warning("⚠️ No patient records found yet. Please run the patient app first.")
else:
    # Show all records
    st.subheader("📑 All Patient Records")
    st.dataframe(df)

    # --- Filters ---
    st.subheader("🔍 Search & Filter")
    name_filter = st.text_input("Search by Name")
    gender_filter = st.selectbox("Filter by Gender", ["All", "Male", "Female", "Other"])
    disease_filter = st.text_input("Search by Disease")

    filtered_df = df.copy()

    if name_filter:
        filtered_df = filtered_df[filtered_df["name"].str.contains(name_filter, case=False, na=False)]
    if gender_filter != "All":
        filtered_df = filtered_df[filtered_df["gender"] == gender_filter]
    if disease_filter:
        filtered_df = filtered_df[filtered_df["predicted_disease"].str.contains(disease_filter, case=False, na=False)]

    st.subheader("📊 Filtered Results")
    st.dataframe(filtered_df)

    # --- Add Recommendation ---
    st.subheader("💊 Add/Update Doctor Recommendation")
    patient_ids = df["id"].tolist()
    selected_id = st.selectbox("Select Patient ID", patient_ids)

    current_record = df[df["id"] == selected_id].iloc[0]
    st.write(f"👤 Patient: {current_record['name']} | 🦠 Predicted Disease: {current_record['predicted_disease']}")

    recommendation = st.text_area("Enter treatment/recommendation", value=current_record["doctor_recommendation"] if pd.notna(current_record["doctor_recommendation"]) else "")

    if st.button("Save Recommendation"):
        cursor.execute("UPDATE patients SET doctor_recommendation=? WHERE id=?", (recommendation, selected_id))
        conn.commit()
        st.success("✅ Recommendation saved successfully!")

    # --- Download Option ---
    st.subheader("⬇️ Download Filtered Records")
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="filtered_patient_records.csv",
        mime="text/csv"
    )

conn.close()
