from models import ProfileConfig, ScoredTask, Task
from selectors import build_daily_plan


def _scored(task_id: str, effort: float, score: float) -> ScoredTask:
    return ScoredTask(
        task=Task(id=task_id, title=task_id.upper(), effort_estimate=effort),
        score=score,
        breakdown={},
    )


def test_big_focus_respects_budget_and_limit():
    profile = ProfileConfig(
        name="test_profile",
        daily_effort_budget_hours=3.0,
        max_big_focus=2,
    )
    tasks = [
        _scored("a", 1.0, 1.0),
        _scored("b", 1.0, 0.9),
        _scored("c", 2.0, 0.8),
    ]

    plan = build_daily_plan(tasks, profile)

    assert len(plan.big_focus) <= profile.max_big_focus
    total_effort = sum(
        task.effort_estimate for task in plan.big_focus + plan.support_tasks
    )
    assert total_effort <= profile.daily_effort_budget_hours + 1e-6


def test_tasks_that_exceed_budget_are_parked():
    profile = ProfileConfig(
        name="test_profile",
        daily_effort_budget_hours=1.0,
        max_big_focus=1,
    )
    tasks = [
        _scored("fits", 1.0, 1.0),
        _scored("too_large", 2.0, 0.9),
    ]

    plan = build_daily_plan(tasks, profile)

    assert [task.id for task in plan.big_focus] == ["fits"]
    assert [task.id for task in plan.parked_tasks] == ["too_large"]
