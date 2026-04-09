import os
from openai import OpenAI


def analyze_input(user_input):
    try:
        client = OpenAI(
            base_url=os.environ.get("API_BASE_URL"),
            api_key=os.environ.get("API_KEY")
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cybersecurity AI."},
                {"role": "user", "content": f"Analyze this attack and classify it (SQL Injection, XSS, Normal): {user_input}"}
            ]
        )

        content = response.choices[0].message.content.lower()

        if "sql" in content:
            return {"attack_type": "SQL Injection", "action": "block"}
        elif "xss" in content:
            return {"attack_type": "XSS", "action": "sanitize"}
        else:
            return {"attack_type": "Normal", "action": "allow"}

    except Exception:
        return {"attack_type": "Normal", "action": "allow"}