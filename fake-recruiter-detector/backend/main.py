# main.py - FastAPI application entry point
# Run with: uvicorn main:app --reload --port 8000

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import AnalyzeRequest, AnalyzeResponse, Highlight
from scoring import analyze_text

app = FastAPI(title="Fake Recruiter Detector API", version="0.1.0")

# CORS — restrict origins via the ALLOWED_ORIGINS env variable in production.
# Example: ALLOWED_ORIGINS="https://yourapp.com,https://www.yourapp.com"
# Defaults to the local Vite dev server when the variable is not set.
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


@app.get("/")
def root():
    """Health-check / welcome endpoint."""
    return {"message": "Fake Recruiter Detector API is running."}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze a recruiter message and return a scam risk score.

    Request body: { "text": "<message>" }
    Response body: { "score": int, "level": str, "flags": [...], "highlights": [...] }
    """
    score, level, flags, matched_phrases = analyze_text(request.text)

    highlights = [Highlight(phrase=phrase) for phrase in matched_phrases]

    return AnalyzeResponse(
        score=score,
        level=level,
        flags=flags,
        highlights=highlights,
    )
