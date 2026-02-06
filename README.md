# SourceTrace

SourceTrace is an OSINT-based fact-checking platform that traces the origin of news claims.

## Tech Stack
- **Frontend**: Next.js (App Router), TailwindCSS, Framer Motion
- **Backend**: FastAPI, SQLAlchemy, SQLite/PostgreSQL
- **Search**: DuckDuckGo (via `ddgs`)

## How to Run (Local)

### Backend
1. Go to `backend/`:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m uvicorn main:app --reload
   ```
   API: [http://localhost:8000](http://localhost:8000)

### Frontend
1. Go to `frontend/`:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   App: [http://localhost:3000](http://localhost:3000)

## Features
- **Claim Analysis**: Enter any headline to search.
- **Source Discovery**: Finds related sources across the web.
- **Credibility Scoring**: Generates a confidence score.
- **Timeline View**: Visualizes when sources appeared.
