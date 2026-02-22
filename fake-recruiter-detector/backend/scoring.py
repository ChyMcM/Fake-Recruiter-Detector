# scoring.py - Rule-based scoring engine for recruiter message analysis

from typing import Dict, List, Tuple

# Each entry maps a suspicious keyword/phrase to a (score_weight, flag_description) tuple.
SUSPICIOUS_PATTERNS: Dict[str, Tuple[int, str]] = {
    "gift card": (30, "Requests payment via gift card"),
    "telegram": (20, "Asks to move conversation to Telegram"),
    "crypto": (25, "Mentions cryptocurrency payment"),
    "bitcoin": (25, "Mentions Bitcoin payment"),
    "wire transfer": (25, "Requests wire transfer"),
    "western union": (30, "Mentions Western Union"),
    "work from home": (10, "Generic work-from-home offer"),
    "no experience": (15, "Claims no experience required"),
    "unlimited earning": (20, "Promises unlimited earnings"),
    "urgent": (10, "Creates urgency pressure"),
    "whatsapp": (15, "Asks to move to WhatsApp"),
    "fee": (20, "Mentions upfront fee"),
    "advance payment": (25, "Requests advance payment"),
    "guaranteed": (15, "Uses guaranteed income language"),
}


def analyze_text(text: str) -> Tuple[int, str, List[str], List[str]]:
    """
    Analyze a recruiter message and return a risk assessment.

    Args:
        text: The recruiter message to analyze.

    Returns:
        A tuple of (score, level, flags, matched_phrases).
        - score: integer 0-100
        - level: "Low", "Medium", or "High"
        - flags: list of human-readable flag descriptions
        - matched_phrases: list of suspicious phrases found in the text
    """
    lower_text = text.lower()
    total_score = 0
    flags: List[str] = []
    matched_phrases: List[str] = []

    for phrase, (weight, description) in SUSPICIOUS_PATTERNS.items():
        if phrase in lower_text:
            total_score += weight
            flags.append(description)
            matched_phrases.append(phrase)

    # Clamp score to 0-100
    score = min(total_score, 100)

    # Determine risk level
    if score >= 60:
        level = "High"
    elif score >= 30:
        level = "Medium"
    else:
        level = "Low"

    return score, level, flags, matched_phrases
