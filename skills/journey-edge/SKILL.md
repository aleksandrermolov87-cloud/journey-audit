---
name: journey-edge
description: Secondary and edge-case scenario audit for customer journeys and user flows — 14 edge-case axes (entry, interruption and return, data errors, ordering, roles, external failures, time, device, accessibility, service boundaries, value failure, emotional state, exit), flow checklists (entry, forms, uploads, waiting, AI answers, payments, empty states, deletion), synthetic personas in description or browser mode, alternative and adjacent journeys ranked by frequency × impact. Part of the journey-audit family; usually run by the journey-edge-auditor agent. Call directly when the user asks only for edge cases, unhappy paths, negative or alternative scenarios — "what if the user…", "what did we miss", "run personas through the prototype". Russian: «краевые сценарии», «нестандартные сценарии», «что мы не учли».
license: MIT
metadata:
  version: "1.1.0"
  family: journey-audit
---

# Family: secondary and edge-case scenarios

> Русская версия: `SKILL.ru.md`, справочники — `references/ru/`.

The family's question: **which paths does the main map skip, what happens on them today, and which of them need to be described?** The logic of the main map and cognitive load belong to other families; write one line under "Hand over to other families" if you notice something there.

## Input

`journey.json`, `frame.md`, the source. Parameters from the orchestrator: `Personas: yes (N) | no`, `Browser: URL | no`, `Mode: full | quick`.

## Methods

| # | Method | File | Gives |
|---|---|---|---|
| 1 | Axes E01–E14 per stage | `references/edge-scenarios.md` | Scenarios with frequency, impact, coverage, priority |
| 2 | Flow checklists | `references/flow-checklists.md` | Typical failures for a step type: entry, input, upload, waiting, AI answer, payment, empty state, deletion |
| 3 | Synthetic personas | `references/synthetic-personas.md` | Where specific kinds of people get stuck and leave. Only with `Personas: yes` |
| 4 | Alternative paths | `references/edge-scenarios.md` → "Scoring" | Top 3–5 scenarios expanded into branches of 3–8 steps |
| 5 | Adjacent journeys | `references/edge-scenarios.md` → "Adjacent journeys" | 3–5 journeys that deserve their own map |

Order: 1 and 2 together stage by stage → 3 (if enabled) → 4 → 5. Personas come after the checklists so you can see what they found beyond them; report that as a separate line: "personas found N findings not covered by the checklists".

### Personas

- If you can launch agents, run one subagent per persona in parallel, on a cheaper model, strictly in two stages (free exploration, then mission).
- If you cannot, play each persona yourself, one after another, each from a clean slate: do not reuse the previous persona's findings.
- The mission wording must not hint at the answer being tested. If a hint slipped in, lower `confidence` of unanimous findings and say so.

### Browser

Only with `Browser: URL`. Any browser automation available to you. Reading forms is fine; submitting is not (except a test environment with explicit permission). Never pay, sign up on third-party services or type passwords.

## Output

- `<work>/edge/findings.json` — contract `journey-audit/references/findings-contract.md`, ids `EDGE-NN`, report in `report_md`. `frequency` and `impact` are required. Persona findings: `check: "P-<id>"` for one persona, `check: "P"` + `personas` for several; class `synthetic`.
- `<work>/edge/branches.json` — expanded alternative paths in the `branches` format of journey-format.md. Name new branches `e1…` to tell them from normalization branches `b1…`.
- `<work>/edge/personas.json` — persona cards and answers, if personas ran.

## Boundaries

Do not change `journey.json`. New branches go only into `edge/branches.json`. Do not invent screens for branches: when the input does not say what happens, write "today: unknown" and propose what should happen.
