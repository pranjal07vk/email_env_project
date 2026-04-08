"""
Email Environment
=================
Defines the EmailEnv class for managing tasks, emails, and grading.
Supports async reset and step methods for OpenENV compatibility.
"""

import random
from typing import Optional

from models import EmailAction, EmailObservation, StepResult
from tasks import TASKS
from grader import grade


class EmailEnv:
    """
    Email environment for triage tasks.
    Each environment is associated with a single task (easy, medium, hard).
    """

    def __init__(self, task_name: str = "easy"):
        self.current_email = None
        self.correct_answer = None
        self.done = False
        self.task_name = task_name

    # -----------------------------
    # Reset environment
    # -----------------------------
    async def reset(self) -> StepResult:
        """
        Reset the environment to start a new episode.
        Returns an initial StepResult with observation.
        """
        self.done = False

        task_data = TASKS[self.task_name]
        emails = task_data["emails"]

        # Pick a random email for this episode
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

    # -----------------------------
    # Step the environment
    # -----------------------------
    async def step(self, action: EmailAction) -> StepResult:
        """
        Take a step in the environment based on user action.
        Returns StepResult including observation, reward, done flag, and info.
        """
        if self.done:
            return StepResult(
                observation=self._get_obs("Episode already finished"),
                reward=0.0,
                done=True,
                info={}
            )

        # Convert action to dict for grading
        action_dict = action.dict()

        # Compute reward using grader
        reward = grade(self.task_name, action_dict, self.correct_answer)

        self.done = True

        feedback = f"Correct: {self.correct_answer} | Your Score: {reward:.2f}"

        return StepResult(
            observation=self._get_obs(feedback),
            reward=reward,
            done=True,
            info={"task": self.task_name}
        )

    # -----------------------------
    # Get current environment state
    # -----------------------------
    def state(self) -> dict:
        return {
            "email": self.current_email,
            "correct": self.correct_answer,
            "done": self.done,
            "task": self.task_name
        }

    # -----------------------------
    # Helper to build observation
    # -----------------------------
    def _get_obs(self, feedback: Optional[str]) -> EmailObservation:
        return EmailObservation(
            email_subject=self.current_email["subject"],
            email_body=self.current_email["body"],
            sender=self.current_email["sender"],
            last_action_feedback=feedback
        )

    # -----------------
    # Close environment 
    # -----------------
    async def close(self):
        """
        Close environment. Placeholder for async cleanup.
        """
        pass

    # -----------------------------
    # Docker support helper
    # -----------------------------
    @classmethod
    async def from_docker_image(cls, image_name: Optional[str] = None):
        """
        Factory method to support creating environment from a Docker image.
        Currently returns a standard EmailEnv instance.
        """
        return cls()