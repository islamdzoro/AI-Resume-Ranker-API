# routes/api.py
from flask import Blueprint, request, jsonify
from ..ranker import rank_resumes_by_semantic_similarity  # <-- updated import
from ..decorators import require_api_key

api = Blueprint('api', __name__)

@api.route('/api/rank-resumes', methods=['POST'])
@require_api_key
def rank_resumes():
    job_description = request.form.get('job_description')
    resume_files = request.files.getlist('resumes')

    if not job_description or not resume_files:
        return jsonify({'error': 'Missing job description or resumes'}), 400

    try:
        results = rank_resumes_by_semantic_similarity(resume_files, job_description)
        return jsonify({
            'results': results,
            'count': len(results),
            'requested_by': request.user.email
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
