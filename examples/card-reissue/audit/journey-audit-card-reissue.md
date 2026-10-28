# Journey audit: reissue a lost debit card

Source: [`journey-map.md`](../journey-map.md) (AI draft, mobile banking app) · frame: [`frame.md`](frame.md) · normalized: [`journey.json`](journey.json)

Persona: commuter, 47, lost the wallet on the way to work; phone in a train, 10 minutes; tech mid, patience low. JTBD: make sure nobody can spend the money and keep paying today. Success: old card blocked, new card ordered, the user knows how to pay until it arrives.

## Verdict

**Rework.** Three P0 goals (pay today, honest blocking failure, one-tap blocking) are solvable inside the current journey; the verdict becomes **Redesign** if the bank cannot issue an instant virtual card.

## Summary

| | |
|---|---|
| Findings | 37 — CJM logic 17 (3 critical, 6 high), edge cases 13 (2 critical, 4 high), cognitive load 7 (3 high) |
| After merging | 8 goals (3 P0, 5 P1), 6 P2 rows, 3 deferred |
| Evidence | The AI map only; 73 % of steps are assumptions |
| Load | No step above 50; flat moderate load without a recovery step; address typing = 25.3 of 45.2 s KLM; exit points at s7, s8, s10 for the low/low profile |
| Personas | 3 of 3 finished `partial`; 2 stuck on the temporary/permanent dialog |
| Vision | V1 one-tap blocking — violated · V2 pay today — violated · V3 delivery date before confirmation — at risk |

## P0 and P1 goals

| Goal | Priority | Metric (target) | Spec |
|---|---|---|---|
| After blocking, the user can pay today | P0 | Permanent blocks followed by a virtual card in the wallet within 10 min (≥ 60 %) | [G-01](verdict/specs/G-01.md) |
| A failed block says the card is NOT blocked and offers retry and a 24/7 line | P0 | Failed blocks resolved within 10 min (≥ 95 %) | [G-02](verdict/specs/G-02.md) |
| Blocking starts with one tap from the home screen | P0 | Taps from home to "card blocked" (4 → 2) | [G-03](verdict/specs/G-03.md) |
| Fee and delivery date are known before the order form | P1 | Orders with fee and date shown before s6 (100 %) | [G-04](verdict/specs/G-04.md) |
| A relative knows on one screen what they may do | P1 | Relatives who name the allowed action (≥ 4 of 5) | [G-05](verdict/specs/G-05.md) |
| Choosing a block type cannot strand the user without a new card | P1 | Temporary blocks from "Lost or stolen" upgraded within 24 h (< 5 %) | [G-06](verdict/specs/G-06.md) |
| The blocked card and the order stay visible until the new card is active | P1 | Users with a pending order who see its status on home (100 %) | [G-07](verdict/specs/G-07.md) |
| An unchanged address is confirmed without typing | P1 | Orders with address confirmed without typing (≥ 80 %) | [G-08](verdict/specs/G-08.md) |

## Owner decisions

Seven, listed in [`verdict.md`](verdict/verdict.md#owner-decisions): instant virtual card, reissue fee, delivery date commitment, meaning of "one tap", representatives, temporary → permanent upgrade, reissue form fields.

## Not checked

Live UI, screens, code and analytics (none provided); screen reader and keyboard; entry from a push or the website.

## Files

[Verdict](verdict/verdict.md) · [CJM logic](cjm/report.md) · [Edge cases](edge/report.md) · [Cognitive load](load/report.md) · [backlog.json](verdict/backlog.json)
