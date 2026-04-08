# Postwrite Style Correction Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a postwrite style-correction pass that removes four specific AI-ish patterns and wire it into final-chapter review only.

**Architecture:** Keep the reusable correction rules in `novel-master`, because they belong to the shared lightweight text-QA layer. Then update `novel-write` so the correction is explicitly enforced during the final merged-draft review, preserving stylistic variation in intermediate drafts.

**Tech Stack:** Markdown skill prompts, Python `unittest` static text checks

---

### Task 1: Lock the new behavior with failing tests

**Files:**
- Modify: `tests/test_novel_write_workflow.py`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

```python
def test_novel_master_adds_postwrite_style_correction_rules(self) -> None:
    content = NOVEL_MASTER.read_text(encoding="utf-8")

    self.assertIn("正文后文风矫正", content)
    self.assertIn("删除用数字硬撑专业感", content)
    self.assertIn("删掉“不是……，而是……”这类先否定再肯定的句式", content)
    self.assertIn("删除不承担推进的平淡比喻", content)
    self.assertIn("少用嘴角、手指等细节偷渡内心", content)
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_novel_write_workflow -v`
Expected: FAIL because the new postwrite correction strings do not exist yet.

**Step 3: Write minimal implementation**

Add the smallest set of new assertions needed to describe the approved behavior, including the final-review integration in `novel-write`.

**Step 4: Run test to verify it passes later**

Run: `python -m unittest tests.test_novel_write_workflow -v`
Expected: PASS after skill docs are updated.

**Step 5: Commit**

```bash
git add tests/test_novel_write_workflow.py
git commit -m "test: cover postwrite style correction rules"
```

### Task 2: Add reusable postwrite correction rules to `novel-master`

**Files:**
- Modify: `plugins/vibe-noveling/skills/novel-master/SKILL.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

The Task 1 test already fails on missing `novel-master` rule text, so reuse that failure instead of creating a second overlapping test.

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_novel_write_workflow -v`
Expected: FAIL on missing postwrite correction wording.

**Step 3: Write minimal implementation**

Add a dedicated subsection to `novel-master` that:

- names the postwrite correction pass,
- defines the four rules,
- explains when to delete versus keep details,
- removes examples that conflict with the new directness preference.

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_novel_write_workflow -v`
Expected: `novel-master` assertions pass once the text exists.

**Step 5: Commit**

```bash
git add plugins/vibe-noveling/skills/novel-master/SKILL.md tests/test_novel_write_workflow.py
git commit -m "feat: add postwrite style correction rules"
```

### Task 3: Wire final-review enforcement into `novel-write`

**Files:**
- Modify: `plugins/vibe-noveling/skills/novel-write/SKILL.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

Reuse the same test file to assert that `novel-write` explicitly runs the targeted correction during final review only.

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_novel_write_workflow -v`
Expected: FAIL because `novel-write` does not yet mention the dedicated final-review correction pass.

**Step 3: Write minimal implementation**

Update the final review section so it explicitly:

- invokes the targeted correction pass,
- lists the same four focus points,
- states that intermediate style drafts should not be flattened too early.

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_novel_write_workflow -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add plugins/vibe-noveling/skills/novel-write/SKILL.md tests/test_novel_write_workflow.py
git commit -m "feat: enforce postwrite style correction in final review"
```

### Task 4: Run final verification

**Files:**
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

No new test. Use the existing full workflow test suite as the verification target.

**Step 2: Run test to verify it fails**

Skip. Earlier tasks already provide the red phase.

**Step 3: Write minimal implementation**

No implementation changes.

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_novel_write_workflow -v`
Expected: all workflow assertions pass.

**Step 5: Commit**

```bash
git add docs/plans/2026-04-07-postwrite-style-correction-design.md docs/plans/2026-04-07-postwrite-style-correction.md tests/test_novel_write_workflow.py plugins/vibe-noveling/skills/novel-master/SKILL.md plugins/vibe-noveling/skills/novel-write/SKILL.md
git commit -m "docs: document postwrite style correction workflow"
```
