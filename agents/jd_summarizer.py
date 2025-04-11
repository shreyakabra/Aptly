from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Load Ollama LLM
def load_llm(model_name="mistral"):
    return Ollama(model=model_name)

# JD Summarizer Prompt Template
def get_prompt_template():
    return PromptTemplate(
        input_variables=["job_description"],
        template="""
You are an AI assistant that reads job descriptions and extracts key information.

Extract and summarize the following details from the job description:
1. Required Skills
2. Required Experience
3. Job Responsibilities
4. Educational Qualifications (if any)

Respond in the following format:
Skills: ...
Experience: ...
Responsibilities: ...
Qualifications: ...

Job Description:
{job_description}
"""
    )

# JD Summarization Chain
def create_summarizer_chain():
    llm = load_llm()
    prompt = get_prompt_template()
    return LLMChain(llm=llm, prompt=prompt)

# Summarize a given JD string
def summarize_job_description(jd_text):
    chain = create_summarizer_chain()
    result = chain.run(job_description=jd_text)
    return result

# CLI for quick testing
if __name__ == "__main__":
    print("=== Job Description Summarizer Agent ===")
    jd_input = input("Paste a job description below:\n\n")
    print("\nSummarizing...\n")
    output = summarize_job_description(jd_input)
    print("=== Extracted Summary ===")
    print(output)
