# journey.json format

One schema for every step of the audit: logic, edge cases, load, vision. Required fields are marked `*`. Fill the rest when there is data; an empty field is better than an invented one.

A complete working example: `examples/card-reissue/journey.json` in the repository.

```json
{
  "title": "Reissue a lost debit card",
  "source": "ai | human | code | mixed",
  "persona": {
    "name": "Commuter, 47, lost the card on the way to work",
    "tech": "low | mid | high",
    "patience": "low | mid | high",
    "context": "mobile app, standing in a train, 10 minutes",
    "goal": "block the card and get a new one without visiting a branch"
  },
  "jtbd": "Make sure nobody can spend my money and keep paying today",
  "trigger": "Notices the wallet is missing",
  "scenario": "main | <name of an edge scenario>",
  "success": "Old card blocked, new card ordered, the user knows how to pay until it arrives",
  "owner_vision": [
    {"id": "V1", "expect": "Blocking takes one tap from the home screen", "steps": ["s2"], "origin": "owner"},
    {"id": "V2", "expect": "The user can pay today with a virtual card", "steps": [], "origin": "product brief, section Goals"}
  ],
  "internal_terms": ["reissue_flow"],
  "allowed_terms": ["IBAN"],
  "steps": [
    {
      "id": "s1",
      "stage": "Notice",
      "actor": "user | system | external",
      "action": "Opens the banking app",
      "response": "Home screen with balance and card tile",
      "channel": "mobile app",
      "feeling": -1,
      "feeling_reason": "Anxious: the wallet is gone",
      "moment_of_truth": false,
      "src": "AI map, row 1",
      "evidence": "",
      "assumption": true,
      "failure": "",
      "recovery": "",
      "failure_severity": "",
      "status_feedback": true,
      "load": {
        "decisions": 1, "max_options": 6, "fields": 0, "new_terms": 0,
        "memory_items": 0, "context_switches": 0, "wait_s": 0, "uncertainty": 1,
        "klm": "M P B B"
      }
    }
  ],
  "branches": [
    {"id": "b1", "from": "s4", "title": "Blocking fails", "steps": ["…same step format, ids b1.s1, b1.s2…"]}
  ]
}
```

## Step fields

| Field | Meaning | Rule |
|---|---|---|
| `id`* | Stable identifier | `s1`, `s2`… In branches write the full id `b1.s1`; the script also accepts a short `s1` inside a branch and adds the prefix. `owner_vision.steps` always uses full ids |
| `actor`* | Who acts | System and external-service actions are separate steps when they take time or can fail |
| `action`* | One action | Verb + object. Two verbs joined by "and then" → split |
| `response` | What the user sees in return | Empty on a user step → finding L06 |
| `feeling` | −2…+2 relative to the previous step | Without `feeling_reason` → L08 |
| `src` | Where in the input the step comes from | Map row, screen, code file. This is not evidence of behaviour |
| `evidence` | Data about real behaviour or verified product state | Interview, analytics, session recording, test run, `code: routes.ts`. A map row does not go here. Empty → guess, and L10 fires on a moment of truth |
| `assumption` | Value inferred, not taken from a source | `true` for everything the AI made up |
| `failure` / `recovery` | What breaks and how to get out | No recovery → L05. `recovery: "unknown"` when the input is silent (medium instead of high/critical) |
| `failure_severity` | Manual severity for L05 | Default: critical on a moment of truth, high elsewhere. Lower it if the way out is obvious from the UI |
| `status_feedback` | Is there a status indicator while waiting | Required when `wait_s ≥ 1` |
| `moment_of_truth` | Step where the user decides whether to stay and trust | Without evidence → L10 |
| `load` | Inputs for the load model | See `journey-load/references/cognitive-load.md`. For system steps fill only `wait_s` and `uncertainty` |
| `load.wait_s` | Wait, seconds | Number or `"unknown"`. Unknown duration is itself a finding (L14); do not write 0 |

## Root fields

| Field | Meaning |
|---|---|
| `owner_vision[].status` | `covered` / `at-risk` / `violated` / `not-mentioned`. Set by the CJM auditor after review; without it the script treats an item with step links as covered |
| `owner_vision[].origin` | `owner` — from the product owner; otherwise where it was reconstructed from. Reports flag reconstructed vision |
| `internal_terms` | Product-internal words users should never see (regex cannot catch them in every language) |
| `allowed_terms` | Abbreviations the audience knows; PDF, JPEG, PNG, HEIC, SMS, QR, PIN, CVV are allowed by default |

## Normalizing someone else's CJM

1. Split table rows ("stage") into one-action steps. Columns "does / sees / response" → `action` / `response`.
2. Columns "undo" or "errors" → `failure` + `recovery` or a separate branch.
3. If the source has no emotions, set them yourself with `assumption: true` and a reason.
4. List in `frame.md` everything you had to invent. The list itself shows where the journey is underspecified.
