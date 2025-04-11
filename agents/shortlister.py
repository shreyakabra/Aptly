import json
import sqlite3
from typing import Dict

DB_PATH = "db/aptly.db"  # Update path if needed

def should_shortlist(candidate_score: Dict) -> bool:
    return (
        candidate_score.get("match_score", 0) >= 75 and
        candidate_score.get("skill_match") in ["Excellent", "Good"] and
        candidate_score.get("experience_match") in ["Exceeds requirement", "Meets requirement"] and
        candidate_score.get("education_match") != "Does not match"
    )

def save_to_db(candidate_name: str, job_title: str, score: Dict, shortlisted: bool, reason: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO shortlist_results (
            candidate_name, job_title, match_score, skill_match,
            experience_match, education_match, remarks, shortlisted, reason
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_name,
        job_title,
        score.get("match_score", 0),
        score.get("skill_match", ""),
        score.get("experience_match", ""),
        score.get("education_match", ""),
        score.get("remarks", ""),
        shortlisted,
        reason
    ))

    conn.commit()
    conn.close()

def shortlist_decision(score: dict, candidate_name: str, job_title: str) -> Dict:
    if not isinstance(score, dict):
        return {
            "shortlisted": False,
            "reason": "Invalid score input format",
            "score": {}
        }

    decision = should_shortlist(score)
    reason = (
        "Candidate meets all required criteria" if decision
        else "Candidate did not meet one or more required criteria"
    )

    # Save to DB
    save_to_db(candidate_name, job_title, score, decision, reason)

    return {
        "candidate_name": candidate_name,
        "job_title": job_title,
        "shortlisted": decision,
        "reason": reason,
        "score": score
    }
        
def get_shortlisted_candidates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT candidate_name, job_title FROM shortlist_results
        WHERE shortlisted = 1
    """)
    
    rows = cursor.fetchall()
    conn.close()

    return [{"candidate_name": row[0], "job_title": row[1]} for row in rows]

# CLI quick test
if __name__ == "__main__":
    score_input = input("Paste Candidate Score JSON:\n")
    candidate_name = input("Enter candidate name:\n")
    job_title = input("Enter job title:\n")
    result = shortlist_decision(score_input, candidate_name, job_title)
    
    print("\n=== Shortlisting Decision ===")
    print(json.dumps(result, indent=2))
