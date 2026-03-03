# main.py - FastAPI application entry point with database logging
# Run with: uvicorn main:app --reload --port 8000

import os
import logging
from typing import Optional
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from models import AnalyzeRequest, AnalyzeResponse, Highlight
from scoring import analyze_text
from ai_screening import analyze_with_openai
from confidence import explain_confidence
from database import get_db, init_db, AnalysisLog

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fake Recruiter Detector API", version="0.1.0")

# CORS — restrict origins via the ALLOWED_ORIGINS env variable in production.
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:8080")
allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database and log startup configuration."""
    init_db()
    logger.info("Application started successfully")


@app.get("/")
def root():
    """Health-check / welcome endpoint."""
    return {"message": "Fake Recruiter Detector API is running."}


def _run_analysis(text: str) -> tuple:
    """
    Run complete analysis pipeline: rules + optional AI.
    Returns: (score, level, flags, matched_phrases, ai_used, ai_score, ai_summary)
    """
    # Rule-based analysis
    rule_score, rule_level, rule_flags, matched_phrases = analyze_text(text)
    
    ai_used = False
    ai_score = None
    ai_summary = None
    final_score = rule_score
    
    # Optional AI analysis
    if os.getenv("OPENAI_API_KEY", "").strip():
        ai_result = analyze_with_openai(text)
        if ai_result:
            ai_used = True
            ai_score = ai_result.score
            ai_summary = ai_result.summary
            
            # Blend scores: 70% rules, 30% AI
            final_score = int((rule_score * 0.7) + (ai_score * 0.3))
            final_score = min(100, max(0, final_score))
    
    # Determine final level based on blended score
    if final_score < 30:
        final_level = "Low"
    elif final_score < 60:
        final_level = "Medium"
    else:
        final_level = "High"
    
    return final_score, final_level, rule_flags, matched_phrases, ai_used, ai_score, ai_summary


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest, db: Session = Depends(get_db)) -> AnalyzeResponse:
    """
    Analyze a recruiter message and return a scam risk score.
    Logs the analysis to the database.

    Request body: { "text": "<message>" }
    Response body: { "score": int, "level": str, "flags": [...], "highlights": [...], "ai_used": bool, "ai_score": int, "ai_summary": str }
    """
    score, level, flags, matched_phrases, ai_used, ai_score, ai_summary = _run_analysis(request.text)
    
    highlights = [Highlight(phrase=phrase) for phrase in matched_phrases]
    
    # Log to database
    log_entry = AnalysisLog(
        message=request.text,
        score=score,
        level=level,
        flags=flags,
        highlights=[h.dict() for h in highlights],
        ai_used=ai_used,
        ai_score=ai_score,
        ai_summary=ai_summary,
    )
    db.add(log_entry)
    db.commit()
    
    return AnalyzeResponse(
        score=score,
        level=level,
        flags=flags,
        highlights=highlights,
        ai_used=ai_used,
        ai_score=ai_score,
        ai_summary=ai_summary,
    )


@app.post("/analyze/confidence")
def analyze_confidence(request: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    Get detailed confidence explanation for an analysis.
    Also logs confidence metrics to the database.
    """
    score, level, flags, matched_phrases, ai_used, ai_score, ai_summary = _run_analysis(request.text)
    
    confidence_score, confidence_level, explanation, factors = explain_confidence(
        score, level, score, flags, matched_phrases, ai_used, ai_score
    )
    
    # Update the most recent analysis log with confidence data
    log_entry = (
        db.query(AnalysisLog)
        .filter(AnalysisLog.message == request.text)
        .order_by(AnalysisLog.created_at.desc())
        .first()
    )
    
    if log_entry:
        log_entry.confidence_score = confidence_score
        log_entry.confidence_level = confidence_level
        log_entry.confidence_explanation = explanation
        log_entry.confidence_factors = factors
        db.commit()
    
    return {
        "score": score,
        "level": level,
        "confidence_score": confidence_score,
        "confidence_level": confidence_level,
        "explanation": explanation,
        "factors": factors,
        "ai_used": ai_used,
        "ai_score": ai_score,
    }


@app.get("/history")
def get_history(
    limit: int = 50,
    days: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get analysis history.
    
    Query parameters:
    - limit: Number of records to return (default: 50, max: 500)
    - days: Filter to results from the last N days (optional)
    """
    limit = min(limit, 500)  # Cap at 500
    
    query = db.query(AnalysisLog).order_by(AnalysisLog.created_at.desc())
    
    if days:
        cutoff = datetime.utcnow() - timedelta(days=days)
        query = query.filter(AnalysisLog.created_at >= cutoff)
    
    logs = query.limit(limit).all()
    
    return {
        "count": len(logs),
        "records": [
            {
                "id": log.id,
                "created_at": log.created_at.isoformat() if log.created_at else None,
                "message": log.message,
                "score": log.score,
                "level": log.level,
                "flags": log.flags,
                "ai_used": log.ai_used,
                "ai_score": log.ai_score,
                "confidence_score": log.confidence_score,
                "confidence_level": log.confidence_level,
            }
            for log in logs
        ]
    }


@app.get("/history/{record_id}")
def get_record(record_id: int, db: Session = Depends(get_db)):
    """Get a single analysis record by ID."""
    log = db.query(AnalysisLog).filter(AnalysisLog.id == record_id).first()
    
    if not log:
        return {"error": "Record not found"}, 404
    
    return {
        "id": log.id,
        "created_at": log.created_at.isoformat() if log.created_at else None,
        "message": log.message,
        "score": log.score,
        "level": log.level,
        "flags": log.flags,
        "highlights": log.highlights,
        "ai_used": log.ai_used,
        "ai_score": log.ai_score,
        "ai_summary": log.ai_summary,
        "confidence_score": log.confidence_score,
        "confidence_level": log.confidence_level,
        "confidence_explanation": log.confidence_explanation,
        "confidence_factors": log.confidence_factors,
    }


@app.get("/statistics")
def get_statistics(
    days: Optional[int] = 7,
    db: Session = Depends(get_db)
):
    """
    Get statistical summary of analyses.
    
    Query parameters:
    - days: Number of days to analyze (default: 7)
    """
    query = db.query(AnalysisLog)
    
    if days:
        cutoff = datetime.utcnow() - timedelta(days=days)
        query = query.filter(AnalysisLog.created_at >= cutoff)
    
    logs = query.all()
    
    if not logs:
        return {
            "period_days": days,
            "total_analyses": 0,
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "low_risk_count": 0,
            "average_score": 0,
            "ai_enabled": bool(os.getenv("OPENAI_API_KEY", "").strip()),
            "ai_analyses_count": 0,
        }
    
    high_count = sum(1 for log in logs if log.level == "High")
    medium_count = sum(1 for log in logs if log.level == "Medium")
    low_count = sum(1 for log in logs if log.level == "Low")
    ai_count = sum(1 for log in logs if log.ai_used)
    avg_score = sum(log.score for log in logs) / len(logs) if logs else 0
    
    return {
        "period_days": days,
        "total_analyses": len(logs),
        "high_risk_count": high_count,
        "medium_risk_count": medium_count,
        "low_risk_count": low_count,
        "average_score": round(avg_score, 2),
        "ai_enabled": bool(os.getenv("OPENAI_API_KEY", "").strip()),
        "ai_analyses_count": ai_count,
    }