import json
import logging
import os
from dataclasses import dataclass
from typing import List, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)


@dataclass
class AIAnalysis:
    score: int
    flags: List[str]
    phrases: List[str]
    summary: str


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def analyze_with_openai(text: str) -> Optional[AIAnalysis]:
    """Analyze text with OpenAI. Returns None on API key missing or critical failures."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning(
            "OPENAI_API_KEY not set; AI screening is disabled. "
            "Set OPENAI_API_KEY to enable advanced fraud detection."
        )
        return None

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")
        return None

    system_prompt = (
        "You are a fraud screening assistant for recruiter messages. "
        "Return strict JSON only with keys: ai_score (0-100), flags (array of short strings), "
        "phrases (array of suspicious exact phrases from input), summary (one sentence)."
    )

    user_prompt = (
        "Analyze this recruiter message for scam risk. Keep output concise and factual.\n\n"
        f"Message:\n{text}"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
    except Exception as e:
        logger.warning(f"OpenAI API call failed (will use rules-only): {e}")
        return None

    raw = (response.choices[0].message.content or "").strip()
    if not raw:
        logger.warning("OpenAI returned empty response")
        return None

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse OpenAI response JSON: {e}")
        return None

    score = max(0, min(100, _safe_int(parsed.get("ai_score"), 0)))
    flags = [str(item).strip() for item in parsed.get("flags", []) if str(item).strip()]
    phrases = [str(item).strip() for item in parsed.get("phrases", []) if str(item).strip()]
    summary = str(parsed.get("summary", "")).strip()

    return AIAnalysis(
        score=score,
        flags=flags[:5],
        phrases=phrases[:8],
        summary=summary,
    )
