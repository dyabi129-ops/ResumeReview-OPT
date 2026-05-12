"""
Optimization Agent
Generates an improved resume version using Groq (LLaMA 3) under factual constraints.
"""

from groq import Groq


class OptimizationAgent:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def optimize(self, resume_text: str, jd_text: str, missing_keywords: list, iteration: int) -> str:
        missing_kw_str = ", ".join(missing_keywords) if missing_keywords else "None"

        prompt = f"""
You are an expert resume coach and ATS optimization specialist.
Your task is to improve the resume below so it better matches the job description.

STRICT CONSTRAINTS (follow all of these without exception):
1. Do NOT invent or fabricate any experience, skills, or achievements.
2. Only rephrase, reorder, or reframe existing content.
3. Naturally integrate the missing keywords below only where they genuinely fit.
4. Preserve all factual information: company names, dates, job titles, education.
5. Keep the resume professional, readable, and human-sounding.
6. Do NOT add any section that does not exist in the original resume.

This is optimization iteration {iteration + 1}. Make meaningful but honest improvements.

Missing Keywords to integrate (only if they genuinely apply):
{missing_kw_str}

Job Description:
{jd_text}

Original Resume:
{resume_text}

Return ONLY the improved resume text. No explanation, no commentary, no markdown.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return response.choices[0].message.content.strip()
