# Simulated cognitive load

Load is not measured here, it is modelled: each step gets observable features that research links to effort, and they are combined into an index with open weights. The index compares steps and versions of one journey; it does not name an absolute value. Weights may be tuned for a product — change them in the script and in this file together.

## What to fill in `load`

| Field | How to count | Why it matters |
|---|---|---|
| `decisions` | How many times the step requires a choice (what to tap, which option, whether to continue) | Every decision is a pause and a chance of error |
| `max_options` | Options in the widest choice of the step | Choice time grows with the logarithm of options (Hick–Hyman) |
| `fields` | Input fields and checkboxes to fill | Typing and checking |
| `new_terms` | Words the user sees for the first time or misreads (statuses, codes, jargon) | An unfamiliar word stops reading |
| `memory_items` | What must be carried from earlier steps: a code from an SMS, a number, document content, which items are already checked | Working memory holds about 4 chunks; errors rise sharply after that |
| `context_switches` | Leaving for another app, tab or the physical world (find a document, open email) | Coming back costs time and part of the context |
| `wait_s` | System wait, seconds, or `"unknown"` | Uncertain waiting is harder than certain waiting |
| `uncertainty` | 0 — clear what happens; 1 — some doubt; 2 — unclear what happens and whether it can be undone | Anxiety consumes attention by itself |
| `klm` | KLM operators separated by spaces | Error-free time of an experienced user |

Do not inflate values for drama. If a feature is not visible in the input, set 0 and say in the report that it was not assessed. Exception: `wait_s` — write `"unknown"`, the script flags it instead of hiding it as zero.

## Step load index (0–100)

```
decisions   = 6 × decisions + (5 × log2(max_options + 1) if decisions > 0)
fields      = 2.5 × fields
terms       = 6 × new_terms
memory      = 6 × min(memory_items, 4) + 15 × max(memory_items − 4, 0)
context     = 7 × context_switches
wait        = k × log2(wait_s + 1), k = 3 with a status indicator, 6 without; × 1.5 for low patience
uncertainty = 8 × uncertainty

index = min(100, (sum) × persona multiplier)
persona multiplier: tech low 1.25 · mid 1.0 · high 0.85
```

Levels: < 25 low, 25–49 moderate, 50–69 high, ≥ 70 overload.

## Accumulated fatigue

```
F₁ = index₁
Fᵢ = 0.75 × Fᵢ₋₁ + indexᵢ
```

Several moderate steps in a row tire more than one heavy step among light ones. A threshold of 120 is roughly three high-load steps in a row.

System steps do not add their index to F: the user decides nothing there. Only the waiting component goes into F (`Fᵢ = 0.75 × Fᵢ₋₁ + wait × multiplier`), and a system step is an exit point only through a wait of 10 s or more without a status.

## Likely exit point

A step is flagged when any of these holds:

- index ≥ 70 (≥ 60 with low patience);
- F ≥ 120 (≥ 100 with low patience) and the step's emotion ≤ −1;
- a wait ≥ 10 s without a status.

This is the model's hypothesis. Phrase it as: "the model flags s5 as a likely exit point: F = 134, 40 s wait without a time estimate".

## KLM time

The Keystroke-Level Model (Card, Moran, Newell) gives error-free execution time. Operators:

| Operator | Value, s | Meaning |
|---|---|---|
| `K` | 0.2 (tech high) · 0.28 (mid) · 0.5 (low) | Keystroke / character. `K*20` — 20 characters |
| `P` | 1.1 | Point with a cursor or a finger at a target |
| `B` | 0.1 | Press or release a button; a tap or click is `B B` |
| `H` | 0.4 | Move the hand between keyboard and mouse; on a phone, change grip |
| `M` | 1.35 | Mental preparation: decide what to do next |
| `W5` | 5 | Wait for the system, seconds |

Place `M` before every new decision and before starting to type; not between parts of one practised action. On a phone typing is slower: the script uses the `low` value of `K` for `mid` and `mid` for `high` when the step's channel or the persona context says mobile/phone.

KLM describes an experienced user without errors, so novices take longer. Use it to compare AS IS and TO BE, not as a time forecast.

## Intrinsic and extraneous

After computing, split every high score:

- **Intrinsic** — set by the job. Understanding a contract, comparing two plans is the work itself; do not remove it, present it more clearly.
- **Extraneous** — added by the interface. Cut it with three levers:
  1. **Remove noise**: duplicated links, competing primary buttons, decoration, copy "for the record", legal text outside the decision moment.
  2. **Familiar models**: the primary button is the most visible, the error sits at the field, progress goes left to right, labels sit above fields, words are the user's.
  3. **Take the work over**: show what was entered earlier, prefill what is known, recommend a default, calculate for the user, show "step N of M".

Quick checks for the report: what is seen first when squinting; would a newcomer know what to do in 3 seconds; what breaks if an element is removed; can the screen be described over the phone; does the user carry anything in their head to the next step.

## What not to cut

- Confirmation of irreversible actions.
- Consent to data processing and medical, legal, financial safeguards.
- Complexity of the offer itself: show it clearly, do not hide it.
- A default that benefits the service and harms the user is not load reduction but manipulation.
