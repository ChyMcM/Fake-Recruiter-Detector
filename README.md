🔎 Fake Recruiter Detector

Fake Recruiter Detector is a full-stack web application designed to help job seekers evaluate the legitimacy of recruiter messages. With the rise of hiring scams across email and social platforms, this tool provides an explainable scam risk score based on linguistic patterns and common fraud indicators.

Rather than functioning as a black-box classifier, the system emphasizes transparency by clearly showing which phrases triggered risk flags and why.

🚀 Features

📋 Paste recruiter message for analysis

📊 Scam probability score (0–100)

⚠️ Risk classification (Low / Medium / High)

🔎 Highlighted suspicious phrases

🧠 Weighted rule-based NLP detection engine

⚡ FastAPI REST backend

💻 React frontend with async API integration

🏗 Architecture Overview

The system is built using a modular full-stack design:

Frontend

React (Vite)

Component-based UI

Asynchronous API calls

Loading + error state handling

Backend

Python FastAPI

RESTful /analyze endpoint

CORS enabled

Modular scoring engine

JSON request/response format

Core Flow

User submits recruiter message.

Backend processes text using weighted rule engine.

System assigns risk score.

Flags and highlighted phrases are returned.

Frontend renders risk summary and flagged content.

🧠 Detection Logic (MVP)

The initial version uses a rule-based scoring system that detects:

Unrealistic compensation claims

Requests for gift cards or cryptocurrency

Off-platform communication (Telegram, WhatsApp, Signal)

Premature requests for sensitive data

Generic greetings or vague job descriptions

Each rule carries a weighted value contributing to the final risk score.

Future versions may integrate machine learning (TF-IDF + logistic regression) for hybrid scoring.

🤖 Optional OpenAI-Assisted Screening

The backend supports optional OpenAI analysis to improve scam detection quality on nuanced messages.

- Rule-based scoring always runs.
- If `OPENAI_API_KEY` is set, the API also runs an OpenAI pass and blends scores:
  - Final score = 70% rule score + 30% AI score
- Response includes:
  - `ai_used` (boolean)
  - `ai_score` (0-100, optional)
  - `ai_summary` (optional short rationale)

Environment variables (backend):

- `OPENAI_API_KEY` = your OpenAI API key
- `OPENAI_MODEL` = model name (default: `gpt-4.1-mini`)

🛠 Tech Stack

Backend:

Python

FastAPI

Regex pattern matching

Frontend:

React

Vite

Fetch API

Dev Tools:

Git

Jira (Agile backlog management)

Docker (planned)

🐳 Docker Compose (Local)

You can run the full app (frontend + backend) with Docker Compose.

From `fake-recruiter-detector`:

```bash
docker compose up --build
```

Open:

- Frontend: `http://localhost:8080`
- Backend health: `http://localhost:8000/`

Optional OpenAI in Docker:

- Set `OPENAI_API_KEY` in your shell before running compose.
- Compose passes `OPENAI_API_KEY` and `OPENAI_MODEL` to the backend container.

Stop:

```bash
docker compose down
```

📦 Installation
Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
Frontend
cd frontend
npm install
npm run dev

Frontend runs on localhost:5173
Backend runs on localhost:8000

📡 API Endpoint
POST /analyze

Request:

{
  "text": "We are hiring immediately! Please contact via Telegram."
}

Response:

{
  "score": 75,
  "level": "High",
  "flags": ["Off-platform communication detected"],
  "highlights": [{"phrase": "Telegram"}]
}

POST /analyze/confidence

Request:

{
  "text": "We are hiring immediately! Please contact via Telegram."
}

Response:

{
  "score": 75,
  "level": "High",
  "confidence_score": 82,
  "confidence_level": "High",
  "explanation": "Confidence is high because multiple consistent signals support this risk level.",
  "factors": [
    "Detected suspicious phrases: hiring immediately, telegram",
    "Triggered 2 risk flags",
    "AI cross-check score: 78/100",
    "Blended final score: 70% rules + 30% AI = 75/100"
  ],
  "ai_used": true,
  "ai_score": 78
}
🧪 Testing Strategy

Unit tests for scoring engine logic

Manual test cases using known scam message patterns

Edge case handling for empty input and short text

📈 Roadmap

User history tracking

Hybrid ML classification model

Domain verification checks

Analytics dashboard

Cloud deployment

CI/CD pipeline

🎯 Project Goals

This project demonstrates:

Backend API design

Rule-based NLP processing

Explainable AI concepts

Frontend-backend integration

Agile project management workflow

It was built to solve a real-world problem while showcasing scalable and modular system design principles.

☸️ Kubernetes (K8s) Setup

Minimal Kubernetes manifests are available in `fake-recruiter-detector/k8s`.

Included resources:

- Namespace: `fake-recruiter-detector`
- Backend Deployment + Service
- Frontend Deployment + Service
- Ingress routing:
  - `/` -> frontend
  - `/analyze` -> backend

1) Build Docker images

From the `fake-recruiter-detector` folder:

```bash
docker build -t fake-recruiter-backend:latest ./backend
docker build -t fake-recruiter-frontend:latest ./frontend
```

2) Apply manifests

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
```

3) Access the app

- If using Docker Desktop Kubernetes with nginx ingress enabled, open the ingress address from:

```bash
kubectl get ingress -n fake-recruiter-detector
```

- For quick local access (without ingress), port-forward frontend service:

```bash
kubectl port-forward svc/frontend 8080:80 -n fake-recruiter-detector
```

Then open `http://localhost:8080`.

Notes:

- Make sure an ingress controller (for example ingress-nginx) is installed before applying `k8s/ingress.yaml`.
- Image names in manifests are currently local tags (`fake-recruiter-backend:latest`, `fake-recruiter-frontend:latest`). For cloud clusters, push images to a registry and update image values in deployments.

🔐 Authentication & Rate Limiting

All API endpoints require authentication by default.

**Authentication:**

All requests to `/analyze` and `/analyze/confidence` require an `X-API-Key` header:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-key-12345" \
  -d '{"text":"your message here"}'
```

**ENV Variables (Backend):**

- `AUTH_ENABLED` (default `true`) — set to `false` for development without authentication
- `VALID_API_KEYS` (default `demo-key-12345`) — comma-separated list of valid keys
- `RATE_LIMIT` (default `100/minute`) — per-IP rate limit (slowapi format: `count/period`)

**Development (Auth Disabled):**

To disable auth for local testing:

```bash
export AUTH_ENABLED=false
uvicorn main:app --reload --port 8000
```

Then requests don't need `X-API-Key` header.

**Docker:**

In `docker-compose.yml`, keys are pulled from `.env`. Example `.env`:

```
VALID_API_KEYS=my-api-key-1,my-api-key-2
AUTH_ENABLED=true
RATE_LIMIT=200/minute
```

## 💾 Database Integration

The backend now logs all analyses to a PostgreSQL database for historical tracking and analytics.

**Features:**
- ✅ Automatic logging of every analysis to the database
- ✅ Historical search and audit trail
- ✅ Per-analysis statistics (risk levels, AI usage, confidence scores)
- ✅ Aggregate analytics across time periods
- ✅ Full analysis details including confidence explanations

**Database Setup (Docker Compose):**

The `docker-compose.yml` includes a PostgreSQL 16 service:

- Container: `frd-db`
- User: `recruiter_user`
- Password: `recruiter_pass`
- Database: `recruiter_db`
- Data persisted in volume: `postgres_data`

**Environment Variable:**
- `DATABASE_URL` (auto-set in compose) — PostgreSQL connection string
  - Default: `postgresql://recruiter_user:recruiter_pass@db:5432/recruiter_db`

**API Endpoints for History & Analytics:**

### `GET /history`
Retrieve recent analyses.

**Query Parameters:**
- `limit` (default: 50, max: 500) — number of records to return
- `days` (optional) — filter to analyses from the last N days

**Example:**
```bash
curl -X GET 'http://localhost:8000/history?limit=20&days=7'
```

**Response:**
```json
{
  "count": 2,
  "records": [
    {
      "id": 2,
      "created_at": "2026-03-02T23:52:27.610053",
      "message": "...",
      "score": 60,
      "level": "High",
      "flags": "...",
      "ai_used": false,
      "ai_score": null,
      "confidence_score": null,
      "confidence_level": null
    }
  ]
}
```

### `GET /history/{record_id}`
Retrieve full details of a single analysis.

**Example:**
```bash
curl -X GET 'http://localhost:8000/history/2'
```

**Response:**
```json
{
  "id": 2,
  "created_at": "2026-03-02T23:52:27.610053",
  "message": "...",
  "score": 60,
  "level": "High",
  "flags": [...],
  "highlights": [...],
  "ai_used": false,
  "ai_score": null,
  "ai_summary": null,
  "confidence_score": null,
  "confidence_level": null,
  "confidence_explanation": null,
  "confidence_factors": null
}
```

### `GET /statistics`
Get statistical summary of analyses.

**Query Parameters:**
- `days` (default: 7) — period to analyze (e.g., last 7 days)

**Example:**
```bash
curl -X GET 'http://localhost:8000/statistics?days=7'
```

**Response:**
```json
{
  "period_days": 7,
  "total_analyses": 42,
  "high_risk_count": 8,
  "medium_risk_count": 15,
  "low_risk_count": 19,
  "average_score": 38.5,
  "ai_enabled": true,
  "ai_analyses_count": 42
}
```

**Database Schema:**

The `analysis_logs` table stores:
- `id` — Primary key
- `created_at` — Timestamp (auto-set)
- `message` — Original recruiter message
- `score` — Final risk score (0-100)
- `level` — Risk level ("Low", "Medium", "High")
- `flags` — Array of matched red flags
- `highlights` — Array of matched phrases for UI highlighting
- `ai_used` — Boolean if AI analysis was performed
- `ai_score` — AI score if available
- `ai_summary` — AI summary text if available
- `confidence_score` — Confidence in the classification
- `confidence_level` — Confidence level ("Low", "Medium", "High")
- `confidence_explanation` — Human-readable explanation
- `confidence_factors` — Array of factors contributing to confidence

**Backend Module:**

The `database.py` module handles:
- SQLAlchemy ORM setup
- Connection pooling to PostgreSQL
- Database initialization on startup
- Dependency injection for session management
