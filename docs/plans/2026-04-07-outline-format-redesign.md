# Outline Format Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Redesign chapter planning so `novel-plan` produces a concise third-person outline for humans, while `novel-write` performs any plot-point slicing internally during drafting.

**Architecture:** This is a prompt-contract change across the planning and writing skills. `novel-plan` and its output reference define the new human-facing outline format, `novel-write` consumes that concise outline and derives internal writing units, and `README.md` documents the updated public workflow. A lightweight unittest file guards against prompt drift.

**Tech Stack:** Markdown prompt specs, Python `unittest`, ripgrep verification

---

### Task 1: Add failing prompt-contract tests

**Files:**
- Modify: `tests/test_novel_write_workflow.py`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

```python
def test_novel_plan_uses_concise_third_person_outline(self):
    self.assertIn("第三人称精简剧情纲要", content)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: FAIL because `novel-plan` still describes plot-point outlines and `novel-write` still assumes exposed plot-point sections.

**Step 3: Write minimal implementation**

Add assertions covering:

- `novel-plan` uses concise third-person outlines
- `novel-write` slices writing units internally
- final chapter output is continuous prose
- README no longer markets `novel-plan` as a scene-by-scene outline tool

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_novel_write_workflow.py
git commit -m "test: cover concise outline workflow"
```

### Task 2: Rewrite the `novel-plan` outline contract

**Files:**
- Modify: `plugins/vibe-noveling/skills/novel-plan/SKILL.md`
- Modify: `plugins/vibe-noveling/skills/novel-plan/references/output.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

```python
def test_novel_plan_uses_concise_third_person_outline(self):
    self.assertIn("第三人称精简剧情纲要", content)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: FAIL because `novel-plan` still instructs the model to produce 10-20 plot points and `> ✏️ 写作提示`.

**Step 3: Write minimal implementation**

Update these areas:

- frontmatter description and key-difference bullets
- planning flow summary
- “第三步” output section
- Opus test wording
- output reference format

Replace plot-point output with:

- concise chapter basics
- start and end state
- task card
- third-person concise story synopsis
- foreshadow handling

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: PASS for the `novel-plan` assertions

**Step 5: Commit**

```bash
git add plugins/vibe-noveling/skills/novel-plan/SKILL.md plugins/vibe-noveling/skills/novel-plan/references/output.md tests/test_novel_write_workflow.py
git commit -m "refactor: simplify chapter outline format"
```

### Task 3: Rewrite the `novel-write` input contract

**Files:**
- Modify: `plugins/vibe-noveling/skills/novel-write/SKILL.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

```python
def test_novel_write_derives_internal_units_and_outputs_continuous_chapter(self):
    self.assertIn("先在正文阶段内部切分写作单元", content)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: FAIL because `novel-write` still assumes exposed plot-point sections and title markers in final output.

**Step 3: Write minimal implementation**

Edit these sections:

- data-source description
- workflow diagram
- outline-reading instructions
- agent prompt templates
- output format and naming
- completion summary

Make `novel-write`:

- derive internal writing units from the concise outline
- keep those units internal to the drafting stage
- generate continuous chapter prose for style drafts and merged output
- stop requiring `【剧情点N：名称】` in final delivery

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: PASS for the `novel-write` assertions

**Step 5: Commit**

```bash
git add plugins/vibe-noveling/skills/novel-write/SKILL.md tests/test_novel_write_workflow.py
git commit -m "refactor: move plot slicing into novel-write"
```

### Task 4: Update public docs and verify

**Files:**
- Modify: `README.md`
- Modify: `docs/plans/2026-04-07-outline-format-redesign-design.md`
- Modify: `docs/plans/2026-04-07-outline-format-redesign.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

```python
def test_readme_describes_concise_outline_and_internal_splitting(self):
    self.assertIn("精简剧情纲要", content)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: FAIL because README still describes `novel-plan` as scene-style outlines.

**Step 3: Write minimal implementation**

Update README feature bullets, skill table, workflow, and project structure to match:

- concise chapter outline in `novel-plan`
- internal slicing in `novel-write`
- continuous chapter output

**Step 4: Run verification**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Run: `rg -n "场景化大纲|剧情点大纲|> ✏️ 写作提示|【剧情点N：名称】|第三人称精简剧情纲要|正文阶段内部切分" README.md plugins/vibe-noveling/skills/novel-plan/SKILL.md plugins/vibe-noveling/skills/novel-plan/references/output.md plugins/vibe-noveling/skills/novel-write/SKILL.md`
Expected: New phrases appear in the active workflow docs; old exposed plot-point requirements are removed from key user-facing paths.

**Step 5: Commit**

```bash
git add README.md docs/plans/2026-04-07-outline-format-redesign-design.md docs/plans/2026-04-07-outline-format-redesign.md tests/test_novel_write_workflow.py plugins/vibe-noveling/skills/novel-plan/SKILL.md plugins/vibe-noveling/skills/novel-plan/references/output.md plugins/vibe-noveling/skills/novel-write/SKILL.md
git commit -m "feat: redesign outline workflow around concise synopses"
```
