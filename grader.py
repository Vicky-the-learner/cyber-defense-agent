from environment import CyberDefenseEnv
from tasks import TASKS

env = CyberDefenseEnv()


def grade_task(level):
    tasks = TASKS[level]
    total_score = 0

    for task in tasks:
        env.reset()

        # 🔥 Inject structured attack into environment
        env.current_input = {
            "type": "test",
            "payload": task["input"],
            "severity": 0.7
        }

        result = env.step()

        analysis = result["info"]["analysis"]
        response = result["info"]["response"]

        detected_attack = analysis.get("attack", "Normal")
        expected_attack = task["expected_attack"]

        blocked = response.get("blocked", False)
        confidence = analysis.get("confidence", 0.5)

        score = 0.0
        reasons = []

        # ---------------- DETECTION ----------------
        if detected_attack == expected_attack:
            score += 0.4
            reasons.append("✔ Correct detection")
        else:
            reasons.append("❌ Wrong detection")

        # ---------------- RESPONSE ----------------
        if blocked:
            score += 0.4
            reasons.append("✔ Attack blocked")
        else:
            score -= 0.2
            reasons.append("❌ Not blocked")

        # ---------------- CONFIDENCE ----------------
        score += min(confidence, 1.0) * 0.2

        total_score += max(0.0, score)

    final_score = total_score / len(tasks)


    if final_score <= 0.0:
        final_score = 0.1
    elif final_score >= 1.0:
        final_score = 0.99

    return round(final_score, 2)


# 🔥 OPTIONAL (FOR BASELINE USE)
def run_baseline():
    results = {}

    for level in TASKS.keys():
        results[level] = grade_task(level)

    return results