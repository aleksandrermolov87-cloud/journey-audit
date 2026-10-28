# Heuristics per step

The index says where it is hard; a heuristic explains why and suggests what to change. Walk heuristics only for steps with index ≥ 50 and for exit points, otherwise the report drowns.

## Nielsen (H1–H10), linked to load features

| Code | Heuristic | Usually visible in | Question to the step |
|---|---|---|---|
| H1 | Visibility of system status | `wait_s`, `uncertainty` | Does the user know what is happening and how long to wait? |
| H2 | Match with the real world | `new_terms` | Are the words the user's, not the product's? |
| H3 | User control and freedom | `uncertainty` | Is there an exit and undo without losing work? |
| H4 | Consistency and standards | `new_terms`, `decisions` | One word, one meaning; one button, one action across the journey? |
| H5 | Error prevention | `fields`, `decisions` | Input constraints, defaults, warnings before the error? |
| H6 | Recognition rather than recall | `memory_items` | Is what is needed from earlier steps shown, not carried in the head? |
| H7 | Flexibility and efficiency | `decisions`, KLM | Is there a shortcut for a returning user? |
| H8 | Aesthetic and minimalist design | `decisions`, `max_options` | Is every element needed on this step? One primary button? |
| H9 | Recognize, diagnose, recover from errors | `uncertainty` | Does the error say what happened, why and what to do? |
| H10 | Help and documentation | `new_terms` | Is help where the term is, not in a separate section? |

## Krug

| Code | Principle | Question |
|---|---|---|
| K1 | Don't make me think | Is there any question mark in the head on this step: "is this a button?", "what does this word mean?" |
| K2 | Clicks don't matter, confidence does | Is every tap obvious and confirming the user is on the right track? Three obvious taps beat one hesitation |
| K3 | Omit half the words | Greetings, instructions nobody reads, polite noise |
| K4 | Trunk test | Landing on this step by a link: is it clear which service this is, where I am, what I can do, where the main action is? |

## Quick checks

- **Squint**: what is seen first? Is it what needs to be done?
- **Three seconds**: would a newcomer know what to do?
- **Subtraction**: remove an element — did anything important break? If not, it is extra.
- **Phone call**: can the screen be described over the phone without confusion?
- **Memory**: does the user carry anything in the head to the next step?

## Copy

Short sentences, active voice, the user's words, the key point first, no negatives where a direct statement works. Answer length on a phone: if the key point does not fit the first screen, that is `memory_items` + `context_switches` (scrolling back and forth).

## Writing a finding

`LOAD-07 · C-s7 · high` — "Address entry on a phone: 40 characters typed, 2 fields, 1 context switch; index 54 (low/low), H5, H6, K2". `fix_hint`: "offer the registered address by default; typing only for a new address".
