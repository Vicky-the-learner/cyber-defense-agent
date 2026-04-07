import os
import subprocess
import sys

# 🔧 Ensure requests is installed (IMPORTANT FIX)
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
HF_TOKEN = os.getenv("HF_TOKEN")  # NO DEFAULT

TASKS = ["easy", "medium", "hard"]


def safe_post(url, payload=None):
    """Safe POST request to avoid crashes"""
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code != 200:
            return None
        return response.json()
    except Exception:
        return None


def run_episode(task):
    # Reset environment
    safe_post(f"{API_BASE_URL}/reset", {"task": task})

    total_reward = 0.0
    steps = 0
    max_steps = 50

    while steps < max_steps:
        result = safe_post(f"{API_BASE_URL}/step", {
            "action": "analyze"
        })

        if not result:
            break

        reward = result.get("reward", 0.0)
        done = result.get("done", False)

        total_reward += reward

        # STEP LOG (important for judges)
        print(f"STEP task={task} step={steps} reward={reward}")

        steps += 1

        if done:
            break

    avg_reward = total_reward / max(steps, 1)
    return round(avg_reward, 2)


def main():
    scores = {}

    for task in TASKS:
        print(f"START task={task}")

        try:
            score = run_episode(task)
        except Exception:
            score = 0.0  # fallback safety

        scores[task] = score

        print(f"END task={task} score={score}")

    print("\n📊 FINAL SCORES")
    print(scores)


if __name__ == "__main__":
    main()