# Pointwise Merge Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update the final-draft merge workflow so it merges one internal writing unit at a time while still outputting a continuous chapter.

**Architecture:** Keep the user-facing output unchanged as continuous prose, but change the documented merge process from a chapter-wide fusion to a writing-unit-by-writing-unit fusion. The unit-level merge keeps the existing style-priority rules and applies them to the current unit before moving on to the next one.

**Tech Stack:** Markdown skill prompts, README documentation, Python `unittest` static text checks

---

### Task 1: Lock unit-by-unit merge behavior with failing tests

**Files:**
- Modify: `tests/test_novel_write_workflow.py`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

```python
def test_novel_write_merges_final_draft_unit_by_unit(self) -> None:
    content = NOVEL_WRITE.read_text(encoding="utf-8")

    self.assertIn("按内部写作单元顺序逐个合并", content)
    self.assertIn("每次只处理当前写作单元在 4 个风格版本中的对应内容", content)
    self.assertIn("最终稿输出为连续章节正文", content)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: FAIL because the merge section still describes chapter-level auto-merge wording.

**Step 3: Write minimal implementation**

Add only the assertions needed to describe the approved merge behavior, plus the matching README expectation.

**Step 4: Run test to verify it passes later**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: PASS after the skill prompt and README are updated.

**Step 5: Commit**

```bash
git add tests/test_novel_write_workflow.py
git commit -m "test: cover unit-by-unit merge workflow"
```

### Task 2: Update `novel-write` merge instructions

**Files:**
- Modify: `plugins/vibe-noveling/skills/novel-write/SKILL.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

Reuse the Task 1 failure instead of adding a second overlapping test.

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: FAIL on missing unit-by-unit merge wording.

**Step 3: Write minimal implementation**

Update the merge section so it explicitly states that:

- merge proceeds in internal writing-unit order,
- only the current unit's four style fragments are merged in each pass,
- the style-priority rules are applied at the unit level,
- the final output remains continuous prose without exposed unit markers.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: PASS for the new `novel-write` assertions.

**Step 5: Commit**

```bash
git add plugins/vibe-noveling/skills/novel-write/SKILL.md tests/test_novel_write_workflow.py
git commit -m "feat: merge novel drafts unit by unit"
```

### Task 3: Sync README wording with the new merge model

**Files:**
- Modify: `README.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

Reuse the README assertions in the same test file so the public docs must mention unit-by-unit merge.

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: FAIL because README still only says auto-merge at the chapter level.

**Step 3: Write minimal implementation**

Update the public workflow summary so `/novel-write` is described as:

- sequentially starting style-writing agents,
- then merging the chapter unit by unit,
- while still producing a final continuous chapter.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_novel_write_workflow.py`
Expected: PASS.

**Step 5: Commit**

```bash
git add README.md tests/test_novel_write_workflow.py
git commit -m "docs: describe unit-by-unit merge workflow"
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
Expected: all workflow assertions pass.

**Step 5: Commit**

```bash
git add docs/plans/2026-04-08-pointwise-merge-design.md docs/plans/2026-04-08-pointwise-merge.md README.md plugins/vibe-noveling/skills/novel-write/SKILL.md tests/test_novel_write_workflow.py
git commit -m "docs: define unit-by-unit merge workflow"
```
