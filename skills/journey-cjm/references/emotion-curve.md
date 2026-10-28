# Emotion curve

## One time unit rule

One step is one loop: the user does one action → the product or the world responds → the user feels something, and the curve moves from its previous level. Steps never overlap, so the map is complete and without overlaps. Feeling is cumulative: a dip right after a rise hurts more than the same dip at the start.

Scale −2…+2 (halves allowed): +2 delighted · +1 pleased, hopeful · 0 neutral · −1 irritated, anxious · −2 angry, ready to quit. Most journeys start slightly above zero: the person arrives with intent.

## Checks

| Code | Check |
|---|---|
| EC1 | Every point has a cause in the same step ("generally anxious" is not a cause) |
| EC2 | The curve goes below zero at least once. If not, it is happy monotony, typical of AI: look for the hidden dip |
| EC3 | A dip after a peak is explained: what exactly broke the expectation |
| EC4 | The ending matches the outcome: success above zero, drop-off below |
| EC5 | Offline steps (find a document, wait for an SMS, call) are on the curve |
| EC6 | Emotions are set for this persona in this context, not for an "average user" |

## Types of dips

Give every dip below zero a type. The type decides who fixes it:

| Type | Who fixes | Example |
|---|---|---|
| Performance | Engineering | Slow load, timeout |
| Product / UX | Product and design | Feature hard to find, confusing order, extra fields |
| Value | Business | The service does not do the job: no data, no service, no right. A button will not fix it |
| External dependency | Partner, integration | Payment gateway, government service, OCR, LLM provider |
| AI answer quality | Prompt, data, evals | Wrong language or format, generic text, fabrication, low trust, the user does not know what to ask |

Write a value failure as a separate finding with `root_cause: "value-failure"`: the verdict will set a business goal for it, not a design goal.

## Peaks

For every peak above +1 name the cause: job done, a fast or unexpectedly convenient detail, an answer that feels personal. Peaks are what TO BE must not break. List them in the report under "Keep".

## Artefact

`emotion-curve.svg` (script `curve`) + table: step · emotion · cause · dip type. If you set the emotions rather than the source, say so (`assumption`).
