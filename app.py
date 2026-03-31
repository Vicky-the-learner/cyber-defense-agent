from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from detector import detect_attack
from responder import respond_to_attack
from reward import calculate_reward
from environment import CyberDefenseEnv

from grader import grade_task
from tasks import TASKS

import uvicorn

app = FastAPI()

env = CyberDefenseEnv()


class InputData(BaseModel):
    input: str


# -------------------- ROOT --------------------

@app.get("/")
def home():
    return {
        "message": "AI Cyber Defense Agent is running",
        "endpoints": [
            "/reset",
            "/step",
            "/state",
            "/tasks",
            "/grader/{level}",
            "/baseline"
        ]
    }


# -------------------- RESET --------------------

@app.api_route("/reset", methods=["GET", "POST"])
def reset_env():
    return env.reset()


# -------------------- STEP (ADVANCED CORE) --------------------

@app.post("/step")
def step(data: dict):
    user_input = data.get("input", "")

    # ---------------- Detection ----------------
    analysis = detect_attack(user_input)

    attack = analysis.get("attack", "none")
    confidence = analysis.get("confidence", 0.5)
    reason = analysis.get("reason", "No threat detected")

    # ---------------- Response ----------------
    response = respond_to_attack(analysis)
    action = response.get("action", "allow")

    # ---------------- Adaptive Defense ----------------
    recent_attacks = [h for h in env.history[-5:] if h["attack"] != "none"]

    if len(recent_attacks) >= 3:
        action = "block"
        reason = "Adaptive defense triggered due to repeated suspicious activity"
        confidence = min(confidence + 0.1, 1.0)

    # ---------------- Threat Level ----------------
    if confidence > 0.9:
        threat_level = "high"
    elif confidence > 0.7:
        threat_level = "medium"
    else:
        threat_level = "low"

    # ---------------- Reward ----------------
    reward = calculate_reward(
        attack=attack,
        action=action,
        confidence=confidence
    )

    # ---------------- Logging ----------------
    log = f"[LOG] Input={user_input} | Attack={attack} | Action={action} | Confidence={confidence:.2f}"

    # ---------------- Update Environment ----------------
    env.history.append({
        "input": user_input,
        "attack": attack,
        "action": action,
        "confidence": confidence
    })

    env.current_input = user_input
    env.last_analysis = analysis
    env.done = True

    return {
        "input": user_input,
        "attack": attack,
        "action": action,
        "confidence": confidence,
        "threat_level": threat_level,
        "reason": reason,
        "reward": reward,
        "logs": log,
        "history": env.history[-5:]
    }


# -------------------- STATE --------------------

@app.get("/state")
def get_state():
    return env.state()


# -------------------- TASKS --------------------

@app.get("/tasks")
def get_tasks():
    return TASKS


# -------------------- GRADER --------------------

@app.get("/grader/{level}")
def run_grader(level: str):
    return {
        "level": level,
        "score": grade_task(level)
    }


# -------------------- BASELINE --------------------

@app.get("/baseline")
def baseline():
    scores = {}

    test_cases = {
        "easy": "' OR 1=1 --",
        "medium": "<script>alert(1)</script>",
        "hard": "admin' OR '1'='1' -- UNION SELECT password FROM users"
    }

    for level, input_data in test_cases.items():
        result = step({"input": input_data})

        score = 1.0 if result["action"] == "block" else 0.0

        # bonus for confidence
        if result["confidence"] > 0.9:
            score += 0.2

        scores[level] = round(score, 2)

    return scores


# -------------------- CORS --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------- RUN --------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)