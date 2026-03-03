from typing import List, Optional, Tuple


def risk_level_from_score(score: int) -> str:
    if score >= 60:
        return "High"
    if score >= 30:
        return "Medium"
    return "Low"


def confidence_level_from_score(score: int) -> str:
    if score >= 75:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


def _distance_from_boundary(score: int, level: str) -> float:
    if level == "Low":
        return max(0.0, (30 - score) / 30)
    if level == "Medium":
        # Confidence is lower near the boundaries (30 and 60), higher near the middle.
        return max(0.0, 1 - (abs(score - 45) / 15))
    return max(0.0, (score - 60) / 40)


def explain_confidence(
    final_score: int,
    level: str,
    rule_score: int,
    flags: List[str],
    matched_phrases: List[str],
    ai_used: bool,
    ai_score: Optional[int],
) -> Tuple[int, str, str, List[str]]:
    boundary_component = min(1.0, _distance_from_boundary(final_score, level))
    evidence_component = min(1.0, len(matched_phrases) / 8)
    ai_component = 0.15 if ai_used else 0.0

    confidence_ratio = (0.45 * boundary_component) + (0.4 * evidence_component) + ai_component
    confidence_score = max(0, min(100, round(confidence_ratio * 100)))
    confidence_level = confidence_level_from_score(confidence_score)

    factors: List[str] = []
    if matched_phrases:
        top_phrases = ", ".join(matched_phrases[:3])
        factors.append(f"Detected suspicious phrases: {top_phrases}")
    if flags:
        factors.append(f"Triggered {len(flags)} risk flags")

    if ai_used and ai_score is not None:
        factors.append(f"AI cross-check score: {ai_score}/100")
        factors.append(f"Blended final score: 70% rules + 30% AI = {final_score}/100")
    else:
        factors.append(f"Rule-based score used: {rule_score}/100 (AI not enabled)")

    if confidence_level == "High":
        explanation = "Confidence is high because multiple consistent signals support this risk level."
    elif confidence_level == "Medium":
        explanation = "Confidence is moderate because signals are present but not strongly clustered."
    else:
        explanation = "Confidence is low because there are limited or mixed risk indicators."

    return confidence_score, confidence_level, explanation, factors
