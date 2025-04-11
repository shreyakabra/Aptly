from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load Ollama LLM
def load_llm(model_name="mistral"):
    return Ollama(model=model_name)

# CV Extraction Prompt Template
def get_cv_prompt_template():
    return PromptTemplate(
        input_variables=["cv_text"],
        template="""
You are a smart AI assistant that parses candidate CVs.

From the CV text below, extract the following:
- Full Name
- Email
- Phone (if available)
- Skills
- Years of Experience
- Education
- Past Job Titles

Respond ONLY in this JSON format:
{{
  "name": "...",
  "email": "...",
  "phone": "...",
  "skills": ["...", "..."],
  "experience_years": "...",
  "education": "...",
  "past_titles": ["...", "..."]
}}

CV:
{cv_text}
"""
    )

# Create the CV extractor chain
def create_cv_chain():
    llm = load_llm()
    prompt = get_cv_prompt_template()
    return LLMChain(llm=llm, prompt=prompt)

# Main function to extract data from CV
def extract_cv_data(cv_text: str) -> dict:
    chain = create_cv_chain()
    raw_output = chain.run(cv_text=cv_text)
    try:
        import json
        return json.loads(raw_output)
    except Exception:
        return {"error": "Failed to parse CV response as JSON", "raw_output": raw_output}

# CLI for quick testing
if __name__ == "__main__":
    print("=== CV Extractor Agent ===")
    cv_input = input("Paste a CV text below:\n\n")
    print("\nExtracting...\n")
    output = extract_cv_data(cv_input)
    print("=== Extracted CV Data ===")
    print(output)
