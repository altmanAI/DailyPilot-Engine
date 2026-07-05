# DailyPilot-Engine

DailyPilot-Engine is the human-centered prioritization core of **DailyPilot by AltmanAI (Altman Family Group, LLC)**.

It transforms messy task lists and shifting schedules into a focused, realistic daily plan that feels calm instead of overwhelming — with explainable, stress-aware scoring logic, not a black box.

**Humanity leads. Intelligence follows.**

---

## What this repo does

- Takes a raw set of tasks/schedule inputs (see `sample_day.json`, `student.json`, `worker_double_shift.json`, `founder.json` for example profiles)
- Scores and selects a realistic daily plan using `scoring.py` and `selectors.py`
- Exposes a data contract via `models.py`
- Ships a CLI entry point: `dailypilot_cli.py`

## Setup

```bash
pip install -r requirements.txt
```

## Run the CLI

```bash
python dailypilot_cli.py --input sample_day.json
```

## Run tests

```bash
python -m pytest test_scoring.py test_selectors.py test_profiles.py
```

## Docs

- `overview.md` — product overview and scoring philosophy
- `architecture.md` — system architecture
- `api.md` — API contract for app integration
- `IOS_BRIDGE.md` — notes on connecting this engine to the DailyPilot iOS app (moved here from the old root README)

## Status

This is the reference implementation of the DailyPilot scoring engine — real, working Python logic with tests, not a concept doc. iOS/production integration is in progress; see `IOS_BRIDGE.md` for the current plan.

## Part of the AltmanAI ecosystem

DailyPilot-Engine is one product surface in the broader AltmanAI system. See [altmanAI/.github](https://github.com/altmanAI/.github) for the organization-level overview, and [altmanAI/altmanai-master-ledger](https://github.com/altmanAI/altmanai-master-ledger) for how releases here connect to the public Proof-of-AI-Human-Impact (PAIHI) record.
