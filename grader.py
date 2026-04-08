"""
Grader Module
=============
Provides scoring functionality for tasks in the Email Triage environment.
Also defines TASK_GRADERS mapping for all supported tasks.
"""

from tasks import TASKS


def grade(task_name: str, action: dict, correct: dict) -> float:
    """
    Compute a normalized score for a given action compared to the correct answer.

    Args:
        task_name (str): Name of the task ('easy', 'medium', 'hard').
        action (dict): Action performed by the user/model.
        correct (dict): Correct action for this email.

    Returns:
        float: Score between 0.01 and 0.99.
    """

    task = TASKS.get(task_name)

    if not task:
        return 0.01

    score = 0.0
    weights = task["weights"]

    for field, weight in weights.items():
        if field in action and action[field] == correct.get(field):
            score += weight

    # Clamp score to (0, 1)
    if score >= 1.0:
        score = 0.99
    elif score <= 0.0:
        score = 0.01

    return score

# Mapping of tasks to grader functions
TASK_GRADERS = {
    "easy": grade,
    "medium": grade,
    "hard": grade
}