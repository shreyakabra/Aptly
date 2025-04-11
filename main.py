import streamlit as st
import pandas as pd
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.runnables import Runnable
from agents.candidate_scorer import score_candidate
from agents.jd_summarizer import summarize_job_description
from agents.cv_extractor import extract_cv_data

# Load JD CSV
@st.cache_data
def load_jd_data():
    df = pd.read_csv("data/job_description.csv", encoding="ISO-8859-1")
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    return df

# Load Ollama LLM
def load_llm():
    return Ollama(model="mistral")

# Set up Streamlit App
st.set_page_config(page_title="Aptly: AI Job Screening System", layout="wide")
st.title("🧠 Aptly - AI-Powered Job Screening System")

tab1, tab2, tab3 = st.tabs(["📄 JD Summarizer", "📤 CV Extractor", "📊 Candidate Scorer"])

# ---------------------- TAB 1: JD SUMMARIZER ----------------------
with tab1:
    st.header("📄 Job Description Summarizer")
    jd_df = load_jd_data()
    jd_index = st.selectbox("Select a JD to summarize:", jd_df.index, format_func=lambda x: f"JD #{x+1}")
    jd_text = jd_df.loc[jd_index, "job_description"]

    st.subheader("Job Description")
    st.write(jd_text)

    if st.button("Summarize JD"):
        with st.spinner("Summarizing..."):
            summary = summarize_job_description(jd_text)
            st.subheader("🔍 JD Summary")
            st.json(summary)

# ---------------------- TAB 2: CV EXTRACTOR ----------------------
with tab2:
    st.header("📤 CV Information Extractor")
    uploaded_cv = st.file_uploader("Upload a CV (.txt only)", type=["txt"])

    if uploaded_cv:
        cv_text = uploaded_cv.read().decode("utf-8")
        st.subheader("📄 CV Preview")
        st.text(cv_text)

        if st.button("Extract CV Info"):
            with st.spinner("Extracting..."):
                extracted = extract_cv_data(cv_text)
                st.subheader("🧠 Extracted CV Information")
                st.json(extracted)

# ---------------------- TAB 3: CANDIDATE SCORER ----------------------
with tab3:
    st.header("📊 Candidate Scoring System")
    selected_jd_idx = st.selectbox("Choose a JD for scoring:", jd_df.index, format_func=lambda x: f"JD #{x+1} - {jd_df.loc[x, 'job_title'] if 'job_title' in jd_df.columns else f'JD #{x+1}'}")
    jd_text_for_score = jd_df.loc[selected_jd_idx, "job_description"]
    uploaded_cv_for_score = st.file_uploader("Upload Candidate CV (.txt)", type=["txt"], key="cv_score")

    if uploaded_cv_for_score:
        cv_text_score = uploaded_cv_for_score.read().decode("utf-8")
        st.subheader("📄 CV Preview")
        st.text(cv_text_score)

        if st.button("Score Candidate"):
            with st.spinner("Scoring candidate against JD..."):
                jd_summary = summarize_job_description(jd_text_for_score)
                cv_data = extract_cv_data(cv_text_score)
                score_result = score_candidate(jd_summary, cv_data)

                st.subheader("📝 Candidate Score Report")
                st.json(score_result)
