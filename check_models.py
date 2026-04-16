"""
check_models.py
---------------
Lists all available Gemini models for your API key and tests
which ones can actually generate content.
"""

import os
from dotenv import load_dotenv
load_dotenv()

from google import genai

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

print("\n=== Listing all available models ===\n")
working = []

for model in client.models.list():
    name = model.name  # e.g. "models/gemini-1.5-flash"
    short = name.replace("models/", "")

    # Only test models that support generateContent
    supported = getattr(model, "supported_actions", []) or []
    if hasattr(model, "supported_generation_methods"):
        supported = model.supported_generation_methods or []

    if "generateContent" not in str(supported):
        print(f"  SKIP  {short}  (no generateContent)")
        continue

    # Quick generation test
    try:
        resp = client.models.generate_content(
            model=short,
            contents="Say: OK",
        )
        print(f"  OK    {short}")
        working.append(short)
    except Exception as e:
        err = str(e)[:80]
        print(f"  FAIL  {short}  -> {err}")

print(f"\n=== Working models ({len(working)}) ===")
for m in working:
    print(f"  ✓  {m}")
print()
