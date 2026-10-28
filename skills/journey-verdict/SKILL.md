---
name: journey-verdict
description: Final verdict for a customer journey audit — merges findings of the CJM logic, edge-case and cognitive load families, resolves conflicts between them, decides a verdict (ready / ready with conditions / rework / redesign), sets priorities P0–P2 and goals with metrics, writes fix specs (TO BE fragment, states, UI copy, Given/When/Then acceptance criteria, analytics events, test cases), a full TO BE journey and a usability validation plan. Part of the journey-audit family; usually run by the journey-verdict agent. Call directly when findings already exist and the user asks "what should we fix first", "prioritize", "write specs", "build a backlog from the CJM audit". Russian: «что чинить первым», «приоритеты и спеки».
license: MIT
metadata:
  version: "1.1.0"
  family: journey-audit
---

# Family: verdict, priorities, specs

> Русская версия: `SKILL.ru.md`, справочники — `references/ru/`.

The family's question: **what to fix, in what order, what counts as fixed, and how to check it.** No new findings are searched here. If merging reveals a gap that no family covered, write it under "Not checked", not into the backlog.

## Input

`<work>/cjm/findings.json`, `<work>/edge/findings.json`, `<work>/load/findings.json` (their `report.md` for context), `<work>/journey.json`, `<work>/frame.md`, `<work>/edge/branches.json` if present.

Validate input: `python3 <Script> findings <work>`. If a family is missing or invalid, work with the rest and state in the verdict which axis is missing.

## Methods

| # | Method | File |
|---|---|---|
| 1 | Merge duplicates, resolve conflicts | `references/merge-and-conflicts.md` |
| 2 | Priorities P0–P2 | `references/prioritization.md` |
| 3 | Goals with metrics | `references/prioritization.md` → "Goals" |
| 4 | Specs | `references/spec-format.md` |
| 5 | TO BE and validation plan | `references/spec-format.md` → "TO BE" and "Validation" |

Starting clusters and scores:

```bash
python3 <Script> merge <work> > <work>/verdict/merged.json
```

The script groups findings by `root_cause` and shared steps and computes a starting score. Merging by meaning, priority and goal wording are your decisions: the script does not read meaning.

## Verdict on the journey

One of four, with a one-line reason:

| Verdict | When |
|---|---|
| Ready | No P0, at most 2 P1 |
| Ready with conditions | No P0, but there are P1 goals without which the journey must not ship to the stated audience |
| Rework | P0 goals exist and are solvable within the current journey |
| Redesign | A P0 concerns the main job or value: in its current form the journey does not do what the user came for |

## Output

When run by the orchestrator, markdown files go as strings into `<work>/verdict/verdict.json` → `files` (key = relative path), and the orchestrator expands them with `journey_check.py render <work>`. When called directly and writing `.md` files is allowed, write them directly.

- `verdict.md`: verdict, summary per family, P0–P2 goal table, conflicts and how they were resolved, what to keep (peaks, useful friction), TO BE with a diff, validation plan, owner decisions, not checked, method notes.
- `specs/G-NN.md` — a spec for every P0 and P1 goal.
- `<work>/verdict/backlog.json` — goals in machine-readable form (schema in `references/spec-format.md`).

## Boundaries

- Do not decide service boundaries, legal, medical or financial frames for the owner. Phrase options and put them under "Owner decisions". Example: "promise a delivery date" may need a logistics commitment; it is not a UI change.
- A goal without a metric is not a goal. If the metric cannot be measured today, say what is needed to measure it.
- Never raise confidence while merging: three synthetic confirmations are still a hypothesis, only with more weight.
