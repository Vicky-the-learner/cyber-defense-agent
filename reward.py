def calculate_reward(detected_attack, expected_attack, action, confidence):
    reward = 0.0

    # 🔥 Detection correctness (major)
    if detected_attack == expected_attack:
        reward += 0.5
    else:
        reward -= 0.3

    # 🔥 Action correctness
    correct_actions = {
        "SQL Injection": "BLOCK_IP",
        "XSS": "SANITIZE_INPUT",
        "none": "ALLOW"
    }

    if correct_actions.get(expected_attack) == action:
        reward += 0.3
    else:
        reward -= 0.2

    # 🔥 Confidence contribution
    reward += min(confidence, 1.0) * 0.2

    # Clamp between 0 and 1
    return round(max(0.0, min(1.0, reward)), 2)