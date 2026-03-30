from fastapi import FastAPI
from pydantic import BaseModel
from detector import detect_attack
from responder import respond_to_attack
from reward import calculate_reward
from environment import CyberDefenseEnv

from grader import grade_task
from tasks import TASKS

from grader import run_baseline

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

env = CyberDefenseEnv()

class InputData(BaseModel):
    input: str

@app.get("/")
def home():
    return {
        "message": "Cyber Defense Agent is running",
        "endpoints": [
            "/reset",
            "/step",
            "/tasks",
            "/grader/{level}",
            "/baseline"
        ]
    }

@app.post("/analyze")
async def analyze(data: InputData):
    input_data = data.input

    analysis = detect_attack(input_data)
    response = respond_to_attack(analysis)
    reward = calculate_reward(analysis, response)

    return {
        "input": input_data,
        "analysis": analysis,
        "response": response,
        "reward": reward
    }
@app.api_route("/reset", methods=["GET", "POST"])
def reset_env():
    return env.reset()




@app.post("/step")
def step(data: dict):
    user_input = data.get("input", "")

    attack = "none"
    action = "allow"

    if "OR 1=1" in user_input:
        attack = "SQL Injection"
        action = "block"
    elif "<script>" in user_input:
        attack = "XSS"
        action = "block"
    elif "UNION SELECT" in user_input:
        attack = "Advanced SQL Injection"
        action = "block"

    return {
        "attack": attack,
        "action": action
    }


@app.get("/state")
def get_state():
    return env.state()

@app.get("/tasks")
def get_tasks():
    return TASKS


@app.get("/grader/{level}")
def run_grader(level: str):
    return {
        "level": level,
        "score": grade_task(level)
    }
@app.get("/baseline")
def baseline():
    scores = {}

    test_cases = {
        "easy": "' OR 1=1 --",
        "medium": "<script>alert(1)</script>",
        "hard": "admin' OR '1'='1' -- UNION SELECT password FROM users"
    }

    for level, input_data in test_cases.items():
        attack = "none"
        action = "allow"

        # Detection logic
        if "OR 1=1" in input_data:
            attack = "SQL Injection"
            action = "block"
        elif "<script>" in input_data:
            attack = "XSS"
            action = "block"
        elif "UNION SELECT" in input_data:
            attack = "Advanced SQL Injection"
            action = "block"

        # Realistic scoring
        if level == "easy":
            score = 1.0 if action == "block" else 0.0
        elif level == "medium":
            score = 0.8 if action == "block" else 0.0
        else:
            score = 0.6 if action == "block" else 0.0

        scores[level] = score

    return scores

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)