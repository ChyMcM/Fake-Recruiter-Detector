# main.py - FastAPI application entry point
# Run with: uvicorn main:app --reload --port 8000

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_screening import analyze_with_openai
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
    rule_score, _, rule_flags, rule_matched_phrases = analyze_text(request.text)
    ai_result = analyze_with_openai(request.text)

    merged_flags = list(dict.fromkeys(rule_flags))
    merged_phrases = list(dict.fromkeys(rule_matched_phrases))

    if ai_result:
        merged_flags = list(dict.fromkeys([*merged_flags, *ai_result.flags]))
        merged_phrases = list(dict.fromkeys([*merged_phrases, *ai_result.phrases]))
        score = min(100, round((rule_score * 0.7) + (ai_result.score * 0.3)))
        ai_used = True
        ai_score = ai_result.score
        ai_summary = ai_result.summary or None
    else:
        score = rule_score
        ai_used = False
        ai_score = None
        ai_summary = None

    if score >= 60:
        level = "High"
    elif score >= 30:
        level = "Medium"
    else:
        level = "Low"

    highlights = [Highlight(phrase=phrase) for phrase in merged_phrases]

    return AnalyzeResponse(
        score=score,
        level=level,
        flags=merged_flags,
        highlights=highlights,
        ai_used=ai_used,
        ai_score=ai_score,
        ai_summary=ai_summary,
    )
