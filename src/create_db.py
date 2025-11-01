# create_db.py
import sqlite3

# Connect (creates file if not exists)
conn = sqlite3.connect("patients.db")
cursor = conn.cursor()

# Create patients table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    duration TEXT,
    symptoms TEXT,
    predicted_disease TEXT,
    doctor_recommendation TEXT
)
""")

conn.commit()
conn.close()
print("Database and table created successfully!")
