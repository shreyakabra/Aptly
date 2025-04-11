import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import json

DB_PATH = "db/aptly.db"

def get_shortlisted_from_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shortlist_results WHERE shortlisted = 1")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def schedule_interviews():
    create_interview_table()
    shortlisted = get_shortlisted_from_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
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

def get_scheduled_interviews():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interviews WHERE status = 'Scheduled'")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_interview_time(interview_id, new_time):
    now = datetime.now().strftime("%Y-%m-%d")
    new_datetime = f"{now} {new_time}:00"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE interviews SET scheduled_time = ? WHERE id = ?", (new_datetime, interview_id))
    conn.commit()
    conn.close()

def cancel_interview(interview_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE interviews SET status = 'Cancelled' WHERE id = ?", (interview_id,))
    conn.commit()
    conn.close()
    
def save_shortlisted_candidate(name, job_title, score):
    conn = sqlite3.connect("aptly.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS shortlisted (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, job_title TEXT, score TEXT)"
    )
    cursor.execute("INSERT INTO shortlisted (name, job_title, score) VALUES (?, ?, ?)", (name, job_title, json.dumps(score)))
    conn.commit()
    conn.close()

def get_shortlisted_candidates():
    conn = sqlite3.connect("aptly.db")
    df = pd.read_sql("SELECT * FROM shortlisted", conn)
    conn.close()
    return df

