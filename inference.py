import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")

TASKS = ["easy", "medium", "hard"]


def run_episode():
    # Reset environment
    requests.post(f"{API_BASE_URL}/reset")

    total_reward = 0
    steps = 0

    while True:
        try:
            response = requests.post(f"{API_BASE_URL}/step", json={})
            result = response.json()
        except Exception:
            continue

        reward = result.get("reward", 0.0)
        done = result.get("done", False)

        total_reward += reward
        steps += 1

        if done:
            break

    # Average reward per episode
    avg_reward = total_reward / max(steps, 1)

    return round(avg_reward, 2)


def main():
    scores = {}

    for task in TASKS:
        score = run_episode()
        scores[task] = score

    print("\n📊 BASELINE SCORES")
    print(scores)


if __name__ == "__main__":
    main()