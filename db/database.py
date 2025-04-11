import sqlite3
import os

# Optional: Create the db folder if it doesn't exist
os.makedirs("db", exist_ok=True)

# Connect to the database (it will be created if it doesn't exist)
conn = sqlite3.connect("db/aptly.db")
cursor = conn.cursor()

# Create the shortlist_results table
cursor.execute("""
CREATE TABLE IF NOT EXISTS shortlist_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT,
    job_title TEXT,
    match_score INTEGER,
    skill_match TEXT,
    experience_match TEXT,
    education_match TEXT,
    remarks TEXT,
    shortlisted BOOLEAN,
    reason TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database and table initialized successfully.")
