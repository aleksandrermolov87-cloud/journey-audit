# Work folder and final report

Language: the user's. Register: facts, numbers, consequences, no evaluative adjectives. The final `journey-audit-<slug>.md` is short: details live in family reports and the verdict, the final report links to them.

## Work folder

```
<work>/
  frame.md                 frame, vision, inputs, what was invented during normalization
  journey.json             normalized journey (shared by all agents, read-only for them)
  cjm/     findings.json · report.md · emotion-curve.svg
  edge/    findings.json · report.md · branches.json · personas.json
  load/    findings.json · report.md · journey.load.json · load-overrides.json · load-*.json · load-curve.svg
  verdict/ verdict.json · verdict.md · backlog.json · merged.json · specs/G-NN.md
  journey-audit-<slug>.md  final report
```

## Final report (orchestrator)

```markdown
# Journey audit: <title>
Frame (5–8 lines) · input version (commit, date)

## Verdict
Verdict and one-line reason (from verdict.md).

## Summary
Findings per family and severity; clusters after merging; P0 / P1 / P2; peak load; exit points;
persona outcomes; vision: covered / at risk / violated / not mentioned.

## P0 and P1 goals
| Goal | Priority | Metric (now → target) | Spec | Findings |

## Owner decisions
## Not checked
## Files
Links to family reports, verdict, specs, JSON.
```

## A single family run without the orchestrator

When a family skill is called directly, its report follows the same sections as `report_md` in `findings-contract.md`: checked, findings, artefacts, not checked, method notes. Findings use the same JSON, so a verdict can still be run later.
