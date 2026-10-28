# Secondary and edge-case scenarios

Goal: find the paths the main map skips and decide which of them need their own description.

## Axes E01–E14

Walk every stage of the journey. Skip an axis that does not apply and note why.

| ID | Axis | Questions |
|---|---|---|
| E01 | Entry | Arrived not from the home screen: a link in an email, search, a bookmark to an inner step, a QR code, another product. Arrived without the context the map assumes |
| E02 | Interruption and return | Closed the tab mid-process, phone died, came back in an hour, in a week, from another device. What is saved, what is lost, does the user know where they stopped |
| E03 | Repeat and expert user | Same journey for the second time. Are consent, onboarding and hints needed again. Is there a shortcut |
| E04 | User data | Empty, too long, wrong, someone else's, a low-quality document, partly filled, wrong format, wrong language, outdated |
| E05 | Order and repetition | Double tap, resubmission, steps in another order, browser back, page reload, two tabs at once |
| E06 | Rights and roles | Another role (relative, accountant, admin), no permission, expired access, shared account, a representative by power of attorney |
| E07 | External dependencies | The service is down, slow, answers partially or in an unexpected format. Money charged, confirmation missing |
| E08 | Time | Weekends, night, an expired document or code, rules changed between visits, time zones |
| E09 | Device and environment | Small screen, one hand, poor network, noise, someone else's device, battery saver, large font |
| E10 | Accessibility | Screen reader, keyboard only, colour blindness, reduced motor control, cognitive differences, limited language proficiency |
| E11 | Service boundaries | A question outside competence, a request the service must not fulfil, an emergency. Is there a route elsewhere |
| E12 | Value not delivered | No answer, no service, no data. Not a UI error but a value failure: what does the user get instead |
| E13 | Emotional state | Anxiety, hurry, distrust, fatigue from the previous step. The same screen reads differently in that state |
| E14 | Exit and consequences | Delete data, withdraw consent, dispute the result, forward the result to someone, print it |

## Scoring

For every scenario found:

- **Frequency** (1–3): 1 — rare, 2 — regular for part of the audience, 3 — for a large share of users.
- **Impact** (1–3): 1 — inconvenience, 2 — lost time or data, 3 — wrong decision, harm, legal risk, drop-off.
- **Coverage**: `described` / `partial` / `none`.
- **Priority** = frequency × impact, plus 2 when coverage is `none`.

Expand the top 5 by priority into alternative paths (3–8 steps, `branches` format of `journey-audit/references/journey-format.md`, file `edge/branches.json`). The rest go into a table.

A `partial` coverage is a finding only when the missing part changes what the user can do; otherwise mention it in the table.

## Adjacent journeys

Separately propose 3–5 journeys that deserve their own map, with one line of reasoning each:

- a failure serious enough to become its own journey (dispute, refund, cancellation, complaint);
- personas implied but not described (relative, support agent, specialist);
- what happened before the first step and what happens after the last;
- frequent edge cases the main path covers in one line.

Do not create these maps; propose a ranked list.

## Row format

| Scenario | Axis | Stage | Frequency | Impact | Coverage | Priority | What happens today | What should happen |
|---|---|---|---|---|---|---|---|---|
| Returns two days later from another phone | E02 | Result | 2 | 2 | none | 6 | unknown: the map has no saving | Sees the previous result or a clear "not saved, here is why" |
