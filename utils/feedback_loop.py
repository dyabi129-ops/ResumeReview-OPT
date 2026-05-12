"""
Constraint Feedback Loop
Orchestrates iterative optimization between agents.
"""

from agents.optimization_agent import OptimizationAgent
from agents.ats_simulation_agent import ATSSimulationAgent
from agents.semantic_matching_agent import SemanticMatchingAgent


def run_feedback_loop(
    opt_agent: OptimizationAgent,
    ats_agent: ATSSimulationAgent,
    semantic_agent: SemanticMatchingAgent,
    resume_text: str,
    jd_text: str,
    parsed: dict,
    iteration: int
) -> dict:
    """
    Single iteration of the constraint feedback loop:
    1. Optimize resume
    2. Re-score with ATS agent
    3. Re-score with semantic agent
    4. Return results
    """
    missing_keywords = parsed.get("ats_result", {}).get("missing_keywords", [])

    # Step 4 — Optimization Agent
    optimized_resume = opt_agent.optimize(
        resume_text=resume_text,
        jd_text=jd_text,
        missing_keywords=missing_keywords,
        iteration=iteration
    )

    # Re-parse with simple skill extraction for re-scoring
    # We rebuild a lightweight parsed dict for re-scoring
    re_parsed = {
        "resume_components": {
            "skills": _extract_skills_simple(optimized_resume),
            "experience": parsed["resume_components"].get("experience", []),
            "education": parsed["resume_components"].get("education", []),
            "summary": parsed["resume_components"].get("summary", ""),
            "certifications": parsed["resume_components"].get("certifications", [])
        },
        "jd_requirements": parsed["jd_requirements"]
    }

    # Step 5 — Re-score ATS
    ats_result = ats_agent.score(re_parsed)

    # Re-score Semantic
    semantic_result = semantic_agent.match(optimized_resume, jd_text)

    return {
        "optimized_resume": optimized_resume,
        "ats_score": ats_result["overall_ats_score"],
        "keyword_score": ats_result["keyword_score"],
        "semantic_similarity": semantic_result["cosine_similarity"],
        "missing_keywords": ats_result["missing_keywords"]
    }


def _extract_skills_simple(text: str) -> list:
    """Lightweight skill extractor for re-scoring without API call."""
    # Returns lines that look like skill entries
    lines = text.split("\n")
    skills = []
    in_skills = False
    for line in lines:
        line = line.strip()
        if "skill" in line.lower():
            in_skills = True
            continue
        if in_skills and line and not line.endswith(":"):
            skills.extend([s.strip() for s in line.replace(",", "|").replace("/", "|").split("|")])
        if in_skills and line == "":
            in_skills = False
    return [s for s in skills if s]
