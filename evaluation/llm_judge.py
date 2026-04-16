"""
llm_judge.py
------------
LLM-as-a-Judge for Metric 2: Tone Accuracy Score (TAS).
Uses google-genai SDK (v1 endpoint).
"""

import re
import time
from openai import OpenAI

JUDGE_MODEL = "z-ai/glm4.7"

JUDGE_SYSTEM_PROMPT = (
    "You are an expert linguistics evaluator specializing in professional business communication. "
    "Your task is to evaluate how well an email matches a requested communication tone. "
    "You must respond with ONLY a JSON object in the exact format: "
    '{"score": <integer 1-10>, "reason": "<one sentence explanation>"}'
)

JUDGE_USER_TEMPLATE = """Evaluate the following email for tone accuracy.

Requested Tone: {tone}

Email:
---
{email}
---

Rate on a scale of 1 to 10 how well this email achieves the requested tone of "{tone}".
- 10 = Perfect match: language, formality, vocabulary, and sentence structure are ideal for this tone
- 7-9 = Good match with minor inconsistencies
- 4-6 = Partial match: some elements align but overall tone is off
- 1-3 = Poor match: tone is largely incorrect or inappropriate

Respond ONLY with a JSON object: {{"score": <integer 1-10>, "reason": "<one sentence>"}}"""

_client = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        _client = OpenAI(
          base_url="https://integrate.api.nvidia.com/v1",
          api_key=os.environ.get("NVIDIA_API_KEY", "")
        )
    return _client

def judge_tone_accuracy(email_text: str, tone: str, retries: int = 5) -> dict:
    """
    Ask the LLM judge to score tone accuracy of an email.
    Returns dict with 'score' (int 1-10) and 'reason' (str).
    """
    client = _get_client()
    prompt = JUDGE_USER_TEMPLATE.format(tone=tone, email=email_text)

    messages = [
        {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=JUDGE_MODEL,
                messages=messages,
                temperature=0.1,
                max_tokens=1024,
                extra_body={"chat_template_kwargs":{"enable_thinking":False,"clear_thinking":False}} # Reasoning might clutter JSON output, so default False or user can change it
            )
            content = response.choices[0].message.content
            raw = (content or "").strip()

            # Strip markdown code fences if present
            raw = re.sub(r"```json\s*|\s*```", "", raw).strip()
            match = re.search(
                r'\{.*?"score"\s*:\s*(\d+).*?"reason"\s*:\s*"([^"]+)".*?\}',
                raw, re.DOTALL
            )
            if match:
                score = max(1, min(10, int(match.group(1))))
                return {"score": score, "reason": match.group(2)}

            # Fallback: extract first number in 1-10 range
            for n in re.findall(r'\b(\d{1,2})\b', raw):
                if 1 <= int(n) <= 10:
                    return {"score": int(n), "reason": "Parsed from unstructured response"}

            return {"score": 5, "reason": "Could not parse judge response"}

        except Exception as e:
            err_str = str(e)
            if attempt < retries - 1:
                wait = 3 * (attempt + 1)
                print(f"    [WARN] Judge API error on attempt {attempt + 1}: retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"    [ERROR] Judge failed after all retries: {e}")
                return {"score": 5, "reason": f"Error: {e}"}
