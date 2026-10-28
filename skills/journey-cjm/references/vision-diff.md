# Owner-vision coverage

## Statuses

| `vision_status` | When |
|---|---|
| `covered` | A step delivers the item and no step contradicts it |
| `at-risk` | Delivered, but a detail may break it (a hint, copy, example) |
| `violated` | A step directly contradicts the item |
| `not-mentioned` | No step touches the item |

Write the status into the finding's `vision_status` (never into journey.json — it is read-only). The `vision` script marks an item "covered" only because a step is linked, without reading its content: it is a draft, review every status.

## What the AI added unasked

A separate list: steps, features, promises, tone that are not in the vision and do not follow from the user's job. For each: does it change the journey (adds a step, a decision, copy) and does it get in the way of a vision item. No "good" or "bad" — the owner decides.

## Reconstructed vision

If an item's `origin` is not `owner`, set `confidence` no higher than `med` in findings about it — except contradictions inside one document (goal vs stage): they hold regardless of the owner's confirmation. Write in the report: "vision reconstructed from <source>, needs the owner's confirmation".

## Findings

A violated item is critical when it concerns safety, money, health, legal rights or the main job; otherwise high. A not-mentioned item is high. Check code = item id (`V2`), plus `vision: ["V2"]`.
