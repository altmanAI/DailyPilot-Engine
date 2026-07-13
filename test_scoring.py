from datetime import date, timedelta

from models import ProfileConfig, Task
from scoring import score_tasks


def test_higher_importance_scores_higher():
    profile = ProfileConfig(name="test_profile")
    low = Task(id="low", title="Low importance", importance=1, urgency=3)
    high = Task(id="high", title="High importance", importance=5, urgency=3)

    scored = score_tasks([low, high], profile)

    assert scored[0].task.id == "high"


def test_nearer_deadline_scores_higher_when_other_fields_match():
    profile = ProfileConfig(name="test_profile")
    due_today = Task(
        id="today",
        title="Due today",
        due_date=date.today(),
        stress_impact="LOW",
    )
    due_later = Task(
        id="later",
        title="Due later",
        due_date=date.today() + timedelta(days=14),
        stress_impact="LOW",
    )

    scored = score_tasks([due_later, due_today], profile)

    assert scored[0].task.id == "today"


def test_score_includes_inspectable_breakdown():
    profile = ProfileConfig(name="test_profile")
    task = Task(id="task", title="Task")

    result = score_tasks([task], profile)[0]

    assert set(result.breakdown) == {
        "importance_n",
        "urgency_n",
        "effort_n",
        "deadline_n",
        "stress_penalty",
        "base_score",
    }
