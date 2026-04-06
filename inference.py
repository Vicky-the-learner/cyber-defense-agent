import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
HF_TOKEN = os.getenv("HF_TOKEN")  # NO DEFAULT

TASKS = ["easy", "medium", "hard"]


def run_episode(task):
    # Reset environment with task
    requests.post(f"{API_BASE_URL}/reset", json={"task": task})

    total_reward = 0
    steps = 0
    max_steps = 50  # safety limit

    while steps < max_steps:
        try:
            response = requests.post(f"{API_BASE_URL}/step", json={
                "action": "analyze"  # simple baseline action
            })
            result = response.json()
        except Exception:
            break  # avoid infinite loop

        reward = result.get("reward", 0.0)
        done = result.get("done", False)

        total_reward += reward
        steps += 1

        if done:
            break

    avg_reward = total_reward / max(steps, 1)
    return round(avg_reward, 2)


def main():
    scores = {}

    for task in TASKS:
        score = run_episode(task)
        scores[task] = score

    print("\n📊 BASELINE SCORES")
    print(scores)


if __name__ == "__main__":
    main()