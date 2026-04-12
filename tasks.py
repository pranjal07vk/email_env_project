"""
Email Triage Tasks
=================

Defines tasks of varying difficulty for the Email Triage environment.
Each task contains:
- emails: sample emails for the task
- weights: grading weights for fields (category, priority, reply)
"""

TASKS = {
    # -------------------------
    # EASY TASK
    # -------------------------
    "easy": {
        "emails": [
            {
                "subject": "Win a FREE iPhone now!!!",
                "body": "Click this link to claim your prize",
                "sender": "marketing",
                "correct": {
                    "category": "spam",
                    "priority": "low",
                    "reply": "ignore"
                }
            },
            {
                "subject": "Meeting with CEO",
                "body": "Urgent meeting tomorrow",
                "sender": "boss",
                "correct": {
                    "category": "important",
                    "priority": "high",
                    "reply": "acknowledge"
                }
            },
            {
                "subject": "Lunch plan",
                "body": "Are you free for lunch?",
                "sender": "friend",
                "correct": {
                    "category": "normal",
                    "priority": "medium",
                    "reply": "respond"
                }
            }
        ],
        "weights": {"category": 1.0},  # only category matters for scoring
    },


    # -------------------------
    # MEDIUM TASK
    # -------------------------
    "medium": {
        "emails": [
            {
                "subject": "Project deadline",
                "body": "The deadline for the project is next week",
                "sender": "manager",
                "correct": {
                    "category": "important",
                    "priority": "high",
                    "reply": "acknowledge"
                }
            },
            {
                "subject": "Team lunch",
                "body": "Let's have a team lunch on Friday",
                "sender": "team_lead",
                "correct": {
                    "category": "normal",
                    "priority": "medium",
                    "reply": "respond"
                }
            },
            {
                "subject": "Discount offer just for you",
                "body": "Get 50% off on all items",
                "sender": "marketing",
                "correct": {
                    "category": "spam",
                    "priority": "low",
                    "reply": "ignore"
                }
            },
            {
                "subject": "Quick question",
                "body": "Hey, can you take a look when you have time?",
                "sender": "manager",
                "correct": {
                    "category": "important",
                    "priority": "medium",
                    "reply": "respond"
                }
            },
            {
                "subject": "Collaboration opportunity",
                "body": "We would love to partner with you. Click here to know more.",
                "sender": "unknown",
                "correct": {
                    "category": "spam",
                    "priority": "low",
                    "reply": "ignore"
                }
            }
        ],
        "weights": {
            "category": 0.6,
            "priority": 0.4
        }
    },


    # -------------------------
    # HARD TASK
    # -------------------------
    "hard": {
        "emails": [
            {
                "subject": "Client escalation",
                "body": "Client is unhappy, needs immediate response",
                "sender": "manager",
                "correct": {
                    "category": "important",
                    "priority": "high",
                    "reply": "acknowledge"
                }
            },
            {
                "subject": "Weekend trip plan",
                "body": "Shall we go for a trip this weekend?",
                "sender": "friend",
                "correct": {
                    "category": "normal",
                    "priority": "medium",
                    "reply": "respond"
                }
            },
            {
                "subject": "You won a lottery!",
                "body": "Claim your money now by clicking here",
                "sender": "unknown",
                "correct": {
                    "category": "spam",
                    "priority": "low",
                    "reply": "ignore"
                }
            },
            {
                "subject": "Quick question",
                "body": "Hey, can you take a look when you have time?",
                "sender": "manager",
                "correct": {
                "category": "important",
                    "priority": "medium",
                    "reply": "respond"
                }
            },
            {
                "subject": "Need your help",
                "body": "I'm stuck with something urgent, please respond ASAP",
                "sender": "friend",
                "correct": {
                    "category": "important",
                    "priority": "high",
                    "reply": "respond"
                }
            },
            {
                "subject": "Update",
                "body": "Sharing this for your reference.",
                "sender": "team_lead",
                "correct": {
                    "category": "normal",
                    "priority": "low",
                    "reply": "ignore"
                }
            }
        ],
        "weights": {
            "category": 0.5,
            "priority": 0.3,
            "reply": 0.2
        }
    }
}