from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    """A single unit of work the engine can prioritize."""

    id: str
    title: str
    description: str = ""
    importance: int = 3
    urgency: int = 3
    effort_estimate: float = 1.0
    stress_impact: str = "MEDIUM"
    due_date: Optional[date] = None
    time_window: Optional[str] = None
    category: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProfileConfig:
    """Configuration that tunes engine behavior for a user or context."""

    name: str
    daily_effort_budget_hours: float = 6.0
    max_big_focus: int = 3
    weights: Dict[str, float] = field(default_factory=dict)
    max_stress_load: float = 1.0


@dataclass
class ScoredTask:
    """A task with a computed score and inspectable factor breakdown."""

    task: Task
    score: float
    breakdown: Dict[str, float]


@dataclass
class Plan:
    """Engine output for a single run."""

    profile_name: str
    timestamp: datetime
    big_focus: List[Task]
    support_tasks: List[Task]
    parked_tasks: List[Task]
    decision_summary: str
    engine_version: str = "0.1.0"


@dataclass
class RunLog:
    """Minimal structured record for local audit or ledger export."""

    timestamp: datetime
    profile_name: str
    input_task_count: int
    big_focus_ids: List[str]
    engine_version: str
    decision_summary: str
