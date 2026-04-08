# Novel Plan 5W1H Alignment Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a required 5W1H alignment step to `novel-plan` so each small plot beat is clarified with the user before the concise chapter outline is generated.

**Architecture:** Keep the final chapter artifact as a concise third-person outline, but insert a dialog-only "small beat alignment card" between scenario design and outline generation. The skill prompt will require 3-8 small plot beats, complete `Who / What / Why / Where / When / How` coverage for each beat, explicit user confirmation before writing the outline, and partial re-alignment in revise mode.

**Tech Stack:** Markdown skill prompts, README documentation, Python `unittest` static text checks

---

### Task 1: Lock the new 5W1H contract with failing tests

**Files:**
- Modify: `tests/test_novel_write_workflow.py`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

```python
def test_novel_plan_requires_plot_point_5w1h_alignment(self) -> None:
    content = NOVEL_PLAN.read_text(encoding="utf-8")

    self.assertIn("拆成 3-8 个小剧情点", content)
    self.assertIn("Who / What / Why / Where / When / How", content)
    self.assertIn("小剧情点对齐卡", content)
    self.assertIn("先确认对齐卡，再生成正式大纲", content)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: FAIL because `novel-plan` does not yet require per-beat 5W1H alignment before outline generation.

**Step 3: Write minimal implementation**

Add only the assertions that capture the approved behavior, including the revise-mode partial re-alignment rule and the "do not write the alignment card into `大纲.md`" requirement.

**Step 4: Run test to verify it passes later**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: PASS after the skill prompt and README are updated.

**Step 5: Commit**

```bash
git add tests/test_novel_write_workflow.py
git commit -m "test: cover novel-plan 5w1h alignment flow"
```

### Task 2: Update `novel-plan` to require the alignment gate

**Files:**
- Modify: `plugins/vibe-noveling/skills/novel-plan/SKILL.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

Reuse the Task 1 failure rather than creating overlapping prompt tests.

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: FAIL on missing 5W1H alignment wording.

**Step 3: Write minimal implementation**

Update the skill prompt so that it explicitly requires:

- splitting the approved direction into 3-8 small plot beats,
- completing `Who / What / Why / Where / When / How` for each beat,
- presenting a `小剧情点对齐卡` to the user before any file write,
- blocking outline generation until the alignment card is confirmed,
- keeping the final `大纲.md` concise and free of the alignment card,
- redoing alignment only for affected beats in revise mode.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: PASS for the new `novel-plan` assertions.

**Step 5: Commit**

```bash
git add plugins/vibe-noveling/skills/novel-plan/SKILL.md tests/test_novel_write_workflow.py
git commit -m "feat: add 5w1h alignment to novel-plan"
```

### Task 3: Sync README with the new planning flow

**Files:**
- Modify: `README.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

Reuse the workflow test file to assert the public docs mention 5W1H clarification before the concise outline is finalized.

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: FAIL because README does not yet describe the alignment-card step.

**Step 3: Write minimal implementation**

Update README so `/novel-plan` is described as:

- clarifying each small plot beat with 5W1H before the outline,
- keeping `大纲.md` as a concise third-person outline,
- leaving writing-unit splitting to `novel-write`.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: PASS.

**Step 5: Commit**

```bash
git add README.md tests/test_novel_write_workflow.py
git commit -m "docs: describe novel-plan 5w1h alignment"
```

### Task 4: Run final verification

**Files:**
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

No new test. Use the updated workflow suite as the final verification target.

**Step 2: Run test to verify it fails**

Skip. Earlier tasks already provide the red phase.

**Step 3: Write minimal implementation**

No implementation changes.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: all workflow assertions pass, including the new `novel-plan` 5W1H contract checks.

**Step 5: Commit**

```bash
git add docs/plans/2026-04-08-novel-plan-5w1h-alignment-design.md docs/plans/2026-04-08-novel-plan-5w1h-alignment.md README.md plugins/vibe-noveling/skills/novel-plan/SKILL.md tests/test_novel_write_workflow.py
git commit -m "docs: define novel-plan 5w1h alignment flow"
```
