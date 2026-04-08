import os
import json
import urllib.request
from ai_agent import analyze_input

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://kiko555-cyber-defense-agent.hf.space"
)

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
        print(f"[ERROR] {url} -> {e}", flush=True)
        return {"reward": 0.0, "done": True}


def choose_action(observation):
    try:
        result = analyze_input(str(observation))

        action = result.get("action", "allow").lower()

        if action == "block":
            return "BLOCK_IP"
        elif action == "sanitize":
            return "SANITIZE_INPUT"
        else:
            return "BLOCK_IP"

    except Exception:
        return "BLOCK_IP"

def run_episode(task):
    print(f"[START] task={task}", flush=True)

    reset_result = safe_post(f"{API_BASE_URL}/reset", {"task": task})
    observation = reset_result.get("observation", "")

    total_reward = 0.0
    steps = 0

    while steps < 50:
        action = choose_action(observation)

        result = safe_post(f"{API_BASE_URL}/step", {"action": action})

        reward = result.get("reward", 0.0)
        done = result.get("done", False)
        observation = result.get("observation", "")

        print(
            f"[STEP] step={steps} action={action} reward={reward}",
            flush=True
        )

        total_reward += reward
        steps += 1

        if done:
            break

    score = round(total_reward / max(steps, 1), 2)

    print(
        f"[END] task={task} score={score} steps={steps}",
        flush=True
    )

    return score


def main():
    scores = {}

    for task in TASKS:
        try:
            score = run_episode(task)
        except Exception as e:
            print(f"[ERROR] task={task} -> {e}", flush=True)
            score = 0.0

        scores[task] = score

    print("[FINAL]", scores, flush=True)


if __name__ == "__main__":
    main()