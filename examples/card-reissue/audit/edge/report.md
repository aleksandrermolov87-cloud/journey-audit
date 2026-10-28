# Edge cases · Reissue a lost debit card

Mode: full. Methods: axes E01–E14 per stage, flow checklists (waiting, form input, confirmation, payments, roles, exit), 3 synthetic personas in description mode, 5 alternative branches, adjacent journeys. Evidence: the AI map only; no screens, analytics or code.

**Findings: 2 critical · 4 high · 6 medium · 1 low.**

## Findings

| ID | Sev | Axis | Steps | Finding | F×I | Evidence |
|---|---|---|---|---|---|---|
| EDGE-01 | critical | E07 | s4, b1.s1, e1.s1 | Blocking failure ends in a generic error; the card stays active | 1×3 | provided |
| EDGE-02 | critical | E12 | s8, s10, e2.s1 | No way to pay before the new card arrives in 5–7 days | 3×3 | provided |
| EDGE-03 | high | P | s3, e3.s1 | 2 of 3 personas could not tell temporary from permanent block; one chose temporary | 2×3 | synthetic |
| EDGE-04 | high | E02 | s5, s10, e5.s3 | After blocking, the home screen loses the card tile; re-entry to reissue is not described | 2×2 | provided |
| EDGE-05 | high | E06 | s1, s6, s7, e4.s1 | No path for a relative acting on behalf of the cardholder | 2×3 | absent |
| EDGE-06 | high | P-p3 | s8, e4.s4 | The order summary does not show the delivery address | 2×3 | synthetic |
| EDGE-07 | medium | E09 | s7, s4, s8 | Poor network in transit is not covered at the two waits | 3×2 | absent |
| EDGE-08 | medium | E05 | s8 | Repeat tap on confirm during the wait may order two cards and charge two fees | 1×2 | hypothesis |
| EDGE-09 | medium | E14 | s5, s8 | No undo after permanent block or order; wallet found later is not covered | 2×2 | provided |
| EDGE-10 | medium | E11 | journey | Transactions already made with the stolen card have no route | 2×3 | absent |
| EDGE-11 | medium | E09 | journey | Phone lost together with the wallet: the app journey is unavailable | 2×3 | absent |
| EDGE-12 | low | E04 | s2 | Several cards on the account: which tile to block is not described | 1×3 | hypothesis |
| EDGE-13 | medium | P-p1 | s8 | Fee amount is not stated in the map's summary | 3×1 | synthetic |

Main finding: the journey secures the money but not the second half of the JTBD. All three personas finished `partial`; none could pay before the new card arrives (EDGE-02), and a failed block ends in a generic error with the card still active (EDGE-01).

## Scenario table (axes)

| Scenario | Axis | Stage | F | I | Coverage | Priority |
|---|---|---|---|---|---|---|
| Pay today before the card arrives | E12 | Done | 3 | 3 | none | 11 |
| Relative acts for a parent | E06 | All | 2 | 3 | none | 8 |
| Stolen card, charges already made | E11 | after Done | 2 | 3 | none | 8 |
| Phone lost with the wallet | E09 | before Notice | 2 | 3 | none | 8 |
| Address wrong or outdated, not on summary | E04 | Reissue | 2 | 3 | none | 8 |
| Network loss at s4 / s7 / s8 | E09 | Block, Reissue | 3 | 2 | none | 8 |
| Temporary block chosen, new card needed | E04 | Block | 2 | 3 | partial | 6 |
| Interrupted between block and order | E02 | Block → Reissue | 2 | 2 | none | 6 |
| Wallet found after permanent block | E14 | Reissue | 2 | 2 | partial | 4 |
| Blocking fails | E07 | Block | 1 | 3 | partial | 3 |
| Double tap on confirm | E05 | Reissue | 1 | 2 | none | 4 |
| Several cards on the account | E04 | Block | 1 | 3 | none | 5 |

Not applicable: E01 (entry from a push or the bank's site is possible but not in scope of the map), E03 (repeat use is rare for this journey), E08 (weekend delivery only adds to the 5–7 days already found), E10 (covered by p2 with large font; screen reader not checked).

Expanded instead of strict top 5: stolen-card charges and phone-lost-too go to adjacent journeys (they start outside this map); network loss is cross-cutting, not a branch. Blocking failure (priority 3) is expanded for its impact on money.

## Alternative branches (`edge/branches.json`)

| Branch | From | Title | Steps | Today |
|---|---|---|---|---|
| e1 | s4 | Blocking fails or times out | 4 | generic error, then unknown |
| e2 | s5 | Pay today before the new card arrives (V2) | 4 | absent |
| e3 | s3 | Temporary block chosen, new card needed | 3 | unknown after the choice |
| e4 | s1 | Relative acts for an elderly parent | 4 | unknown |
| e5 | s5 | Interrupted between blocking and ordering | 3 | unknown |

Proposed behaviour in the branches is marked "Proposed"; no screens were invented.

## Synthetic personas

Description mode, two stages: home screen without a task, then the mission with 9 screens under shuffled labels.

| Persona | Outcome | Exit | Main friction | Quote |
|---|---|---|---|---|
| p1 Dan, 29, first time in the app | partial | s8 | No way to pay today; fee amount unknown | "So what do I pay for lunch today?" |
| p2 Valentina, 66, large font, low literacy | partial | s3 | Chose temporary: permanent reads as irreversible | "Which one is the permanent one?" |
| p3 Marina, 41, acting for her father | partial | — | Address not on the summary; unsure she may act | "Is it even mine to do this?" |

- Shared friction (2+): block dialog without consequences (p1, p2); generic spinner error (all 3); 'BLOCKED_PERM' / 'reissue' unclear (p1, p2).
- Personas found 2 findings not covered by the checklists: EDGE-06 (address missing from summary), EDGE-13 (fee amount unknown).
- Hint check: missions avoid the words block, reissue, virtual. The dialog's own labels were shown, so unanimity at s3 is weighted lower.
- Check with people: p2's choice at s3 with 5 low-literacy users; p3's address check with users who moved in the last year.

## Adjacent journeys (ranked)

1. Dispute charges made with a stolen card: frequent after theft, money at stake, no entry in the map.
2. Block a card without the app (phone lost too, or no smartphone): the emergency route the map assumes away.
3. Act on behalf of a relative: a persona in the frame without a policy or path.
4. Track and activate the new card: the map ends at the order; delivery, activation and PIN are not described.
5. Found the wallet: cancel the order, fee refund, what happens to the permanent block.

## Hand over to other families

- CJM: s8 shows fee and delivery term in response to confirming; V3 ("date before confirmation") likely violated.
- CJM: V1 one-tap blocking contradicts s2 (two taps plus a 9-action screen).
- Load: s7 address entry, K*40 on a phone in a moving train.
- Load: internal status 'BLOCKED_PERM' and the word 'reissue' shown to users (s5).

## Not checked

- Live product, screens, code, analytics: none provided.
- E10 screen reader and keyboard; E01 entry from push or website.
- Persona answers come from one model run each; findings are `synthetic` until checked with people.

## Method notes

- The persona protocol asks to neutralize tested labels; at s3 the label is the object of the test, so it stayed visible.
- `Personas: yes (3)` is below the 4–6 recommended by the method; the cast follows frame.md.
