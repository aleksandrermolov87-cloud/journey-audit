# Synthetic personas

A synthetic persona is an LLM walking the journey as a specific person. It finds places where the journey relies on knowledge that person does not have. It does not replace real users: its findings have the class `synthetic` and need validation with people.

## Choosing the cast

4–6 personas. Choose by traits that break journeys, not by demographics:

| Trait | Example |
|---|---|
| First time, no context | Came by a link, does not know what the service is |
| In a hurry | 2 minutes between tasks, skims |
| Low digital literacy | Cannot tell a field from a button, afraid to tap "the wrong thing" |
| Returning | Was here a week ago, expects everything to be saved |
| Another role | A relative for the customer, an accountant for the director |
| Assistive technology | Screen reader, large font, keyboard only |
| Sceptic / anxious | Looks for a catch, checks every claim |
| Domain expert | Knows the subject better than the service, checks facts |

Persona card:

```json
{
  "id": "p3",
  "name": "Irina, 61",
  "role": "customer",
  "tech": "low", "patience": "low",
  "device": "Android, large font, mobile internet",
  "arrival": "her daughter sent a link in a messenger: 'do it there'",
  "knows_cold": "her own accounts and how she has used them for years",
  "objections": "does not trust websites, afraid of data leaks",
  "would_convert_if": "sees the result is based on a document she trusts",
  "gives_up_when": "unclear what to tap, or asked to register"
}
```

## Protocol

1. **Free exploration.** No mission, no explanation of how the service works. The persona writes what it noticed first, what it understood in 5 seconds, what it believes is tappable, what it expects.
2. **Mental model.** How the persona would name the service, where it expects functions to live, what it thinks happens after a tap.
3. **Mission.** A neutral task in the persona's own words, without screen names ("block the card you lost"). The persona records choices, detours, doubts and where it would stop.
4. **Wrap-up.** Outcome (`done` / `partial` / `abandoned` / `blocked`), exit step, quotes in the persona's voice, top 3 fixes.

Do not show the intended route before stage 3 ends. If the persona goes the wrong way, that is the finding.

If a transition is unknown (no screen in the input), the persona does not invent it: the step is `unknown`.

## Description mode (no browser)

A list of screens in order already hints at the route, so never give the whole journey in one prompt. Run two stages:

1. **Stage A (free exploration and mental model).** Give the subagent the persona card and only the first screen (copy, buttons, fields). No mission. Questions: what did you notice first, what did you understand in 5 seconds, what would you tap, what do you expect after it, how would you name this service. Short JSON answer.
2. **Stage B (mission).** A new call or a continuation: the mission + screens one at a time in response to the persona's actions. If step-by-step is impossible, give screens with shuffled labels `screen A, B, C` without step numbers or stage names, and let the persona choose where to go. Remove or neutralize labels that name the concept you are testing. If the persona goes where the input has no screen, the step is `unknown`.

**Do not hint at the answer with the mission.** Do not use words from button names, stage names or the expected result; do not single out the word you are testing. The mission is the person's task in their words. If a hint slipped in, report it and lower the weight of unanimity.

Stage B answer — JSON only:

```json
{
  "persona": "p3",
  "first_impression": "what was understood in 5 seconds",
  "mental_model": "how they would name the service and what they expect",
  "path": [{"step": "s1", "did": "", "expected": "", "got": "", "sentiment": 0, "stuck": false}],
  "outcome": "done | partial | abandoned | blocked",
  "exit_step": "s4 | null",
  "friction": [{"step": "", "what": "", "severity": "high|med|low"}],
  "quotes": ["2–4 lines in the persona's voice"],
  "top_fixes": [{"fix": "", "why": ""}]
}
```

Run subagents in parallel on a cheaper model. Merge answers yourself: where 2 or more personas got stuck is a strong signal; where one did is a hypothesis.

## Browser mode (prototype or live site)

One run — one persona. Steps:

1. Open the entry URL, take a screenshot of the first screen, record the 5-second impression before scrolling.
2. Move the way the persona would: read the page text, tap what it would consider relevant.
3. Every 3 actions append notes (URL, expectation, result) to `edge/runs/<persona>/journal.json`.
4. Budget: 15–30 actions. The persona may leave early; leaving is data.

Limits: forms may be opened and read but not submitted unless it is a test environment and the user explicitly allowed it. Never pay, create accounts on third-party services or type passwords. Never use real personal data.

## Cast summary

| Persona | Outcome | Exit step | Main friction | Quote |
|---|---|---|---|---|

After the table: shared friction (2+ personas), differences between personas, what to check with real people.
