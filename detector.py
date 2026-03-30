# detector.py

from ai_detector import ai_detect
import re
import urllib.parse


# 🔥 Enhanced normalization
def normalize_input(input_data: str):
    decoded = urllib.parse.unquote(input_data)  # decode %xx
    return decoded.lower().strip()


# 🔥 Strong patterns (HARD MODE)
SQLI_PATTERNS = [
    r"(\bor\b|\band\b).*=.*",
    r"union.*select",
    r"select.*from",
    r"drop\s+table",
    r"insert\s+into",
    r"--",
]

XSS_PATTERNS = [
    r"<script.*?>.*?</script>",
    r"onerror=",
    r"onload=",
    r"javascript:",
    r"<img.*?>",
    r"<svg.*?>",
]


def rule_based_detection(input_data: str):
    data = normalize_input(input_data)

    for pattern in SQLI_PATTERNS:
        if re.search(pattern, data):
            return {
                "attack": "SQL Injection",
                "severity": "HIGH",
                "confidence": 0.9,
                "source": "rule-based"
            }

    for pattern in XSS_PATTERNS:
        if re.search(pattern, data):
            return {
                "attack": "XSS",
                "severity": "HIGH",
                "confidence": 0.9,
                "source": "rule-based"
            }

    return {
        "attack": "Normal",
        "severity": "LOW",
        "confidence": 0.2,
        "source": "rule-based"
    }


def detect_attack(input_data: str):
    try:
        ai_result = ai_detect(input_data)

        # 🔥 If AI gives weak/unknown → trust rules
        if ai_result.get("attack", "").lower() in ["unknown", "normal"]:
            return rule_based_detection(input_data)

        return {
            "attack": ai_result.get("attack", "Unknown"),
            "severity": ai_result.get("severity", "LOW"),
            "confidence": ai_result.get("confidence", 0.5),
            "explanation": ai_result.get("explanation", ""),
            "source": "AI"
        }

    except Exception as e:
        fallback = rule_based_detection(input_data)

        return {
            **fallback,
            "explanation": f"AI failed: {str(e)}",
            "source": "fallback"
        }