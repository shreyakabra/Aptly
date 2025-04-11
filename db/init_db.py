import sqlite3

DB_PATH = "aptly.db"  # Adjust path if needed

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
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
            reason TEXT
        );
    """)

    conn.commit()
    conn.close()
    print("Table 'shortlist_results' created successfully.")

if __name__ == "__main__":
    create_table()

