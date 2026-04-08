from tasks import TASKS


def grade(task_name: str, action: dict, correct: dict) -> float:
    """
    Returns score between 0.0 and 1.0
    """

    task = TASKS.get(task_name)

    if not task:
        return 0.01

    score = 0.0
    weights = task["weights"]

    for field, weight in weights.items():
        if field in action and action[field] == correct.get(field):
            score += weight

    # clamp to [0,1]
    if score >= 1.0:
        score = 0.99
    elif score <= 0.0:
        score = 0.01

    return score

TASK_GRADERS = {
    "easy": grade,
    "medium": grade,
    "hard": grade
}