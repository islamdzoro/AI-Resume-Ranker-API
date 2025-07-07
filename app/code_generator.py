def generate_ranker_code():
    flask_code = '''@app.route('/rank-resumes', methods=['POST'])
def rank_resumes():
    resumes = request.files.getlist('resumes')
    job_description = request.form.get('job_description')

    # Placeholder logic — replace with your ranking algorithm
    ranked = [resume.filename for resume in resumes]
    return jsonify({
        "job_description": job_description,
        "ranked_resumes": ranked
    })'''

    html_code = '''<form method="POST" action="/rank-resumes" enctype="multipart/form-data">
  <label>Upload Resumes:</label><br>
  <input type="file" name="resumes" multiple required><br><br>

  <label>Paste Job Description:</label><br>
  <textarea name="job_description" rows="6" cols="50" required></textarea><br><br>

  <button type="submit">Rank Resumes</button>
</form>'''

    return flask_code, html_code
