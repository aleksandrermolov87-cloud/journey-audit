# AGENTS.md — journey-audit

Instructions for coding agents that do not load Agent Skills automatically.

## What this repository is

Five skills for auditing a customer journey map (CJM), user flow or service scenario:

| Path | Role |
|---|---|
| `skills/journey-audit/SKILL.md` | Orchestrator — start here |
| `skills/journey-cjm/SKILL.md` | CJM logic family |
| `skills/journey-edge/SKILL.md` | Secondary and edge-case scenarios family |
| `skills/journey-load/SKILL.md` | Simulated cognitive load family |
| `skills/journey-verdict/SKILL.md` | Verdict, priorities, specs family |

Russian instructions: `SKILL.ru.md` and `references/ru/` next to each skill.

## When a user asks to audit, review or validate a journey

1. Read `skills/journey-audit/SKILL.md` and follow it.
2. If you can run subagents, launch the three auditors in parallel with the briefs in `skills/journey-audit/agents/`.
3. If you cannot, run the auditors one after another, each from a clean context: read only that auditor's brief and its family skill.
4. Run the verdict last.

## Helper script

```bash
python3 skills/journey-audit/scripts/journey_check.py --help
```

Python 3.8+, standard library only. Commands: check, load, vision, curve, findings, merge, render. `--lang ru` for Russian output.

## Tests

```bash
python3 -m unittest discover -s tests
```
