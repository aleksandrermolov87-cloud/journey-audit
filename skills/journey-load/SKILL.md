---
name: journey-load
description: Simulated cognitive load audit for customer journeys and user flows — per-step load index 0–100 with open weights (decisions, options per Hick's law, fields, new terms, working-memory items, context switches, waiting, uncertainty), Keystroke-Level Model (KLM) time, accumulated fatigue, likely exit points, sensitivity across persona profiles, Nielsen and Krug heuristics per step, intrinsic vs extraneous load with three levers to cut it. Part of the journey-audit family; usually run by the journey-load-auditor agent. Call directly when the user asks only about load — "where will users get tired", "how many decisions on this step", "is this screen overloaded", "compare load AS IS vs TO BE". Russian: «когнитивная нагрузка», «где пользователь устанет».
license: MIT
metadata:
  version: "1.0.0"
  family: journey-audit
---

# Family: simulated cognitive load

> Русская версия: `SKILL.ru.md`, справочники — `references/ru/`.

The family's question: **on which steps does the journey demand more attention, memory and decisions than the job needs, and what can be taken off the user?** Map logic and edge cases belong to other families; write one line under "Hand over to other families" if you notice something there.

Everything here is a model, not a measurement. Show the formula and the contributions in the report, not only the total.

## Input

`journey.json`, `frame.md`, the source, screenshots and UI copy if available.

## Methods

| # | Method | File | Gives |
|---|---|---|---|
| 1 | Refine `load` features per step | `references/cognitive-load.md` → "What to fill in" | Honest counts of decisions, options, memory, terms, waiting |
| 2 | Index, KLM, fatigue, exit points | `references/cognitive-load.md` + script | Per-step table |
| 3 | Persona sensitivity | `references/persona-sensitivity.md` | Steps that break only for some people |
| 4 | Heuristics per step | `references/heuristics.md` | Which principles are broken where the index is high, and why |
| 5 | Intrinsic vs extraneous, levers | `references/cognitive-load.md` → "Intrinsic and extraneous" | What to cut, what to keep, what to present more clearly |

### Refining features

The `load` values in `journey.json` were set during normalization and are rough. Do not change `journey.json`: copy it to `<work>/load/journey.load.json`, refine `load` there and log every change in `<work>/load/load-overrides.json`:

```json
[{"step": "s7", "field": "context_switches", "from": 0, "to": 1, "why": "address is copied from a messenger"}]
```

### Computing

```bash
J=<work>/load/journey.load.json
python3 <Script> load $J --persona-tech mid  --persona-patience mid  --json > <work>/load/load-mid.json
python3 <Script> load $J --persona-tech low  --persona-patience low  --json > <work>/load/load-low.json
python3 <Script> load $J --persona-tech high --persona-patience high --json > <work>/load/load-high.json
python3 <Script> curve $J --persona-tech low --persona-patience low -o <work>/load/load-curve.svg
```

`<Script>` is `journey-audit/scripts/journey_check.py`; the orchestrator passes its path. Add `--lang ru` for Russian output.

**Branches**: the script computes the main path. For a branch, build a temporary JSON with the branch as `steps` and run `load` on it; save to `load/load-branches.json`.

**Unknown waits** (`wait_s: "unknown"`) count as zero. If the evidence has measurements, compute a separate scenario with them (`load-wait-scenario.json`) and name the source.

## Output

- `<work>/load/findings.json` — contract `journey-audit/references/findings-contract.md`, ids `LOAD-NN`, report in `report_md`. Check code: `C-<step>` for index and fatigue, `H<n>` / `K<n>` for a heuristic, `KLM` for time. Put the index, level, main contributions and persona profile into `detail`. Friction that protects the user gets `useful_friction: true`.
- `journey.load.json`, `load-overrides.json`, `load-*.json`, `load-curve.svg`.

## Boundaries

Do not present the index as a conversion forecast. Severity: overload (≥ 70) or an exit point on the main path — `high`; `critical` only when overload leads to a wrong decision or harm (confirmed wrong data without reading, missed a warning), matching the contract's definition. Everything else — `medium`. If an overload appears only after your refinements, report the index before and after.
