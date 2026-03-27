def calculate_reward(analysis, response):
    attack = analysis.get("attack")
    action = response.get("action")

    # Perfect actions
    if attack == "SQL Injection" and action == "BLOCK_IP":
        return 1.0

    if attack == "XSS" and action == "SANITIZE_INPUT":
        return 1.0

    if attack == "Normal" and action == "ALLOW":
        return 1.0

    # Partial correct
    if attack != "Normal" and action != "ALLOW":
        return 0.5

    # Wrong action
    return 0.0