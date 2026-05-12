# ResumeReview-OPT

> A Constrained Multi-Agent Optimization Framework for ATS-Aware Resume Alignment

ResumeReview-OPT is an AI-powered resume optimization system built as part of an IEEE conference paper project at Menedżerska Akademia Nauk Stosowanych w Warszawie. The system uses a pipeline of four specialized AI agents to analyze a resume against a job description and iteratively improve it to maximize ATS (Applicant Tracking System) alignment — without fabricating any information.

---

## What It Does

Most job applications are filtered by ATS software before a human ever reads them. ResumeReview-OPT helps candidates understand how their resume is being scored and improves it automatically using AI.

The system runs five steps:

1. **Parsing Agent** — Extracts structured data from the resume and job description using LLaMA 3.3 70B
2. **ATS Simulation Agent** — Scores keyword coverage and resume structure, mimicking real ATS behavior
3. **Semantic Matching Agent** — Measures meaning-level alignment using SBERT (all-MiniLM-L6-v2)
4. **Optimization Agent** — Rewrites the resume under strict factual constraints using LLaMA 3.3 70B
5. **Constraint Feedback Loop** — Re-scores and refines the resume across multiple passes

---

## Features

- 📄 Upload resume as PDF or paste as text
- 💼 Paste any job description
- 🏭 Select your target industry for smarter keyword prioritization
- 📊 ATS scores with detailed breakdown explaining each result
- 🔍 Side-by-side comparison of original vs optimized resume
- 🟢🔴 Highlighted diff showing exactly what changed
- 🎤 Predicted interview questions (technical, behavioral, situational, industry-specific)
- 📄 Export optimized resume as PDF or TXT
- ⚡ Powered by Groq (free, fast LLaMA 3.3 inference)

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM | LLaMA 3.3 70B via Groq API |
| Semantic Similarity | SBERT — all-MiniLM-L6-v2 |
| Web Framework | Streamlit |
| PDF Reading | PyMuPDF (fitz) |
| PDF Export | fpdf2 |
| Diff Engine | Python difflib |
| Language | Python 3.10+ |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/dyabi129-ops/resumereview-opt.git
cd resumereview-opt
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Windows users:** use `py -m pip install -r requirements.txt`

### 3. Add your Groq API key

Open `app.py` and replace line 13:

```python
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"
```

Get a free key at **https://console.groq.com**

### 4. Run the app

```bash
streamlit run app.py
```

> **Windows users:** use `py -m streamlit run app.py`

### 5. Open in browser

Go to **http://localhost:8501**

---

## Project Structure

```
resumereview-opt/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── agents/
│   ├── parsing_agent.py            # Parses resume and JD into structured JSON
│   ├── ats_simulation_agent.py     # Rule-based ATS keyword and structure scoring
│   ├── semantic_matching_agent.py  # SBERT cosine similarity scoring
│   ├── optimization_agent.py       # LLaMA 3.3 resume optimizer with constraints
│   └── interview_agent.py          # Interview question generator
└── utils/
    ├── feedback_loop.py            # Orchestrates the iterative optimization loop
    ├── pdf_reader.py               # Extracts text from uploaded PDF resumes
    └── pdf_exporter.py             # Exports optimized resume as PDF
```

---

## How the Constraint System Works

The Optimization Agent is instructed through its system prompt to follow these rules on every pass:

- ❌ Do NOT invent or fabricate any experience, skills, or achievements
- ✅ Only rephrase, reorder, or reframe existing content
- ✅ Integrate missing keywords only where they genuinely apply
- ✅ Preserve all factual information — company names, dates, job titles, education
- ✅ Keep the resume professional, readable, and human-sounding

This makes ResumeReview-OPT both effective and ethically sound.

---

## Research Paper

This project was developed as part of an IEEE conference paper:

**"ResumeReview-OPT: A Constrained Multi-Agent Optimization Framework for ATS-Aware Resume Alignment"**

Wydział Zarządzania i Nauk Technicznych  
Menedżerska Akademia Nauk Stosowanych w Warszawie, Polska

Authors: Haytham Dyabi, Erlanbek Arapbaev, Paul Odimmegwa, Takura Lionel Muparutsa, Kumar Nalinaksh

---

## Requirements

```
streamlit>=1.32.0
pymupdf>=1.24.0
groq>=0.9.0
sentence-transformers>=2.7.0
torch>=2.0.0
fpdf2>=2.7.0
```

---

## License

This project was developed for academic purposes as part of a university research paper. All rights reserved by the authors.

