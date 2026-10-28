# Specs, TO BE, validation

## Goal spec — `specs/G-NN.md`

A spec lets a designer, developer or coding agent make the fix without repeating the audit. Write it so it can go into a ticket as is.

```markdown
# G-01 · P0 · <goal in one sentence>

## Problem
What happens to the user today, 2–4 lines. Links to findings (CJM-03, EDGE-01, LOAD-05) and their evidence classes.

## Goal and metric
Metric · now · target · how to measure.

## Scope
Affected AS IS steps (ids) → what changes. What is out of scope.

## TO BE journey (fragment)
| Step | User does | Sees | Response | Undo / way back |
Only changed and new steps.

## States
| State | What the user sees | What they can do |
Default · loading · empty · error · offline · refused / out of scope · partial result — only those relevant to the goal.

## UI copy
Exact strings: headings, buttons, errors, hints. The user's words, no internal terms. Mark copy that needs legal or domain review.

## Acceptance criteria
- Given … When … Then …
(3–8, each verifiable by a test or a manual check)

## Analytics
Events with parameters used to compute the metric.

## Test cases
From edge scenarios and branches: input → expected result. At least one negative case and one accessibility case.

## Do not break
Peaks of the emotion curve, useful friction, vision items already covered.

## Owner decisions
Questions without which the spec cannot be finished. Options, if any.

## Dependencies and effort
Contracts, backend, content, reviews. S / M / L with a one-line reason.
```

No specs for P2: a row in the goal table with `fix_hint` is enough.

## `verdict.json`

```json
{
  "verdict": "Rework",
  "verdict_reason": "one line",
  "files": {"verdict.md": "<markdown>", "specs/G-01.md": "<markdown>"}
}
```

The orchestrator expands `files` with `journey_check.py render <work>`.

## `backlog.json`

```json
{
  "verdict": "Ready | Ready with conditions | Rework | Redesign",
  "verdict_reason": "one line",
  "goals": [
    {
      "id": "G-01", "priority": "P0", "title": "…",
      "metric": {"name": "…", "current": "not measured", "target": "≥ 80 %", "measure": "event …"},
      "findings": ["CJM-03", "EDGE-01"], "families": ["cjm", "edge"],
      "owner": "product", "effort": "M", "score": 34.2,
      "steps": ["s3", "b1.s1"], "spec": "specs/G-01.md",
      "owner_decisions": ["…"]
    }
  ],
  "deferred": ["EDGE-14", "LOAD-09"],
  "not_checked": ["…"]
}
```

## TO BE

The full journey table in the same format as the source (same columns), with the changes of all P0 and P1 goals. Below it, a diff:

- **Added**: step → goal
- **Removed**: step → goal
- **Split**: step → into which
- **Changed**: step → what exactly
- **Kept as useful friction**: step → why

If goals depend on owner decisions, show TO BE with the default option and mark the fork.

## Validation with people

5–8 tasks for a usability test or interview. Each is tied to a goal and a hypothesis:

```
1. G-01 · hypothesis: after blocking a card the user does not know how to pay today
   Task: "You have just blocked your lost card. Buy a coffee with your phone."
   Participants: 5 commuters, 2 of them 55+
   Success: ≥ 4 of 5 pay within 3 minutes without help
```

Validate first the hypotheses that P0 goals with med or low confidence rest on.
