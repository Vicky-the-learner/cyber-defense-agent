def respond_to_attack(analysis):
    attack = analysis.get("attack", "Normal")

    if attack == "SQL Injection":
        return {
            "action": "BLOCK_IP",
            "message": "Blocked IP due to SQL Injection"
        }

    elif attack == "XSS":
        return {
            "action": "SANITIZE_INPUT",
            "message": "Input sanitized due to XSS"
        }

    else:
        return {
            "action": "ALLOW",
            "message": "No threat detected"
        }