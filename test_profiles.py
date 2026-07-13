import json
from pathlib import Path


PROFILE_NAMES = {
    "student.json",
    "worker_double_shift.json",
    "founder.json",
}


def test_profiles_are_valid_json_objects():
    base_dir = Path(__file__).resolve().parent
    discovered = {path.name for path in base_dir.glob("*.json") if path.name != "sample_day.json"}

    assert PROFILE_NAMES.issubset(discovered)

    for name in PROFILE_NAMES:
        path = base_dir / name
        with path.open("r", encoding="utf-8") as profile_file:
            profile = json.load(profile_file)

        assert isinstance(profile, dict)
        assert profile.get("name")
        assert profile.get("daily_effort_budget_hours", 0) > 0
        assert profile.get("max_big_focus", 0) >= 1
