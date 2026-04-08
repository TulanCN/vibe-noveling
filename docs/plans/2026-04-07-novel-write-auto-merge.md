# Novel Write Auto Merge Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update the `novel-write` workflow so it always generates all style drafts, auto-merges them into the final chapter, keeps intermediate drafts, and preserves plot-point segmentation in the merged output.

**Architecture:** This change is prompt-and-doc driven. The main behavior lives in `plugins/vibe-noveling/skills/novel-write/SKILL.md`, with `README.md` documenting the user-facing workflow. A lightweight unittest suite will guard against regressions in the documented workflow and merging rules.

**Tech Stack:** Markdown prompt specs, Python `unittest`, ripgrep-based verification

---

### Task 1: Add failing workflow tests

**Files:**
- Create: `tests/test_novel_write_workflow.py`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

```python
def test_novel_write_defaults_to_all_styles(self):
    self.assertIn("默认并行创作全部 4 种写作风格", content)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: FAIL because the old workflow still describes user-selected styles and manual merge.

**Step 3: Write minimal implementation**

Update the skill and README text until the new workflow language appears and the old workflow language is removed.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_novel_write_workflow.py plugins/vibe-noveling/skills/novel-write/SKILL.md README.md
git commit -m "feat: automate novel-write style merging"
```

### Task 2: Rewrite `novel-write` workflow

**Files:**
- Modify: `plugins/vibe-noveling/skills/novel-write/SKILL.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

```python
def test_merged_chapter_preserves_plot_point_sections(self):
    self.assertIn("最终合并稿也必须保留剧情点切分", content)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: FAIL because merged-output segmentation is not yet specified.

**Step 3: Write minimal implementation**

Edit these sections in `plugins/vibe-noveling/skills/novel-write/SKILL.md`:

- Frontmatter description
- Goal and core philosophy
- Full workflow diagram
- Step 3 through Step 7
- Delivery, output format, naming, and completion sections

Add explicit merge rules:

- Base draft: 卖报小郎君
- Scenery donor: 海明威
- Battle donor: 大仲马
- Avoid excessive metaphor
- Replace third-person summary passages with direct scene writing and dialogue from other drafts
- Keep `【剧情点N：名称】` in the merged chapter

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: PASS

**Step 5: Commit**

```bash
git add plugins/vibe-noveling/skills/novel-write/SKILL.md tests/test_novel_write_workflow.py
git commit -m "refactor: update novel-write auto-merge workflow"
```

### Task 3: Update public docs

**Files:**
- Modify: `README.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

```python
def test_readme_describes_auto_merge_workflow(self):
    self.assertIn("自动合并生成最终稿", readme)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: FAIL because README still describes manual merge.

**Step 3: Write minimal implementation**

Update README feature bullets and the main workflow sequence to match the new auto-merge behavior while clarifying that intermediate drafts are still preserved.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: PASS

**Step 5: Commit**

```bash
git add README.md tests/test_novel_write_workflow.py
git commit -m "docs: describe novel-write automatic merge flow"
```

### Task 4: Verify the final state

**Files:**
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Run focused tests**

Run: `python3 -m unittest tests.test_novel_write_workflow -v`
Expected: PASS

**Step 2: Run targeted grep checks**

Run: `rg -n "用户选择 2-3 种写作风格|用户手动合并|默认并行创作全部 4 种写作风格|自动合并生成最终稿|最终合并稿也必须保留剧情点切分" README.md plugins/vibe-noveling/skills/novel-write/SKILL.md`
Expected: Only the new workflow phrases remain in active instructions.

**Step 3: Review diff**

Run: `git diff -- README.md plugins/vibe-noveling/skills/novel-write/SKILL.md tests/test_novel_write_workflow.py docs/plans/2026-04-07-novel-write-auto-merge*.md`
Expected: Only workflow docs, tests, and plan docs changed.

**Step 4: Commit**

```bash
git add README.md plugins/vibe-noveling/skills/novel-write/SKILL.md tests/test_novel_write_workflow.py docs/plans/2026-04-07-novel-write-auto-merge*.md
git commit -m "feat: automate novel-write draft merging"
```
