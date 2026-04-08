# reward.py
def calculate_reward(analysis, response, attack):
    reward = 0.0   # ← THIS WAS MISSING, causing crash every time
    details = []

    attack_type = attack.get("type", "normal") if isinstance(attack, dict) else "normal"
    is_actual_attack = attack_type.lower() != "normal"
    detected_attack = analysis["is_attack"]
    blocked = response.get("blocked", False)
    confidence = analysis.get("confidence", 0.5)
    severity = attack.get("severity", 0.5)

    if is_actual_attack and detected_attack:
        reward += 0.3
        details.append("✔ Correct detection")
    elif is_actual_attack and not detected_attack:
        reward -= 0.3
        details.append("❌ Missed attack")
    elif not is_actual_attack and detected_attack:
        reward -= 0.2
        details.append("⚠ False positive")
    else:
        reward += 0.1
        details.append("✔ Correctly ignored normal input")

    if detected_attack and blocked:
        reward += 0.4
        details.append("✔ Attack blocked")
    elif detected_attack and not blocked:
        reward -= 0.2
        details.append("❌ Detected but not blocked")
    elif not detected_attack and blocked:
        reward -= 0.2
        details.append("⚠ Blocked normal traffic")

    if confidence > 0.8:
        reward += 0.1
        details.append("✔ High confidence")

    if severity > 0.8 and blocked:
        reward += 0.1
        details.append("✔ Handled critical attack")

    if is_actual_attack and not blocked:
        reward -= 0.2
        details.append("❌ Attack not mitigated")

    reward = max(0.0, min(1.0, reward))
    return {"reward": round(reward, 2), "details": details}
