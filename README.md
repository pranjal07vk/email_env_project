---
title: Email Triage Env
emoji: 🐨
colorFrom: pink
colorTo: red
sdk: docker
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference


## Overview

Email Triage Env is a **sequential decision-making environment** designed to evaluate intelligent agents in realistic inbox management scenarios.

Unlike simple classification tasks, this environment requires agents to:

- Process multiple emails within a single episode
- Make context-aware decisions under uncertainty
- Balance trade-offs between urgency, importance, and relevance
- Handle ambiguous and noisy real-world email patterns

The environment is specifically designed for:
- Reinforcement Learning experimentation
- LLM-based decision-making systems
- Human-like reasoning under partial information

Each episode simulates a mini inbox, where incorrect decisions (e.g., missing urgent emails or responding to spam) result in penalties, making the task non-trivial and strategy-dependent.

## Key Features

- **Multi-step Episodes**  
  Agents process 3–5 emails sequentially in a single episode.

- **Stateful Environment**  
  Decisions affect cumulative reward across the episode.

- **Reward + Penalty System**  
  - Missing important emails → penalty  
  - Responding to spam → penalty  
  - Incorrect prioritization → penalty  

- **Ambiguous & Realistic Emails**  
  Includes uncertain and noisy inputs that require reasoning, not just keyword matching.

- **LLM-Compatible Design**  
  Supports structured LLM outputs for decision-making pipelines.

Project Structure
.
├── app.py            # FastAPI server for the email environment
├── env.py            # Core environment logic (reset, step, state)
├── models.py         # EmailAction, EmailObservation, StepResult, and predict logic
├── graders.py        # Task grading functions
├── tasks.py          # Task definitions and emails
├── inference.py      # Example inference loop using OpenAI / LLM
├── README.md         # This file
└── requirements.txt  # Python dependencies 


Setup Instructions

1. Clone the repo:

    git clone <your-repo-url>
    cd email-triage-env

2. Install dependencies:

    pip install -r requirements.txt

3. Environment Variables:
    Set the following environment variables for inference or API calls:

    export API_BASE_URL="https://router.huggingface.co/v1"
    export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
    export API_KEY="<your-hf-api-key>"


Running the API

Start the FastAPI server:
    python app.py

Endpoints:

| Endpoint | Method | Description                                                          |
| -------- | ------ | -------------------------------------------------------------------- |
| `/`      | GET    | Health check: returns `{ "message": "Email Triage API is running" }` |
| `/reset` | POST   | Resets the environment and returns the first email observation       |
| `/step`  | POST   | Takes an action and returns the next observation and reward          |

Example request to /step:

{
  "category": "spam",
  "priority": "low",
  "reply": "ignore"
}


Running Inference

inference.py demonstrates an automated agent interacting with all tasks sequentially.

    python inference.py

Output format (stdout):

    [START] task=easy env=email_triage_env model=Qwen2.5
    [STEP] step=1 action=spam/low/ignore reward=1.00 done=false error=null
    [STEP] step=2 action=important/high/acknowledge reward=0.00 done=true error=null
    [END] success=true steps=2 score=0.75 rewards=1.00,0.00

[START] – Marks beginning of a task episode
[STEP] – Shows each action taken and the reward
[END] – Summary of success, total steps, and scores


Tasks & Difficulty

    | Task   | Difficulty   | Features                                                            |
    | ------ | ------------ | ------------------------------------------------------------------- |
    | easy   | Beginner     | Only email category matters; reward based on `category` correctness |
    | medium | Intermediate | Category + priority weighted; simple textual emails                 |
    | hard   | Advanced     | Category, priority, and reply considered; mixed and tricky emails   |


Grading & Rewards

Each field (category, priority, reply) is weighted per task.
Score is normalized to [0.0, 1.0].
Episode is considered successful if score ≥ 0.1.


## 🤖 Agent Design

The environment supports both rule-based and LLM-based agents.

The provided `inference.py` demonstrates:
- LLM-driven decision making
- Structured parsing of model outputs into actions
- Robust fallback handling for invalid responses

Agents are expected to interpret email context and produce:

category: spam / important / normal  
priority: high / medium / low  
reply: ignore / acknowledge / respond


## Conclusion

This environment goes beyond simple classification tasks by introducing:

- Sequential decision making
- Real-world ambiguity
- Strategy-dependent rewards

It provides a lightweight yet expressive testbed for evaluating intelligent agents in practical scenarios.

