# Merging and conflicts

## Merging duplicates

The three families often see one problem from different sides: logic — "failure without a way out", edge cases — "out-of-scope request without a route", load — "uncertainty 2 on the refusal step". That is one goal, not three.

Merge findings into a **cluster** when at least one holds:

1. same `root_cause`;
2. `steps` overlap and the `fix_hint`s lead to one change;
3. one finding is a consequence of another (value failure → emotion −2 → exit point).

Do not merge when the fixes differ, even on one step: "remove a term" and "add a time estimate" are two goals.

A cluster inherits from its **lead finding** — the one with the highest severity (on a tie, the stronger evidence class):

- severity, confidence, evidence class, frequency and impact. Other findings in the cluster do not raise them: a medium finding with high confidence does not make a critical finding with med confidence confident;
- `vision` — the union;
- the list of families — in the report. A finding confirmed by 2–3 families weighs more (the "confirmation" multiplier), but its evidence class does not change. A family whose finding entered only as a constraint ("do not touch", `useful_friction`) does not count as confirmation.

The `merge` script clusters only by identical `root_cause` with a shared step and takes maxima. It is a draft: families often name one cause with different labels, and one label can hide different fixes. Merging by meaning and splitting are yours; list in "Method notes" where you departed from the script.

## Conflicts between families

| Conflict | How to resolve |
|---|---|
| Load: "remove the confirmation step"; logic or edge: "the confirmation prevents an error" | The step stays if `useful_friction: true` or it confirms an irreversible action, consent, a medical, legal or financial safeguard. The goal becomes "make the confirmation faster" (show the source next to each line instead of one checkbox for everything) |
| Edge: "add a branch / warning"; load: "the step is already overloaded" | The branch is needed, but not on the main screen: progressive disclosure, a separate state, shown only on condition |
| Logic: "the map drifts from the live product" | First decide what is true: the map (plan) or the product (fact). Without it there is nothing to spec. Goes to "Owner decisions" as a P0 blocker |
| Synthetic personas vs provided evidence | Provided evidence (code, product, data) wins. A persona shows that a person may not notice what works; that is a goal about visibility, not existence |
| Families set different severities | Take the lead finding's severity, but show in the table who set what |

Every resolved conflict is a line in `verdict.md` → "Conflicts": what clashed, what was decided, why.
