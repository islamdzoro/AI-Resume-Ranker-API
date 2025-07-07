# utils/ranker.py
from sentence_transformers import SentenceTransformer, util
from .utils import extract_text_from_pdf

model = SentenceTransformer('all-MiniLM-L6-v2')  # You can load this once globally

def rank_resumes_by_semantic_similarity(resume_files, job_description):
    resume_texts = [extract_text_from_pdf(f) for f in resume_files]
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    results = []
    for file, resume_text in zip(resume_files, resume_texts):
        resume_embedding = model.encode(resume_text, convert_to_tensor=True)
        similarity = util.cos_sim(job_embedding, resume_embedding).item()
        results.append({
            "filename": file.filename,
            "score": round(similarity, 4)
        })

    results.sort(key=lambda x: x['score'], reverse=True)
    return results
