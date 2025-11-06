import json
import os


def test_profiles_are_valid_json():
    base_dir = os.path.join(os.path.dirname(__file__), "..", "engine", "profiles")
    for name in os.listdir(base_dir):
        if not name.endswith(".json"):
            continue
        path = os.path.join(base_dir, name)
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
