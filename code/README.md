# LegalEase — AI-Powered Legal Document Generator

FastAPI + Streamlit + Gemini application for generating editable legal-document drafts and exporting them as TXT, DOCX and PDF.

## Structure

```text
LegalEase/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   └── routes.py
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── document_utils/
│   ├── __init__.py
│   └── exporters.py
├── frontend/
│   ├── __init__.py
│   └── app.py
├── assets/
│   └── README.txt
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows setup

```powershell
cd LegalEase
py -3.11 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and add your Gemini API key.

## Backend

```powershell
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs

## Frontend

Open a second terminal:

```powershell
cd LegalEase
.\.venv\Scripts\activate
streamlit run frontend/app.py
```

Open http://localhost:8501

## Demo mode

To test the complete UI without Gemini:

```env
DEMO_MODE=true
```

Restart the backend after changing `.env`.

## Safety

LegalEase creates AI-generated drafts, not legal advice. Review documents with a qualified legal professional before signing or relying on them. Never commit `.env` to Git.
