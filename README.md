# ResumeReview-OPT

A Constrained Multi-Agent Optimization Framework for ATS-Aware Resume Alignment.
Powered by **Groq (LLaMA 3 70B)** + **SBERT** — completely free to run.

## Setup

### 1. Get a free Groq API key
- Go to https://console.groq.com
- Sign up and go to API Keys → Create API Key
- Copy the key (starts with `gsk_`)

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Open in browser
Go to **http://localhost:8501**

Paste your Groq API key in the sidebar, then paste your resume and job description and click **Run Optimization Pipeline**.

---

## Project Structure

```
ResumeReview-OPT/
├── app.py                          # Main Streamlit UI
├── requirements.txt                # Python dependencies
├── agents/
│   ├── parsing_agent.py            # LLaMA 3 parses resume + JD into JSON
│   ├── ats_simulation_agent.py     # Rule-based ATS keyword + structure scoring
│   ├── semantic_matching_agent.py  # SBERT cosine similarity (all-MiniLM-L6-v2)
│   └── optimization_agent.py      # LLaMA 3 resume optimizer with constraints
└── utils/
    └── feedback_loop.py            # Iterative optimization orchestrator
```

## Pipeline Steps

1. **Parsing Agent** — Extracts structured data from resume and JD using LLaMA 3
2. **ATS Simulation Agent** — Scores keyword coverage and resume structure (no API needed)
3. **Semantic Matching Agent** — Cosine similarity via SBERT (runs locally)
4. **Optimization Agent** — Rewrites resume under strict factual constraints using LLaMA 3
5. **Constraint Feedback Loop** — Iterates steps 2–4 to progressively improve alignment
