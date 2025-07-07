import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(file_storage):
    with fitz.open(stream=file_storage.read(), filetype="pdf") as doc:
        return " ".join([page.get_text() for page in doc])

def rank_resumes_by_similarity(resume_files, job_description):
    resume_texts = [extract_text_from_pdf(f) for f in resume_files]
    documents = [job_description] + resume_texts

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    job_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(job_vector, resume_vectors).flatten()
    ranked = sorted(zip(resume_files, similarities), key=lambda x: x[1], reverse=True)

    return [
        {"filename": file.filename, "score": round(score, 4)}
        for file, score in ranked
    ]


# utils/auth.py
from functools import wraps
from flask import request, jsonify
from .models import User  # adjust import to your structure

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid Authorization header."}), 401

        token = auth_header.split("Bearer ")[1].strip()

        user = User.query.filter_by(api_key=token).first()
        if not user:
            return jsonify({"error": "Invalid or revoked API key."}), 403

        request.user = user  # attach user to request for downstream use
        return f(*args, **kwargs)
    return decorated_function
