# main.py

from agents.jd_summarizer import summarize_job_description
from agents.cv_extractor import extract_cv_data
from agents.candidate_scorer import score_candidate
from agents.shortlister import shortlist_decision
from utils.db_utils import schedule_interviews, get_scheduled_interviews, update_interview_time, cancel_interview


def process_candidate(jd_text, cv_text, candidate_name=None, job_title=None, interview_date=None, interview_time=None):
    try:
        # Summarize the Job Description
        jd_summary = summarize_job_description(jd_text)

        # Extract CV Info
        cv_data = extract_cv_data(cv_text)

        # Candidate Scoring
        score = score_candidate(jd_summary, cv_data)

        # Shortlisting
        shortlisting = shortlist_decision(score, candidate_name or cv_data.get("name", "Unknown"), job_title or "Unknown")

        # Schedule Interview (if shortlisted)
        interview_info = None
        if shortlisting.get("shortlisted") and interview_date and interview_time:
            interview_info = schedule_interviews(
                candidate_name=shortlisting["score"].get("candidate_name", "Unknown"),
                job_title=job_title,
                date=interview_date,
                time=interview_time
            )

        return {
            "jd_summary": jd_summary,
            "cv_data": cv_data,
            "score": score,
            "shortlisting": shortlisting,
            "interview": interview_info
        }

    except Exception as e:
        return {
            "error": f"Something went wrong: {str(e)}"
        }


def fetch_interviews():
    return get_scheduled_interviews()


def reschedule_interview(interview_id, new_date, new_time):
    return update_interview_time(interview_id, new_date, new_time)


def remove_interview(interview_id):
    return cancel_interview(interview_id)
