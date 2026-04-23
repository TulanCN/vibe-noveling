# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Run the full prompt-contract regression suite: `python3 -m unittest tests/test_novel_write_workflow.py -v`
- Run a single regression test: `python3 -m unittest tests.test_novel_write_workflow.NovelWriteWorkflowTests.<test_name> -v`
- Search workflow contract text across shipped prompts: `rg -n "<pattern>" README.md plugins/vibe-noveling/skills plugins/vibe-noveling/agents tests/test_novel_write_workflow.py`

## Architecture

This repository is a Claude Code plugin, not a traditional application. The main product surface is prompt contracts.

- Root `.claude-plugin/marketplace.json` is the marketplace manifest.
- `plugins/vibe-noveling/` is the publishable plugin root.
- `plugins/vibe-noveling/.claude-plugin/plugin.json` holds plugin metadata.
- `plugins/vibe-noveling/skills/` contains the shipped workflow contracts, supporting references, and small Python tools.
  - `booming`, `fuck-it`, `novel-bookplan`, `novel-discuss`, `novel-init`, `novel-knowledge`, `novel-name`, `novel-plan`, `novel-progress`, `novel-snapshot`, `novel-sync`, `novel-write`
- `plugins/vibe-noveling/agents/` contains the built-in subagent prompts used by the writing workflow.
  - `consistency-guard` (一致性校验), `context-collector` (上下文收集), `writer-dazhongma` (大仲马风), `writer-zhouzi` (会说话的肘子风)
- `README.md` is the public product and contributor guide; keep it aligned with shipped behavior.
- `tests/test_novel_write_workflow.py` is the prompt-contract regression suite. Most assertions validate wording, file layout, and workflow guarantees rather than runtime business logic.
- `docs/plans/` stores workflow design history and implementation notes. Search here before changing a workflow that may already have a recorded rationale.

## Working Rules

- Treat prompt wording changes like code changes. In this repo, docs, prompt files, references, and tests are different projections of the same product behavior.
- Prefer edits under `plugins/vibe-noveling/` when changing shipped behavior.
- Update `README.md` whenever user-facing workflow, installation, capabilities, or file layout changes.
- Update `tests/test_novel_write_workflow.py` whenever a behavior change affects prompt-contract text, output structure, agent names, or directory conventions.
- Add or update `docs/plans/*.md` for material workflow or design changes so future sessions can recover the rationale.
- Do not assume `.claude/` and `plugins/vibe-noveling/` are permanent mirrors. Confirm whether the task targets the local development copy, the shipped plugin, or both before editing.

## High-Value Files

- `README.md`: external behavior, installation, workflow narrative, and validation commands.
- `AGENT.md`: repository-specific collaboration guidance for AI coding agents and human contributors.
- `plugins/vibe-noveling/skills/<skill>/SKILL.md`: primary contract for each skill.
- `plugins/vibe-noveling/skills/<skill>/references/`: supporting contract text that often needs to stay aligned with the main skill prompt.
- `plugins/vibe-noveling/agents/*.md`: built-in agent prompts that must stay aligned with calling skills.
- `tests/test_novel_write_workflow.py`: contract lockfile in test form.

## Gotchas

- Many changes require coordinated edits across `plugins/vibe-noveling/...`, `README.md`, `tests/test_novel_write_workflow.py`, and sometimes `docs/plans/`.
- A change that looks like "just docs" may still be a product behavior change if it alters prompt wording or documented workflow guarantees.
- The repository contains local/generated artifacts that should usually be left alone unless the task explicitly targets them.

## Avoid Touching Unless Required

- `.omc/`
- `plugins/.snapshots/`
- `plugins/vibe-noveling/skills/novel-knowledge/.venv/`
- `**/__pycache__/`

## Before Finishing

- Check that edited prompt contracts do not conflict with `README.md` or the regression tests.
- Run `python3 -m unittest tests/test_novel_write_workflow.py -v` after behavior-changing edits.
- If metadata or release-facing descriptions changed, verify whether `plugins/vibe-noveling/.claude-plugin/plugin.json`, root marketplace metadata, and `README.md` all still agree.
