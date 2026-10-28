# CJM logic · Reissue a lost debit card

Mode: full. Methods: script checks L01–L20, mature-map review (method 4), emotion curve, service layers, vision coverage. Source: AI draft `journey-map.md`, no other evidence.

## Summary

17 findings: **3 critical · 6 high · 7 medium · 1 low**.

The map does half of the job. It blocks the card, but the second half of the JTBD ("keep paying for things today") has no stage. The journey ends on a home screen without any card, 5–7 days before the new one arrives. Two of three owner vision items are broken by content, though the script marks them covered by step links.

## Findings

| ID | Sev | Check | Steps | Finding |
|---|---|---|---|---|
| CJM-01 | critical | H1 | s10 | Stated job "keep paying today" has no stage; journey ends with no card |
| CJM-02 | critical | V1 | s1–s3 | "One tap from home" vs 3+ taps, 9-action screen, choice dialog |
| CJM-07 | critical | L05 | b1.s1 | Blocking failure: generic error, card stays active, no way out |
| CJM-03 | high | V2 | — | Virtual card for paying today is in no step |
| CJM-04 | high | V3 | s8 | Delivery as "5–7 days", only in the summary at confirmation |
| CJM-05 | high | H1 | s6, s8 | Fee first appears in the order summary |
| CJM-06 | high | L05 | s3 | Wrong block type stops the reissue; recovery unknown |
| CJM-10 | high | L13 | s9 | Issuer rejection / missing push not described |
| CJM-12 | high | L10 | s3, s8 | Moments of truth assumed; 73 % of steps assumed |
| CJM-08 | medium | L14 | s4 | Block wait duration unknown |
| CJM-09 | medium | L19 | s5 | BLOCKED_PERM shown to the user |
| CJM-11 | medium | L04 | s2 | Two actions merged in one step |
| CJM-13 | medium | H1 | s7 | "On the move" vs typing a full address |
| CJM-14 | medium | L18 | s6 | Card design and name on card asked on reissue |
| CJM-15 | medium | L15 | s10 | Wait, delivery, activation, return visit not on the map |
| CJM-16 | medium | L07 | s5 | No check of spending between loss and block |
| CJM-17 | low | NORM | s3, b1.s1 | Some journey.json facts are not in the map |

### Severity changes vs the script

- L05 s3: medium → high (moment of truth, failure stops the main job).
- L05/L14 b1.s1: high → critical, merged into CJM-07 (card stays spendable).
- L13 s4: dropped, its failure is branch b1.
- L11 folded into CJM-12; L12 folded into CJM-01.
- Vision: V1 covered → violated, V3 covered → at-risk (script reads step links only).

## Mature-map review

**Contradictions inside the document**

1. "Keep paying for things today" (Who and why, JTBD, success) vs row 8 "Home screen without a card tile" → CJM-01.
2. V1 "one tap" vs rows 2–3 → CJM-02.
3. "Usually on the phone, often on the move" vs row 6 "Types the delivery address" → CJM-13.

**Map vs live product:** not possible, no screenshots, code or analytics (L16 not checked).

**Moments of truth**

| Step | Decision | Evidence | Failure / way out |
|---|---|---|---|
| s3 | Which block type | none | Temporary → no reissue; recovery unknown |
| s8 | Accept fee and a week without a card | none | Not described |

**Failures without a way out:** s3 (unknown), b1.s1 (none), s9 (not described).

**Skew:** the map is detailed on the happy-path screens. It is silent on errors (one line for the whole journey), on the time after the order, and on fraud checks.

## Emotion curve

`cjm/emotion-curve.svg`. All emotions were set during normalization (assumption), not taken from the source.

| Step | Emotion | Cause | Dip type |
|---|---|---|---|
| s1 | −1 | Wallet is gone | Trigger (outside product) |
| s2 | −1 | Searching for the block action | Product / UX |
| s3 | −1 | Unclear which block type | Product / UX |
| s5 | +1 | Money is safe | — (peak) |
| s6 | 0 | Expected one tap, got a form | Product / UX |
| s7 | −1 | Typing an address in a train | Product / UX |
| s8 | −1 | A week without a card, unannounced fee | Value + Product / UX |
| s10 | −1 | Cannot pay for lunch today | **Value** |

- EC2: dips present, no happy monotony.
- EC4/L12: the success ending sits at −1, which contradicts the claimed success.
- Value failures (s8, s10) need a business decision (instant virtual card, fee policy), not a screen change. See CJM-01 and CJM-03.
- **Keep:** the relief at s5 ("money is safe"), the only point above zero. TO BE must keep the block confirmation clear and early.

## Service layers (seams only)

| Step | Frontstage | Backstage | Issue |
|---|---|---|---|
| s4 | Spinner | Processing provider blocks the card | No duration (SL2) |
| b1.s1 | Generic error | Provider timeout | User cannot tell the card is still active (SL2, SL6) |
| s5 | BLOCKED_PERM | Card status | Backstage code in frontstage (SL1) |
| s9 | Push | Issuer accepts order | No failure, no in-app status (SL3) |

## Vision coverage

| Item | Script | After review | Finding |
|---|---|---|---|
| V1 one-tap blocking | covered | **violated** | CJM-02 |
| V2 pay today, virtual card | not mentioned | not mentioned | CJM-03, CJM-01 |
| V3 date before confirm | covered | at-risk | CJM-04 |

Added by the AI without being asked: card design and name on card in the reissue form (CJM-14); the temporary/permanent choice on blocking (CJM-06). Each one adds a decision. The owner decides whether to keep them.

## Hand over to other families

- edge: temporary block later turned into permanent; card found after a permanent block; relative acting for an elderly parent; no network in a tunnel during s4; old card still in a phone wallet / subscriptions.
- edge: second visit, so where the user sees the order after the card tile disappears.
- load: s2 has 9 options; s7 has about 40 keystrokes in a moving train; s6 has 8 options across 3 fields.
- load: the first-time app user and the large-font persona at s2–s3.

## Not checked

- L16: map vs live product. No screenshots, code or analytics.
- Real emotions and moments of truth: no research data.
- Generic error text and block duration: unknown in the source.

## Method notes

- New `root_cause` label `unrequested-scope` (CJM-14): none of the listed labels covers "fields the AI added beyond the job". `implementation-in-map` is about design or tech details, not about extra user decisions.
- The `vision` script's "covered" status is easy to misread as a result. Two of three items changed on review.
