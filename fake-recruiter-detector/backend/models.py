# models.py - Pydantic request/response models for the /analyze endpoint

from pydantic import BaseModel
from typing import List


class AnalyzeRequest(BaseModel):
    """Request body: the recruiter message text to analyze."""
    text: str


class Highlight(BaseModel):
    """A single suspicious phrase found in the message."""
    phrase: str


class AnalyzeResponse(BaseModel):
    """Response body returned by the /analyze endpoint."""
    score: int          # 0-100 risk score
    level: str          # "Low", "Medium", or "High"
    flags: List[str]    # human-readable flag descriptions
    highlights: List[Highlight]  # suspicious phrases for UI highlighting
