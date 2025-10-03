import google.generativeai as genai
import json
import re

def clean_empty(d):
    if isinstance(d, dict):
        return {k: clean_empty(v) for k, v in d.items() if v not in [None, [], {}, ""]}
    elif isinstance(d, list):
        return [clean_empty(v) for v in d if v not in [None, [], {}, ""]]
    else:
        return d

def extract_json(text):
    """
    Extract JSON object from string, removing backticks if present.
    """
    # Remove Markdown json block if exists
    text = re.sub(r"```json\s*|\s*```", "", text, flags=re.IGNORECASE).strip()
    try:
        return json.loads(text)
    except Exception:
        return None

def run_brief_mode(query: str, document_text: str, model="gemini-1.5-flash"):
    if not document_text:
        return None

    prompt = f"""
You are a **Legal Document Briefing Assistant**.

Mode: **Briefings (Structured Dictionary Mode)**.

Task:
- Extract metadata: document_type, issuer, date, recipient, recipient_address, PAN, subject, reference numbers.
- Summarize the document in plain language.
- Extract key_sections as objects with 'section' and 'content'.
- Include obligations, risks, definitions, and notes.
- Remove any empty fields automatically.
- Do NOT provide advice or recommendations.
- Output should be valid JSON that can be returned as a Python dict.

Document Context:
{document_text}

User Query:
{query}
"""

    model_instance = genai.GenerativeModel(model)
    response = model_instance.generate_content(prompt)

    # Try parsing JSON from the model output
    result_json = extract_json(response.text)

    if not result_json:
        # fallback if parsing fails
        result_json = {"document": {"summary": response.text.strip()}}

    result_json = clean_empty(result_json)
    return result_json
