import streamlit as st
import difflib
from agents.parsing_agent import ParsingAgent
from agents.ats_simulation_agent import ATSSimulationAgent
from agents.semantic_matching_agent import SemanticMatchingAgent
from agents.optimization_agent import OptimizationAgent
from agents.interview_agent import InterviewAgent
from utils.feedback_loop import run_feedback_loop
from utils.pdf_reader import extract_text_from_pdf
from utils.pdf_exporter import export_resume_as_pdf


GROQ_API_KEY = "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"
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="ResumeReview-OPT",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }
.stApp { background: #080808; }

/* ── HERO ── */
.hero {
    background: #080808;
    padding: 90px 72px 80px;
    position: relative;
    overflow: hidden;
    border-bottom: 1px solid #161616;
}
.hero::before {
    content: '';
    position: absolute;
    top: -200px; right: -100px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(56,189,248,0.07) 0%, transparent 65%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -150px; left: 20%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(99,102,241,0.06) 0%, transparent 65%);
    pointer-events: none;
}
.eyebrow {
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 22px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(3rem, 5.5vw, 5rem);
    font-weight: 800;
    color: #ffffff;
    line-height: 1.03;
    letter-spacing: -0.03em;
    margin-bottom: 24px;
}
.hero-title em { color: #38bdf8; font-style: normal; }
.hero-desc {
    font-size: 1.05rem;
    color: #4a4a4a;
    max-width: 540px;
    line-height: 1.75;
    margin-bottom: 40px;
    font-weight: 300;
}
.tags { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 50px; }
.tag {
    background: #111;
    border: 1px solid #1e1e1e;
    color: #555;
    font-size: 0.75rem;
    padding: 5px 13px;
    border-radius: 100px;
}

/* ── FEATURES ── */
.features {
    background: #080808;
    padding: 80px 72px;
    border-bottom: 1px solid #111;
}
.feat-label {
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 14px;
}
.feat-heading {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 48px;
    letter-spacing: -0.02em;
}
.feat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 16px;
}
.feat-card {
    background: #0d0d0d;
    border: 1px solid #161616;
    border-radius: 14px;
    padding: 28px 22px;
    transition: border-color 0.2s, transform 0.2s;
}
.feat-card:hover { border-color: #38bdf8; transform: translateY(-2px); }
.feat-n {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #1a1a1a;
    margin-bottom: 14px;
}
.feat-t {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.92rem;
    color: #e0e0e0;
    margin-bottom: 8px;
}
.feat-d { font-size: 0.81rem; color: #3a3a3a; line-height: 1.65; }

/* ── TOOL PAGE ── */
.tool-page { background: #080808; min-height: 100vh; padding: 52px 72px 80px; }
.tool-heading {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.025em;
    margin-bottom: 4px;
}
.tool-sub { font-size: 0.88rem; color: #333; margin-bottom: 36px; }

/* ── Config bar ── */
.cfg {
    background: #0d0d0d;
    border: 1px solid #161616;
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 32px;
}
.cfg-label {
    font-size: 0.67rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #2a2a2a;
    margin-bottom: 6px;
}

/* ── Inputs ── */
.input-lbl {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    color: #ccc;
    margin-bottom: 10px;
}
.stTextArea textarea {
    background: #0d0d0d !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 12px !important;
    color: #ddd !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.87rem !important;
    padding: 14px !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus { border-color: #38bdf8 !important; outline: none !important; }
.stTextInput input {
    background: #0d0d0d !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 10px !important;
    color: #ddd !important;
    font-size: 0.88rem !important;
    padding: 10px 14px !important;
}
.stSelectbox > div > div {
    background: #0d0d0d !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 10px !important;
    color: #ddd !important;
}
.stRadio label {
    background: #0d0d0d !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 8px !important;
    color: #888 !important;
    padding: 6px 16px !important;
    font-size: 0.83rem !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #38bdf8 !important;
    color: #000 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px 28px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: #7dd3fc !important;
    transform: translateY(-1px) !important;
}
.stDownloadButton > button {
    background: #111 !important;
    color: #ddd !important;
    border: 1px solid #222 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 12px 22px !important;
    font-size: 0.88rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: #38bdf8 !important;
    color: #000 !important;
    border-color: #38bdf8 !important;
}

/* ── Divider ── */
.div { height: 1px; background: #111; margin: 36px 0; }

/* ── Step header ── */
.sh { display: flex; align-items: flex-start; gap: 14px; margin-bottom: 22px; margin-top: 36px; }
.sn {
    background: #38bdf8;
    color: #000;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 0.78rem;
    min-width: 30px; height: 30px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 2px;
}
.st-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.1rem; color: #e0e0e0; }
.st-desc { font-size: 0.8rem; color: #2d2d2d; margin-top: 2px; }

/* ── Score cards ── */
.score-row { display: flex; gap: 14px; margin: 18px 0; }
.score-card {
    flex: 1;
    background: #0d0d0d;
    border: 1px solid #161616;
    border-radius: 14px;
    padding: 26px 20px;
    text-align: center;
}
.sv {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 6px;
}
.sl { font-size: 0.72rem; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: #2a2a2a; }
.sc-hi { color: #4ade80; }
.sc-md { color: #fbbf24; }
.sc-lo { color: #f87171; }

/* ── Keywords ── */
.kw-wrap { display: flex; flex-wrap: wrap; gap: 7px; margin: 14px 0; }
.kw-hit { background: #052e16; border: 1px solid #14532d; color: #4ade80; font-size: 0.75rem; font-weight: 500; padding: 4px 11px; border-radius: 100px; }
.kw-miss { background: #2d0a0a; border: 1px solid #5b1a1a; color: #f87171; font-size: 0.75rem; font-weight: 500; padding: 4px 11px; border-radius: 100px; }

/* ── Breakdown ── */
.bk {
    background: #0d0d0d;
    border: 1px solid #161616;
    border-left: 3px solid #38bdf8;
    border-radius: 0 10px 10px 0;
    padding: 16px 18px;
    margin-bottom: 10px;
}
.bk-t { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.88rem; color: #ccc; margin-bottom: 5px; }
.bk-d { font-size: 0.82rem; color: #333; line-height: 1.65; }

/* ── Agent log ── */
.alog {
    background: #0a0a0a;
    border: 1px solid #141414;
    border-left: 3px solid #38bdf8;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-family: 'DM Sans', monospace;
    font-size: 0.8rem;
    color: #2a2a2a;
    margin: 5px 0;
}

/* ── Result banner ── */
.result-banner {
    background: #0d0d0d;
    border: 1px solid #161616;
    border-radius: 16px;
    padding: 32px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 20px 0 28px;
    gap: 20px;
}
.rn { font-family: 'Syne', sans-serif; font-size: 3.2rem; font-weight: 800; color: #fff; }
.rn.good { color: #4ade80; }
.rl { font-size: 0.72rem; color: #2a2a2a; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }
.rarrow { font-size: 1.8rem; color: #1a1a1a; }
.rbadge { background: #38bdf8; color: #000; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem; padding: 10px 22px; border-radius: 100px; }

/* ── Diff ── */
.diff-box {
    background: #0d0d0d;
    border: 1px solid #161616;
    border-radius: 12px;
    padding: 22px;
    font-family: 'DM Sans', monospace;
    font-size: 0.82rem;
    line-height: 1.9;
    color: #444;
    max-height: 500px;
    overflow-y: auto;
}
.da { background: #052e16; color: #4ade80; padding: 1px 4px; border-radius: 3px; }
.dr { background: #2d0a0a; color: #f87171; padding: 1px 4px; border-radius: 3px; text-decoration: line-through; }

/* ── Interview ── */
.iq-lbl { font-family: 'Syne', sans-serif; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #38bdf8; margin: 22px 0 8px; }
.iq { background: #0d0d0d; border: 1px solid #161616; border-radius: 10px; padding: 14px 16px; margin-bottom: 7px; font-size: 0.88rem; color: #aaa; line-height: 1.65; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 2px; border-bottom: 1px solid #141414; background: transparent; }
.stTabs [data-baseweb="tab"] { font-family: 'Syne', sans-serif !important; font-weight: 600 !important; font-size: 0.83rem !important; color: #2a2a2a !important; padding: 10px 20px !important; background: transparent !important; }
.stTabs [aria-selected="true"] { color: #e0e0e0 !important; border-bottom: 2px solid #38bdf8 !important; }

/* ── Expander ── */
.streamlit-expanderHeader { background: #0d0d0d !important; border: 1px solid #161616 !important; border-radius: 10px !important; color: #555 !important; font-size: 0.83rem !important; }

/* ── Slider ── */
.stSlider [data-testid="stSlider"] { color: #38bdf8; }

/* ── Caption ── */
.stCaption { color: #2a2a2a !important; font-size: 0.78rem !important; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "landing"

def sc(s):
    return "sc-hi" if s >= 70 else ("sc-md" if s >= 45 else "sc-lo")

def build_diff(orig, opt):
    ow, nw = orig.split(), opt.split()
    matcher = difflib.SequenceMatcher(None, ow, nw)
    out = []
    for op, a0, a1, b0, b1 in matcher.get_opcodes():
        if op == "equal":   out.append(" ".join(ow[a0:a1]))
        elif op == "insert": out.append(f'<span class="da">{" ".join(nw[b0:b1])}</span>')
        elif op == "delete": out.append(f'<span class="dr">{" ".join(ow[a0:a1])}</span>')
        elif op == "replace": out.append(f'<span class="dr">{" ".join(ow[a0:a1])}</span> <span class="da">{" ".join(nw[b0:b1])}</span>')
    return " ".join(out)

# ═════════════════════════════════════════════════════════════════════════════
# LANDING
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">✦ IEEE Conference Paper Project — MANS Warsaw</div>
        <div class="hero-title">Your resume,<br><em>finally optimized.</em></div>
        <div class="hero-desc">
            A pipeline of 5 specialized AI agents analyzes your resume against any job description
            and rewrites it to maximize ATS alignment — without fabricating anything.
        </div>
        <div class="tags">
            <span class="tag">🤖 Multi-Agent Pipeline</span>
            <span class="tag">🎯 ATS Simulation</span>
            <span class="tag">🧠 SBERT Semantic Matching</span>
            <span class="tag">🔄 Constraint Feedback Loop</span>
            <span class="tag">📄 PDF Export</span>
            <span class="tag">🎤 Interview Prep</span>
            <span class="tag">⚡ Powered by LLaMA 3.3</span>
        </div>
    </div>
    <div class="features">
        <div class="feat-label">✦ What it does</div>
        <div class="feat-heading">Eight features.<br>One pipeline.</div>
        <div class="feat-grid">
            <div class="feat-card"><div class="feat-n">01</div><div class="feat-t">Parse & Understand</div><div class="feat-d">Extracts skills, experience, and education from your resume and the job description using LLaMA 3.3 70B.</div></div>
            <div class="feat-card"><div class="feat-n">02</div><div class="feat-t">ATS Simulation</div><div class="feat-d">Scores your resume on keyword coverage and structure — exactly how real ATS systems evaluate candidates.</div></div>
            <div class="feat-card"><div class="feat-n">03</div><div class="feat-t">Semantic Matching</div><div class="feat-d">Uses SBERT embeddings to measure how semantically aligned your resume is with the job — beyond keywords.</div></div>
            <div class="feat-card"><div class="feat-n">04</div><div class="feat-t">Constrained Optimization</div><div class="feat-d">Rewrites your resume under strict factual constraints — no fabrication, only honest improvements.</div></div>
        </div>
        <div class="feat-grid">
            <div class="feat-card"><div class="feat-n">05</div><div class="feat-t">Industry Aware</div><div class="feat-d">Choose your target industry so agents prioritize the skills and keywords that matter most for your field.</div></div>
            <div class="feat-card"><div class="feat-n">06</div><div class="feat-t">Interview Prep</div><div class="feat-d">Predicts likely interview questions — technical, behavioral, situational, and industry-specific.</div></div>
            <div class="feat-card"><div class="feat-n">07</div><div class="feat-t">Side by Side + Diff</div><div class="feat-d">Compare your original and optimized resume, with every change highlighted in green and red.</div></div>
            <div class="feat-card"><div class="feat-n">08</div><div class="feat-t">PDF Export</div><div class="feat-d">Download your optimized resume as a clean formatted PDF ready to send to any employer.</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button("✦ Launch ResumeReview-OPT", use_container_width=True):
            st.session_state.page = "tool"
            st.rerun()

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TOOL PAGE
# ═════════════════════════════════════════════════════════════════════════════
else:
    st.markdown('<div class="tool-page">', unsafe_allow_html=True)

    cb, _ = st.columns([1, 8])
    with cb:
        if st.button("← Home"):
            st.session_state.page = "landing"
            st.rerun()

    st.markdown('<div class="tool-heading">ResumeReview-OPT</div>', unsafe_allow_html=True)
    st.markdown('<div class="tool-sub">Upload your resume, paste the job description, and let the agents do the work.</div>', unsafe_allow_html=True)

    # Config bar — no API key field, users never see it
    st.markdown('<div class="cfg">', unsafe_allow_html=True)
    cc1, cc2 = st.columns([2, 1])
    with cc1:
        st.markdown('<div class="cfg-label">Target Industry</div>', unsafe_allow_html=True)
        industry = st.selectbox("ind", [
            "Technology / Software", "Data Science / AI", "Finance / Banking",
            "Healthcare / Medical", "Marketing / Advertising", "Engineering",
            "Education / Academia", "Consulting / Management", "Legal", "Other"
        ], label_visibility="collapsed")
    with cc2:
        st.markdown('<div class="cfg-label">Optimization Passes</div>', unsafe_allow_html=True)
        max_iterations = st.slider("iters", 1, 5, 2, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # Inputs
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="input-lbl">📄 Your Resume</div>', unsafe_allow_html=True)
        resume_mode = st.radio("m", ["📎 Upload PDF", "✏️ Paste Text"], horizontal=True, label_visibility="collapsed")
        resume_text = ""
        if resume_mode == "📎 Upload PDF":
            up = st.file_uploader("f", type=["pdf"], label_visibility="collapsed")
            if up:
                with st.spinner("Reading PDF..."):
                    resume_text = extract_text_from_pdf(up)
                st.success(f"✅ Resume loaded — {len(resume_text):,} characters extracted")
                with st.expander("Preview extracted text"):
                    st.text(resume_text[:800] + ("..." if len(resume_text) > 800 else ""))
        else:
            resume_text = st.text_area("rt", height=280, placeholder="Paste your full resume here...", label_visibility="collapsed")

    with col2:
        st.markdown('<div class="input-lbl">💼 Job Description</div>', unsafe_allow_html=True)
        jd_text = st.text_area("jd", height=320, placeholder="Paste the full job description here...", label_visibility="collapsed")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    run_btn = st.button("✦ Run Optimization Pipeline", use_container_width=True)

    if run_btn:
        if GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE":
            st.error("Please open app.py and replace YOUR_GROQ_API_KEY_HERE with your actual Groq key.")
        elif not resume_text.strip():
            st.error("Please upload or paste your resume.")
        elif not jd_text.strip():
            st.error("Please paste the job description.")
        else:
            api_key = GROQ_API_KEY

            # STEP 1
            st.markdown('<div class="sh"><div class="sn">1</div><div><div class="st-title">Parsing Agent</div><div class="st-desc">Extracting structured data from your resume and job description</div></div></div>', unsafe_allow_html=True)
            parsing_agent = ParsingAgent(api_key)
            try:
                with st.spinner("Analyzing documents..."):
                    parsed = parsing_agent.parse(resume_text, jd_text)
                with st.expander("View parsed data"):
                    ca, cb2 = st.columns(2)
                    with ca:
                        st.caption("Resume Components")
                        st.json(parsed["resume_components"])
                    with cb2:
                        st.caption("JD Requirements")
                        st.json(parsed["jd_requirements"])
            except Exception as e:
                st.error(f"Parsing failed: {e}")
                st.stop()

            st.markdown('<div class="div"></div>', unsafe_allow_html=True)

            # STEP 2
            st.markdown('<div class="sh"><div class="sn">2</div><div><div class="st-title">ATS Simulation Agent</div><div class="st-desc">Scoring your resume against ATS criteria</div></div></div>', unsafe_allow_html=True)
            ats_agent = ATSSimulationAgent()
            ats_result = ats_agent.score(parsed)
            kw, ss, ov = ats_result["keyword_score"], ats_result["structure_score"], ats_result["overall_ats_score"]

            st.markdown(f"""
            <div class="score-row">
                <div class="score-card"><div class="sv {sc(kw)}">{kw}%</div><div class="sl">Keyword Coverage</div></div>
                <div class="score-card"><div class="sv {sc(ss)}">{ss}%</div><div class="sl">Structure Score</div></div>
                <div class="score-card"><div class="sv {sc(ov)}">{ov}%</div><div class="sl">Overall ATS Score</div></div>
            </div>""", unsafe_allow_html=True)

            with st.expander("Why did I get these scores?"):
                st.markdown(f"""
                <div class="bk"><div class="bk-t">🔑 Keyword Coverage — {kw}%</div><div class="bk-d">{"Your resume covers most keywords from the job description." if kw>=75 else "Several important keywords are missing — the optimizer will integrate them naturally." if kw>=40 else "Most keywords are missing. Significant optimization is needed."}</div></div>
                <div class="bk"><div class="bk-t">🏗 Structure Score — {ss}%</div><div class="bk-d">Based on detected sections: Skills, Experience, Education, Summary, Certifications. {"All major sections found — great structure." if ss>=80 else "Some sections are missing or not clearly labeled."}</div></div>
                <div class="bk"><div class="bk-t">🎯 Overall ATS Score — {ov}%</div><div class="bk-d">Weighted: 70% keywords + 30% structure. {"Strong — should pass most ATS filters." if ov>=70 else "Moderate — optimization will help." if ov>=45 else "Low — your resume may be filtered before a human sees it."}</div></div>
                """, unsafe_allow_html=True)

            kw_html = '<div class="kw-wrap">'
            for k in ats_result["matched_keywords"]: kw_html += f'<span class="kw-hit">✓ {k}</span>'
            for k in ats_result["missing_keywords"]:  kw_html += f'<span class="kw-miss">✗ {k}</span>'
            st.markdown(kw_html + '</div>', unsafe_allow_html=True)

            st.markdown('<div class="div"></div>', unsafe_allow_html=True)

            # STEP 3
            st.markdown('<div class="sh"><div class="sn">3</div><div><div class="st-title">Semantic Matching Agent</div><div class="st-desc">Measuring meaning-level alignment using SBERT</div></div></div>', unsafe_allow_html=True)
            semantic_agent = SemanticMatchingAgent()
            with st.spinner("Computing semantic similarity..."):
                semantic_result = semantic_agent.match(resume_text, jd_text)
            sem_pct = int(semantic_result["cosine_similarity"] * 100)

            st.markdown(f"""
            <div class="score-row">
                <div class="score-card"><div class="sv {sc(sem_pct)}">{sem_pct}%</div><div class="sl">Semantic Similarity</div></div>
                <div class="score-card"><div class="sv" style="font-size:1.5rem;padding-top:10px">{semantic_result["alignment_level"]}</div><div class="sl">Alignment Level</div></div>
            </div>""", unsafe_allow_html=True)

            st.markdown('<div class="div"></div>', unsafe_allow_html=True)

            # STEPS 4–5
            st.markdown('<div class="sh"><div class="sn">4–5</div><div><div class="st-title">Optimization + Feedback Loop</div><div class="st-desc">Iteratively rewriting your resume under factual constraints</div></div></div>', unsafe_allow_html=True)
            opt_agent = OptimizationAgent(api_key)
            pb = st.progress(0)
            log_slot = st.empty()
            best_resume = resume_text
            best_score = ov
            parsed["ats_result"] = ats_result

            for i in range(max_iterations):
                log_slot.markdown(f'<div class="alog">⟳ Pass {i+1} of {max_iterations} — rewriting and re-scoring...</div>', unsafe_allow_html=True)
                result = run_feedback_loop(opt_agent, ats_agent, semantic_agent, best_resume, jd_text, parsed, i)
                best_resume = result["optimized_resume"]
                best_score = result["ats_score"]
                parsed["ats_result"]["missing_keywords"] = result["missing_keywords"]
                pb.progress((i + 1) / max_iterations)

            log_slot.markdown(f'<div class="alog">✓ Complete — {max_iterations} pass{"es" if max_iterations > 1 else ""} done</div>', unsafe_allow_html=True)

            st.markdown('<div class="div"></div>', unsafe_allow_html=True)

            # RESULTS
            st.markdown('<div class="sh"><div class="sn">✓</div><div><div class="st-title">Results</div><div class="st-desc">Your optimized resume is ready</div></div></div>', unsafe_allow_html=True)

            improvement = best_score - ov
            badge = f"+{improvement} pts 🎉" if improvement > 0 else ("No change" if improvement == 0 else f"{improvement} pts")

            st.markdown(f"""
            <div class="result-banner">
                <div><div class="rn">{ov}%</div><div class="rl">Original Score</div></div>
                <div class="rarrow">→</div>
                <div><div class="rn good">{best_score}%</div><div class="rl">Optimized Score</div></div>
                <div class="rbadge">{badge}</div>
            </div>""", unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["📄 Side by Side", "🔍 What Changed", "🎤 Interview Questions"])

            with tab1:
                co, cop = st.columns(2, gap="large")
                with co:
                    st.caption("Original")
                    st.text_area("o", value=resume_text, height=480, label_visibility="collapsed")
                with cop:
                    st.caption("Optimized")
                    st.text_area("op", value=best_resume, height=480, label_visibility="collapsed")

            with tab2:
                st.markdown('<div style="font-size:0.8rem;color:#2a2a2a;margin-bottom:12px">🟢 Green = added &nbsp;&nbsp; 🔴 Red = removed</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="diff-box">{build_diff(resume_text, best_resume)}</div>', unsafe_allow_html=True)

            with tab3:
                st.markdown(f'<div style="font-size:0.82rem;color:#2a2a2a;margin-bottom:4px">Industry: <span style="color:#38bdf8">{industry}</span></div>', unsafe_allow_html=True)
                with st.spinner("Generating interview questions..."):
                    try:
                        qs = InterviewAgent(api_key).generate(best_resume, jd_text, industry)
                        for cat, lbl in [("technical","🔧 Technical"),("behavioral","🧠 Behavioral"),("situational","💡 Situational"),("industry_specific",f"🏭 {industry}")]:
                            st.markdown(f'<div class="iq-lbl">{lbl}</div>', unsafe_allow_html=True)
                            for q in qs.get(cat, []):
                                st.markdown(f'<div class="iq">{q}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Interview generator failed: {e}")

            st.markdown('<div class="div"></div>', unsafe_allow_html=True)
            st.markdown('<div style="font-family:Syne,sans-serif;font-weight:700;font-size:0.95rem;color:#ccc;margin-bottom:14px">Download your optimized resume</div>', unsafe_allow_html=True)
            dl1, dl2 = st.columns(2)
            with dl1:
                st.download_button("⬇ Download as TXT", data=best_resume, file_name="optimized_resume.txt", mime="text/plain", use_container_width=True)
            with dl2:
                try:
                    pdf_bytes = export_resume_as_pdf(best_resume)
                    st.download_button("📄 Download as PDF", data=pdf_bytes, file_name="optimized_resume.pdf", mime="application/pdf", use_container_width=True)
                except Exception as e:
                    st.warning(f"PDF export error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
