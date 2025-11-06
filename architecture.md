# DailyPilot-Engine – Architecture

The engine is intentionally small and composable:

- `engine.core.models` – data models (Task, ProfileConfig, Plan, RunLog)
- `engine.core.scoring` – scoring logic
- `engine.core.selectors` – turns scored tasks into a daily plan
- `engine.profiles` – JSON configs for different life contexts
- `integrations.cli` – command-line harness for experiments and testing
