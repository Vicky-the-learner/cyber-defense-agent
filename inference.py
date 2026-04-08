import os
import json
import urllib.request

API_BASE_URL = os.getenv("API_BASE_URL")

if not API_BASE_URL:
    print("ERROR: API_BASE_URL not set")
    exit(0)

TASKS = ["easy", "medium", "hard"]


def safe_post(url, data=None):
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8") if data else None,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode())
    except Exception:
        return {"reward": 0.0, "done": True}


def run_episode(task):
    safe_post(f"{API_BASE_URL}/reset", {"task": task})

    total_reward = 0.0
    steps = 0

    while steps < 50:
        result = safe_post(f"{API_BASE_URL}/step", {"action": "analyze"})

        reward = result.get("reward", 0.0)
        done = result.get("done", False)

        print(f"STEP task={task} step={steps} reward={reward}")

        total_reward += reward
        steps += 1

        if done:
            break

    return round(total_reward / max(steps, 1), 2)


def main():
    scores = {}

    for task in TASKS:
        print(f"START task={task}")
        try:
            score = run_episode(task)
        except Exception:
            score = 0.0
        scores[task] = score
        print(f"END task={task} score={score}")

    print("\nFINAL SCORES")
    print(scores)


if __name__ == "__main__":
    main()
