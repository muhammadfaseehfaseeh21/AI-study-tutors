# 📚 AI Study Tutor

A Streamlit app powered by Groq (`openai/gpt-oss-120b`) that helps you study smarter.

## Features
- **Explain a Concept** – get any topic explained at your level
- **Quiz Me** – auto-generated multiple-choice quizzes with an answer key
- **Flashcards** – quick front/back flashcards for any topic
- **Study Plan** – a day-by-day plan based on your deadline and free hours
- **Ask a Doubt** – free-form chat with the tutor

## File structure
```
ai-study-tutor/
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml.example
```

## Deploy on Streamlit Cloud (recommended — no local setup needed)
1. Create a new GitHub repo and upload these files (`app.py`, `requirements.txt`, `README.md`).
2. Do **not** upload a real `secrets.toml` — that file is only an example.
3. Go to [share.streamlit.io](https://share.streamlit.io), sign in, and click **New app**.
4. Pick your repo, branch, and set the main file to `app.py`.
5. Before deploying (or after, in **Settings → Secrets**), add:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
6. Get a free Groq API key at [console.groq.com/keys](https://console.groq.com/keys) if you don't have one.
7. Click **Deploy**. Your app will be live at a public `streamlit.app` URL.

## Running locally (optional)
```bash
pip install -r requirements.txt
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml and paste your real Groq API key
streamlit run app.py
```
