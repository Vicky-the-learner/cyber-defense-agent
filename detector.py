from ai_detector import ai_detect
import re

# Fallback rule-based patterns (backup system)
SQLI_PATTERNS = [
    r"(\bor\b|\band\b).*=.*",
    r"union.*select",
    r"select.*from",
]

XSS_PATTERNS = [
    r"<script.*?>.*?</script>",
    r"onerror=",
    r"javascript:"
]


def rule_based_detection(input_data: str):
    input_data = input_data.lower()

    for pattern in SQLI_PATTERNS:
        if re.search(pattern, input_data):
            return {
                "attack": "SQL Injection",
                "severity": "HIGH",
                "confidence": 0.8,
                "source": "rule-based"
            }

    for pattern in XSS_PATTERNS:
        if re.search(pattern, input_data):
            return {
                "attack": "XSS",
                "severity": "HIGH",
                "confidence": 0.8,
                "source": "rule-based"
            }

    return {
        "attack": "Normal",
        "severity": "LOW",
        "confidence": 0.2,
        "source": "rule-based"
    }


def detect_attack(input_data: str):
    # Rule-based result (trusted baseline)
    rule_result = rule_based_detection(input_data)

    try:
        ai_result = ai_detect(input_data)

        # 🔥 If AI matches rule → trust AI
        if ai_result.get("attack") == rule_result.get("attack"):
            return {
                **ai_result,
                "source": "AI"
            }

        # ⚠️ If mismatch → prefer rule (more reliable for known attacks)
        return {
            **rule_result,
            "explanation": f"AI disagreed. Rule-based result used. AI said: {ai_result.get('attack')}",
            "source": "hybrid-rule"
        }

    except Exception as e:
        return {
            **rule_result,
            "explanation": f"AI failed: {str(e)}",
            "source": "fallback"
        }