from tasks import TASKS
from environment import CyberDefenseEnv
print("Grader Loaded")
env = CyberDefenseEnv()

def grade_task(level):
    tasks = TASKS[level]
    total_score = 0

    for task in tasks:
        env.reset()
        result = env.step(task["input"])

        detected = result["state"]["analysis"]["attack"]
        action = result["response"]["action"]
        confidence = result["state"]["analysis"].get("confidence", 0)

        score = 0

        # Detection score
        if detected == task["expected_attack"]:
            score += 0.4

        # Action score
        if (detected == "SQL Injection" and action == "BLOCK_IP") or \
           (detected == "XSS" and action == "SANITIZE_INPUT"):
            score += 0.4

        # Confidence score
        score += min(confidence, 1.0) * 0.2

        total_score += score

    return round(total_score / len(tasks), 2)
def run_baseline():
    results = {}

    for level in TASKS.keys():
        results[level] = grade_task(level)

    return results