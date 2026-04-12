"""
Inference Script
================
Handles running the Email Triage environment with an LLM model.
Emits standardized [START], [STEP], [END] logs for evaluation.

STDOUT FORMAT
-------------
- [START] task=<task_name> env=<benchmark> model=<model_name>
- [STEP]  step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
- [END]   success=<true|false> steps=<n> score=<score> rewards=<r1,r2,...,rn>
"""

import asyncio
import os
import textwrap
from typing import List, Optional

from openai import OpenAI

from env import EmailEnv
from models import EmailAction
from grader import TASK_GRADERS

# -------------------------
# Environment & Model Setup
# -------------------------
IMAGE_NAME = os.getenv("IMAGE_NAME") # If you are using docker image 
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")
TASK_NAME = os.getenv("TASK_NAME", "easy")
BENCHMARK = "email_triage_env"

# Inference configuration
MAX_STEPS = 8
TEMPERATURE = 0.7
MAX_TOKENS = 150
SUCCESS_SCORE_THRESHOLD = 0.1  # normalized score in (0, 1)

# Max possible reward: 
_MAX_REWARD_PER_STEP = MAX_TOKENS * 0.1
MAX_TOTAL_REWARD = MAX_STEPS * _MAX_REWARD_PER_STEP

# System prompt guiding the model
SYSTEM_PROMPT = """
    You are an email triage assistant.

    Given an email, decide:
    - category: spam / important / normal
    - priority: high / medium / low
    - reply: ignore / acknowledge / respond

    Output STRICTLY in this format:

    category: <value>
    priority: <value>
    reply: <value>

    No extra text.
""".strip()


# -------------------------
# Logging helpers
# -------------------------

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )

def log_end(success: bool, steps: int, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}")


# -------------------------
# Prompt construction
# -------------------------
def build_user_prompt(step: int, last_email: str, last_reward: float, history: List[str]) -> str:
    """
    Construct the message sent to the LLM at each step, including history and previous reward.
    """
    history_block = "\n".join(history[-4:]) if history else "None"
    return textwrap.dedent(
        f"""
        Step: {step}
        Email content: {last_email!r}
        Last reward: {last_reward:.2f}
        Previous steps:
        {history_block}
        Send your next message.
        """
    ).strip()


def get_model_message(client: OpenAI, step: int, last_echoed: str, last_reward: float, history: List[str]) -> str:
    """
    Query the LLM to generate the next message.
    Returns 'hello' on failure or empty response.
    """
    user_prompt = build_user_prompt(step, last_echoed, last_reward, history)
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        text = (completion.choices[0].message.content or "").strip()
        return text if text else "hello"
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return "hello"
    

# -------------------------
# LLM Output → Structured Action
# -------------------------
def parse_llm_output(text: str):
    try:
        lines = text.lower().splitlines()
        data = {}

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()

        return EmailAction(
            category=data.get("category", "normal"),
            priority=data.get("priority", "medium"),
            reply=data.get("reply", "respond"),
        )
    except Exception:
        return EmailAction("normal", "medium", "respond")


# -------------------------
# Main inference loop
# -------------------------
async def main() -> None:
    """
    Run inference for all tasks defined in TASK_GRADERS.
    """
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )

    for TASK_NAME in TASK_GRADERS.keys():  
        history: List[str] = [] 
        rewards: List[float] = []
        steps_taken = 0
        score = 0.0
        success = False

        # Initialize environment
        env = await EmailEnv.from_docker_image(IMAGE_NAME)
        log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

        try:
            # Reset environment
            result = await env.reset() # OpenENV.reset()
            last_email = result.observation.email_body
            last_reward = 0.0

            for step in range(1, MAX_STEPS + 1):
                if result.done:
                    break
                
                # Generate next message
                llm_output = get_model_message(client, step, last_email, last_reward, history)
                action = parse_llm_output(llm_output)

                # Convert model output to structured action
                llm_output = get_model_message(client, step, last_email, last_reward, history)
                action = parse_llm_output(llm_output)

                # Take step in environment
                result = await env.step(action)
                obs = result.observation

                reward = result.reward or 0.0
                done = result.done
                error = None

                # Track results
                rewards.append(reward)
                steps_taken = step
                last_email = obs.email_body
                last_reward = reward

                log_step(step=step, action=f"{action.category}/{action.priority or 'none'}/{action.reply or 'none'}", reward=reward, done=done, error=error)

                history.append(f"Step {step}: {llm_output!r} -> reward {reward:+.2f}")

                if done:
                    break
            
            # Compute final score
            score = sum(rewards) / len(rewards) if rewards else 0.0
            score = min(max(score, 0.0), 1.0)  # clamp to [0, 1]
            success = score >= SUCCESS_SCORE_THRESHOLD

        finally:
            try:
                await env.close()
            except Exception as e:
                print(f"[DEBUG] env.close() error (container cleanup): {e}", flush=True)
            log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

# -------------------------
# Entrypoint
# -------------------------
if __name__ == "__main__":
    asyncio.run(main())