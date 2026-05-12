"""
ATS Simulation Agent
Mimics ATS scoring behavior using rule-based keyword matching and structure checks.
"""

import re


class ATSSimulationAgent:

    STRUCTURE_SECTIONS = ["experience", "education", "skills", "summary", "objective", "certifications"]

    def score(self, parsed: dict) -> dict:
        """
        Scores the resume against the job description.
        Returns keyword score, structure score, overall ATS score,
        matched keywords, and missing keywords.
        """
        resume = parsed.get("resume_components", {})
        jd = parsed.get("jd_requirements", {})

        # ── Keyword scoring ───────────────────────────────────────────────────
        jd_keywords = [kw.lower().strip() for kw in jd.get("keywords", [])]
        required_skills = [s.lower().strip() for s in jd.get("required_skills", [])]
        all_target_keywords = list(set(jd_keywords + required_skills))

        resume_skills = [s.lower().strip() for s in resume.get("skills", [])]
        resume_text_blob = " ".join(resume_skills)

        # Also check inside experience bullets
        for exp in resume.get("experience", []):
            for bullet in exp.get("bullets", []):
                resume_text_blob += " " + bullet.lower()

        matched = []
        missing = []
        for kw in all_target_keywords:
            if kw in resume_text_blob:
                matched.append(kw)
            else:
                missing.append(kw)

        keyword_score = round((len(matched) / len(all_target_keywords)) * 100) if all_target_keywords else 0

        # ── Structure scoring ─────────────────────────────────────────────────
        # Check which standard sections are present in the parsed resume
        section_hits = 0
        if resume.get("skills"):
            section_hits += 1
        if resume.get("experience"):
            section_hits += 1
        if resume.get("education"):
            section_hits += 1
        if resume.get("summary"):
            section_hits += 1
        if resume.get("certifications"):
            section_hits += 1

        structure_score = round((section_hits / 5) * 100)

        # ── Overall ATS score ─────────────────────────────────────────────────
        overall_ats_score = round(keyword_score * 0.7 + structure_score * 0.3)

        return {
            "keyword_score": keyword_score,
            "structure_score": structure_score,
            "overall_ats_score": overall_ats_score,
            "matched_keywords": matched,
            "missing_keywords": missing
        }
