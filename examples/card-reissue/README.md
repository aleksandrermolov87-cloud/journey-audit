# Example: reissue a lost debit card

An AI-drafted customer journey for a mobile banking app, audited end to end with `journey-audit`. Everything here was produced by the skill family itself; the only hand-written files are the source map and the frame.

| Step | File |
|---|---|
| Source map (AI draft) | [`journey-map.md`](journey-map.md) |
| Frame, vision, what was assumed | [`audit/frame.md`](audit/frame.md) |
| Normalized journey | [`audit/journey.json`](audit/journey.json) |
| CJM logic report | [`audit/cjm/report.md`](audit/cjm/report.md) · [emotion curve](audit/cjm/emotion-curve.svg) |
| Edge-case report, branches, personas | [`audit/edge/report.md`](audit/edge/report.md) · [`branches.json`](audit/edge/branches.json) · [`personas.json`](audit/edge/personas.json) |
| Cognitive load report | [`audit/load/report.md`](audit/load/report.md) · [load curve](audit/load/load-curve.svg) |
| **Verdict** | [`audit/verdict/verdict.md`](audit/verdict/verdict.md) |
| Specs | [`audit/verdict/specs/`](audit/verdict/specs) — G-01…G-08 |
| One-page summary | [`audit/journey-audit-card-reissue.md`](audit/journey-audit-card-reissue.md) |

## In one paragraph

The map blocks the card and orders a new one, and every step "works". The audit found that the job's second half — *keep paying today* — has no step at all: the journey ends on a home screen without a card, 5–7 days before the new one arrives. A failed block ends in a generic error while the card stays active. "One-tap blocking" from the brief takes four taps and a confusing temporary/permanent dialog. Verdict: **Rework**, 3 P0 and 5 P1 goals, each with a spec.

## Reproduce the script part

```bash
S=../../skills/journey-audit/scripts/journey_check.py
python3 $S check journey.json
python3 $S load  journey.json --persona-tech low --persona-patience low
python3 $S findings audit
python3 $S merge audit | head -40
```

`journey.json` next to this file is the input as normalized by the orchestrator; `audit/journey.json` is the same file inside the work folder.
