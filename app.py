from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from environment import CyberDefenseEnv
from grader import grade_task

app = FastAPI()

env = CyberDefenseEnv()


@app.get("/")
def home():
    return {"message": "Cyber Defense Agent running"}


# ✅ RESET (OpenEnv compliant)
@app.post("/reset")
async def reset_env(request: Request):
    try:
        data = await request.json()
    except:
        data = {}

    task = data.get("task", "easy")
    return env.reset(task)


# ✅ STEP
@app.post("/step")
async def step(request: Request):
    try:
        action = await request.json()
    except:
        action = {}

    result = env.step(action)

    return {
        "observation": result.get("observation", {}),
        "reward": result.get("reward", 0.0),
        "done": result.get("done", False),
        "info": result.get("info", {})
    }


@app.get("/tasks")
def get_tasks():
    return {"tasks": ["easy", "medium", "hard"]}


@app.post("/grader")
def run_grader(data: dict):
    task = data.get("task", "easy")
    score = grade_task(task)

    return {"task": task, "score": float(score)}


@app.get("/baseline")
def baseline():
    scores = {}

    for task in ["easy", "medium", "hard"]:
        try:
            env.reset(task)
            total = 0

            for _ in range(5):
                r = env.step({"action": "BLOCK_IP"})
                total += r.get("reward", 0)

            scores[task] = round(total / 5, 2)

        except:
            scores[task] = 0.0

    return scores


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)