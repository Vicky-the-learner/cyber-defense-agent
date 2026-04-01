#responder.py


def respond_to_attack(analysis):
    attack = analysis.get("attack_type", "Normal")

    if attack == "SQL Injection":
        return {
            "action": "BLOCK_IP",
            "blocked": True,
            "confidence": analysis.get("confidence", 0.5),
            "message": "Blocked IP due to SQL Injection"
        }

    elif attack == "XSS":
        return {
            "action": "SANITIZE_INPUT",
            "blocked": True,
            "confidence": analysis.get("confidence", 0.5),
            "message": "Input sanitized due to XSS"
        }

    else:
        return {
            "action": "ALLOW",
            "blocked": False,
            "confidence": analysis.get("confidence", 0.5),
            "message": "No threat detected"
        }