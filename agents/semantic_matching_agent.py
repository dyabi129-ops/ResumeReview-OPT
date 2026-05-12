"""
Semantic Matching Agent
Computes semantic similarity between resume and job description using SBERT embeddings.
"""

from sentence_transformers import SentenceTransformer, util


class SemanticMatchingAgent:
    def __init__(self):
        # all-MiniLM-L6-v2 is lightweight, fast, and strong for sentence similarity
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def match(self, resume_text: str, jd_text: str) -> dict:
        """
        Computes cosine similarity between resume and job description embeddings.
        Returns similarity score and alignment level label.
        """
        resume_embedding = self.model.encode(resume_text, convert_to_tensor=True)
        jd_embedding = self.model.encode(jd_text, convert_to_tensor=True)

        cosine_sim = float(util.cos_sim(resume_embedding, jd_embedding)[0][0])
        cosine_sim = round(cosine_sim, 4)

        # Alignment level label
        if cosine_sim >= 0.75:
            alignment_level = "High ✅"
        elif cosine_sim >= 0.50:
            alignment_level = "Medium ⚠️"
        else:
            alignment_level = "Low ❌"

        return {
            "cosine_similarity": cosine_sim,
            "alignment_level": alignment_level
        }
