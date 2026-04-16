"""
Handles LLM API calls for both Model A and Model B using the OpenAI SDK.
Isolates prompt engineering impact by running different templates against the same model.
"""

import os
import re
import time
from openai import OpenAI
from dotenv import load_dotenv
from generator.prompt_builder import build_advanced_prompt, build_baseline_prompt

load_dotenv()

MODEL_A_NAME = "z-ai/glm4.7"
MODEL_B_NAME = "z-ai/glm4.7"

_client = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
          base_url="https://integrate.api.nvidia.com/v1",
          api_key=os.environ.get("NVIDIA_API_KEY", "")
        )
    return _client

def _call_gemini(model_name: str, system_prompt: str, user_prompt: str, retries: int = 5) -> str:
    """
    Call an LLM model via the OpenAI SDK.
    """
    client = _get_client()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=4096,
                extra_body={"chat_template_kwargs":{"enable_thinking":True,"clear_thinking":False}}
            )
            
            # Since the user wants to print reasoning if any, we'll extract just content for the result
            content = response.choices[0].message.content
            return (content or "").strip()

        except Exception as e:
            if attempt < retries - 1:
                wait = 3 * (attempt + 1)
                time.sleep(wait)
            else:
                raise RuntimeError(f"All retries exhausted for {model_name}. Underlying error: {e}") from e


def generate_model_a(intent: str, key_facts: list[str], tone: str) -> str:
    """Model A: gemini-1.5-flash + Advanced Role-Playing + Few-Shot prompt."""
    system_prompt, user_prompt = build_advanced_prompt(intent, key_facts, tone)
    return _call_gemini(MODEL_A_NAME, system_prompt, user_prompt)


def generate_model_b(intent: str, key_facts: list[str], tone: str) -> str:
    """Model B: gemini-1.5-flash + Minimal baseline prompt."""
    system_prompt, user_prompt = build_baseline_prompt(intent, key_facts, tone)
    return _call_gemini(MODEL_B_NAME, system_prompt, user_prompt)


def generate_email(intent: str, key_facts: list[str], tone: str, model: str = "A") -> str:
    """Unified entry point. model='A' → Model A, model='B' → Model B."""
    if model.upper() == "A":
        return generate_model_a(intent, key_facts, tone)
    elif model.upper() == "B":
        return generate_model_b(intent, key_facts, tone)
    else:
        raise ValueError(f"Unknown model '{model}'. Use 'A' or 'B'.")
