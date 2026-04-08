🐨 Email Triage Environment
Color Theme: Pink → Red
SDK: Docker (optional)
Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

Overview

Email Triage Env is a lightweight environment for testing automated email triage agents. The environment simulates a simple inbox with emails of varying importance and types. Your agent’s task is to classify each email as spam, important, or normal, assign a priority, and optionally provide a reply action.

The environment provides rewards based on correct classification, making it suitable for reinforcement learning or rule-based AI experiments.

This project includes:

A REST API (FastAPI) for interacting with the environment.
An inference script that demonstrates automated interaction with the environment using a language model.
Predefined tasks of different difficulty levels: easy, medium, and hard.
Grading logic that scores actions based on accuracy.


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


Example Agent Logic

models.py provides a simple rule-based agent:

    if sender == "marketing":
        return EmailAction("spam", "low", "ignore")
    elif sender == "boss":
        return EmailAction("important", "high", "acknowledge")
    else:
        return EmailAction("normal", "medium", "respond")

You can replace this logic with a custom AI model or LLM using inference.py.


Notes

The project is hackathon-ready: includes environment, API, example inference, grading, and tasks.
Optional Docker support: use EmailEnv.from_docker_image(image_name) if you want containerized execution.
Keep inference.py and API logs visible during judging for validation.

