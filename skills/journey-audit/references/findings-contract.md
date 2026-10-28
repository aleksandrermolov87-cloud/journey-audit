# Findings contract

All three auditors write findings in one format; otherwise the verdict cannot compare and merge them. `journey_check.py findings <work>` validates the contract. JSON values are always in English; prose fields (`title`, `detail`, …) are in the user's language.

## `<family>/findings.json`

```json
{
  "family": "cjm | edge | load",
  "journey": "journey.json",
  "mode": "full | quick",
  "methods": ["L01–L20", "emotion-curve", "health-review"],
  "not_checked": ["L16 — no screenshots of the live UI"],
  "summary": "2–4 lines with numbers",
  "report_md": "# CJM logic · …\n\n…full family report in markdown…",
  "findings": [
    {
      "id": "CJM-01",
      "family": "cjm",
      "check": "L05",
      "severity": "critical",
      "steps": ["s3", "b1.s1"],
      "title": "Temporary block cannot be turned into a reissue",
      "detail": "What exactly is wrong, quoting the input",
      "evidence_class": "provided",
      "evidence_ref": "journey-map.md, row 3",
      "consequence": "What happens to the user",
      "fix_hint": "Direction of the fix, one or two lines",
      "confidence": "high",
      "frequency": 2,
      "impact": 3,
      "useful_friction": false,
      "vision": ["V1"],
      "vision_status": "violated",
      "personas": ["p2", "p3"],
      "root_cause": "dead-end-failure"
    }
  ]
}
```

## Fields

| Field | Required | Values |
|---|---|---|
| `id` | yes | `CJM-NN`, `EDGE-NN`, `LOAD-NN`, unique within the file |
| `family` | yes | Matches the file's family |
| `check` | yes | Family check code: `L05`, `E11`, `P-p3`, `C-s7`, `H3`, `V2` |
| `severity` | yes | `critical` — the journey fails the job or misleads; `high` — visible failure of experience; `medium` — a gap; `low` — map quality |
| `steps` | yes | Full step ids from journey.json or edge/branches.json; `[]` for the whole journey |
| `title` | yes | Up to 90 characters, a fact, not a judgement |
| `evidence_class` | yes | `provided` (the input contains the text, screen, code, data) · `absent` (the input is silent about something that must be there) · `synthetic` (a simulated persona did it) · `interpretation` · `hypothesis` · `unknown`. If a finding rests on a fact and on a conclusion from it, use the fact's class and put the conclusion into `detail` marked "interpretation:" |
| `evidence_ref` | with `provided` | File and place |
| `confidence` | yes | `high` · `med` · `low` — confidence in the interpretation |
| `frequency` | edge: yes | 1–3: share of users affected |
| `impact` | edge: yes | 1–3: inconvenience · lost time or data · harm, wrong decision, drop-off |
| `useful_friction` | no | `true` if the finding is about friction that protects the user; the verdict speeds it up but never removes it |
| `vision` / `vision_status` | no | Vision items the finding confirms or breaks; `covered` · `at-risk` · `violated` · `not-mentioned` |
| `personas` | no | Persona ids where it showed up (`check: "P"` for several personas) |
| `root_cause` | no, strongly advised | Label from the list below; the verdict merges duplicates across families by it |

## `root_cause` labels

Pick from the list, otherwise the verdict will not see that three families found one cause. The label names the cause, not the symptom: a refusal without a route is `boundary-without-alternative` for logic, edge cases and load alike.

`boundary-without-alternative` · `goal-contradiction` · `value-failure` · `silent-mode-switch` · `hidden-without-explanation` · `unknown-wait` · `internal-language` · `no-return-path` · `missing-role` · `merged-steps` · `mobile-context` · `answer-overload` · `external-system-failure` · `dead-end-failure` · `map-vs-product-drift` · `no-evidence` · `no-emergency-path` · `data-error-without-fix` · `implementation-in-map` · `unrequested-scope`

Add a new label only if none fits, and explain it in the report.

## Family report: the `report_md` field

Some environments forbid subagents from creating `.md` files. The report therefore goes as a markdown string into the `report_md` field of the same `findings.json`; the orchestrator expands it into `<family>/report.md` with `journey_check.py render <work>`. Do not work around such a restriction through the shell.

Contents of `report_md`: what was checked, findings table, family artefacts (curve, load table, persona summary, expanded branches), "Hand over to other families", "Not checked", "Method notes" (where the family instructions were unclear).

## Returning to the orchestrator

No more than 5 lines: findings by severity, main finding, file paths, what was not checked.

Validate your own file with `journey_check.py findings <work> --family <cjm|edge|load>` so that other families' missing files do not get in the way.
