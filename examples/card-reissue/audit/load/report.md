# Cognitive load · Reissue a lost debit card

Model, not measurement. Index 0–100 with open weights (`skills/journey-load/references/cognitive-load.md`); KLM is error-free time of an experienced user. Main persona from `frame.md`: tech mid, patience low.

## What was checked

- Refined `load` features (3 changes, `load/load-overrides.json`).
- Index, KLM, fatigue and exit points for four profiles: high/high, mid/mid, mid/low (main persona), low/low.
- Branch b1 computed after s1–s3 so fatigue carries over.
- Nielsen and Krug heuristics for steps with an exit point and for shared peaks.

## Refinements

| Step | Field | From → to | Reason |
|---|---|---|---|
| s6 | max_options | 8 → 3 | Map lists 3 form parts; number of card designs not given |
| s7 | fields | 2 → 1 | Map shows one address field |
| s7 | context_switches | 1 → 0 | Map does not say the address is looked up elsewhere |

Effect on the main persona: s7 42.9 → 33.4; exit points at s7, s8, s10 (F 109.1, 109.7, 100.5) disappear, F peaks at 99.3 on s8. In low/low the exit points remain.

## Load table (main persona mid/low · low/low)

| Step | Index | Level | F | KLM, s | Main contributions |
|---|---|---|---|---|---|
| s1 | 28.0 · 35.0 | moderate | 28.0 · 35.0 | 2.65 | decisions 20, uncertainty 8 |
| s2 | 36.6 · 45.8 | moderate | 57.6 · 72.0 | 5.3 | decisions 29, uncertainty 8 |
| s3 | 35.9 · 44.9 | moderate | 79.2 · 98.9 | 2.65 | uncertainty 16, decisions 14 |
| s4 (system) | 8.0 · 10.0 | low | 59.4 · 74.2 | — | wait unknown, uncertainty 8 |
| s5 | 25.9 · 32.4 | moderate | 70.4 · 88.1 | 1.35 | decisions 14, terms 12 |
| s6 | 29.5 · 36.9 | moderate | 82.3 · 102.9 | 2.65 | decisions 22, fields 8 |
| s7 | 33.4 · 41.8 | moderate | 95.2 · **119.0** | 25.3 | decisions 19, memory 12 |
| s8 | 27.9 · 34.9 | moderate | 99.3 · **124.1** | 2.65 | decisions 14, uncertainty 8 |
| s9 (system) | 9.0 · 11.2 | low | 83.5 · 104.4 | — | wait 9 |
| s10 | 32.0 · 40.0 | moderate | 94.6 · **118.3** | 2.65 | uncertainty 16, decisions 16 |

Bold: exit point (F ≥ 100 with low patience and emotion ≤ −1). Total KLM 45.2 s (mid, low), 36.4 s (high). Curve: `load/load-curve.svg` (low/low).

No step reaches 50 on the main path. The load is flat: 8 user steps between 25 and 46, none below 25, so fatigue builds without a recovery step.

Branch b1 (blocking fails): b1.s1 60.6 (mid/low), 75.7 overload (low/low), 30 s wait without status, exit point. The 30 s comes from normalization.

## Persona sensitivity

| Profile | Peak | Max F | Exit points |
|---|---|---|---|
| high/high | s2 31.1 | 84.4 | — |
| mid/mid | s2 36.6 | 99.3 | — |
| mid/low (main) | s2 36.6 | 99.3 | — |
| low/low | s2 45.8 | 124.1 | s7, s8, s10 |

- Shared peak: s2 in every profile. Extraneous (menu depth, 9 options).
- Switch steps: s7, s8, s10 become exit points only in low/low.
- KLM: s7 typing is 25.3 s of 45.2 s; on a phone the gap between profiles is all in typing.
- Not modelled: large font (form and summary scroll, more memory items), screen reader (spinner and live status at s4), one hand in a train (P costs more).

## Findings

| Id | Check | Severity | Steps | Title |
|---|---|---|---|---|
| LOAD-01 | C-s7 | high | s7 | Address typing takes 56% of KLM time |
| LOAD-02 | C-s8 | high | s8 | Fee and delivery first shown at confirmation |
| LOAD-03 | C-s4 | high | s4, b1.s1 | Unknown blocking wait; 30 s silent wait on failure |
| LOAD-04 | C-s2 | medium | s1, s2 | Two screens and 9 actions before Block |
| LOAD-05 | C-s3 | medium | s3 | Block type without consequences (useful friction) |
| LOAD-06 | C-s5 | medium | s5 | Internal status BLOCKED_PERM on confirmation |
| LOAD-07 | C-s10 | medium | s10 | No way to pay today at the end |

## Intrinsic and extraneous

| Step | Intrinsic (keep, present clearly) | Extraneous (lever) |
|---|---|---|
| s2 | — | Menu depth, 9 options → remove noise: Lost card on the home tile |
| s3 | Choice of irreversible block | Unexplained options → familiar model: outcome-based labels, default |
| s5 | Confirmation that money is safe | Internal status → user words |
| s6–s7 | Confirming where to send the card | 40 keystrokes → take the work over: prefill address |
| s8 | Accepting fee and delivery time | First mention of fee → show earlier |
| s10 | — | Open question about paying today → take the work over: virtual card |

## Hand over to other families

- CJM: temporary block at s3 has no route to reissue (map's failure note, recovery unknown).
- CJM: V2 virtual card has no step in the journey.
- CJM: fee is a value issue not mentioned before s8.
- Edge: b1 has no recovery; generic error text unknown.
- Edge: home screen without a card tile at s10 — what the user sees on next login.

## Not checked

- No screens: s1 home screen options (6), card design count and summary layout not verified.
- Real blocking and issuer wait times: not in the source; no wait scenario computed.
- Copy of the s3 dialog and the error in b1.

## Method notes

- An exit point on the final step (s10) is read as leaving without a payment method, since the order is already placed.
- Patience changes only waits and exit thresholds, so mid/mid and mid/low give the same user-step indices.
