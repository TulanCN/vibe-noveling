# Bookplan No Chapter Count Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Remove chapter-count and chapter-range coupling from `novel-bookplan` so full-book planning and `future/` maintenance operate on volumes, beats, responsibility bands, and state changes instead of chapter quantities.

**Architecture:** Update the `novel-bookplan` prompt contract and its STC hierarchy reference together so the skill consistently speaks in volume-level and structural terms. Lock the new contract with static text tests and sync the README wording so users see the same boundary in public docs.

**Tech Stack:** Markdown skill prompts, Markdown docs, Python `unittest` static text checks

---

### Task 1: Add failing tests for the no-chapter-count contract

**Files:**
- Modify: `tests/test_novel_write_workflow.py`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

```python
def test_novel_bookplan_avoids_chapter_count_coupling(self) -> None:
    content = NOVEL_BOOKPLAN.read_text(encoding="utf-8")
    hierarchy = BOOKPLAN_HIERARCHY.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    self.assertIn("全书规划阶段不预设章节数", content)
    self.assertNotIn("对应的大致章节范围", content)
    self.assertNotIn("| Beat | 对应卷 | 大致章节 | 关键事件 | 状态 |", content)
    self.assertNotIn("第 1 段（开卷 3-5 章）", content)
    self.assertNotIn("第 1 段（1-4 章）", hierarchy)
    self.assertIn("不预设章节数", readme)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: FAIL because the current prompt still contains chapter-range wording and README does not mention the new contract.

**Step 3: Write minimal implementation**

Only add assertions that describe the approved contract boundary.

**Step 4: Run test to verify it passes later**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: PASS after the prompt, reference, and README updates land.

**Step 5: Commit**

```bash
git add tests/test_novel_write_workflow.py
git commit -m "test: cover chapterless book planning contract"
```

### Task 2: Update the `novel-bookplan` prompt contract

**Files:**
- Modify: `plugins/vibe-noveling/skills/novel-bookplan/SKILL.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

Reuse the Task 1 failure instead of adding overlapping assertions.

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: FAIL on chapter-range and chapter-count wording.

**Step 3: Write minimal implementation**

Update `novel-bookplan` so it explicitly states that:

- full-book planning does not preset chapter counts,
- beat blueprints use volume mapping rather than chapter ranges,
- volume planning uses responsibility bands instead of numeric chapter segments,
- `future/` maintenance manages long-range structure and events without chapter-count prerequisites.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: PASS for the `novel-bookplan` assertions after the reference and README are also synced.

**Step 5: Commit**

```bash
git add plugins/vibe-noveling/skills/novel-bookplan/SKILL.md tests/test_novel_write_workflow.py
git commit -m "feat: remove chapter count from book planning"
```

### Task 3: Sync the STC hierarchy reference and README wording

**Files:**
- Modify: `plugins/vibe-noveling/skills/novel-bookplan/references/stc-hierarchy.md`
- Modify: `README.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

Reuse the same workflow suite so the reference and README must reflect the chapterless contract too.

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: FAIL until the reference removes numeric chapter-band examples and README advertises the new boundary.

**Step 3: Write minimal implementation**

Update the hierarchy examples to use volume-position or responsibility-band language, and update the README description of `/novel-bookplan` so it says planning is done by volume and beats without preset chapter counts.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add README.md plugins/vibe-noveling/skills/novel-bookplan/references/stc-hierarchy.md tests/test_novel_write_workflow.py
git commit -m "docs: describe chapterless book planning"
```

### Task 4: Run final verification

**Files:**
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

No new test. Reuse the updated workflow suite as the final verification target.

**Step 2: Run test to verify it fails**

Skip. Earlier tasks already provide the red phase.

**Step 3: Write minimal implementation**

No implementation changes.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: all workflow assertions pass, including the new `novel-bookplan` contract checks.

**Step 5: Commit**

```bash
git add docs/plans/2026-04-08-bookplan-no-chapter-count-design.md docs/plans/2026-04-08-bookplan-no-chapter-count.md README.md plugins/vibe-noveling/skills/novel-bookplan/SKILL.md plugins/vibe-noveling/skills/novel-bookplan/references/stc-hierarchy.md tests/test_novel_write_workflow.py
git commit -m "docs: remove chapter count from book planning contract"
```
