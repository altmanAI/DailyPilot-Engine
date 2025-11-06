# DailyPilot-Engine

DailyPilot-Engine is the prioritization core of **DailyPilot by AltmanAI (Altman Family Group, LLC)**.  
It takes messy tasks and shifting schedules and turns them into a realistic, focused daily plan that feels calm instead of overwhelming.

---

## What it does

- Scores tasks by importance, urgency, effort, and timing
- Builds a small “Today’s Focus” list (your Big 3–5)
- Suggests optional supporting tasks and safely parks the rest
- Produces explainable output so you can see *why* each task was chosen

DailyPilot-Engine is:

- **Human-centered** – Optimized for real life, not just more checkmarks  
- **Deterministic** – Same inputs → same outputs (easy to test and debug)  
- **Embeddable** – Usable from mobile, web, or backend services  

---

## Core concepts

**Task**

Typical fields:

- `title`, `description`
- `importance`, `urgency`
- `effort_estimate`
- optional `due_date` or `time_window`

**Profile**

Profiles tune the behavior for different people and seasons of life (founders, shift workers, students, etc.) by changing weights and time budgets.

**Plan**

Engine output is a simple structure:

- `big_focus` – the few tasks that really matter today  
- `support_tasks` – helpful if time/energy allow  
- `parked_tasks` – explicitly deferred, not forgotten  

---

## Example flow

1. Collect tasks from your app, calendar, or a JSON file.
2. Choose a profile (e.g. `founder`, `double_shift_worker`, `student`).
3. Run the engine to score, sort, and build a plan.
4. Show the plan in your UI and let the human make the final call.

---

## Quick start (developer preview)

```bash
git clone https://github.com/altmanAI/DailyPilot-Engine.git
cd DailyPilot-Engine
