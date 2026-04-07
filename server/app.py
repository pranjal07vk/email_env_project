from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from env import EmailEnv
from models import EmailAction

app = FastAPI()
env = EmailEnv()


class ActionRequest(BaseModel):
    category: str
    priority: str | None = None
    reply: str | None = None


@app.post("/reset")
async def reset():
    result = await env.reset()
    return result.model_dump()


@app.post("/step")
async def step(action: ActionRequest):
    action_obj = EmailAction(**action.dict())
    result = await env.step(action_obj)
    return result.model_dump()


# ✅ REQUIRED main function
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# ✅ REQUIRED entrypoint
if __name__ == "__main__":
    main()