---
name: journey-cjm
description: CJM logic audit — structural checks L01–L20 for customer journey maps, emotion curve analysis, service blueprint layers (frontstage/backstage), mature-map review (contradictions between goals and steps, drift between the map and the live product), owner-vision coverage. Part of the journey-audit family; usually run by the journey-cjm-auditor agent. Call directly only when the user asks about the logic of a journey map alone — "is this CJM consistent", "are steps merged", "where do these emotions come from", "does the map match the intent" — without edge cases or cognitive load. Russian: «логика CJM», «проверь карту пути».
license: MIT
metadata:
  version: "1.1.0"
  family: journey-audit
---

# Family: CJM logic

> Русская версия: `SKILL.ru.md`, справочники — `references/ru/`.

The family's question: **does the journey do the user's job the way it claims, and does it contradict itself?** Coverage of edge cases and cognitive load belong to other families; if you notice something there, write one line under "Hand over to other families".

## Input

`journey.json`, `frame.md` (frame, vision, evidence list), the source. When run without the orchestrator, first normalize the journey following `journey-audit/references/journey-format.md`.

## Methods

| # | Method | File | Gives |
|---|---|---|---|
| 1 | Structural checks L01–L20 | `references/cjm-logic.md` | Frame gaps, failures without a way out, missing responses, evidence |
| 2 | Emotion curve | `references/emotion-curve.md` | Emotions follow events; types of dips; value failure vs UI failure |
| 3 | Service layers | `references/service-layers.md` | What the user sees, what the system does, what stands behind it; where the map mixes layers |
| 4 | Mature-map review | `references/health-review.md` | Contradictions between sections, drift from the live product, moments of truth, skewed coverage |
| 5 | Vision coverage | `references/vision-diff.md` | Covered / at risk / violated / not mentioned + what the AI added unasked |

Order: mechanics of methods 1–3 by script → manual part starting with method 4 → manual part of methods 1–3 → method 5.

```bash
python3 <Script> check  <work>/journey.json --json > <work>/cjm/script-check.json
python3 <Script> vision <work>/journey.json
python3 <Script> curve  <work>/journey.json -o <work>/cjm/emotion-curve.svg
```

`<Script>` is `journey-audit/scripts/journey_check.py`; the orchestrator passes its path. Add `--lang ru` for Russian output.

Script severities are a starting point: review them by meaning and say in the finding when you change one.

**The most valuable findings are invisible to the script**: a goal contradicted by a step, the map describing a different product than the one that runs, a silent mode switch, promises the journey does not keep. Start the manual part with them (method 4).

## Output

- `<work>/cjm/findings.json` — contract `journey-audit/references/findings-contract.md`, ids `CJM-NN`, report in `report_md`.
- `<work>/cjm/emotion-curve.svg`, `<work>/cjm/script-check.json`.

## Boundaries

Do not change `journey.json`. A normalization error is a `low` finding with `check: "NORM"`. Do not design solutions — that is the verdict's job: `fix_hint` is a direction in one or two lines.
