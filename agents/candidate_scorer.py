from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
import json

# Load Ollama model
def load_llm(model_name="mistral"):
    return Ollama(model=model_name)

# Scoring prompt
scoring_prompt = PromptTemplate(
    input_variables=["jd_summary", "cv_info"],
    template="""
You are a strict job matching assistant. Respond ONLY in the following valid JSON format:

{{
  "match_score": <score out of 100>,
  "skill_match": "<Excellent | Good | Average | Poor>",
  "experience_match": "<Exceeds requirement | Meets requirement | Below requirement>",
  "education_match": "<Matches requirement | Partially matches | Does not match>",
  "remarks": "<short explanation of candidate-job fit>"
}}

JD Summary:
{jd_summary}

CV Info:
{cv_info}
"""
)

# Score candidate
def score_candidate(jd_summary: str, cv_info: str):
    llm = load_llm()
    chain: Runnable = scoring_prompt | llm
    result = chain.invoke({"jd_summary": jd_summary, "cv_info": cv_info})
    
    print("\n=== Raw LLM Output ===\n", result)

    # Optional: try parsing to dict for safety
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON from LLM", "raw_output": result}

# CLI test
if __name__ == "__main__":
    jd_summary = input("Paste the JD summary JSON:\n")
    cv_info = input("Paste the CV extracted JSON:\n")
    print("\nScoring...\n")
    score = score_candidate(jd_summary, cv_info)
    print("=== Candidate Score ===")
    print(score)
