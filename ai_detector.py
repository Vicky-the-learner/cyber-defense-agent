import ollama
import json

def ai_detect(input_data: str):
    prompt = f"""
You are a cybersecurity AI.

Analyze the input and respond ONLY in JSON format.

Example:
{{
  "attack": "SQL Injection",
  "severity": "HIGH",
  "confidence": 0.95,
  "explanation": "Reason here"
}}

Input: {input_data}

IMPORTANT:
- Output ONLY valid JSON
- No extra text
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response['message']['content']

    try:
        return json.loads(content)
    except:
        return {
            "attack": "Unknown",
            "severity": "LOW",
            "confidence": 0.3,
            "explanation": content
        }