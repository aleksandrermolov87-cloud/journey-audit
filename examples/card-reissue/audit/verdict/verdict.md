# Verdict · Reissue a lost debit card

**Rework.** The journey blocks the card but leaves the user with no way to pay for 5–7 days, and a failed block ends in a generic error while the card stays active. All three P0 goals fit inside the current journey. If the bank cannot issue an instant virtual card (owner decision 1), the verdict becomes **Redesign**: half of the JTBD would then have no answer in the app.

Input: 37 findings (cjm 17 · edge 13 · load 7), all three families valid. Evidence: the AI map only. No screens, code or analytics; 73 % of steps are assumptions.

## Summary by family

| Family | Findings | Main point |
|---|---|---|
| CJM logic | 3 critical · 6 high · 7 medium · 1 low | "Keep paying today" has no stage; V1 and V3 are violated by content; the success ending sits at emotion −1 |
| Edge cases | 2 critical · 4 high · 6 medium · 1 low | All 3 synthetic personas finished `partial`; failed block has no way out; no path for a relative |
| Cognitive load | 3 high · 4 medium | No step above 50; flat load with no recovery step. Address typing is 25.3 of 45.2 s KLM. Exit points at s7, s8, s10 only for the low/low profile |

## Goals

| Goal | Pri | What must become true | Metric · target | Findings | Owner | Effort | Score |
|---|---|---|---|---|---|---|---|
| G-01 | P0 | After blocking, the user can pay today | Permanent blocks followed by a virtual card in the phone wallet within 10 min · ≥ 60 % | CJM-01, CJM-03, EDGE-02, LOAD-07 | business/content | L | 36.0 |
| G-02 | P0 | A failed block says the card is NOT blocked and offers retry and a 24/7 line | Failed blocks resolved (retry or call) within 10 min · ≥ 95 % | CJM-07, EDGE-01, CJM-08, LOAD-03 | engineering | M | 18.0 |
| G-03 | P0 | Blocking starts with one tap from the home screen | Taps from home to "card blocked" · 4 → 2 | CJM-02, LOAD-04 | design | M | 45.0 |
| G-04 | P1 | Fee and delivery date are known before the order form | Orders where fee and date were shown before s6 · 100 % | CJM-04, CJM-05, LOAD-02, EDGE-13 | product | M | 18.0 |
| G-05 | P1 | A relative knows on one screen what they may do for the cardholder | Relatives in test who name the allowed action · ≥ 4 of 5 | EDGE-05 | legal or domain review | S | 16.8 |
| G-06 | P1 | Choosing a block type cannot strand the user without a new card | Temporary blocks from "Lost or stolen" upgraded within 24 h · < 5 % | CJM-06, EDGE-03 (LOAD-05 as constraint) | design | M | 15.0 |
| G-07 | P1 | The blocked card and the order stay visible in the app until the new card is active | Users with a pending order who see its status on home · 100 % | CJM-10, CJM-15, EDGE-04 | product | M | 15.0 |
| G-08 | P1 | An unchanged address is confirmed without typing and shown on the summary | Orders with address confirmed without typing · ≥ 80 % | LOAD-01, CJM-13, EDGE-06 | design | M | 12.6 |

Score = severity × confidence × reach × impact × confirmation / effort (`skills/journey-verdict/references/prioritization.md`). G-03 is P0 by rule (violated vision item on the main job), not by order of score.

**P2** (no specs):

| Findings | Score | Fix hint |
|---|---|---|
| CJM-09, LOAD-06 | 7.5 | Replace BLOCKED_PERM and "reissue" with plain words (covered by G-02 copy for s5) |
| CJM-11, CJM-17 | 6.0 | Map revision: split s2; list invented facts in frame.md |
| CJM-16, EDGE-10 | 5.3 | Adjacent journey: transactions since the loss with "I did not make this" |
| EDGE-11 | 4.2 | Adjacent journey: block without the app; hotline on the public site |
| EDGE-07 | 4.2 | Keep the form draft; idempotent block request; state after reconnect |
| CJM-14 | 4.2 | Card design and name on card: prefilled from the old card, optional (owner decision 6) |

**Deferred:** EDGE-08 (double order on repeat tap, hypothesis), EDGE-09 (cancel order before shipping; the irreversibility line moved to G-06), EDGE-12 (several cards, low confidence).

## Conflicts

| What clashed | Decision | Why |
|---|---|---|
| CJM-02 "remove or default the block-type question" vs LOAD-05 "keep it, useful friction" | Keep the dialog, preselect permanent when entered from "Lost or stolen" (G-03, G-06) | Permanent block is irreversible; the confirmation is a financial safeguard. Made faster, not removed |
| CJM-02 critical vs LOAD-04 medium on the same steps | Critical | Lead finding violates owner vision V1 |
| LOAD-02 "fee on the s5 button" vs CJM-05 "before the form" vs CJM-04 "date on s6 and s8" | Show fee and date on the s5 confirmation, repeat on s8 | One change satisfies all three; s8 only confirms known values |
| EDGE-03 (2 of 3 personas chose wrong) vs CJM-06 (provided failure note) | CJM-06 leads; EDGE-03 stays a hypothesis | Synthetic evidence adds weight, not class |
| LOAD-03 confidence low (30 s wait is from normalization) inside a critical cluster | Cluster keeps CJM-07 values; 30 s not used as a baseline | Lead finding sets confidence; the wait must be measured (G-02) |
| Script K-20 grouped EDGE-11 with LOAD-04 | Split: LOAD-04 → G-03, EDGE-11 → P2 | Different fixes: home entry vs blocking without the app |

## Keep

- **s5 relief "money is safe"**, the only point above zero. TO BE keeps the confirmation first and early; offers come below it.
- **s3 block-type confirmation** (useful friction, LOAD-05): faster with outcome labels and a default, still a deliberate tap.
- **s8 order summary**: stays as the final check of fee, date and address.

## TO BE

Default options of the owner decisions. Fork marked ⑂.

| Stage | User does | Sees | Response | Undo |
|---|---|---|---|---|
| 1. Notice | Opens the app | Home with balance; card tile with "Lost or stolen?" | — | — |
| 2. Block | Taps "Lost or stolen?" | Dialog: two options described by outcome, "Block for good and get a new card" preselected | — | Cancel |
| 3. Block | Taps "Block card" | "Blocking card •• 1234…" with expected time | Provider blocks the card | — |
| 3a. Block failed | — | "Your card is NOT blocked yet" · Try again · Call 24/7 block line | — | Try again |
| 4. Block | Reads the confirmation | "Card •• 1234 is blocked. Nobody can pay with it." · Pay today · Order a new card: fee, arrives by date | — | — |
| 5. Pay today ⑂ | Taps "Get a virtual card" | Virtual card ready · "Add to phone wallet" | Issues the virtual card | Skip |
| 6. Reissue | Taps "Order a new card" | Form: address from profile, design and name from the old card | — | Back |
| 7. Reissue | Confirms or edits the address | Prefilled address; typing only for a new one | — | Edit |
| 8. Reissue | Confirms the order | Summary: fee, delivery by date, address with Edit | Order accepted; status in the app | — |
| 9. Done | Returns to home | Card tile: "New card ordered, arrives by date" · virtual card active | Push on each status change | Track order |

- **Added:** 3a → G-02 · 5 → G-01 · status tile on 9 → G-07 · "Acting for someone else?" link on 2 → G-05
- **Changed:** 1–2 entry from the home tile → G-03 · 2 dialog labels and default → G-06 · 4 plain-language confirmation with fee and date → G-04, P2 · 6–7 prefilled address → G-08 · 8 address on summary → G-08 · 9 home tile → G-07
- **Removed:** old s2 "card settings with 9 actions" from the main path → G-03 (still reachable from the card screen)
- **Kept as useful friction:** 2 block-type confirmation (irreversible) · 8 summary before ordering

## Validation with people

Run first: tasks 1–3 (P0 goals, all on assumptions).

1. **G-01** · hypothesis: after blocking, users do not know how to pay today. Task: "You have just blocked your lost card. Buy a coffee with your phone." 5 commuters, 2 of them 55+. Success: ≥ 4 of 5 add the virtual card to the wallet within 3 min without help.
2. **G-03** · hypothesis: users look for blocking inside card settings. Task: "Your wallet is gone. Make sure nobody can use your card." 5 first-time users. Success: ≥ 4 of 5 reach the block dialog with one tap from home.
3. **G-02** · hypothesis: after a generic error users think the card is blocked. Task: prototype with forced failure; "Is your card safe now?" 5 users. Success: 5 of 5 answer "no" and pick retry or call.
4. **G-06** · hypothesis: low-literacy users pick temporary (EDGE-03). Task: "You will not find this wallet again. Block the card." 5 users 60+, large font. Success: ≥ 4 of 5 choose permanent and can say why.
5. **G-04** · hypothesis: the fee and the week without a card surprise users at s8. Task: order a new card, then "What will it cost and when will it arrive?" asked before the summary. 5 users. Success: ≥ 4 of 5 answer both correctly.
6. **G-08** · hypothesis: users moved in the last year do not check the address. Task: order a new card to a new home. 5 users who moved. Success: 5 of 5 notice and change the address before confirming.
7. **G-05** · hypothesis: relatives do not know whether they may act. Task: "Your father lost his card. Help him." 5 relatives of people 70+. Success: ≥ 4 of 5 name the allowed action within 1 min.

## Owner decisions

1. **Instant virtual card (V2).** Can the bank issue one right after a permanent block? Default: yes. If no: Redesign; options are a temporary card at a branch, cash by code at an ATM, or an honest "you cannot pay by card until <date>".
2. **Reissue fee for a lost card.** Charge, waive, or waive for theft. G-04 needs the rule and the amount.
3. **Delivery date.** A concrete date needs a logistics commitment. Options: "by <date>" from courier SLA; date range with calendar dates; "5–7 days" with the earliest date.
4. **Meaning of V1 "one tap".** Default: one tap opens the block dialog, the confirmation tap stays (irreversible action). Alternative: one tap blocks temporarily, permanent follows.
5. **Representatives.** May a relative block a card, order a reissue, change the address? Default: block only via the 24/7 line; reissue only by the cardholder. Needs legal review.
6. **Temporary → permanent.** Can a temporary block be upgraded in the app and still allow a reissue? Default: yes.
7. **Reissue form fields.** Keep card design and name on card, prefilled from the old card, or drop them.

## Not checked

- Map vs live product (L16): no screens, code or analytics. Specs describe the map; verify against the product before building.
- Real blocking and issuer wait times; text of the generic error; copy of the s3 dialog.
- Screen reader and keyboard (E10), entry from push or the bank's site (E01).
- Real emotions and moments of truth: all emotions set during normalization.
- Adjacent journeys not audited: disputes after theft, blocking without the app, tracking and activating the new card.

## Method notes

- Merged by meaning beyond the script: K-01 + K-03 (+ LOAD-07) → G-01; K-06 + K-07 → G-02; K-09 + K-14 → G-07; K-12 + K-18 → G-08; K-05 + K-16 (+ K-22 as constraint) → G-06; LOAD-04 moved from K-20 to G-03.
- CJM-12 (moments of truth unvalidated, script P1) is not a fix; it became validation tasks 4–5. CJM-17 moved to P2 map revision.
- EDGE-05 kept at P1 by rule "high on the main path", although most of its spec waits for owner decision 5.
- Confidence was not raised anywhere: EDGE-03, EDGE-06 and EDGE-13 remain synthetic; LOAD findings remain model outputs.
- Effort set by the verdict: S 1 · M 2 · L 3. G-01 is L because issuing and provisioning a virtual card may need a backend and a wallet integration.
