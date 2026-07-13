# DailyPilot Engine

> A transparent reference engine for turning a task list into a bounded, reviewable daily plan.

**Humanity leads. Intelligence follows.**

DailyPilot Engine is a small Python reference implementation maintained by AltmanAI, an Altman Family Group LLC initiative. It demonstrates explainable task scoring and effort-budgeted plan construction without hiding the decision logic behind a black box.

## Status

- **Lifecycle:** Reference implementation
- **Language:** Python 3.10+
- **Core runtime dependencies:** Python standard library only
- **Production integration:** Separate product integration work may be in progress; this repository alone is not a production service
- **Decision authority:** Human review required

This engine is not medical, mental-health, legal, financial, employment, education, or safety-critical decision software. It does not understand the full context of a person's obligations, risks, accessibility needs, relationships, or wellbeing.

## What it does

1. Accepts tasks expressed through the `Task` data model.
2. Normalizes importance, urgency, effort, and deadline proximity.
3. Applies a visible stress-impact penalty.
4. Produces a score and factor breakdown for every task.
5. Builds a plan constrained by an effort budget and maximum focus-task count.
6. Parks work that does not fit within the configured budget.
7. Writes a structured local run log when the CLI is used.

## What it does not do

- autonomously decide what a person must do;
- guarantee that a generated plan is safe, complete, healthy, fair, or optimal;
- resolve calendar conflicts, task dependencies, travel time, emergencies, or hidden obligations;
- infer a person's mental state or diagnose stress;
- replace professional or domain-qualified judgment;
- execute external actions or access accounts, calendars, messages, or private services;
- learn from user data or send task data to an external model provider.

The current scoring method is an inspectable heuristic. A high-stress task may be deprioritized by the configured penalty even when outside context makes it essential. Users and integrators must review results and preserve a direct correction or override path.

## Repository layout

```text
.
├── engine/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py         # Task, profile, score, plan, and run-log models
│   │   ├── scoring.py        # Transparent scoring heuristic and breakdown
│   │   └── selectors.py      # Effort-budgeted plan construction
│   └── profiles/
│       ├── student.json
│       ├── worker_double_shift.json
│       └── founder.json
├── dailypilot_cli.py         # Local command-line harness
├── sample_day.json           # Example task input
├── test_scoring.py           # Scoring behavior tests
├── test_selectors.py         # Plan-selection behavior tests
└── test_profiles.py          # Profile integrity tests
```

The package layout prevents collisions with Python standard-library modules and provides one consistent import path for code, tests, CLI use, and documentation.

## Quick start

Clone the repository and enter its directory, then run:

```bash
python dailypilot_cli.py sample_day.json --profile worker_double_shift
```

The CLI prints the plan and writes a local JSON record under `logs/`. The `logs/` directory should not be committed.

### Input format

The task file must be a JSON array. Each task requires `id` and `title`; other supported fields include:

```json
{
  "id": "finish_report",
  "title": "Finish client report",
  "description": "Due soon and important for income.",
  "importance": 5,
  "urgency": 5,
  "effort_estimate": 2.0,
  "stress_impact": "MEDIUM",
  "due_date": "2026-07-15",
  "category": "work"
}
```

`due_date`, when supplied through JSON, must use `YYYY-MM-DD`.

## Python usage

```python
from engine.core import ProfileConfig, Task, build_daily_plan, score_tasks

profile = ProfileConfig(name="example", daily_effort_budget_hours=3.0)
tasks = [Task(id="prepare_demo", title="Prepare product demo", importance=5)]

scored = score_tasks(tasks, profile)
plan = build_daily_plan(scored, profile)
```

## Run tests

Install the test runner in an isolated environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "pytest>=8,<10"
python -m pytest -q
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

The GitHub Actions workflow runs compilation, tests, and a CLI smoke test across supported Python versions.

## Scoring model

Default weights:

| Factor | Weight | Interpretation |
|---|---:|---|
| Importance | 0.40 | User-supplied significance, normalized from 1–5 |
| Urgency | 0.30 | User-supplied time pressure, normalized from 1–5 |
| Effort | 0.20 | Shorter estimated tasks receive a larger contribution |
| Deadline | 0.10 | Due and near-due tasks receive a larger contribution |

The profile may override these weights. A stress-impact penalty is then subtracted:

| Stress impact | Penalty |
|---|---:|
| LOW | 0.00 |
| MEDIUM | 0.10 |
| HIGH | 0.25 |

Every result includes the normalized factors, base score, and penalty. This supports inspection but does not prove that the weights are universally appropriate.

## Human-first integration requirements

Any product integration should provide:

- clear disclosure that the plan is generated assistance;
- understandable factor explanations;
- direct editing, correction, override, and dismissal controls;
- no coercive language or false certainty;
- no high-stakes use without qualified review and additional safeguards;
- data minimization and explicit privacy controls;
- monitoring for harmful or systematically poor recommendations;
- a documented rollback or disable path;
- an AI System Card and release record for material deployments.

Review the organization-wide governance and release controls in [`altmanAI/.github`](https://github.com/altmanAI/.github).

## Documentation

- [`overview.md`](overview.md) — product and scoring overview
- [`architecture.md`](architecture.md) — current architecture and boundaries
- [`api.md`](api.md) — Python reference usage
- [`IOS_BRIDGE.md`](IOS_BRIDGE.md) — integration planning notes; not a production-readiness claim
- [`SECURITY.md`](SECURITY.md) — private vulnerability reporting

## Security and privacy

Do not submit real private task lists, credentials, health details, financial records, customer data, or confidential business information to public issues or pull requests.

Report security-sensitive findings privately as described in [`SECURITY.md`](SECURITY.md).

## Contributing

Focused contributions are welcome. Every material pull request should include:

- a linked objective or issue;
- tests or reproducible validation;
- capability and limitation updates;
- security, privacy, accessibility, and human-impact review;
- rollback considerations;
- disclosure of material AI assistance.

## License

The repository license controls use and redistribution. Public visibility and reference status do not imply endorsement, certification, fitness for a particular purpose, or authorization for high-stakes deployment.

## P.A.I.H.I.

- **Proof:** Tests and inspectable score breakdowns support bounded behavior claims.
- **Alignment:** The engine assists human prioritization without claiming human authority.
- **Integrity:** Limitations and non-goals are documented explicitly.
- **Humanity:** Integrations must preserve agency, privacy, accessibility, correction, and recourse.
- **Impact:** Useful outcomes should be evaluated with versioned evidence rather than assumed from demonstrations.
