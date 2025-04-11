import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect("aptly.db")
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

print("Database and table created successfully.")
