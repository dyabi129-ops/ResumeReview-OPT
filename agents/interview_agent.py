"""
Interview Question Generator Agent
Predicts likely interview questions based on the job description and resume.
"""

from groq import Groq
import json


class InterviewAgent:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def generate(self, resume_text: str, jd_text: str, industry: str) -> dict:
        prompt = f"""
You are an expert interview coach specializing in the {industry} industry.
Based on the job description and resume below, generate likely interview questions.

Return ONLY valid JSON with these exact keys:
- technical (list of 4 technical/skill-based questions for this role)
- behavioral (list of 4 behavioral questions starting with "Tell me about a time...")
- situational (list of 3 situational questions starting with "What would you do if...")
- industry_specific (list of 3 questions specific to the {industry} industry)

Each question should be a string. No numbering. No explanation. Only JSON.

Job Description:
{jd_text}

Resume:
{resume_text}
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
