from fastapi import FastAPI
from pydantic import BaseModel
from detector import detect_attack
from responder import respond_to_attack
from reward import calculate_reward
from environment import CyberDefenseEnv

from grader import grade_task
from tasks import TASKS

from grader import run_baseline

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
@app.post("/reset")
def reset_env():
    return env.reset()


@app.post("/step")
async def step_env(data: InputData):
    return env.step(data.input)


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
    return run_baseline()