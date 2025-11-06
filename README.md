# DailyPilot-Engine

DailyPilot-Engine is the prioritization engine behind **DailyPilot by AltmanAI**.  
It turns messy task lists and shifting schedules into a focused, realistic daily plan that feels calm instead of overwhelming.

---

## What it does

- Ranks tasks using importance, urgency, time, and effort
- Builds a small set of “Today’s Focus” tasks (e.g. your Big 3)
- Suggests optional supporting tasks and safely parks the rest
- Produces explainable output so you can see *why* something is recommended

DailyPilot-Engine is designed to be:

- **Human-centered** – Supports real life (energy, constraints, context), not just productivity metrics  
- **Deterministic** – Same inputs → same outputs (easy to test and debug)  
- **Embeddable** – Can be used from mobile, web, or backend services  

---

## Core concepts

**Task**

Each task can include:

- Title and description  
- Importance and urgency scores  
- Effort estimate (how long / how hard)  
- Optional due date or time window  

**Profile**

Profiles tune how the engine behaves for different people and seasons of life:

- Founders / creators  
- Shift workers  
- Students / learners  

A profile defines weightings (importance vs urgency etc.) and time budget rules for the day.

**Plan**

Engine output is a simple structure:

- `big_focus` – the few tasks that really matter today  
- `support_tasks` – helpful if you have time and energy  
- `parked_tasks` – everything else, explicitly deferred (not forgotten)

---

## Example flow (conceptual)

1. Collect tasks (from app, calendar, or a simple JSON file).
2. Choose a profile (e.g. `founder`, `double_shift_worker`, or `student`).
3. Run the engine to:
   - score and sort tasks
   - build a plan for today
4. Present the plan in your app’s UI and let the human make the final call.

---

## Quick start (developer preview)

> Language and tooling here are examples; adapt to your stack.

```bash
git clone https://github.com/altmanAI/DailyPilot-Engine.git
cd DailyPilot-Engine
