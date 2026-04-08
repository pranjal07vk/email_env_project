import random
from typing import Optional

from models import EmailAction, EmailObservation, StepResult
from tasks import TASKS
from grader import grade


class EmailEnv:
    def __init__(self, task_name: str = "easy"):
        self.current_email = None
        self.correct_answer = None
        self.done = False
        self.task_name = task_name

    # -------- RESET --------
    async def reset(self) -> StepResult:
        self.done = False

        task_data = TASKS[self.task_name]
        emails = task_data["emails"]

        self.current_email = random.choice(emails)
        self.correct_answer = self.current_email["correct"]

        obs = EmailObservation(
            email_subject=self.current_email["subject"],
            email_body=self.current_email["body"],
            sender=self.current_email["sender"],
            last_action_feedback=f"Task: {self.task_name}"
        )

        return StepResult(
            observation=obs,
            reward=0.0,
            done=False,
            info={"task": self.task_name}
        )

    # -------- STEP --------
    async def step(self, action: EmailAction) -> StepResult:
        if self.done:
            return StepResult(
                observation=self._get_obs("Episode already finished"),
                reward=0.0,
                done=True,
                info={}
            )

        # Convert action to dict for grading
        action_dict = action.dict()

        # Use grader
        reward = grade(self.task_name, action_dict, self.correct_answer)

        self.done = True

        feedback = f"Correct: {self.correct_answer} | Your Score: {reward:.2f}"

        return StepResult(
            observation=self._get_obs(feedback),
            reward=reward,
            done=True,
            info={"task": self.task_name}
        )

    # -------- STATE --------
    def state(self) -> dict:
        return {
            "email": self.current_email,
            "correct": self.correct_answer,
            "done": self.done,
            "task": self.task_name
        }

    # -------- HELPER --------
    def _get_obs(self, feedback: Optional[str]) -> EmailObservation:
        return EmailObservation(
            email_subject=self.current_email["subject"],
            email_body=self.current_email["body"],
            sender=self.current_email["sender"],
            last_action_feedback=feedback
        )

    # -------- CLOSE --------
    async def close(self):
        pass

    # -------- DOCKER SUPPORT --------
    @classmethod
    async def from_docker_image(cls, image_name: Optional[str] = None):
        return cls()