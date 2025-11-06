import argparse
import json
import os
from datetime import datetime
from typing import List

from engine.core.models import Task, ProfileConfig, RunLog
from engine.core.scoring import score_tasks
from engine.core.selectors import build_daily_plan


def load_profile(profile_name: str) -> ProfileConfig:
    base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "engine", "profiles")
    path = os.path.join(base_dir, f"{profile_name}.json")
    if not os.path.exists(path):
        raise SystemExit(f"Profile not found: {profile_name} (expected {path})")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return ProfileConfig(**data)


def load_tasks(path: str) -> List[Task]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    tasks: List[Task] = []
    for item in raw:
        tasks.append(Task(**item))
    return tasks


def save_log(plan, profile: ProfileConfig, log_dir: str = "logs") -> str:
    os.makedirs(log_dir, exist_ok=True)
    log = RunLog(
        timestamp=plan.timestamp,
        profile_name=profile.name,
        input_task_count=len(plan.big_focus) + len(plan.support_tasks) + len(plan.parked_tasks),
        big_focus_ids=[t.id for t in plan.big_focus],
        engine_version=plan.engine_version,
        decision_summary=plan.decision_summary,
    )
    record = {
        "timestamp": log.timestamp.isoformat() + "Z",
        "profile": log.profile_name,
        "input_task_count": log.input_task_count,
        "big_focus_ids": log.big_focus_ids,
        "engine_version": log.engine_version,
        "decision_summary": log.decision_summary,
    }
    filename = f"dailypilot_run_{log.timestamp.strftime('%Y%m%dT%H%M%S')}.json"
    path = os.path.join(log_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run DailyPilot-Engine on a JSON task file.")
    parser.add_argument("tasks", help="Path to a JSON file containing a list of tasks.")
    parser.add_argument(
        "--profile",
        default="worker_double_shift",
        help="Profile name to use (default: worker_double_shift).",
    )
    args = parser.parse_args()

    profile = load_profile(args.profile)
    tasks = load_tasks(args.tasks)

    scored = score_tasks(tasks, profile)
    plan = build_daily_plan(scored, profile)

    print("")
    print("=== DailyPilot-Engine Plan ===")
    print(f"Profile: {plan.profile_name}")
    print(f"Timestamp (UTC): {plan.timestamp.isoformat()}Z")
    print("")
    print("Today’s Focus:")
    for t in plan.big_focus:
        print(f"- {t.title} (id={t.id})")

    if plan.support_tasks:
        print("")
        print("Support Tasks:")
        for t in plan.support_tasks:
            print(f"- {t.title} (id={t.id})")

    if plan.parked_tasks:
        print("")
        print("Parked Tasks:")
        for t in plan.parked_tasks:
            print(f"- {t.title} (id={t.id})")

    print("")
    print("Summary:")
    print(plan.decision_summary)

    log_path = save_log(plan, profile)
    print("")
    print(f"Log written to: {log_path}")


if __name__ == "__main__":
    main()
