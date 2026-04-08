"""
SecureMail OpenEnv HTTP server.

Endpoints:
- POST /reset: return the initial observation
- POST /step: apply one action and return observation, reward, done, info
- GET /state: return current observation without advancing
- GET /health: liveness check
- GET /tasks: list available tasks
"""

import json
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from env import PhishingEnv

app = FastAPI(title="SecureMail OpenEnv", version="1.0.0")
env = PhishingEnv()


class StepRequest(BaseModel):
    label: str


class StepResponse(BaseModel):
    observation: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any]


@app.post("/reset")
async def reset(request: Request) -> Dict[str, Any]:
    """
    Reset the environment.
    Accepts empty body, {}, or {"task_index": N}.
    """
    from tasks import TASKS

    task_index = None
    try:
        body = await request.body()
        if body and body.strip() not in (b"", b"{}"):
            data = json.loads(body)
            task_index = data.get("task_index")
    except Exception:
        pass  # If body parsing fails, do a random reset.

    if task_index is not None:
        if not (0 <= task_index < len(TASKS)):
            raise HTTPException(
                status_code=400,
                detail=f"task_index out of range (0-{len(TASKS)-1})",
            )
        obs = env.reset_with_task(TASKS[task_index])
    else:
        obs = env.reset()

    return {"observation": obs.model_dump()}


@app.get("/state")
def state() -> Dict[str, Any]:
    if env.current_task is None:
        raise HTTPException(status_code=400, detail="Call /reset first.")
    return {"observation": env.state().model_dump()}


@app.post("/step")
def step(request: StepRequest) -> StepResponse:
    if env.current_task is None:
        raise HTTPException(status_code=400, detail="Call /reset first.")
    if env.done:
        raise HTTPException(status_code=400, detail="Episode done. Call /reset.")

    valid_labels = {"safe", "suspicious", "phishing"}
    if request.label not in valid_labels:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid label '{request.label}'. Must be one of: {sorted(valid_labels)}",
        )

    obs, reward, done, info = env.step({"label": request.label})
    return StepResponse(observation=obs.model_dump(), reward=reward, done=done, info=info)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks() -> Dict[str, Any]:
    from tasks import TASKS

    return {
        "total": len(TASKS),
        "tasks": [
            {
                "index": i,
                "difficulty": t["difficulty"],
                "category": t["category"],
                "label": t["label"],
            }
            for i, t in enumerate(TASKS)
        ],
    }
