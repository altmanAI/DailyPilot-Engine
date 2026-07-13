import argparse
import json
from datetime import date, timezone
from pathlib import Path
from typing import List

from models import ProfileConfig, RunLog, Task
from scoring import score_tasks
from selectors import build_daily_plan

BASE_DIR = Path(__file__).resolve().parent


def load_profile(profile_name: str) -> ProfileConfig:
    path = BASE_DIR / f"{profile_name}.json"
    if not path.exists():
        raise SystemExit(f"Profile not found: {profile_name} (expected {path})")

    with path.open("r", encoding="utf-8") as profile_file:
        data = json.load(profile_file)

    if not isinstance(data, dict):
        raise SystemExit(f"Profile must be a JSON object: {path}")

    return ProfileConfig(**data)


def load_tasks(path: str) -> List[Task]:
    task_path = Path(path)
    with task_path.open("r", encoding="utf-8") as task_file:
        raw = json.load(task_file)

    if not isinstance(raw, list):
        raise SystemExit(f"Task input must be a JSON array: {task_path}")

    tasks: List[Task] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise SystemExit(f"Task at index {index} must be a JSON object")

        task_data = dict(item)
        due_date = task_data.get("due_date")
        if isinstance(due_date, str):
            try:
                task_data["due_date"] = date.fromisoformat(due_date)
            except ValueError as exc:
                raise SystemExit(
                    f"Task at index {index} has an invalid due_date; use YYYY-MM-DD"
                ) from exc

        tasks.append(Task(**task_data))

    return tasks


def _utc_timestamp(timestamp) -> str:
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def save_log(plan, profile: ProfileConfig, log_dir: str = "logs") -> str:
    log_directory = Path(log_dir)
    log_directory.mkdir(parents=True, exist_ok=True)

    log = RunLog(
        timestamp=plan.timestamp,
        profile_name=profile.name,
        input_task_count=len(plan.big_focus) + len(plan.support_tasks) + len(plan.parked_tasks),
        big_focus_ids=[task.id for task in plan.big_focus],
        engine_version=plan.engine_version,
        decision_summary=plan.decision_summary,
    )

    record = {
        "timestamp": _utc_timestamp(log.timestamp),
        "profile": log.profile_name,
        "input_task_count": log.input_task_count,
        "big_focus_ids": log.big_focus_ids,
        "engine_version": log.engine_version,
        "decision_summary": log.decision_summary,
    }

    filename = f"dailypilot_run_{log.timestamp.strftime('%Y%m%dT%H%M%S')}.json"
    path = log_directory / filename
    with path.open("w", encoding="utf-8") as log_file:
        json.dump(record, log_file, indent=2)

    return str(path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the DailyPilot reference engine on a JSON task file."
    )
    parser.add_argument("tasks", help="Path to a JSON array of tasks")
    parser.add_argument(
        "--profile",
        default="worker_double_shift",
        help="Profile JSON name without extension (default: worker_double_shift)",
    )
    args = parser.parse_args()

    profile = load_profile(args.profile)
    tasks = load_tasks(args.tasks)

    scored = score_tasks(tasks, profile)
    plan = build_daily_plan(scored, profile)

    print("\n=== DailyPilot-Engine Plan ===")
    print(f"Profile: {plan.profile_name}")
    print(f"Timestamp (UTC): {_utc_timestamp(plan.timestamp)}")

    print("\nToday’s Focus:")
    for task in plan.big_focus:
        print(f"- {task.title} (id={task.id})")

    if plan.support_tasks:
        print("\nSupport Tasks:")
        for task in plan.support_tasks:
            print(f"- {task.title} (id={task.id})")

    if plan.parked_tasks:
        print("\nParked Tasks:")
        for task in plan.parked_tasks:
            print(f"- {task.title} (id={task.id})")

    print("\nSummary:")
    print(plan.decision_summary)

    log_path = save_log(plan, profile)
    print(f"\nLog written to: {log_path}")


if __name__ == "__main__":
    main()
