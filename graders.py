from models import Reward

def evaluate(task: dict, output: str) -> Reward:
    """
    Deterministic grader — scores 0.0 to 1.0 with breakdown.
    Rewards incremental progress, not just final answer.
    """
    output_lower = output.lower()
    score = 0.0
    breakdown = {}
    feedback_parts = []

    expected = task.get("expected_keywords", [])
    wrong = task.get("wrong_keywords", [])
    task_type = task.get("type", "")

    # 1. Keyword matching (0.0 - 0.6)
    matched = [kw for kw in expected if kw in output_lower]
    keyword_score = min(len(matched) / max(len(expected), 1), 1.0) * 0.6
    breakdown["keyword_match"] = round(keyword_score, 2)
    score += keyword_score

    if matched:
        feedback_parts.append(f"Correct keywords found: {matched}")
    else:
        feedback_parts.append("No expected keywords found in response")

    # 2. Wrong keyword penalty (up to -0.3)
    wrong_matched = [kw for kw in wrong if kw in output_lower]
    penalty = len(wrong_matched) * 0.15
    breakdown["penalty"] = round(-penalty, 2)
    score = max(0.0, score - penalty)

    if wrong_matched:
        feedback_parts.append(f"Penalized for: {wrong_matched}")

    # 3. Response length quality (0.0 - 0.2)
    word_count = len(output.split())
    if word_count >= 20:
        length_score = 0.2
    elif word_count >= 10:
        length_score = 0.1
    else:
        length_score = 0.0
    breakdown["response_quality"] = round(length_score, 2)
    score += length_score
    feedback_parts.append(f"Response length: {word_count} words")

    # 4. Task-specific bonus (0.0 - 0.2)
    bonus = 0.0
    if task_type == "email" and any(w in output_lower for w in ["policy", "procedure", "review"]):
        bonus = 0.2
        feedback_parts.append("Bonus: Referenced policy/procedure")
    elif task_type == "security" and any(w in output_lower for w in ["immediately", "urgent", "asap", "now"]):
        bonus = 0.2
        feedback_parts.append("Bonus: Indicated urgency")
    elif task_type == "fix" and any(w in output_lower for w in ["policy", "rule", "procedure", "standard"]):
        bonus = 0.2
        feedback_parts.append("Bonus: Included policy recommendation")
    breakdown["task_bonus"] = round(bonus, 2)
    score = min(1.0, score + bonus)

    final_score = round(score, 2)
    return Reward(
        score=final_score,
        breakdown=breakdown,
        feedback=" | ".join(feedback_parts)
    )