# app.py

import streamlit as st
import pandas as pd
import json
from agents.jd_summarizer import summarize_job_description
from agents.cv_extractor import extract_cv_data
from agents.candidate_scorer import score_candidate
from agents.shortlister import shortlist_decision
from utils.db_utils import (
    schedule_interviews,
    get_scheduled_interviews,
    update_interview_time,
    cancel_interview
    save_shortlisted_candidate,
    get_shortlisted_candidates
)

st.set_page_config(page_title="Aptly", layout="wide")

# ---------------------- SETUP ----------------------
@st.cache_data
def load_jd_data():
    df = pd.read_csv("data/job_description.csv", encoding="ISO-8859-1")
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    return df

uploaded_jd_file = st.file_uploader("Upload JD file (.csv)", type=["csv"])
if uploaded_jd_file:
    jd_df = pd.read_csv(uploaded_jd_file)
else:
    jd_df = load_jd_data()

st.title("🧠 Aptly - AI-Powered Job Screening System")

# Sidebar CV Status
if "cv_data" in st.session_state:
    st.sidebar.success("✅ CV Extracted")
    if st.sidebar.button("🔁 Reset CV"):
        st.session_state.pop("cv_data")
        st.session_state.pop("cv_text")

# ---------------------- TABS ----------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 JD Summarizer", "📤 CV Extractor", "📊 Candidate Scorer",
    "✅ Shortlister", "📅 Interview Scheduler"
])

# ---------------------- TAB 1: JD SUMMARIZER ----------------------
with tab1:
    st.header("📄 Job Description Summarizer")
    jd_index = st.selectbox("Select a JD to summarize:", jd_df.index, format_func=lambda x: f"JD #{x+1}")
    jd_text = jd_df.loc[jd_index, "job_description"]

    st.subheader("📃 Job Description")
    st.write(jd_text)

    if st.button("🔍 Summarize JD"):
        with st.spinner("Summarizing..."):
            summary = summarize_job_description(jd_text)
            st.subheader("📌 Summary")
            st.json(summary)

# ---------------------- TAB 2: CV EXTRACTOR ----------------------
with tab2:
    st.header("📤 CV Information Extractor")
    uploaded_cv = st.file_uploader("Upload a CV (.txt only)", type=["txt"])
    st.markdown("### 📂 Or Upload Multiple CVs:")
    uploaded_cvs = st.file_uploader("Upload Multiple CVs (.txt)", type=["txt"], accept_multiple_files=True, key="multi_cv")

    if uploaded_cvs:
        for file in uploaded_cvs:
            st.write(f"📄 {file.name}")
            text = file.read().decode("utf-8")
            st.text(text)
            # Optional: You could auto-extract and score here


    if uploaded_cv:
        cv_text = uploaded_cv.read().decode("utf-8")
        st.session_state["cv_text"] = cv_text
        st.subheader("📄 CV Preview")
        st.text(cv_text)

        if st.button("🧠 Extract CV Info"):
            with st.spinner("Extracting..."):
                extracted = extract_cv_data(cv_text)
                st.session_state["cv_data"] = extracted
                st.success("CV Information extracted successfully.")
                st.json(extracted)

# ---------------------- TAB 3: CANDIDATE SCORER ----------------------
with tab3:
    st.header("📊 Candidate Scoring")
    jd_index = st.selectbox("Select JD for Scoring:", jd_df.index, format_func=lambda x: f"JD #{x+1}")
    jd_text = jd_df.loc[jd_index, "job_description"]

    if "cv_data" in st.session_state:
        if st.button("📊 Score Candidate"):
            with st.spinner("Scoring..."):
                jd_summary = summarize_job_description(jd_text)
                score = score_candidate(jd_summary, st.session_state["cv_data"])
                st.session_state["score"] = score  # Save for shortlister
                st.subheader("📝 Score Report")
                st.json(score)
    else:
        st.warning("⚠️ Please upload and extract a CV in the 'CV Extractor' tab.")

# ---------------------- TAB 4: SHORTLISTER ----------------------
with tab4:
    st.header("✅ Candidate Shortlister")
    candidate_name = st.text_input("Candidate Name")
    jd_index = st.selectbox("Select JD for Shortlisting:", jd_df.index, format_func=lambda x: f"JD #{x+1}")
    job_title = jd_df.loc[jd_index, "job_title"] if "job_title" in jd_df.columns else f"JD #{jd_index+1}"
    jd_text = jd_df.loc[jd_index, "job_description"]

    if "cv_data" in st.session_state:
        if st.button("✅ Score & Shortlist"):
            with st.spinner("Processing..."):
                jd_summary = summarize_job_description(jd_text)
                score = score_candidate(jd_summary, st.session_state["cv_data"])
                score_json = json.dumps(score)
                result = shortlist_decision(score, candidate_name, job_title)
                st.session_state["shortlisting"] = result  # Save for scheduler
                st.subheader("📋 Shortlisting Result")
                st.json(result)
    else:
        st.warning("⚠️ Please upload and extract a CV in the 'CV Extractor' tab.")

# ---------------------- TAB 5: INTERVIEW SCHEDULER ----------------------
with tab5:
    st.header("📅 Interview Scheduler")

    st.subheader("📌 Schedule New Interview")
    cname = st.text_input("Candidate Name", key="cname")
    jtitle = st.text_input("Job Title", key="jtitle")
    idate = st.date_input("Date")
    itime = st.time_input("Time")

    if st.button("📅 Schedule Interview"):
        interview = schedule_interviews(cname, jtitle, str(idate), str(itime))
        st.success("Interview scheduled successfully!")
        st.json(interview)

    st.subheader("📜 Scheduled Interviews")
    df = get_scheduled_interviews()
    st.dataframe(df)

    st.subheader("✏️ Reschedule or ❌ Cancel Interview")
    selected_id = st.number_input("Enter Interview ID", min_value=1, step=1)
    new_date = st.date_input("New Date", key="new_date")
    new_time = st.time_input("New Time", key="new_time")

    if st.button("🔁 Reschedule"):
        update_interview_time(selected_id, str(new_date), str(new_time))
        st.success("Interview rescheduled!")

    if st.button("❌ Cancel"):
        cancel_interview(selected_id)
        st.success("Interview cancelled.")

    st.markdown("---")
    st.subheader("📧 Confirmation Mock")
    if st.button("📨 Generate Confirmation"):
        st.info(f"📨 Confirmation email: Interview with {cname} for {jtitle} is scheduled on {idate} at {itime}.")
