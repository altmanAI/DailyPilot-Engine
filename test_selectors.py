from engine.core.models import Task, ProfileConfig, ScoredTask
from engine.core.selectors import build_daily_plan


def test_big_focus_respects_budget_and_limit():
    profile = ProfileConfig(name="test_profile", daily_effort_budget_hours=3.0, max_big_focus=2)

    tasks = [
        ScoredTask(task=Task(id="a", title="A", effort_estimate=1.0), score=1.0, breakdown={}),
        ScoredTask(task=Task(id="b", title="B", effort_estimate=1.0), score=0.9, breakdown={}),
        ScoredTask(task=Task(id="c", title="C", effort_estimate=2.0), score=0.8, breakdown={}),
    ]

    plan = build_daily_plan(tasks, profile)
    assert len(plan.big_focus) <= profile.max_big_focus
    total_effort = sum(t.effort_estimate for t in plan.big_focus + plan.support_tasks)
    assert total_effort <= profile.daily_effort_budget_hours + 1e-6
