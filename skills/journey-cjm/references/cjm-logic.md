# CJM logic: checks L01–L20

Severity: **critical** — the journey fails the job or misleads; **high** — visible failure of experience; **medium** — a gap that will surface later; **low** — map quality.

Column "Script": ✓ — `journey_check.py check` finds it, ◐ — finds candidates, you decide, — — reading only.

## Frame

| ID | Check | Severity | Script |
|---|---|---|---|
| L01 | A trigger is stated: what exactly starts the journey | medium | ✓ |
| L02 | A success criterion is stated from the user's side and can be verified | high | ✓ |
| L03 | One persona and one scenario per map. Two personas in one table are two maps | medium | ✓ |
| L04 | One action per step. Merged actions hide waits and errors between them | medium | ◐ |
| L05 | Every failure has a way out (retry, another path, a human). Critical on a moment of truth, high elsewhere, medium when the input does not say (`recovery: "unknown"`) | critical / high / medium | ✓ |
| L06 | Every user action has a visible response | high | ✓ |
| L07 | The journey ends with the job done or an explicit exit. Ending at "sees the answer" without checking that the answer solved the job is a gap | medium | — |

## Emotions and evidence

| ID | Check | Severity | Script |
|---|---|---|---|
| L08 | Every emotion has a cause in the step's events | medium | ✓ |
| L09 | A jump of more than 2 between neighbouring steps is explained by an event (failure, result) | medium | ✓ |
| L10 | Moments of truth are backed by evidence, not a guess | high | ✓ |
| L11 | The share of `assumption: true` steps is stated. Above 70 % the whole map is a hypothesis — say so | low / medium | ✓ |
| L12 | The ending matches the curve: "success" with a negative final emotion is a contradiction | high | ✓ |

## System and environment

| ID | Check | Severity | Script |
|---|---|---|---|
| L13 | Steps of external systems (payments, SMS, government services, OCR, LLM) have a described failure | high | ✓ |
| L14 | A wait of 1 s or more has a status; 10 s or more also has cancel or leave-and-return. Unknown duration (`wait_s: "unknown"`) — medium | high / medium | ✓ |
| L15 | Offline steps and steps outside the product (find a document, call someone, wait for a code) are on the map. The deepest dips are often there | medium | — |
| L16 | No step relies on a screen, state or data missing from the inputs. Also: drift between the map and the live product (screenshots, test run, code) — the map describes a different product | critical / high | — |

## Match with intent

| ID | Check | Severity | Script |
|---|---|---|---|
| L17 | Every vision item is covered by a step or explicitly marked as not covered | high | ✓ (`vision`) |
| L18 | No steps or promises the owner did not ask for (extra feature, different tone, wider boundaries) | medium | — |
| L19 | What the user sees (responses of any step, failure texts) uses the user's words, not internal entity names or codes. Add non-Latin internal words to `internal_terms` | medium | ◐ |
| L20 | 6–20 steps. Fewer — merged; more — two journeys mixed | low | ✓ |

## Typical errors of AI-generated journeys

Look for them on purpose; they appear almost every time:

- **Happy monotony**: emotion rises or holds on every step, no dips.
- **The system always answers**: no timeouts, partial results, external refusals.
- **The user always understands**: no "rereads", "searches", "goes back".
- **Internal language**: the "sees" column contains status names, entities, contract codes.
- **Undo as the answer to everything**: every step has "Cancel", nobody says what the user does after cancelling.
- **No return**: only the first visit is described; a second visit, session restore and history are not.
- **Boundary without an alternative**: "request declined" without where to go next.
- **Solution first**: the "pain" column already contains features, the problem itself is missing.

## Writing a logic finding

`L05 · critical · s5 "Check"` — Failure "check takes > 60 s" is not described; no way out. Class: absent. Consequence: the user does not know whether to wait or leave. Fix hint: status with a time estimate, "notify me when ready".
