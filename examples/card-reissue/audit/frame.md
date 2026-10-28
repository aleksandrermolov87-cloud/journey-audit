# Audit frame: reissue a lost debit card

| | |
|---|---|
| Source | `examples/card-reissue/journey-map.md` (AI draft) |
| Version | First version in this repository |
| Main persona | Commuter, 47, lost the card on the way to work; phone, standing in a train, 10 minutes; tech mid, patience low |
| Other personas | First-time app user; low digital literacy, large font; relative acting for an elderly parent |
| JTBD | Make sure nobody can spend my money and keep paying for things today |
| Trigger | Notices the wallet is missing at the station |
| Scenario | Main: block permanently → reissue |
| Success | Old card blocked, new card ordered, the user knows how to pay until it arrives |
| Device | Mobile app |
| Source of the journey | AI |

## Owner's vision

From the product brief in the source (`origin: owner`): V1 one-tap blocking from the home screen · V2 pay today with a virtual card · V3 delivery date shown before confirmation.

## Evidence

None besides the map. No screenshots, analytics or code.

## Invented during normalization

1. Stage 2 split into "taps the card tile" + "opens settings" kept in one step (s2) to show L04.
2. Emotions of all user steps set during normalization (`assumption: true`).
3. Moments of truth: s3 (block type), s8 (order summary).
4. Duration of blocking (s4) is not in the map → `wait_s: "unknown"`.
5. Branch b1 "blocking fails" built from the Errors section; the generic error text is unknown. Its 30 s wait without status is an assumption, not in the source.
6. s3 failure "chooses temporary block, cannot order a new card later" is inferred from the two-option dialog; recovery set to `unknown`.
