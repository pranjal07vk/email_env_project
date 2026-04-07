from pydantic import BaseModel
from typing import Optional


# What agent sends to environment
class EmailAction(BaseModel):
    category: str  # spam / important / normal
    priority: Optional[str] = None  # high / medium / low
    reply: Optional[str] = None  # reply template


# What environment returns to agent
class EmailObservation(BaseModel):
    email_subject: str
    email_body: str
    sender: str  # e.g., "unknown", "boss", "marketing"
    last_action_feedback: Optional[str] = None


# Reward model (optional but good practice)
class EmailReward(BaseModel):
    score: float  # 0.0 to 1.0


# Full step result wrapper (IMPORTANT for OpenEnv style)
class StepResult(BaseModel):
    observation: EmailObservation
    reward: float
    done: bool
    info: Optional[dict] = None