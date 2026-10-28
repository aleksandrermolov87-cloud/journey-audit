# Persona sensitivity

The same journey can be moderate for a confident user and an overload for an unsure one. A finding "the journey breaks only for some people" is more useful than an average index.

## Three runs

| Profile | `--persona-tech` | `--persona-patience` | Represents |
|---|---|---|---|
| Confident | high | high | Uses similar services, not in a hurry |
| Average | mid | mid | Baseline |
| Vulnerable | low | low | Low digital literacy, hurry or stress, small screen |

If `frame.md` describes a specific persona, add a fourth run with its values.

## What to compare

- **Switch steps**: the level changes between profiles (moderate → overload). The interface relies on skill there. Each such step is a `C-<step>` finding naming the profile it breaks for.
- **Shared peaks**: high load in every profile. Usually intrinsic load of the job or a value failure, not the interface.
- **Exit points only in the vulnerable profile**: candidates for testing with people of that profile.
- **KLM difference** between profiles: steps with typing grow most. On a phone this argues for choice instead of input.

## Modifiers the script does not model

Mention them in the finding text, not in the index:

- Screen reader: every context switch and live update costs more; reading order matters more than visual hierarchy.
- Large font: a long answer becomes multi-screen scrolling; `memory_items` grows (what was above).
- One hand, walking, noise: `P` is more expensive, small targets are worse.
- Anxiety about health or money: `uncertainty` one level higher than for a calm person in the same situation.
