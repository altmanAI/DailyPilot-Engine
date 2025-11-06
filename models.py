from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional, Dict, Any


@dataclass
class Task:
    """A single unit of work the engine can prioritize."""

    id: str
    title: str
    description: str = ""
    importance: int = 3
    urgency: int = 3
    effort_estimate: float = 1.0  # in hours
    stress_impact: str = "MEDIUM"  # LOW | MEDIUM | HIGH
    due_date: Optional[date] = None
    time_window: Optional[str] = None  # free text for now
    category: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProfileConfig:
    """Configuration that tunes how the engine behaves for a user or context."""

    name: str
    daily_effort_budget_hours: float = 6.0
    max_big_focus: int = 3
    weights: Dict[str, float] = field(default_factory=dict)
    max_stress_load: float = 1.0  # 0–1 scale


@dataclass
class ScoredTask:
    """Wrapper around a Task with a computed score and explanation."""

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
    """Minimal structured log record, suitable for AINet / ledger export."""

    timestamp: datetime
    profile_name: str
    input_task_count: int
    big_focus_ids: List[str]
    engine_version: str
    decision_summary: str
