# DailyPilot Engine Architecture

## Current structure

The reference engine intentionally uses a small root-module architecture:

- `models.py` — task, profile, scored-task, plan, and run-log data models;
- `scoring.py` — transparent factor normalization, weighting, deadline treatment, and stress penalty;
- `selectors.py` — effort-budgeted plan construction;
- `dailypilot_cli.py` — local JSON input, profile loading, output display, and run logging;
- root-level profile JSON files — example configuration for different contexts;
- root-level test files — behavior and integrity evidence.

This layout is the current source of truth. A future packaging migration must update implementation imports, tests, CLI paths, documentation, and release instructions in the same reviewed change.

## Data flow

```text
Task JSON
   │
   ▼
Task data models ──► score_tasks() ──► ordered ScoredTask records
                                             │
Profile JSON ─────────────────────────────────┤
                                             ▼
                                   build_daily_plan()
                                             │
                                             ▼
                              focus / support / parked tasks
                                             │
                                             ▼
                               human review + local run log
```

## Trust boundaries

The reference engine:

- reads local JSON supplied by the operator;
- performs deterministic local Python calculations except for current-date and timestamp inputs;
- writes local log files;
- does not call external AI models, APIs, accounts, calendars, or messaging services;
- does not authenticate users or manage production data.

A product integration changes these boundaries and requires a separate security, privacy, evaluation, and release review.

## Explainability

Each scored task retains:

- normalized importance;
- normalized urgency;
- normalized inverse effort;
- normalized deadline proximity;
- stress penalty;
- base score;
- final score.

This makes the heuristic inspectable. It does not guarantee that the factors or weights are appropriate for every person or context.

## Human-control requirements

Integrations must preserve:

- review before consequential action;
- correction and override;
- clear status and limitation disclosure;
- no false claim of objectivity or optimality;
- no hidden external action;
- an operator-controlled disable or rollback path;
- privacy and data-minimization controls.

## Known limitations

The current engine does not model:

- task dependencies;
- fixed calendar events or travel time;
- emergencies or safety-critical obligations;
- multi-day optimization;
- changing energy across a day;
- fairness across people or teams;
- accessibility accommodations;
- emotional, medical, financial, or legal consequences;
- uncertainty in user-entered importance, urgency, effort, or stress values.

These are explicit engineering boundaries, not future capability claims.
