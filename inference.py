import os
import requests
import json

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://kiko555-cyber-defense-agent.hf.space"
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

def choose_action(observation):
    """Read the attack type and pick the right defense action."""
    if not observation:
        return "BLOCK_IP"

    obs_str = str(observation).lower()

    # SQL Injection and XSS → sanitize the input
    if any(k in obs_str for k in ["sql", "select", "insert", "xss", "<script>", "javascript"]):
        return "SANITIZE_INPUT"

    # Brute force, port scan, path traversal → block the IP
    if any(k in obs_str for k in ["brute", "force", "scan", "traversal", "../", "flood"]):
        return "BLOCK_IP"

    # Command injection → sanitize
    if any(k in obs_str for k in ["cmd", "command", "exec", "bash", "shell", ";"]):
        return "SANITIZE_INPUT"

    # Default: block
    return "BLOCK_IP"

def run_episode(task):
    print(f"\nResetting for task={task}")
    reset_result = safe_post(f"{API_BASE_URL}/reset", {"task": task})
    observation = reset_result.get("observation", "")

    total_reward = 0.0
    steps = 0

    while steps < 50:
        action = choose_action(observation)
        result = safe_post(f"{API_BASE_URL}/step", {"action": action})

        reward = result.get("reward", 0.0)
        done = result.get("done", False)
        observation = result.get("observation", "")  # read next attack

        print(f"  STEP task={task} step={steps} action={action} reward={reward}")
        total_reward += reward
        steps += 1

        if done:
            break

    return round(total_reward / max(steps, 1), 2)

def main():
    scores = {}
    for task in TASKS:
        print(f"\nSTART task={task}")
        try:
            score = run_episode(task)
        except Exception as e:
            print(f"  Exception: {e}")
            score = 0.0
        scores[task] = score
        print(f"END task={task} score={score}")

    print("\nFINAL SCORES")
    print(scores)

if __name__ == "__main__":
    main()
