from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, jsonify
from .models import User
from . import db
from .email_utils import send_verification_email
from .code_generator import generate_ranker_code
from .utils import rank_resumes_by_similarity
import requests 
from werkzeug.utils import secure_filename
from .ranker import rank_resumes_by_semantic_similarity

auth = Blueprint('auth', __name__)

@auth.route('/rank-resumes', methods=['POST'])
def rank_resumes():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    api_key = auth_header.split(" ")[1]
    user = User.query.filter_by(api_key=api_key).first()
    if not user:
        return jsonify({"error": "Invalid API key"}), 403

    resumes = request.files.getlist('resumes')
    job_description = request.form.get('job_description')

    if not resumes or not job_description:
        return jsonify({"error": "Missing resumes or job description"}), 400

    ranked = rank_resumes_by_semantic_similarity(resumes, job_description)

    return jsonify({
        "job_description": job_description,
        "ranked_resumes": ranked
    })



@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.generate_verification_token()
        db.session.add(new_user)
        db.session.commit()

        #  Send verification email
        if send_verification_email(email, username, new_user.verification_token):
            flash('Registration successful! Please check your email to verify your account.')
        else:
            flash('Registration succeeded, but failed to send verification email.')
            new_user.generate_api_key()
            db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if not user.is_verified:
                flash('Please verify your email before logging in.')
                return redirect(url_for('auth.login'))

            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully.')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/resend-verification', methods=['GET', 'POST'])
def resend_verification():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            if user.is_verified:
                flash('Your email is already verified. You can log in.')
                return redirect(url_for('auth.login'))

            user.generate_verification_token()
            db.session.commit()
            if send_verification_email(user.email, user.username, user.verification_token):
                flash('Verification email resent. Please check your inbox.')
            else:
                flash('Failed to send verification email. Try again later.')
        else:
            flash('No account found with that email.')

        return redirect(url_for('auth.login'))

    return render_template('resend_verification.html')


@auth.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@auth.route('/generate-api', methods=['GET', 'POST'])
def generate_api():
    if 'user_id' not in session:
        flash('Please log in to access the API generator.')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        flask_code, html_code = generate_ranker_code()
        return render_template('generated_code.html', flask_code=flask_code, html_code=html_code)

    return render_template('generate_api.html')

@auth.route('/regenerate-api-key', methods=['POST'])
def regenerate_api_key():
    if 'user_id' not in session:
        flash('Please log in.')
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    user.generate_api_key()
    db.session.commit()
    flash('API key regenerated.')
    return redirect(url_for('auth.dashboard'))

@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

@auth.route('/verify/<token>')
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()
    if user:
        user.is_verified = True
        user.verification_token = None
        db.session.commit()
        flash('Email verified! You can now log in.')
        return redirect(url_for('auth.login'))
    else:
        flash('Invalid or expired verification link.')
        return redirect(url_for('auth.register'))

@auth.route('/docs')
def docs():
    return render_template('docs.html', response=None)

# Inside your auth.py or views.py

from flask import request, render_template, redirect, url_for, flash
from .models import User
from .utils import rank_resumes_by_similarity  # import your real function

@auth.route('/try-api', methods=['POST'])
def try_api():
    api_key = request.form.get('api_key')
    resumes = request.files.getlist('resumes')
    job_description = request.form.get('job_description')

    if not api_key or not resumes or not job_description:
        flash("All fields are required.")
        return redirect(url_for('auth.docs'))

    user = User.query.filter_by(api_key=api_key).first()
    if not user:
        return render_template('docs.html', response=" Invalid API key.")

    try:
        # ✅ Use the actual ranking logic
        results = rank_resumes_by_semantic_similarity(resumes, job_description)

        return render_template(
            'docs.html',
            response=results,
            job_description=job_description
        )
    except Exception as e:
        return render_template('docs.html', response=f" Error: {str(e)}")
