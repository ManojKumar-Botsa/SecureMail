"""
Run an LLM agent against the SecureMail environment.

Required environment variables before submission:
- API_BASE_URL: LLM API endpoint (default: Hugging Face router)
- MODEL_NAME: model id (default: Qwen/Qwen2.5-72B-Instruct)
- HF_TOKEN: API key
- SECUREMAIL_URL: base URL for the running SecureMail server

STDOUT format is strict and used by scorers:
[START] task=<task_name> env=<benchmark> model=<model_name>
[STEP]  step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
[END]   success=<true|false> steps=<n> score=<score> rewards=<r1,r2,...,rn>
"""

import asyncio
import os
import textwrap
from typing import List, Optional

import httpx
from openai import OpenAI

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "")
ENV_BASE_URL = os.getenv("SECUREMAIL_URL", "http://localhost:7860").rstrip("/")

BENCHMARK = "SecureMail"
MAX_STEPS = 1  # single-step classification episode
TEMPERATURE = 0.2
MAX_TOKENS = 50
SUCCESS_SCORE = 0.5  # reward >= 0.5 counts as success

SYSTEM_PROMPT = textwrap.dedent(
    """
    You are a cybersecurity analyst focused on email threat detection.
    You will see the body of an email. Classify it as exactly one of:
        safe        - legitimate email with no threat signals
        suspicious  - unclear email that should be reviewed by a human
        phishing    - malicious email trying to steal credentials or money

    Rules:
    - Reply with one word only: safe, suspicious, or phishing.
    - Do not add punctuation or explanation.
    - If unsure between phishing and suspicious, choose suspicious.
    - Requests for credentials, payment changes, or "click here" are phishing signals.
    """
).strip()


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} "
        f"done={str(done).lower()} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


def classify_email(client: OpenAI, email_text: str) -> str:
    """Ask the LLM for a label and normalize output."""
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Email:\n{email_text}"},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        raw = (completion.choices[0].message.content or "").strip().lower()

        # Read first token only in case the model adds extra words.
        first_word = raw.split()[0] if raw else "suspicious"
        if first_word in {"safe", "suspicious", "phishing"}:
            return first_word

        # Fallback heuristics for off-format responses.
        if "phish" in raw:
            return "phishing"
        if "suspic" in raw:
            return "suspicious"
        return "safe"
    except Exception as exc:
        print(f"[DEBUG] LLM call failed: {exc}", flush=True)
        return "suspicious"


async def run_episode(
    client: OpenAI,
    http: httpx.AsyncClient,
    task_index: int,
    task_name: str,
) -> float:
    """Run one episode and return the score in [0.0, 1.0]."""
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=task_name, env=BENCHMARK, model=MODEL_NAME)

    try:
        reset_resp = await http.post(
            f"{ENV_BASE_URL}/reset",
            json={"task_index": task_index},
            timeout=30,
        )
        reset_resp.raise_for_status()
        obs = reset_resp.json()["observation"]
        email_text = obs["email_text"]

        label = classify_email(client, email_text)
        steps_taken = 1

        step_resp = await http.post(
            f"{ENV_BASE_URL}/step",
            json={"label": label},
            timeout=30,
        )
        step_resp.raise_for_status()
        step_data = step_resp.json()

        reward = float(step_data["reward"])
        done = bool(step_data["done"])
        rewards.append(reward)

        log_step(step=1, action=label, reward=reward, done=done, error=None)

        score = reward
        success = score >= SUCCESS_SCORE

    except Exception as exc:
        print(f"[DEBUG] Episode error: {exc}", flush=True)
        if not rewards:
            rewards = [0.0]
        score = 0.0
        steps_taken = max(steps_taken, 1)

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

    return score


async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    async with httpx.AsyncClient() as http:
        try:
            tasks_resp = await http.get(f"{ENV_BASE_URL}/tasks", timeout=30)
            tasks_resp.raise_for_status()
            tasks_data = tasks_resp.json()["tasks"]
        except Exception as exc:
            print(f"[DEBUG] Could not fetch task list: {exc}", flush=True)
            tasks_data = [{"index": i, "difficulty": "unknown"} for i in range(25)]

        all_scores: List[float] = []
        for task in tasks_data:
            idx = task["index"]
            diff = task.get("difficulty", "unknown")
            name = f"email-{diff}-{idx}"
            score = await run_episode(client, http, task_index=idx, task_name=name)
            all_scores.append(score)

    avg = sum(all_scores) / len(all_scores) if all_scores else 0.0
    print(f"\n[SUMMARY] tasks={len(all_scores)} avg_score={avg:.3f}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
