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
