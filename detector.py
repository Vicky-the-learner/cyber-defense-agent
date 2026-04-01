# detector.py

from ai_detector import ai_detect
import re
import urllib.parse


def normalize_input(input_data: str):
    decoded = urllib.parse.unquote(input_data)  # decode %xx encoding
    return decoded.lower().strip()


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

COMMAND_INJECTION_PATTERNS = [
    r"&&",
    r"\|\|",
    r";\s*",
    r"rm\s+-rf",
    r"bash\s+-i",
]

PATH_TRAVERSAL_PATTERNS = [
    r"\.\./",
    r"/etc/passwd",
]


def rule_based_detection(payload: str):
    data = normalize_input(payload)

    # SQL Injection
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, data):
            return build_result(
                attack="SQL Injection",
                severity="HIGH",
                confidence=0.9,
                source="rule-based",
                explanation=f"Matched SQL pattern: {pattern}"
            )

    # XSS
    for pattern in XSS_PATTERNS:
        if re.search(pattern, data):
            return build_result(
                attack="XSS",
                severity="HIGH",
                confidence=0.9,
                source="rule-based",
                explanation=f"Matched XSS pattern: {pattern}"
            )

    # Command Injection
    for pattern in COMMAND_INJECTION_PATTERNS:
        if re.search(pattern, data):
            return build_result(
                attack="Command Injection",
                severity="CRITICAL",
                confidence=0.95,
                source="rule-based",
                explanation=f"Matched command injection pattern: {pattern}"
            )

    # Path Traversal
    for pattern in PATH_TRAVERSAL_PATTERNS:
        if re.search(pattern, data):
            return build_result(
                attack="Path Traversal",
                severity="HIGH",
                confidence=0.85,
                source="rule-based",
                explanation=f"Matched path traversal pattern: {pattern}"
            )

    # Normal traffic
    return build_result(
        attack="Normal",
        severity="LOW",
        confidence=0.2,
        source="rule-based",
        explanation="No malicious patterns detected"
    )


def build_result(attack, severity, confidence, source, explanation):
    return {
        "is_attack": attack.lower() != "normal",
        "attack_type": attack,
        "severity": severity,
        "confidence": round(confidence, 2),
        "source": source,
        "explanation": explanation
    }



def detect_attack(input_data):
    """
    Supports:
    - raw string input
    - structured attack object (from attacker.py)
    """

    try:
        
        if isinstance(input_data, dict):
            payload = input_data.get("payload", "")
            attack_type_hint = input_data.get("type", "unknown")
        else:
            payload = input_data
            attack_type_hint = "unknown"

        
        ai_result = ai_detect(payload)

        ai_attack = ai_result.get("attack", "").lower()

        
        if ai_attack not in ["unknown", "normal", ""]:
            return build_result(
                attack=ai_result.get("attack", "Unknown"),
                severity=ai_result.get("severity", "MEDIUM"),
                confidence=ai_result.get("confidence", 0.6),
                source="AI",
                explanation=ai_result.get("explanation", "AI detected anomaly")
            )

       
        rule_result = rule_based_detection(payload)

        # Boost confidence if hint matches
        if attack_type_hint.lower() in rule_result["attack_type"].lower():
            rule_result["confidence"] = min(1.0, rule_result["confidence"] + 0.1)
            rule_result["explanation"] += " | Matched attacker hint"

        return rule_result

    except Exception as e:
        fallback = rule_based_detection(payload)

        fallback["source"] = "fallback"
        fallback["explanation"] += f" | AI failed: {str(e)}"

        return fallback