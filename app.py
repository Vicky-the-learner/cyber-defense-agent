from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from environment import CyberDefenseEnv
from grader import grade_task

app = FastAPI()

# Initialize environment
env = CyberDefenseEnv()

# FINAL VERSION FIXED TASKS FORMAT


@app.get("/")
def home():
    return {
        "message": "AI Cyber Defense Agent is running",
        "endpoints": [
            "/reset",
            "/step",
            "/state",
            "/tasks",
            "/grader",
            "/baseline"
        ]
    }


@app.api_route("/reset", methods=["GET", "POST"])
def reset_env(data: dict = {}):
    task = data.get("task", "easy")
    return env.reset(task)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/step")
def step(action: dict = {}):
    try:
        result = env.step(action)
    except Exception:
        result = {
            "observation": {},
            "reward": 0.0,
            "done": True,
            "info": {"error": "step failed"}
        }

    return {
        "observation": result.get("observation", {}),
        "reward": result.get("reward", 0.0),
        "done": result.get("done", False),
        "info": result.get("info", {})
    }



@app.get("/state")
def get_state():
    try:
        return env.state()
    except Exception:
        return {"state": "error"}



@app.get("/tasks")
def get_tasks():
    return {
        "tasks": ["easy", "medium", "hard"]
    }


@app.post("/grader")
def run_grader(data: dict):
    try:
        task = data.get("task", "easy")
        score = grade_task(task)
    except Exception:
        task = "unknown"
        score = 0.0

    return {
        "task": task,
        "score": float(score)
    }


@app.get("/baseline")
def baseline():
    scores = {}

    for task in ["easy", "medium", "hard"]:
        try:
            env.reset(task)
            total_reward = 0.0

            for _ in range(5):
                result = env.step({"action": "analyze"})
                total_reward += result.get("reward", 0.0)

                if result.get("done", False):
                    break

            scores[task] = round(total_reward / 5, 2)

        except Exception:
            scores[task] = 0.0

    return scores

@app.get("/debug")
def debug():
    return {"status": "routes working"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



