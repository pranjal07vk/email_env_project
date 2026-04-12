"""
Email Environment
=================
Defines the EmailEnv class for managing tasks, emails, and grading.
Supports async reset and step methods for OpenENV compatibility.
"""

import random
from typing import Optional, List

from models import EmailAction, EmailObservation, StepResult
from tasks import TASKS
from grader import grade


class EmailEnv:
    """
    Email environment for triage tasks.
    Each environment is associated with a single task (easy, medium, hard).
    """

    def __init__(self, task_name: str = "easy"):
        self.task_name = task_name
        self.done = False
        self.inbox: List[dict] = []
        self.current_index = 0
        self.correct_answers: List[dict] = []
        self.total_reward = 0.0

    # -----------------------------
    # Reset environment
    # -----------------------------
    async def reset(self) -> StepResult:
        """
        Reset the environment to start a new episode.
        Returns an initial StepResult with observation.
        """
        self.done = False
        self.current_index = 0
        self.total_reward = 0.0

        task_data = TASKS[self.task_name]
        emails = task_data["emails"]

        # Pick a multiple emails for this episode
        k = random.randint(3, min(5, len(emails)))
        self.inbox = random.sample(emails, k)
        self.correct_answers = [email["correct"] for email in self.inbox]

        return StepResult(
            observation=self._get_obs(f"Task: {self.task_name} | Email 1/{len(self.inbox)}"),
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
        
        current_email = self.inbox[self.current_index]
        correct = self.correct_answers[self.current_index]

        # Convert action to dict for grading
        action_dict = action.model_dump()

        # Compute reward using grader
        reward = grade(self.task_name, action_dict, self.correct_answer)

        penalty = 0.0

        if correct["category"] == "important" and action_dict.get("category") != "important":
            penalty -= 0.3

        # replied to spam
        if correct["category"] == "spam" and action_dict.get("reply") not in ["ignore", None]:
            penalty -= 0.2

        # wrong priority for urgent
        if correct.get("priority") == "high" and action_dict.get("priority") != "high":
            penalty -= 0.2

        reward = max(0.01, min(0.99, reward + penalty))

        self.total_reward += reward
        self.current_index += 1

        if self.current_index >= len(self.inbox):
            self.done = True

        feedback = f"Step {self.current_index}: reward={reward:.2f}"

        return StepResult(
            observation=self._get_obs(feedback),
            reward=reward,
            done=self.done,
            info={"task": self.task_name}
        )
    
    # -----------------------------
    # Helper to build observation
    # -----------------------------
    def _get_obs(self, feedback: Optional[str]) -> EmailObservation:
        current_email = self.inbox[self.current_index]

        return EmailObservation(
            email_subject=current_email["subject"],
            email_body=current_email["body"],
            sender=current_email["sender"],
            last_action_feedback=feedback
        )

    # -----------------------------
    # Get current environment state
    # -----------------------------
    def state(self) -> dict:
        return {
            "inbox": self.inbox,
            "current_index": self.current_index,
            "done": self.done,
            "task": self.task_name
        }

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