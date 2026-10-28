# Priorities and goals

## Cluster score

```
severity weight  critical 8 · high 4 · medium 2 · low 1
confidence       high 1.0 · med 0.7 · low 0.4
reach            frequency (1–3); if missing: 3 for main-path steps, 1 for branches
impact           impact (1–3); if missing: critical 3 · high 2 · medium 1 · low 1
confirmation     1 + 0.25 × (families in the cluster − 1)
effort           S 1 · M 2 · L 3 — you estimate it from fix_hint

score = severity weight × confidence × reach × impact × confirmation / effort
```

The `merge` script computes everything but effort (it assumes M = 2). Set the effort and recompute.

## Levels

| Level | Rule | Meaning |
|---|---|---|
| P0 | Any `critical` with confidence med or higher; a violated vision item about safety, health, money, rights or the main job; the "map or product — which is true" blocker | Without it the journey fails the job or misleads. Fix before release |
| P1 | Score ≥ 12, or `high` on the main path, or an exit point of the vulnerable profile on a moment of truth | Visible failure of experience for a significant share of people |
| P2 | The rest with score ≥ 3 | Improvements and map gaps |
| Deferred | Score < 3, or low confidence without a way to validate | Backlog without a date; list in one line |

At most 5 P0 and 7 P1 goals. If you get more, first review merging (one cause may be spread over several goals). If merging is honest and there are still more, move the lowest-scoring P1 to P2 and say so.

If a P0 depends on an owner decision (for example, whether the service promises something at all), set the verdict by the default option and state in the reason the condition under which it changes.

## Value failures

Clusters with `root_cause: "value-failure"` get the label "business / content", not "design". The goal changes the offer or the data, not a screen.

## Goals

Every P0 and P1 cluster becomes a goal:

```
G-01 · P0 · <what must become true for the user, one sentence>
Metric: <what we measure> · now: <value or "not measured"> · target: <value> · how: <event, test, interview>
Findings: CJM-03, EDGE-01, LOAD-05
Decision owner: design | product | business/content | engineering | legal or domain review
Effort: S | M | L
```

Good goals are phrased from the user's side and can be checked:

- "A user who blocks a lost card can pay the same day" · metric: share of blocks followed by a virtual card issued within 10 minutes · target ≥ 80 % · event `virtual_card_issued_after_block`.
- "The user knows how long the check takes" · metric: share of sessions with a time estimate shown within 3 s of the wait starting · target ≥ 95 %; share of cancels during the wait · now unknown · target −30 % from baseline.

Bad: "improve the UX of the result", "reduce load", "make it clearer".

If there is no baseline, the first task of the goal is to add the event and capture the baseline. Write that into the spec.
