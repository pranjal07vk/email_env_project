# Defines different difficulty levels

TASKS = {
    "easy": {
        "description": "Classify email as spam, important, or normal",
        "required_fields": ["category"],
        "weights": {
            "category": 1.0
        }
    },

    "medium": {
        "description": "Classify email + assign priority",
        "required_fields": ["category", "priority"],
        "weights": {
            "category": 0.6,
            "priority": 0.4
        }
    },

    "hard": {
        "description": "Classify email + priority + reply",
        "required_fields": ["category", "priority", "reply"],
        "weights": {
            "category": 0.5,
            "priority": 0.3,
            "reply": 0.2
        }
    }
}