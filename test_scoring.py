import datetime
from engine.core.models import Task, ProfileConfig
from engine.core.scoring import score_tasks


def test_higher_importance_scores_higher():
    profile = ProfileConfig(name="test_profile")
    low = Task(id="low", title="Low importance", importance=1, urgency=3)
    high = Task(id="high", title="High importance", importance=5, urgency=3)

    scored = score_tasks([low, high], profile)
    assert scored[0].task.id == "high"
