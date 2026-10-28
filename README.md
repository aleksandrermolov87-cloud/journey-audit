# journey-audit — customer journey map (CJM) audit skills for AI agents

**Find what an AI-generated customer journey gets wrong — logic gaps, missed edge cases, hidden cognitive load — and get prioritized fixes with specs.**

[![test](https://github.com/aleksandrermolov87-cloud/journey-audit/actions/workflows/test.yml/badge.svg)](https://github.com/aleksandrermolov87-cloud/journey-audit/actions/workflows/test.yml)
![license](https://img.shields.io/badge/license-MIT-blue)
![skills](https://img.shields.io/badge/agent%20skills-5-5b4bd6)
![agents](https://img.shields.io/badge/subagents-4-1f9d55)
![languages](https://img.shields.io/badge/lang-EN%20%7C%20RU-orange)

> Русская версия: [README.ru.md](README.ru.md)

AI drafts journeys that look finished: every step succeeds, the user understands everything on the first try, external systems always answer. A person who knows the product sees three kinds of gaps. `journey-audit` checks each of them with its own auditor agent, in parallel, and a verdict agent turns the findings into **priorities, measurable goals and implementation-ready specs**.

![Architecture](docs/assets/architecture.svg)

## Contents

- [What you get](#what-you-get)
- [Install](#install)
- [Use](#use)
- [Skills and agents](#skills-and-agents)
- [Example](#example)
- [How it stays honest](#how-it-stays-honest)
- [Docs](#docs)
- [FAQ](#faq)

## What you get

| Auditor | Looks for | Methods |
|---|---|---|
| **CJM logic** | Steps that contradict the brief, failures without a way out, emotions without causes, a map that drifts from the live product, owner-vision coverage | 20 structural checks, emotion curve, service-blueprint layers, mature-map review |
| **Edge cases** | Interruption and return, wrong data, other roles, external failures, service boundaries, value not delivered, accessibility | 14 edge-case axes, flow checklists, synthetic personas (two-stage, unprimed), alternative and adjacent journeys |
| **Cognitive load** | Steps that demand more decisions, memory and attention than the job needs; likely exit points | Load index with open weights, Keystroke-Level Model, fatigue, 3 persona profiles, Nielsen and Krug heuristics |
| **Verdict** | What to fix first and what "fixed" means | Merge and conflict rules, P0–P2, goals with metrics, specs with Given/When/Then, TO BE journey, usability test plan |

Outputs, all in one work folder:

- `verdict/verdict.md` — Ready / Ready with conditions / Rework / Redesign, with P0–P2 goals;
- `verdict/specs/G-NN.md` — one spec per P0/P1 goal: problem, metric, TO BE fragment, states, UI copy, acceptance criteria, analytics events, test cases;
- `verdict/backlog.json` — the same for trackers and scripts;
- family reports with the emotion curve, load tables, branches and persona results.

## Install

**As a plugin** (skills + the four agent types, recommended):

```text
/plugin marketplace add aleksandrermolov87-cloud/journey-audit
/plugin install journey-audit@journey-audit
```

**Skills only**, with the open skills CLI:

```bash
npx skills add aleksandrermolov87-cloud/journey-audit
```

**Manually** — clone and copy the five skill folders into your agent's skills directory:

```bash
git clone https://github.com/aleksandrermolov87-cloud/journey-audit.git
cp -r journey-audit/skills/* ~/.claude/skills/
```

The skills follow the open Agent Skills format (`SKILL.md` with YAML frontmatter), so any agent that loads skills from a folder can use them. Agents without skill support can follow [AGENTS.md](AGENTS.md). Requirements: Python 3.8+ for the helper script, nothing else.

## Use

Ask in plain words, in English or Russian:

```text
Audit the customer journey in docs/onboarding-cjm.md.
My vision: setup takes one sitting; we never ask for data we already have.
```

```text
What edge cases did we miss in this checkout flow? Run 4 personas through the prototype at https://staging.example.com
```

```text
Проверь CJM в docs/onboarding-cjm.md: логика, краевые сценарии, нагрузка. Дай приоритеты и спеки.
```

Modes: full audit (default), quick (no personas, no expanded branches), one family only, or verdict only when findings already exist.

## Skills and agents

| Skill | Role | Call it directly when you want |
|---|---|---|
| [`journey-audit`](skills/journey-audit/SKILL.md) | Orchestrator: frame, normalize, launch, assemble | A full audit |
| [`journey-cjm`](skills/journey-cjm/SKILL.md) | CJM logic family | Only the logic of the map |
| [`journey-edge`](skills/journey-edge/SKILL.md) | Edge-case scenarios family | Only missed scenarios, personas |
| [`journey-load`](skills/journey-load/SKILL.md) | Cognitive load family | Only load, AS IS vs TO BE |
| [`journey-verdict`](skills/journey-verdict/SKILL.md) | Verdict, priorities, specs | Priorities and specs from existing findings |

Agents (plugin install): `journey-cjm-auditor`, `journey-edge-auditor`, `journey-load-auditor`, `journey-verdict`. Their briefs live in [`skills/journey-audit/agents/`](skills/journey-audit/agents).

Every skill ships in English (`SKILL.md`, `references/`) and Russian (`SKILL.ru.md`, `references/ru/`). The agent answers in the user's language.

## Example

[`examples/card-reissue`](examples/card-reissue) — an AI-drafted journey "reissue a lost debit card" in a mobile bank, audited end to end: input map, normalized JSON, three family reports, verdict, specs.

Result: **Rework** — 37 findings merged into 3 P0 and 5 P1 goals. The headline: the job says "keep paying today", and no step of the AI-drafted journey lets the user pay for the 5–7 days until the new card arrives. Read the [one-page summary](examples/card-reissue/audit/journey-audit-card-reissue.md) or the [verdict](examples/card-reissue/audit/verdict/verdict.md).

```bash
python3 skills/journey-audit/scripts/journey_check.py check examples/card-reissue/journey.json
python3 skills/journey-audit/scripts/journey_check.py load  examples/card-reissue/journey.json --persona-tech low --persona-patience low
```

![Emotion and load curve](docs/assets/example-curve.svg)

## How it stays honest

- **Evidence classes never mix.** Every finding is `provided`, `absent`, `interpretation`, `synthetic`, `hypothesis` or `unknown`. Synthetic personas and the load model produce hypotheses, not facts.
- **No invented screens.** What the input does not show stays `unknown`.
- **Independent auditors.** They never read each other's findings before the verdict.
- **Useful friction stays.** Confirmations of irreversible actions, consent and legal or safety steps are made faster, never removed.
- **Value failures are named.** If the service does not do the job, the verdict sets a business goal, not a UI tweak.
- **Owner decisions stay with the owner.** Service boundaries, legal, medical and financial frames are listed as options.

## Docs

- [Visual guide](docs/GUIDE.md) · [Визуальная инструкция](docs/GUIDE.ru.md)
- [journey.json format](skills/journey-audit/references/journey-format.md)
- [Findings contract](skills/journey-audit/references/findings-contract.md)
- [Research behind the methods](skills/journey-audit/references/methods.md)

## FAQ

**Does it replace user research?** No. It tells you what to test and with whom; every P0 resting on a hypothesis comes with a validation task.

**Can it audit a journey written by a human?** Yes. The checks are the same; AI-generated journeys simply fail them more often.

**What inputs work?** A CJM table, a document, a user flow, screenshots, a prototype URL, front-end code — or any combination.

**Does the browser mode submit forms?** No. It reads pages and stops before any submit, payment or sign-up.

**Can I tune the load model?** Yes. Weights are documented in [`cognitive-load.md`](skills/journey-load/references/cognitive-load.md) and live in one function of the script.

## Contributing

Issues and pull requests are welcome: new edge-case axes, flow checklists for other domains, translations, script improvements. Run `python3 -m unittest discover -s tests` before sending a change.

## License

[MIT](LICENSE)

---

**Keywords:** customer journey map audit · CJM review · user journey validation · user flow audit · UX audit · heuristic evaluation · edge cases and unhappy paths · cognitive load · Keystroke-Level Model · service blueprint · synthetic users · persona testing · usability test plan · acceptance criteria · product specs · AI-generated UX review · agent skills · subagents
