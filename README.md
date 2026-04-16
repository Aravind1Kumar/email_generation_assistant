# 📧 Email Generation Assistant — AI Engineer Assessment

A production-ready **Email Generation Assistant** that uses advanced LLM prompt engineering to generate professional emails, evaluated against 3 custom metrics across two model/strategy configurations.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- An **Nvidia API Key**: [Get one from Nvidia API](https://build.nvidia.com/)

### 2. Installation

```bash
# Clone / navigate to the project
cd email-gen-assistant

# Install dependencies
pip install -r requirements.txt

# Copy and fill in your API key
copy .env.example .env
# → Open .env and replace "your_nvidia_api_key_here" with your actual key
```

### 3. Run the Full Evaluation
```bash
python run_evaluation.py
```
This will:
- Run all 10 test scenarios through **Model A** (z-ai/glm4.7, advanced prompting) and **Model B** (z-ai/glm4.7, baseline prompting)
- Score each email on 3 custom metrics
- Output results to `reports/evaluation_results.json` and `reports/evaluation_results.csv`
- Print a comparative summary to the console

### 4. Launch the Interactive Demo UI
```bash
python app.py
```
Opens a Gradio web app where you can input any Intent, Facts, and Tone and generate an email on demand.

---

## 📁 Project Structure

```
email-gen-assistant/
├── README.md
├── requirements.txt
├── .env.example
├── run_evaluation.py          # Main evaluation runner
├── app.py                     # Gradio demo UI
├── generator/
│   ├── prompt_builder.py      # Advanced prompt templates
│   └── email_generator.py     # LLM API calls for both models
├── evaluation/
│   ├── test_scenarios.py      # 10 scenarios + human reference emails
│   ├── metrics.py             # 3 custom metric implementations
│   ├── llm_judge.py           # LLM-as-a-Judge for Tone Accuracy
│   └── evaluator.py           # Evaluation orchestrator
└── reports/
    ├── evaluation_results.json
    ├── evaluation_results.csv
    └── final_analysis.md      # Comparative analysis report
```

---

## 🧠 Advanced Prompting Technique

**Technique: Role-Playing + Few-Shot Examples (Hybrid)**

The prompt template assigns the LLM an expert business communication persona and provides 2 few-shot examples before the actual task. This:
- **Role-Playing** anchors the tone and voice of the model
- **Few-Shot Examples** establish the expected structure (Subject + Body)
- **Structured input** (Intent / Facts / Tone) ensures reliable, parseable outputs

See `generator/prompt_builder.py` for the full template.

---

## 📊 3 Custom Evaluation Metrics

| Metric | Type | Range | Focus |
|--------|------|-------|-------|
| **Fact Recall Score (FRS)** | Automated (NLP) | 0–100% | Are all key facts present in the email? |
| **Tone Accuracy Score (TAS)** | LLM-as-a-Judge | 1–10 | Does the email match the requested tone? |
| **Fluency & Clarity Score (FCS)** | Automated (grammar + readability) | 0–10 | Is the email grammatically correct and readable? |

### Metric Logic

**FRS**: For each Key Fact bullet, extract key tokens (nouns, numbers, proper nouns). Check what percentage appear in the generated email text. Score = (matched_facts / total_facts) × 100.

**TAS**: An LLM judge call is made with the prompt: *"Rate 1–10 how well this email achieves a [TONE] tone."* The integer score is parsed from the response.

**FCS**: Two sub-scores averaged:
- Grammar score: `max(0, 10 - grammar_error_count)` via `language_tool_python`
- Readability score: Flesch Reading Ease mapped to 0–10 (professional range: 40–70 ease)

---

## 🔬 Model Comparison

| | Model A | Model B |
|---|---|---|
| Model | `z-ai/glm4.7` | `z-ai/glm4.7` |
| Prompt | Role + Few-Shot (Advanced) | Minimal (Baseline) |
| Goal | Best possible quality | Baseline for comparison |

Results and analysis in `reports/final_analysis.md`.

---

## 📄 Output Files

After running `run_evaluation.py`:
- `reports/evaluation_results.json` — Full structured results with metric definitions
- `reports/evaluation_results.csv` — Spreadsheet-friendly scores for all 10 scenarios
- `reports/final_analysis.md` — One-page comparative analysis

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `NVIDIA_API_KEY` | Your Nvidia API key (required) |
