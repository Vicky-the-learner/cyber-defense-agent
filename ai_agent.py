def analyze_input(user_input):
    return {"attack": "unknown", "action": "allow"}
import json

import ollama

def analyze_input(user_input):
    prompt = f"""
You are a cybersecurity AI.

Analyze the input and respond ONLY in valid JSON.

Input:
{user_input}

Output format:
{{
  "attack": "SQL Injection / XSS / none",
  "action": "block / allow"
}}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]

    try:
        return json.loads(content)
    except:
        return {"attack": "unknown", "action": "allow"}