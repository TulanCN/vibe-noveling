# Chapter Directory Layout Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate the chapter artifact path contract from flat `chapters/ch-xxxx*.md` files to per-volume, per-chapter directories such as `chapters/vol-01/ch-0001/正文.md`, with no legacy-path compatibility.

**Architecture:** Treat the new chapter directory as the canonical storage root for every chapter artifact. Update every prompt contract that reads or writes chapter files so they consistently resolve through `chapters/vol-{volume}/ch-{chapter}/`, and lock that contract with static text tests plus README documentation.

**Tech Stack:** Markdown skill prompts, Markdown docs, Python `unittest` static text checks

---

### Task 1: Add failing tests for the new chapter-directory contract

**Files:**
- Modify: `tests/test_novel_write_workflow.py`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

```python
def test_chapter_artifacts_live_in_volume_chapter_directories(self) -> None:
    novel_plan = NOVEL_PLAN.read_text(encoding="utf-8")
    novel_write = NOVEL_WRITE.read_text(encoding="utf-8")
    novel_sync = NOVEL_SYNC.read_text(encoding="utf-8")
    context_collector = CONTEXT_COLLECTOR.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    self.assertIn("chapters/vol-{volume_padded}/ch-{chapter_padded}/大纲.md", novel_plan)
    self.assertIn("chapters/vol-{volume_padded}/ch-{chapter_padded}/正文.md", novel_write)
    self.assertIn("chapters/vol-{volume_padded}/ch-{chapter_padded}/正文.md", novel_sync)
    self.assertIn("chapters/vol-{volume_padded}/ch-{chapter_padded}/上下文.md", context_collector)
    self.assertIn("chapters/vol-01/ch-0001/正文.md", readme)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: FAIL because all prompts still reference flat `chapters/ch-xxxx*.md` paths.

**Step 3: Write minimal implementation**

Only add assertions that describe the approved directory contract and no compatibility behavior.

**Step 4: Run test to verify it passes later**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: PASS after all prompt files and README are updated.

**Step 5: Commit**

```bash
git add tests/test_novel_write_workflow.py
git commit -m "test: cover chapter directory layout contract"
```

### Task 2: Update `novel-plan` and `context-collector` path contracts

**Files:**
- Modify: `plugins/vibe-noveling/skills/novel-plan/SKILL.md`
- Modify: `plugins/vibe-noveling/agents/context-collector.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

Reuse the Task 1 failure instead of adding overlapping assertions.

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: FAIL on missing volume/chapter directory wording.

**Step 3: Write minimal implementation**

Update both prompt contracts so they:

- define the chapter root as `chapters/vol-{volume_padded}/ch-{chapter_padded}/`,
- read and write `大纲.md` / `上下文.md` / `Opus试写.md` / `Opus报告.md` / `缺失设定.md` under that root,
- explicitly refuse to fall back to old flat chapter files,
- require volume resolution before writing files.

**Step 4: Run test to verify it passes later**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: PASS once downstream prompt files and README are also updated.

**Step 5: Commit**

```bash
git add plugins/vibe-noveling/skills/novel-plan/SKILL.md plugins/vibe-noveling/agents/context-collector.md tests/test_novel_write_workflow.py
git commit -m "feat: move planning artifacts into chapter directories"
```

### Task 3: Update `novel-write` and `novel-sync` path contracts

**Files:**
- Modify: `plugins/vibe-noveling/skills/novel-write/SKILL.md`
- Modify: `plugins/vibe-noveling/skills/novel-sync/SKILL.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

Reuse the same workflow suite so these prompts also have to honor the new paths.

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: FAIL until write/read paths point to the new directory layout.

**Step 3: Write minimal implementation**

Update both prompts so they:

- read the planning artifacts from the chapter root directory,
- write final prose and style drafts to `正文.md` and style-named files in the same chapter directory,
- remove legacy flat-path fallback text,
- describe sync and confirmation messages using the new paths.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: PASS after all prompt files are aligned.

**Step 5: Commit**

```bash
git add plugins/vibe-noveling/skills/novel-write/SKILL.md plugins/vibe-noveling/skills/novel-sync/SKILL.md tests/test_novel_write_workflow.py
git commit -m "feat: write chapter drafts into volume directories"
```

### Task 4: Sync README documentation with the new layout

**Files:**
- Modify: `README.md`
- Test: `tests/test_novel_write_workflow.py`

**Step 1: Write the failing test**

Reuse the same test file so public docs are covered by the directory-contract assertions.

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: FAIL because README still documents flat files in `chapters/`.

**Step 3: Write minimal implementation**

Update the README so it documents:

- the new `chapters/vol-xx/ch-xxxx/` tree,
- sample artifact names inside each chapter directory,
- any command examples or workflow references that mention old flat paths.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_novel_write_workflow.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add README.md tests/test_novel_write_workflow.py
git commit -m "docs: describe chapter directory layout"
```

### Task 5: Run final verification

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
Expected: all workflow assertions pass, including the new directory-layout checks.

**Step 5: Commit**

```bash
git add docs/plans/2026-04-08-chapter-directory-layout-design.md docs/plans/2026-04-08-chapter-directory-layout.md README.md plugins/vibe-noveling/agents/context-collector.md plugins/vibe-noveling/skills/novel-plan/SKILL.md plugins/vibe-noveling/skills/novel-sync/SKILL.md plugins/vibe-noveling/skills/novel-write/SKILL.md tests/test_novel_write_workflow.py
git commit -m "docs: define chapter directory layout"
```
