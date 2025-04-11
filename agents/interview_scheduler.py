import sqlite3
from datetime import datetime, timedelta
from agents.shortlister import get_shortlisted_candidates

DB_PATH = "db/aptly.db"

def create_interview_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            job_title TEXT,
            scheduled_time DATETIME,
            status TEXT DEFAULT 'Scheduled',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def schedule_interviews():
    create_interview_table()
    shortlisted = get_shortlisted_candidates()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Mock schedule: assign each interview 1 hour apart starting now
    start_time = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    scheduled = []

    for i, candidate in enumerate(shortlisted):
        interview_time = start_time + timedelta(hours=i)
        
        cursor.execute("""
            INSERT INTO interviews (candidate_name, job_title, scheduled_time)
            VALUES (?, ?, ?)
        """, (
            candidate["candidate_name"],
            candidate["job_title"],
            interview_time.strftime("%Y-%m-%d %H:%M:%S")
        ))

        scheduled.append({
            "candidate_name": candidate["candidate_name"],
            "job_title": candidate["job_title"],
            "scheduled_time": interview_time.strftime("%A %d %B %Y, %I:%M %p")
        })

    conn.commit()
    conn.close()
    return scheduled

# Quick test
if __name__ == "__main__":
    result = schedule_interviews()
    for entry in result:
        print(entry)
