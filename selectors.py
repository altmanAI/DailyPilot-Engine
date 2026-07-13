from datetime import datetime
from typing import List

from models import Plan, ProfileConfig, ScoredTask, Task


def build_daily_plan(scored_tasks: List[ScoredTask], profile: ProfileConfig) -> Plan:
    """Build a bounded plan from tasks already ordered by score.

    The selector respects the configured effort budget and focus-task limit.
    It does not understand calendar conflicts, dependencies, safety-critical
    obligations, or consequences beyond the fields supplied by the caller.
    A human should review the resulting plan before acting on it.
    """

    effort_budget = profile.daily_effort_budget_hours
    used_effort = 0.0

    big_focus: List[Task] = []
    support_tasks: List[Task] = []
    parked_tasks: List[Task] = []

    for scored in scored_tasks:
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

    return Plan(
        profile_name=profile.name,
        timestamp=datetime.utcnow(),
        big_focus=big_focus,
        support_tasks=support_tasks,
        parked_tasks=parked_tasks,
        decision_summary=summary,
    )
