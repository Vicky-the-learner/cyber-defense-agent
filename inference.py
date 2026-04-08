import os
import urllib.request
import json

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://kiko555-cyber-defense-agent.hf.space"  # fixed typo: was "kikossy"
)

if not API_BASE_URL:
    print("ERROR: API_BASE_URL not set")
    exit(1)

TASKS = ["easy", "medium", "hard"]


def safe_post(url, data=None):
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8") if data else b"{}",
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"  [safe_post error] {url} -> {e}")
        return {"reward": 0.0, "done": True}


def run_episode(task):
    print(f"  Resetting for task={task}")
    safe_post(f"{API_BASE_URL}/reset", {"task": task})

    total_reward = 0.0
    steps = 0

    while steps < 50:
        result = safe_post(f"{API_BASE_URL}/step", {"action": "analyze"})

        reward = result.get("reward", 0.0)
        done = result.get("done", False)

        print(f"  STEP task={task} step={steps} reward={reward}")

        total_reward += reward
        steps += 1

        if done:
            break

    avg = round(total_reward / max(steps, 1), 2)
    return avg


def main():
    scores = {}

    for task in TASKS:
        print(f"\nSTART task={task}")
        try:
            score = run_episode(task)
        except Exception as e:
            print(f"  Exception during task={task}: {e}")
            score = 0.0
        scores[task] = score
        print(f"END task={task} score={score}")

    print("\nFINAL SCORES")
    print(scores)


if __name__ == "__main__":
    main()
