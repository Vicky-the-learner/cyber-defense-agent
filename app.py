from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from environment import CyberDefenseEnv
from grader import grade_task
from tasks import TASKS

app = FastAPI()

# Initialize environment
env = CyberDefenseEnv()


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


# -------------------- STEP (FIXED CORE) --------------------

@app.post("/step")
def step():
    """
    Uses environment directly (OpenEnv compliant)
    """
    result = env.step()

    return {
        "observation": result["observation"],
        "reward": result["reward"],
        "done": result["done"],
        "info": result["info"]
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

    for level in ["easy", "medium", "hard"]:
        env.reset()

        total_reward = 0

        for _ in range(5):
            result = env.step()

            total_reward += result["reward"]

            if result["done"]:
                break

        scores[level] = round(total_reward / 5, 2)

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