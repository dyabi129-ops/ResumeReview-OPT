"""
Parsing Agent
Extracts structured components from resume and job description using Groq (LLaMA 3).
"""

import json
from groq import Groq


class ParsingAgent:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def _chat(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()

    def parse(self, resume_text: str, jd_text: str) -> dict:
        resume_prompt = f"""
Extract structured information from the resume below.
Return ONLY valid JSON with these exact keys:
- skills (list of strings)
- experience (list of dicts with: title, company, duration, bullets as list of strings)
- education (list of dicts with: degree, institution, year)
- certifications (list of strings)
- summary (string or null)

Return ONLY the JSON object, no explanation, no markdown, no backticks.

Resume:
{resume_text}
"""

        jd_prompt = f"""
Extract structured requirements from the job description below.
Return ONLY valid JSON with these exact keys:
- required_skills (list of strings)
- preferred_skills (list of strings)
- responsibilities (list of strings)
- required_experience_years (int or null)
- education_requirement (string or null)
- keywords (list of important ATS keywords as strings)

Return ONLY the JSON object, no explanation, no markdown, no backticks.

Job Description:
{jd_text}
"""

        resume_raw = self._chat(resume_prompt)
        jd_raw = self._chat(jd_prompt)

        # Strip markdown code fences if model adds them anyway
        def clean_json(s):
            s = s.strip()
            if s.startswith("```"):
                s = s.split("```")[1]
                if s.startswith("json"):
                    s = s[4:]
            return s.strip()

        resume_components = json.loads(clean_json(resume_raw))
        jd_requirements = json.loads(clean_json(jd_raw))

        return {
            "resume_components": resume_components,
            "jd_requirements": jd_requirements
        }
