🧠 Aptly -- AI-Powered Job Screening System
==========================================

**Aptly** is a Generative AI-based multi-agent job screening system that automates the hiring pipeline---from job description summarization to candidate shortlisting and interview scheduling.

> 🔍 Built for a hackathon focused on **"Enhancing Job Screening with AI and Data Intelligence"**, Aptly leverages **on-premise LLMs** via Ollama, embedding models, local vector stores, and SQLite to create a fully functional, end-to-end intelligent hiring solution.

* * * * *

🚀 Features
-----------

-   📝 **Job Description Summarization Agent**\
    Parses and summarizes long job descriptions into concise key points using LLMs.

-   📄 **CV Parsing Agent**\
    Extracts structured candidate information (skills, experience, education) from raw CVs.

-   📊 **Candidate Scoring Agent**\
    Scores candidates based on semantic similarity between JDs and CVs using embeddings.

-   ✅ **Shortlisting Agent**\
    Automatically shortlists top candidates based on scoring threshold.

-   📅 **Interview Scheduling Agent** *(Upcoming)*\
    Schedules interviews and updates candidate status in the pipeline.

-   💬 **Streamlit Frontend**\
    Interactive UI to upload JDs and CVs, run agents, and manage the hiring process.

* * * * *

🛠️ Tech Stack
--------------

| Layer | Technology |
| --- | --- |
| **LLMs** | Ollama + Mistral (on-premise) |
| **Framework** | Python, LangChain, Custom Multi-Agent System |
| **Frontend** | Streamlit |
| **Backend** | Python + SQLite |
| **Storage** | Local Filesystem |

* * * * *

🗂️ Project Structure
---------------------
```bash
aptly/
├── app.py                  # Streamlit UI
├── main.py                 # Backend logic for orchestrating agents
├── agents/
│   ├── jd_summarizer.py    # Job Description Summarization Agent
│   ├── cv_parser.py        # CV Parsing Agent
│   ├── candidate_scorer.py # Candidate Scoring Agent
│   └── shortlister.py      # Candidate Shortlisting Agent
├── utils/
│   ├── db_utils.py         # SQLite database utility functions
│   └── file_utils.py       # File I/O handlers for CVs and JDs
├── data/
│   ├── resumes/            # Uploaded candidate resumes
│   ├── jds/                # Uploaded job descriptions
│   └── shortlisted/        # Output folder for shortlisted candidates
├── assets/                 # Sample JDs and CVs
├── aptly.db                # SQLite database file
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
`

* * * * *

🧪 How to Run Locally
---------------------

### ✅ Step 1: Install Dependencies

bash

CopyEdit

`pip install -r requirements.txt`

### ✅ Step 2: Start Ollama with Gemma 3B

bash

CopyEdit

`ollama run mistral`

### ✅ Step 3: Launch the Streamlit App

bash

CopyEdit

`streamlit run app.py`

* * * * *

🧠 Agents Overview
------------------

### 🔹 Job Description (JD) Summarizer Agent

-   Accepts raw JD text or file input.

-   Uses an LLM to extract:

    -   Role responsibilities

    -   Required skills

    -   Experience

    -   Education

-   Outputs a structured, concise summary.

### 🔹 CV Parser Agent

-   Accepts uploaded resumes in PDF or text format.

-   Extracts:

    -   Name, contact details

    -   Work experience

    -   Skills and qualifications

-   Converts unstructured data into structured format.

### 🔹 Candidate Scoring Agent

-   Converts JD and CVs into embeddings.

-   Uses cosine similarity + rule-based logic.

-   Outputs a **match score** (0--100).

### 🔹 Shortlisting Agent

-   Applies a scoring threshold (e.g., 70).

-   Saves shortlisted candidates to the SQLite DB.

-   Displays them in a sortable table.

### 🔹 Interview Scheduling Agent *(Coming Soon)*

-   Allocates interview slots.

-   Updates candidate status in the database (e.g., *Pending*, *Scheduled*).

* * * * *

📊 Sample Output
----------------

| Candidate | Score | Matched Role | Interview Status |
| --- | --- | --- | --- |
| John Doe | 88 | Data Scientist | Pending |
| Priya Verma | 76 | ML Engineer | Scheduled |
| Mohamed Ali | 82 | AI Researcher | Pending |

* * * * *

📌 Notes
--------

-   Ensure **Ollama** is running before launching the app.

-   Uploaded files are saved in the `data/` directory.

-   SQLite DB auto-creates tables. If not, use `init_db()` from `db_utils.py`.

* * * * *

🎯 Future Enhancements
----------------------

-   ✅ Email notifications for scheduled interviews

-   ✅ Google Calendar / Outlook API integration

-   ✅ ATS Integration for enterprise hiring

-   ✅ Multi-role JD screening support

-   ✅ Analytics Dashboard (candidate funnel, JD metrics)

* * * * *

👨‍💻 Team
----------

| Member | Role |
| --- | --- |
| **Shreya Kabra** | LLM + Multi-Agent Lead |

* * * * *

📄 License
----------

This project is licensed under the **MIT License**.

* * * * *

🤝 Contributing
---------------

We welcome community contributions!\
Fork the repo → Create a feature branch → Submit a Pull Request 🚀

* * * * *

🧾 Hackathon Submission Includes
--------------------------------

✅ Fully functional Streamlit demo\
✅ Multi-agent architecture (LangChain + Custom agents)\
✅ SQLite-backed candidate pipeline\
✅ Sample CVs and JDs for testing\
✅ GitHub repository with full documentation

* * * * *

📎 Resources
------------

-   [LangChain](https://www.langchain.com/)

-   [Ollama](https://ollama.ai/)

-   [Streamlit](https://streamlit.io/)

-   [Mistral]

* * * * *

Let me know if you'd like:

-   A `requirements.txt` generated

-   Sample CVs or JDs added

-   A `demo.gif`/video embedded

-   GitHub badges (Streamlit status, Python version, etc.) added at the top
