from datetime import date
from typing import List, Dict
from .models import Task, ProfileConfig, ScoredTask


def _normalize(value: float, min_value: float, max_value: float) -> float:
    if max_value == min_value:
        return 0.0
    value = max(min_value, min(max_value, value))
    return (value - min_value) / (max_value - min_value)


def _stress_penalty(stress_impact: str) -> float:
    mapping = {
        "LOW": 0.0,
        "MEDIUM": 0.1,
        "HIGH": 0.25,
    }
    return mapping.get(stress_impact.upper(), 0.1)


def score_tasks(tasks: List[Task], profile: ProfileConfig) -> List[ScoredTask]:
    """Score tasks for a given profile.

    This is a simple, transparent scoring model meant as a solid starting point.
    """

    weights: Dict[str, float] = {
        "importance": 0.4,
        "urgency": 0.3,
        "effort": 0.2,
        "deadline": 0.1,
    }
    weights.update(profile.weights or {})

    today = date.today()
    scored: List[ScoredTask] = []

    for task in tasks:
        importance_n = _normalize(task.importance, 1, 5)
        urgency_n = _normalize(task.urgency, 1, 5)
        effort_n = 1.0 - _normalize(task.effort_estimate, 0.25, 8.0)

        if task.due_date:
            days_to_due = (task.due_date - today).days
            if days_to_due <= 0:
                deadline_n = 1.0
            elif days_to_due >= 14:
                deadline_n = 0.0
            else:
                deadline_n = 1.0 - (days_to_due / 14.0)
        else:
            deadline_n = 0.0

        base_score = (
            weights["importance"] * importance_n
            + weights["urgency"] * urgency_n
            + weights["effort"] * effort_n
            + weights["deadline"] * deadline_n
        )

        penalty = _stress_penalty(task.stress_impact)
        final_score = max(0.0, base_score - penalty)

        breakdown = {
            "importance_n": importance_n,
            "urgency_n": urgency_n,
            "effort_n": effort_n,
            "deadline_n": deadline_n,
            "stress_penalty": penalty,
            "base_score": base_score,
        }

        scored.append(ScoredTask(task=task, score=final_score, breakdown=breakdown))

    scored.sort(key=lambda st: st.score, reverse=True)
    return scored
