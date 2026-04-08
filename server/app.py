"""
Email Triage API
================
FastAPI server exposing endpoints to interact with EmailEnv.
Provides:
- /reset : Resets the environment and returns the initial state
- /step  : Takes an action and returns the environment's response
- /      : Health check endpoint
"""

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from env import EmailEnv
from models import EmailAction

# Initialize FastAPI app
app = FastAPI()
# Initialize the environment
env = EmailEnv()

# -----------------------------
# Pydantic model for request
# -----------------------------
class ActionRequest(BaseModel):
    category: str
    priority: str | None = None
    reply: str | None = None


# -----------------------------
# API Endpoints
# -----------------------------

@app.post("/reset")
async def reset():
    """
    Reset the email environment and return the initial observation.
    """
    result = await env.reset()
    return result.model_dump()


@app.post("/step")
async def step(action: ActionRequest):
    """
    Take a step in the environment based on user-provided action.
    Returns the observation after the step.
    """
    action_obj = EmailAction(**action.dict())
    result = await env.step(action_obj)
    return result.model_dump()

@app.get("/")
def home():
    """
    Health check endpoint
    """
    return {"message": "Email Triage API is running"}


# -----------------------------
# Entry point for uvicorn
# -----------------------------
def main():
    """
    Run the FastAPI app with uvicorn.
    """
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()