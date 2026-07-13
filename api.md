# DailyPilot Engine Python Reference

## Import the core interface

```python
from engine.core import ProfileConfig, Task, build_daily_plan, score_tasks
```

Direct module imports are also available:

```python
from engine.core.models import ProfileConfig, Task
from engine.core.scoring import score_tasks
from engine.core.selectors import build_daily_plan
```

This is a reference interface at version `0.1.0`, not a guarantee of long-term package compatibility. Breaking changes must be versioned and documented.

## Minimal example

```python
from engine.core import ProfileConfig, Task, build_daily_plan, score_tasks

profile = ProfileConfig(
    name="example",
    daily_effort_budget_hours=3.0,
    max_big_focus=2,
)

tasks = [
    Task(
        id="prepare_demo",
        title="Prepare product demo",
        importance=5,
        urgency=4,
        effort_estimate=2.0,
        stress_impact="MEDIUM",
    ),
    Task(
        id="organize_notes",
        title="Organize notes",
        importance=3,
        urgency=2,
        effort_estimate=0.5,
        stress_impact="LOW",
    ),
]

scored = score_tasks(tasks, profile)
plan = build_daily_plan(scored, profile)

for result in scored:
    print(result.task.title, result.score, result.breakdown)

print([task.title for task in plan.big_focus])
print([task.title for task in plan.support_tasks])
print([task.title for task in plan.parked_tasks])
```

## Data contracts

### `Task`

Required:

- `id: str`
- `title: str`

Selected optional fields:

- `description: str`
- `importance: int` — intended range 1–5
- `urgency: int` — intended range 1–5
- `effort_estimate: float` — hours
- `stress_impact: str` — `LOW`, `MEDIUM`, or `HIGH`
- `due_date: date | None`
- `time_window: str | None`
- `category: str | None`
- `meta: dict`

The dataclass does not currently enforce every intended range. Integrators must validate untrusted input before constructing tasks.

### `ProfileConfig`

- `name: str`
- `daily_effort_budget_hours: float`
- `max_big_focus: int`
- `weights: dict[str, float]`
- `max_stress_load: float`

`max_stress_load` is present in the data model but is not currently enforced by the selector. Do not represent it as an active safety constraint.

### `ScoredTask`

Contains the original task, final score, and factor breakdown.

### `Plan`

Contains focus tasks, support tasks, parked tasks, a UTC timestamp, summary, profile name, and engine version.

## Integration requirements

Before using this reference logic in a product:

- validate all untrusted input;
- document code and configuration versions;
- preserve score explanations;
- provide human correction and override;
- add privacy, authentication, authorization, abuse, and incident controls appropriate to the product;
- evaluate behavior on representative and adverse scenarios;
- do not use the output as sole authority for consequential decisions;
- document monitoring and rollback.
