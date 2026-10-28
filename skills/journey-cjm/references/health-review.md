# Mature-map review

A method for a map that already looks finished. The task is to find weak spots, not to retell the map.

## 1. Contradictions inside the document

Compare goal sections ("who and why", goals, principles, constraints) with journey stages. For every statement about what the user wants, find the stage that delivers it. Typical gaps:

- a goal names a need, and a stage declines it (a service boundary cuts the main job);
- a principle ("we never give advice X") is broken by a hint, field placeholder or example;
- the context ("usually on a phone") is not reflected in actions (drag and drop, hover, keyboard shortcuts).

Such a finding is critical or high with `root_cause: "goal-contradiction"` and class `provided`: both quotes come from one document. It does not depend on the owner confirming the vision.

## 2. Map vs live product

If `frame.md` lists screenshots, test runs, accessibility trees or code, compare 3–5 key screens: first screen, main action, result, error. Record drift as L16 with `root_cause: "map-vs-product-drift"` and a file reference. Compare dates: a screenshot older than the map's commit means the map is a plan; newer means the map is outdated.

## 3. Moments of truth

List the steps where the user decides whether to trust the service and continue. For each: is there evidence (interviews, analytics), is there a failure and a way out. A moment of truth without evidence is a hypothesis to validate with people (L10).

## 4. Failures without a way out

Walk all steps with a failure. For each: what the user sees, what they can do, where the way out leads. "Cancel" without an answer to "and then what" is not a way out.

## 5. Thin coverage and skew

- Steps with only the required fields among detailed ones — the map is not thought through there.
- Skew: detailed about animation and components, silent about errors, data, roles, accessibility. Phrase it as "the map is detailed on X, silent on Y".

## 6. What the AI added beyond the job

Design and implementation decisions inside a CJM (component choices, animation timings, API contracts) are not the user's journey. Mark them as L18 (`root_cause: "implementation-in-map"`) and split: what affects the experience (keep in the map) and what does not (move to a design doc).
