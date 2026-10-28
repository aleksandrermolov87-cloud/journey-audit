# Flow checklists

Give each step a type and walk its checklist. Every item is a "what happens if…" question. An answer in the input → coverage `described` / `partial`; no answer → `none` and a finding. Skip items that do not apply silently.

Before design (preflight) the same questions reveal decisions to make before screens exist. If the journey is still an idea, answer "not decided" and turn the item into a question for the owner.

## Entry and first screen

- Arrived by a deep link, bypassing the home screen: is it clear where they are and what happens here?
- Is a role or mode choice needed before starting, and what if the wrong one is picked?
- Is it clear within 5 seconds what the service will and will not do?
- What does a returning user see: the start or the place they stopped?
- Is there a single primary action on the screen?

## Text and form input

- Empty, whitespace only, too long, pasted with junk.
- Is the error shown at the field with a reason and a fix, or in a banner at the top?
- Is the draft kept on error, leaving, reload?
- Are limits visible before the user exceeds them?
- Are all fields needed, or can some be prefilled or asked later?

## File upload and camera

- Wrong format, too big, several pages, bad shot, rotated, someone else's document.
- Camera capture on a phone, not only file picking.
- Re-upload over the first file, delete, replace.
- Consent to processing: when, with what text, on whose behalf, what if declined.
- Partly recognized: what does the user see and how do they correct it?

## Waiting for the system

- Is the duration known and shown? What if it takes three times longer than usual?
- Can the user leave and come back to the result, get a notification?
- Cancel: what exactly is cancelled, what is kept?
- Double tap and resubmission while waiting.
- Network lost during the wait and after it.

## AI or reference answer

- No answer: what does the user see and where should they go?
- A question outside the boundaries: a refusal with a route (to whom, where, what to do) or a bare "I can't"?
- Urgent or dangerous situation: is there a separate path that does not depend on how the question is phrased?
- Partial, outdated, low-confidence answer: can the user see that?
- A safety filter hid the text: what stays on screen and what should the user do?
- The user does not know what to ask: are there example questions?
- The answer mode switched (for example, a check was skipped): is the user told?

## Confirmation and decision

- Confirms without reading, by ear, on behalf of someone else.
- A mistake in confirmation: how is it corrected afterwards?
- Confirming an irreversible action: is there a pause, an undo, a clear consequence?

## Payments and money

- Money charged, no confirmation. Double charge. Refund.
- Price changed between steps. Discount not applied.
- Payment provider down or slow.

## Empty and zero states

- First launch without data: what to do first?
- Search or filter without results: what to offer?
- Everything deleted: how to restore, how to start over?

## Deletion, exit, consequences

- Delete data, withdraw consent, sign out: what happens to results?
- Undo deletion: how long, what is restored?
- Forward the result to a specialist, accountant, relative: in what form?
- Dispute the result or complain: where?

## Roles and representatives

- A relative, guardian or employee acts on someone's behalf: who is "you" in the copy, who gives consent, whose data is it?
- Shared account or device: can one person see another's data?
