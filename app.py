"""
app.py
------
Interactive Gradio demo UI for the Email Generation Assistant.

Usage:
    python app.py

Opens a local web interface at http://127.0.0.1:7860
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("NVIDIA_API_KEY"):
    print("\n[ERROR] NVIDIA_API_KEY is not set. Please configure your .env file.\n")
    sys.exit(1)

import gradio as gr
from generator.email_generator import generate_email

TONE_OPTIONS = [
    "Professional",
    "Formal",
    "Empathetic",
    "Friendly",
    "Diplomatic",
    "Confident",
    "Firm and Urgent",
    "Warm and Grateful",
    "Persuasive",
    "Urgent and Assertive",
    "Casual",
    "Custom (type below)",
]

MODEL_OPTIONS = {
    "Model A — z-ai/glm4.7 (Advanced Prompt)": "A",
    "Model B — z-ai/glm4.7 (Baseline Prompt)": "B",
}


def generate(intent: str, facts_raw: str, tone: str, custom_tone: str, model_label: str) -> str:
    """Parse inputs and call the generator."""
    if not intent.strip():
        return "⚠️ Please enter an email intent."

    effective_tone = custom_tone.strip() if tone == "Custom (type below)" and custom_tone.strip() else tone

    # Parse facts (one per line, strip bullet characters)
    key_facts = [
        line.lstrip("-•* ").strip()
        for line in facts_raw.strip().splitlines()
        if line.strip()
    ]
    if not key_facts:
        return "⚠️ Please enter at least one key fact."

    model = MODEL_OPTIONS.get(model_label, "A")

    try:
        result = generate_email(intent, key_facts, effective_tone, model=model)
        return result
    except Exception as e:
        return f"❌ Generation failed: {e}"


with gr.Blocks(
    title="📧 Email Generation Assistant",
    theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate"),
    css="""
        .header { text-align: center; margin-bottom: 1rem; }
        .header h1 { font-size: 2rem; font-weight: 700; }
        .header p { color: #6b7280; font-size: 1rem; }
        .generate-btn { width: 100%; font-size: 1.1rem !important; }
        footer { display: none !important; }
    """,
) as demo:

    gr.HTML("""
        <div class="header">
            <h1>📧 Email Generation Assistant</h1>
            <p>Powered by Nvidia API (z-ai/glm4.7) — Advanced Role-Playing + Few-Shot Prompt Engineering</p>
        </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ✍️ Email Inputs")

            intent_input = gr.Textbox(
                label="Intent",
                placeholder="e.g. Follow up after a job interview",
                lines=2,
            )

            facts_input = gr.Textbox(
                label="Key Facts (one per line)",
                placeholder="- Interviewed on Tuesday for the PM role\n- Discussed OKR framework\n- Available to start in 2 weeks",
                lines=6,
            )

            tone_input = gr.Dropdown(
                label="Tone",
                choices=TONE_OPTIONS,
                value="Professional",
            )

            custom_tone_input = gr.Textbox(
                label="Custom Tone (if selected above)",
                placeholder="e.g. Nostalgic and warm",
                visible=False,
            )

            def toggle_custom(tone):
                return gr.update(visible=(tone == "Custom (type below)"))

            tone_input.change(toggle_custom, inputs=tone_input, outputs=custom_tone_input)

            model_input = gr.Radio(
                label="Model / Prompt Strategy",
                choices=list(MODEL_OPTIONS.keys()),
                value=list(MODEL_OPTIONS.keys())[0],
            )

            generate_btn = gr.Button("⚡ Generate Email", variant="primary", elem_classes="generate-btn")

        with gr.Column(scale=1):
            gr.Markdown("### 📨 Generated Email")
            output_box = gr.Textbox(
                label="Output",
                lines=22,
                show_copy_button=True,
                placeholder="Your generated email will appear here...",
            )

    generate_btn.click(
        fn=generate,
        inputs=[intent_input, facts_input, tone_input, custom_tone_input, model_input],
        outputs=output_box,
    )

    gr.Markdown("""
---
**How to use:**
1. Enter a clear **Intent** (the purpose of the email)
2. List **Key Facts** that must appear in the email — one per line
3. Select the desired **Tone**
4. Choose a **Model/Prompt Strategy** to see how it affects output quality
5. Click **Generate Email**
    """)

if __name__ == "__main__":
    print("\n📧 Email Generation Assistant — Demo UI")
    print("Opening at: http://127.0.0.1:7860\n")
    demo.launch(server_port=7860, share=False)
