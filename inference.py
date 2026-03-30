import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv("HF_TOKEN", "dummy")

client = OpenAI(api_key=API_KEY)

TASKS = ["easy", "medium", "hard"]

def run_task(task):
    requests.post(f"{API_BASE_URL}/reset")

    inputs = [
        "' OR 1=1 --",
        "<script>alert(1)</script>",
        "normal user input"
    ]

    total_score = 0

    for inp in inputs:
        response = requests.post(
            f"{API_BASE_URL}/step",
            json={"task": task, "input": inp}
        )

        try:
            result = response.json()
        except:
            continue

        attack = result.get("attack", "none")
        action = result.get("action", "allow")

        # simple scoring logic
        if attack != "none" and action == "block":
            total_score += 1
        elif attack == "none" and action == "allow":
            total_score += 1

    return total_score / len(inputs)


def main():
    scores = {}

    for task in TASKS:
        score = run_task(task)
        scores[task] = score

    print(scores)


if __name__ == "__main__":
    main()