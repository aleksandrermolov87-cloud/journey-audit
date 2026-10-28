# Changelog

## 1.1.0 — 2026-10-28

- Codex plugin: `.codex-plugin/plugin.json` with a store card, repo marketplace `.agents/plugins/marketplace.json`, `agents/openai.yaml` for every skill, icon and logo.
- Codex custom agents: `codex/agents/*.toml` for the three auditors and the verdict agent.
- Claude Code plugin and marketplace pass `claude plugin validate --strict`.
- Script and briefs are found through symlinked and cached plugin installs (`find -L`).

## 1.0.0 — 2026-10-28

- Orchestrator skill `journey-audit` with four agent briefs and a shared findings contract.
- Family skills: `journey-cjm` (CJM logic), `journey-edge` (edge-case scenarios), `journey-load` (simulated cognitive load), `journey-verdict` (priorities, goals, specs).
- Helper script `journey_check.py`: check, load, vision, curve, findings, merge, render; English and Russian output.
- Plugin manifest and marketplace entry with four agent types.
- English and Russian instructions, visual guide, worked example `examples/card-reissue`.
