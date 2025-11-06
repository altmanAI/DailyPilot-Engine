from datetime import datetime
from typing import List
from .models import ScoredTask, ProfileConfig, Plan, Task


def build_daily_plan(scored_tasks: List[ScoredTask], profile: ProfileConfig) -> Plan:
    """Turn scored tasks into a daily plan.

    Strategy:
    - Walk tasks in order of score.
    - Add tasks to big_focus until we hit max_big_focus or run out.
    - Add additional tasks as support if there is budget left.
    - Anything that does not fit within the effort budget is parked.
    """

    effort_budget = profile.daily_effort_budget_hours
    used_effort = 0.0

    big_focus: List[Task] = []
    support_tasks: List[Task] = []
    parked_tasks: List[Task] = []

    for idx, scored in enumerate(scored_tasks):
        task = scored.task
        task_effort = max(0.0, task.effort_estimate)

        if used_effort + task_effort <= effort_budget:
            used_effort += task_effort
            if len(big_focus) < profile.max_big_focus:
                big_focus.append(task)
            else:
                support_tasks.append(task)
        else:
            parked_tasks.append(task)

    summary = (
        f"Selected {len(big_focus)} big focus task(s) and "
        f"{len(support_tasks)} support task(s) within "
        f"{used_effort:.1f}h of a {effort_budget:.1f}h budget. "
        f"Parked {len(parked_tasks)} task(s)."
    )

    plan = Plan(
        profile_name=profile.name,
        timestamp=datetime.utcnow(),
        big_focus=big_focus,
        support_tasks=support_tasks,
        parked_tasks=parked_tasks,
        decision_summary=summary,
    )
    return plan
