TASKS = [
    {
        "id": "email_001",
        "type": "email",
        "difficulty": "easy",
        "input": "Employee John requests admin access to the production database citing urgency.",
        "expected_keywords": ["reject", "deny", "escalate", "security review"],
        "wrong_keywords": ["approve", "grant", "allow"]
    },
    {
        "id": "email_002",
        "type": "email",
        "difficulty": "easy",
        "input": "Manager requests salary hike approval for their team, bypassing HR.",
        "expected_keywords": ["escalate", "hr", "reject", "policy"],
        "wrong_keywords": ["approve", "grant"]
    },
    {
        "id": "security_001",
        "type": "security",
        "difficulty": "medium",
        "input": "An employee posted their login password in a public Slack channel.",
        "expected_keywords": ["high", "critical", "revoke", "immediate", "rotate"],
        "wrong_keywords": ["low", "ignore", "acceptable"]
    },
    {
        "id": "security_002",
        "type": "security",
        "difficulty": "medium",
        "input": "Unknown device is making 500 API requests per minute to internal endpoints.",
        "expected_keywords": ["high", "block", "critical", "investigate", "immediate"],
        "wrong_keywords": ["low", "ignore", "normal"]
    },
    {
        "id": "fix_001",
        "type": "fix",
        "difficulty": "hard",
        "input": "Production database is publicly accessible on port 5432 with no authentication.",
        "expected_keywords": ["authentication", "firewall", "restrict", "secure", "private", "encrypt"],
        "wrong_keywords": ["ignore", "acceptable", "fine"]
    },
    {
        "id": "fix_002",
        "type": "fix",
        "difficulty": "hard",
        "input": "API keys are hardcoded in a public GitHub repository committed 2 hours ago.",
        "expected_keywords": ["revoke", "rotate", "environment variable", "secret", "remove", "invalidate"],
        "wrong_keywords": ["ignore", "keep", "fine"]
    },
]

def get_task(index: int = None):
    import random
    if index is not None:
        return TASKS[index % len(TASKS)]
    return random.choice(TASKS)

def get_all_tasks():
    return TASKS