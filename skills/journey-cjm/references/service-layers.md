# Service layers (CJM + service blueprint)

A journey map and a service blueprint share the same step columns. On top is what the user lives through, below is what the service does. Logic errors often hide at the seam between layers.

| Layer | Contents | Source |
|---|---|---|
| Doing | Observable user action | Fact: map, code, session recording |
| Thinking | Inner voice | Always a guess, mark `assumption` |
| Feeling | −2…+2 | See `emotion-curve.md` |
| Pain / opportunity | Friction and direction | A guess until research exists |
| Frontstage | Screen, email, SMS, system dialog — concrete | Fact |
| Backstage | Calls, jobs, state transitions | Fact from code or contract |
| Support | Systems and services under the step | Fact |
| Evidence | Interviews, analytics, recordings | Empty until it exists — a person fills it |

## Checks

| Code | Check |
|---|---|
| SL1 | Frontstage contains no backstage words: statuses, entities, contract codes. If it does, the user will see them or the map misstates what they see (`root_cause: "internal-language"`) |
| SL2 | Every backstage step that takes time or can fail has a frontstage reflection: status, error, time estimate |
| SL3 | Every supporting system a step depends on has a described failure (see L13) |
| SL4 | "Thinking", "pain", "opportunity" are marked as guesses. Presented as facts → a finding with class `hypothesis` |
| SL5 | System actions that change what the user knows (mode switched, data not verified, part of the answer hidden) are visible in frontstage. A silent mode switch is critical if the user then decides on a wrong basis (`root_cause: "silent-mode-switch"`) |
| SL6 | Steps where the backstage decides for the user (rejects, filters, truncates) explain in frontstage what happened and what to do (`root_cause: "hidden-without-explanation"`) |

Do not draw the whole blueprint. The table is needed only for steps with a seam problem.
