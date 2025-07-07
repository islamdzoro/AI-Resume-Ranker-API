# 🧠 AI Resume Ranker API

An intelligent, production-ready Resume Ranking API for developers, recruiters, and HR tech platforms.  
Inspired by Stripe & Paystack API experiences — complete with authentication, dashboard, and live testing interface.

Built with **Flask + Sentence Transformers + PDF Parsing + Semantic AI**, this API helps you automatically score and rank resumes against any job description using powerful language understanding models.

---

## 🚀 Features

- ✅ **API Key Authentication** with secure Bearer token format
- 🧾 **Semantic Resume Ranking** using transformer embeddings (not just keyword matching)
- 📤 Supports **batch PDF uploads**
- 📬 **JSON API responses** with ranked relevance scores
- 🧪 **Live Testing Interface** on the dashboard
- 🔐 **Secure User System** with login, signup, hashed passwords
- 🔁 **API Key Regeneration** from the dashboard
- 📚 Beautiful **API Documentation Page** with copyable code samples
- 🧰 **Try It Now**: Upload resumes + job text and see live scoring
- 📈 Ready for usage tracking, analytics, or rate limiting
- 💼 Built for scaling into a full SaaS product

---

## 🌐 Live Demo

> Coming soon: hosted on Render or Railway (e.g., [https://resume-ranker.example.com](https://resume-ranker.example.com))

---

## 📦 API Overview

### 🔗 Endpoint

```

POST /api/rank-resumes

```

### 🔐 Authentication

Send your API key in the request header:

```

Authorization: Bearer amn=your\_api\_key\_here

````

### 📤 Request Parameters

| Name            | Type             | Required | Description                          |
|-----------------|------------------|----------|--------------------------------------|
| resumes         | `file[] (PDF)`   | ✅ Yes   | One or more PDF resumes              |
| job_description | `string`         | ✅ Yes   | Job description text to compare with |

---

## 📥 Example Usage

### 🧪 Try It via cURL

```bash
curl -X POST https://yourdomain.com/api/rank-resumes \
  -H "Authorization: Bearer amn=sk_live_abc123xyz" \
  -F "resumes=@resume1.pdf" \
  -F "resumes=@resume2.pdf" \
  -F "job_description=We are hiring a backend Django developer..."
````

### 📦 Sample Response

```json
{
  "results": [
    {
      "filename": "resume1.pdf",
      "score": 0.8745
    },
    {
      "filename": "resume2.pdf",
      "score": 0.6721
    }
  ],
  "count": 2,
  "requested_by": "user@example.com"
}
```

---

## 🛠 Tech Stack

* **Backend:** Flask, Blueprints, Jinja2
* **AI:** SentenceTransformers (`all-MiniLM-L6-v2`)
* **PDF Parsing:** PyMuPDF
* **Auth:** Flask sessions + hashed passwords
* **Database:** SQLite (dev) / PostgreSQL-ready
* **Frontend:** Bootstrap 5 + custom Jinja templates
* **Hosting:** Render / Railway / PythonAnywhere
* **Docs UI:** Fully embedded HTML + live form

---

## 🧪 Try It Now (via Dashboard)

* Register/Login
* View and copy your API Key
* Paste a job description
* Upload 1–5 resumes (PDF)
* Get AI-scored ranking results instantly

---

## 🧑‍💻 Developer Setup

```bash
git clone https://github.com/yourusername/resume-ranker-api.git
cd resume-ranker-api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
flask run
```

Perfect — thanks for the clarification.

You're right to **remove the real email password** before pushing to GitHub — sensitive credentials should never be committed. Instead, include **placeholder values** in the `.env` section of your `README.md`.

---

## ✅ Updated `.env` Example for README

Here's the correct `.env` block to include in the `README.md`:

```ini
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///db.sqlite3

# ✅ Email credentials for verification system
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password_here
```

> 📌 **Note:** Use an **App Password** (not your actual Gmail password) if you're using Gmail SMTP. App passwords are safer and Gmail-compliant.

---

## 🔒 Additional Security Tip

To prevent accidental exposure:

* Add `.env` to your `.gitignore`
* Use environment variables in production (Render, Railway, Fly.io all support this)

**`.gitignore` entry:**

.env
```

---

## ✅ Bonus (Optional): Mention in README

You can also add a small note under **Developer Setup** in your README:

> 📧 **Note:** To enable email verification links, set `EMAIL_USER` and `EMAIL_PASS` in your `.env`. We recommend using an App Password with Gmail or a transactional email provider like Mailgun or SendGrid.


## 💡 Future Features

* ✅ API usage tracking
* ⏳ Rate limiting (per API key)
* 📊 Dashboard analytics
* 🧠 Resume summarization API
* 📁 CSV/JSON result export
* 🧩 SDKs for Python & JS

---

## 🤝 Contributing

Pull requests are welcome! Let's build the future of AI recruiting tools together.

---

## 📜 License

MIT License

---

## 📬 Contact

Made with ❤️ by [Muhammad Aminu Umar](mailto:webcodelabb@gmail.com)
🔗 [LinkedIn](https://linkedin.com/in/webcodelab) | [GitHub](https://github.com/webcodelabb)

