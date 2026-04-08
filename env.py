import random

from pydantic import BaseModel

from grader import grade
from tasks import TASKS


class Observation(BaseModel):
    email_text: str


class Action(BaseModel):
    label: str


class PhishingEnv:
    def __init__(self):
        self.current_task = None
        self.done = False

    def reset(self) -> Observation:
        """Reset with a random task."""
        self.current_task = random.choice(TASKS)
        self.done = False
        return Observation(email_text=self.current_task["email"])

    def reset_with_task(self, task: dict) -> Observation:
        """Reset with a specific task."""
        self.current_task = task
        self.done = False
        return Observation(email_text=self.current_task["email"])

    def state(self) -> Observation:
        return Observation(email_text=self.current_task["email"])

    def step(self, action: dict) -> tuple:
        """
        Apply action and return (observation, reward, done, info).
        action['label'] must be one of: safe, suspicious, phishing.
        """
        reward = grade(action["label"], self.current_task["label"])
        self.done = True
        return (
            self.state(),
            reward,
            self.done,
            {
                "difficulty": self.current_task["difficulty"],
                "category": self.current_task.get("category", "unknown"),
                "expected_label": self.current_task["label"],
                "explanation": self.current_task.get("explanation", ""),
            },
        )
