from agents.jd_summarizer import summarize_job_description
from agents.cv_extractor import extract_cv_data
from agents.candidate_scorer import score_candidate

def test_flow():
    jd = "We need a Python developer with ML skills, familiarity with FastAPI, and good communication."
    cv = """Name: Jane Doe
Skills: Python, FastAPI, Machine Learning, Teamwork
Experience: 3 years"""

    summary = summarize_job_description(jd)
    print("✅ JD Summary:", summary)

    cv_data = extract_cv_data(cv)
    print("✅ CV Extracted:", cv_data)

    score = score_candidate(summary, cv_data)
    print("✅ Candidate Score:", score)

test_flow()
