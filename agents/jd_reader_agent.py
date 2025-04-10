import csv
import os
from typing import List, Dict
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

# Load the JD file
def load_job_descriptions(filepath: str) -> List[str]:
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row['Job Description'] for row in reader if row.get('Job Description')]

# Summarize JD using Ollama
class JDReaderAgent:
    def __init__(self):
        self.llm = Ollama(model="mistral")

    def summarize_jd(self, jd_text: str) -> str:
        docs = [Document(page_content=jd_text)]
        chain = load_summarize_chain(self.llm, chain_type="stuff")
        summary = chain.run(docs)
        return summary

if __name__ == "__main__":
    jd_file = "data/job_description.csv"
    jds = load_job_descriptions(jd_file)
    agent = JDReaderAgent()

    for idx, jd_text in enumerate(jds):
        print(f"\n🔍 Summary for JD {idx+1}:")
        summary = agent.summarize_jd(jd_text)
        print(summary)
