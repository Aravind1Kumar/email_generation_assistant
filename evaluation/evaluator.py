"""
evaluator.py
------------
Orchestrates the full evaluation pipeline.

For each of the 10 test scenarios:
  1. Generate an email with Model A (gemini-2.0-flash, Advanced Prompt)
  2. Generate an email with Model B (gemini-1.5-pro, Baseline Prompt)
  3. Score both emails on all 3 custom metrics
  4. Collect and return all results
"""

import time
from tqdm import tqdm

from evaluation.test_scenarios import SCENARIOS
from evaluation.metrics import evaluate_all
from generator.email_generator import generate_model_a, generate_model_b


def run_evaluation(delay_between_calls: float = 5.0) -> dict:
    """
    Run the full evaluation for all scenarios and both models.

    Args:
        delay_between_calls: seconds to sleep between API calls to avoid rate limiting.

    Returns:
        Full results dict ready for JSON serialization.
    """
    model_a_results = []
    model_b_results = []

    print("\n" + "=" * 65)
    print("  EMAIL GENERATION ASSISTANT — FULL EVALUATION")
    print("=" * 65)
    print(f"  Running {len(SCENARIOS)} scenarios × 2 models = {len(SCENARIOS) * 2} LLM calls")
    print(f"  + {len(SCENARIOS) * 2} LLM-as-a-Judge calls for Tone Accuracy")
    print("=" * 65 + "\n")

    for scenario in tqdm(SCENARIOS, desc="Scenarios", unit="scenario"):
        sid = scenario["id"]
        intent = scenario["intent"]
        key_facts = scenario["key_facts"]
        tone = scenario["tone"]

        print(f"\n[Scenario {sid}] {intent} | Tone: {tone}")

        # ── Model A ──────────────────────────────────────────────────────
        print(f"  → Generating with Model A (z-ai/glm4.7, Advanced Prompt)...")
        email_a = generate_model_a(intent, key_facts, tone)
        time.sleep(delay_between_calls)

        print(f"  → Scoring Model A...")
        scores_a = evaluate_all(email_a, key_facts, tone)
        time.sleep(delay_between_calls)

        model_a_results.append({
            "scenario_id": sid,
            "intent": intent,
            "tone": tone,
            "generated_email": email_a,
            "frs": scores_a["summary"]["frs"],
            "tas": scores_a["summary"]["tas"],
            "fcs": scores_a["summary"]["fcs"],
            "detail": scores_a,
        })

        print(f"     FRS={scores_a['summary']['frs']:.1f}%  "
              f"TAS={scores_a['summary']['tas']}/10  "
              f"FCS={scores_a['summary']['fcs']:.2f}/10")

        # ── Model B ──────────────────────────────────────────────────────
        print(f"  → Generating with Model B (z-ai/glm4.7, Baseline Prompt)...")
        email_b = generate_model_b(intent, key_facts, tone)
        time.sleep(delay_between_calls)

        print(f"  → Scoring Model B...")
        scores_b = evaluate_all(email_b, key_facts, tone)
        time.sleep(delay_between_calls)

        model_b_results.append({
            "scenario_id": sid,
            "intent": intent,
            "tone": tone,
            "generated_email": email_b,
            "frs": scores_b["summary"]["frs"],
            "tas": scores_b["summary"]["tas"],
            "fcs": scores_b["summary"]["fcs"],
            "detail": scores_b,
        })

        print(f"     FRS={scores_b['summary']['frs']:.1f}%  "
              f"TAS={scores_b['summary']['tas']}/10  "
              f"FCS={scores_b['summary']['fcs']:.2f}/10")

    # ── Compute averages ─────────────────────────────────────────────────
    def avg(results, key):
        vals = [r[key] for r in results if isinstance(r[key], (int, float))]
        return round(sum(vals) / len(vals), 2) if vals else 0.0

    avg_a = {"frs": avg(model_a_results, "frs"), "tas": avg(model_a_results, "tas"), "fcs": avg(model_a_results, "fcs")}
    avg_b = {"frs": avg(model_b_results, "frs"), "tas": avg(model_b_results, "tas"), "fcs": avg(model_b_results, "fcs")}

    # ── Assemble final output ─────────────────────────────────────────────
    return {
        "metric_definitions": {
            "FRS": {
                "name": "Fact Recall Score",
                "range": "0–100 (%)",
                "type": "Automated NLP token overlap",
                "logic": "Tokenize each Key Fact and the generated email. A fact is 'recalled' if ≥60% of its key tokens appear in the email. Score = (recalled_facts / total_facts) × 100.",
            },
            "TAS": {
                "name": "Tone Accuracy Score",
                "range": "1–10",
                "type": "LLM-as-a-Judge (Gemini)",
                "logic": "A Gemini judge is prompted with the email and requested tone. It returns a 1–10 integer score with a one-sentence justification.",
            },
            "FCS": {
                "name": "Fluency & Clarity Score",
                "range": "0–10",
                "type": "Automated (grammar checker + Flesch Reading Ease)",
                "logic": "Average of: (1) Grammar score = max(0, 10 − error_count). (2) Readability score = Flesch Reading Ease mapped to 0–10, targeting professional range of 40–70.",
            },
        },
        "model_a": {
            "name": "z-ai/glm4.7 (Advanced Prompt: Role + Few-Shot)",
            "scenarios": model_a_results,
            "averages": avg_a,
        },
        "model_b": {
            "name": "z-ai/glm4.7 (Baseline Prompt: Minimal)",
            "scenarios": model_b_results,
            "averages": avg_b,
        },
    }
