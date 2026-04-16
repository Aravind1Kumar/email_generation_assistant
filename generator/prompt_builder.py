"""
Advanced prompt engineering using a Hybrid Role-Playing + Few-Shot technique.

The strategy:
  1. ROLE-PLAYING: Assign the LLM an expert business communication persona.
  2. FEW-SHOT EXAMPLES: Provide 2 worked examples so the model learns the
     expected structure (Subject line + professional body).
  3. STRUCTURED INPUT: Inject Intent, Key Facts, and Tone into a consistent
     template for reliable, parseable outputs.
"""

# ---------------------------------------------------------------------------
# Few-Shot Examples embedded directly in the system prompt
# ---------------------------------------------------------------------------
FEW_SHOT_EXAMPLES = """
--- EXAMPLE 1 ---
INPUT:
  Intent: Follow up after a job interview
  Key Facts:
    - Interviewed on Monday for the Senior Data Analyst role
    - Discussed experience with Python and SQL dashboards
    - Available to start immediately
  Tone: Professional

OUTPUT:
Subject: Follow-Up: Senior Data Analyst Interview – [Your Name]

Dear [Hiring Manager's Name],

Thank you for taking the time to speak with me on Monday regarding the Senior Data Analyst position. Our conversation about leveraging Python for automated reporting and building SQL-driven dashboards was particularly engaging, and it reinforced my enthusiasm for this opportunity.

I wanted to reiterate that I am available to start immediately and remain very interested in contributing to your team. Please do not hesitate to reach out if you require any additional information from my end.

I look forward to hearing from you.

Warm regards,
[Your Name]

--- EXAMPLE 2 ---
INPUT:
  Intent: Request proposal details from a vendor
  Key Facts:
    - Vendor is TechSupply Co.
    - Need pricing for 500 units of the X200 server model
    - Deadline for proposal submission is May 30th
  Tone: Formal

OUTPUT:
Subject: Request for Proposal – X200 Server Units | TechSupply Co.

Dear TechSupply Co. Sales Team,

I am writing on behalf of our procurement department to formally request a detailed proposal for the supply of 500 units of the X200 server model. We would appreciate a comprehensive breakdown of unit pricing, bulk discount options, and estimated delivery timelines.

Please note that all proposals must be submitted no later than May 30th to be considered in our current evaluation cycle.

Should you require any further clarification, please do not hesitate to contact us directly. We look forward to your prompt response.

Yours sincerely,
[Your Name]
Procurement Department
"""

# ---------------------------------------------------------------------------
# System prompt — Role-Playing persona
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are an expert business communication specialist with 15 years of experience "
    "drafting professional emails across industries including finance, technology, "
    "legal, and sales. You are known for writing emails that are clear, concise, "
    "appropriately toned, and always include every piece of information the client specifies. "
    "You never omit requested facts, never add unsolicited information, and you always "
    "begin with a clear subject line in the format 'Subject: ...'."
)

# ---------------------------------------------------------------------------
# Advanced prompt template (used for Model A)
# ---------------------------------------------------------------------------
ADVANCED_PROMPT_TEMPLATE = """
You are an expert business communication specialist with 15 years of experience.
Your task is to write a professional email based on the inputs below.

Here are two examples of how you should structure your response:
{few_shot_examples}
---

Now write an email for the following request. Follow the same structure exactly.
Include a Subject line, then a blank line, then the email body.
Make sure EVERY fact listed in Key Facts appears clearly in the email body.

INPUT:
  Intent: {intent}
  Key Facts:
{key_facts_formatted}
  Tone: {tone}

OUTPUT:
"""

# ---------------------------------------------------------------------------
# Baseline prompt template (used for Model B — minimal, no role, no examples)
# ---------------------------------------------------------------------------
BASELINE_PROMPT_TEMPLATE = """
Write a professional email.
Intent: {intent}
Key Facts: {key_facts_inline}
Tone: {tone}
"""


def build_advanced_prompt(intent: str, key_facts: list[str], tone: str) -> tuple[str, str]:
    """
    Build the advanced (Role + Few-Shot) prompt.

    Returns:
        (system_prompt, user_prompt) tuple for use with chat-style APIs.
    """
    key_facts_formatted = "\n".join(f"    - {fact}" for fact in key_facts)
    user_prompt = ADVANCED_PROMPT_TEMPLATE.format(
        few_shot_examples=FEW_SHOT_EXAMPLES,
        intent=intent,
        key_facts_formatted=key_facts_formatted,
        tone=tone,
    )
    return SYSTEM_PROMPT, user_prompt


def build_baseline_prompt(intent: str, key_facts: list[str], tone: str) -> tuple[str, str]:
    """
    Build the minimal/baseline prompt (no role, no examples).

    Returns:
        (system_prompt, user_prompt) tuple — system_prompt is empty for baseline.
    """
    key_facts_inline = "; ".join(key_facts)
    user_prompt = BASELINE_PROMPT_TEMPLATE.format(
        intent=intent,
        key_facts_inline=key_facts_inline,
        tone=tone,
    )
    return "", user_prompt  # No system prompt for baseline
