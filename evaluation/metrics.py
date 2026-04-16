"""
Three custom evaluation metrics for the Email Generation Assistant.

METRIC 1: Fact Recall Score (FRS)
  Type    : Automated (NLP token overlap)
  Range   : 0–100 (percentage)
  Focus   : Does the generated email include all key facts?

  Logic   : For each Key Fact string:
              1. Tokenize into meaningful words (lowercase, strip punctuation,
                 remove stopwords).
              2. Check if >=60% of the fact's tokens appear in the email text.
              3. FRS = (facts_matched / total_facts) × 100

METRIC 2: Tone Accuracy Score (TAS)
  Type    : LLM-as-a-Judge
  Range   : 1–10
  Focus   : Does the email's style match the requested tone?

  Logic   : An LLM call rates the email 1–10 against the requested tone.
            See evaluation/llm_judge.py for the full judge prompt.

METRIC 3: Fluency & Clarity Score (FCS)
  Type    : Automated (grammar checker + readability formula)
  Range   : 0–10
  Focus   : Is the email grammatically correct and appropriately readable?

  Logic   : Two sub-scores averaged:
    - Grammar (0–10): 10 − min(grammar_errors, 10) via language_tool_python
    - Readability (0–10): Flesch Reading Ease mapped to 0–10.
        Professional emails target a Flesch score of 40–70.
        - ease >= 70  → 10 (very easy, clear)
        - ease 40–70 → linearly scaled 5–10
        - ease < 40  → linearly scaled 0–5 (too complex)
"""

import re
import string
import textstat
from evaluation.llm_judge import judge_tone_accuracy

# ─── Common English stopwords (lightweight, no NLTK dependency) ───────────
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "is", "are", "was", "were", "be", "been", "has", "have",
    "had", "do", "does", "did", "will", "would", "could", "should", "may",
    "might", "shall", "this", "that", "these", "those", "i", "we", "you",
    "he", "she", "it", "they", "me", "us", "him", "her", "them", "my",
    "our", "your", "his", "its", "their", "by", "from", "as", "into",
    "about", "after", "before", "during", "through", "not", "no", "so",
    "if", "then", "than", "also", "just", "up", "out",
}


def _tokenize(text: str) -> set[str]:
    """Lowercase, remove punctuation, split, remove stopwords."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    return {t for t in tokens if t not in STOPWORDS and len(t) > 1}


# ─────────────────────────────────────────────────────────────────────────────
# METRIC 1: Fact Recall Score (FRS)
# ─────────────────────────────────────────────────────────────────────────────

def fact_recall_score(email_text: str, key_facts: list[str], threshold: float = 0.6) -> dict:
    """
    Compute the Fact Recall Score.

    Args:
        email_text : The generated email text.
        key_facts  : List of key fact strings that must appear.
        threshold  : Fraction of a fact's tokens that must be present (default 0.6).

    Returns:
        {
          "score": float (0–100),
          "facts_matched": int,
          "total_facts": int,
          "detail": list of per-fact results
        }
    """
    email_tokens = _tokenize(email_text)
    detail = []
    matched = 0

    for fact in key_facts:
        fact_tokens = _tokenize(fact)
        if not fact_tokens:
            detail.append({"fact": fact, "matched": True, "overlap": 1.0})
            matched += 1
            continue

        overlap = len(fact_tokens & email_tokens) / len(fact_tokens)
        is_matched = overlap >= threshold
        if is_matched:
            matched += 1
        detail.append({
            "fact": fact,
            "matched": is_matched,
            "overlap_ratio": round(overlap, 3),
        })

    total = len(key_facts)
    score = round((matched / total) * 100, 1) if total > 0 else 0.0

    return {
        "score": score,
        "facts_matched": matched,
        "total_facts": total,
        "detail": detail,
    }


# ─────────────────────────────────────────────────────────────────────────────
# METRIC 2: Tone Accuracy Score (TAS)
# ─────────────────────────────────────────────────────────────────────────────

def tone_accuracy_score(email_text: str, tone: str) -> dict:
    """
    Compute the Tone Accuracy Score via LLM-as-a-Judge.

    Args:
        email_text : The generated email text.
        tone       : The requested tone (e.g., "Professional", "Urgent").

    Returns:
        {
          "score": int (1–10),
          "reason": str
        }
    """
    result = judge_tone_accuracy(email_text, tone)
    return {
        "score": result["score"],
        "reason": result["reason"],
    }


# ─────────────────────────────────────────────────────────────────────────────
# METRIC 3: Fluency & Clarity Score (FCS)
# ─────────────────────────────────────────────────────────────────────────────

def _grammar_score(email_text: str) -> dict:
    """
    Compute grammar sub-score using language_tool_python.
    Returns score 0–10 and error count.
    """
    try:
        import language_tool_python
        tool = language_tool_python.LanguageTool("en-US")
        matches = tool.check(email_text)
        error_count = len(matches)  # Count all flagged issues
        score = max(0.0, 10.0 - error_count)
        tool.close()
        return {"grammar_score": round(score, 1), "error_count": error_count}
    except Exception as e:
        # Graceful fallback if language_tool_python is unavailable
        print(f"    [WARN] Grammar check unavailable: {e}. Using fallback score.")
        return {"grammar_score": 8.0, "error_count": -1, "note": "grammar_tool_unavailable"}


def _readability_score(email_text: str) -> dict:
    """
    Compute readability sub-score from Flesch Reading Ease.
    Professional emails target 40–70. Scores outside this range are penalized.
    """
    ease = textstat.flesch_reading_ease(email_text)

    if ease >= 70:
        # Very easy to read — good for most professional contexts
        score = 10.0
    elif ease >= 40:
        # Professional sweet spot: linearly scale 40–70 → 5–10
        score = 5.0 + ((ease - 40) / 30.0) * 5.0
    else:
        # Too complex/dense: linearly scale 0–40 → 0–5
        score = max(0.0, (ease / 40.0) * 5.0)

    return {"readability_score": round(score, 2), "flesch_ease": round(ease, 2)}


def fluency_clarity_score(email_text: str) -> dict:
    """
    Compute the Fluency & Clarity Score (FCS).

    Returns:
        {
          "score": float (0–10),
          "grammar_score": float,
          "readability_score": float,
          "grammar_errors": int,
          "flesch_ease": float
        }
    """
    grammar = _grammar_score(email_text)
    readability = _readability_score(email_text)

    combined = round((grammar["grammar_score"] + readability["readability_score"]) / 2, 2)

    return {
        "score": combined,
        "grammar_score": grammar["grammar_score"],
        "readability_score": readability["readability_score"],
        "grammar_errors": grammar.get("error_count", -1),
        "flesch_ease": readability["flesch_ease"],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Convenience: run all 3 metrics at once
# ─────────────────────────────────────────────────────────────────────────────

def evaluate_all(email_text: str, key_facts: list[str], tone: str) -> dict:
    """
    Run all three metrics and return a combined result dict.
    """
    frs = fact_recall_score(email_text, key_facts)
    tas = tone_accuracy_score(email_text, tone)
    fcs = fluency_clarity_score(email_text)

    return {
        "fact_recall": frs,
        "tone_accuracy": tas,
        "fluency_clarity": fcs,
        "summary": {
            "frs": frs["score"],
            "tas": tas["score"],
            "fcs": fcs["score"],
        },
    }
