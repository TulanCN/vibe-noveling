# Default Novel Style Design

**Goal:** Add a project-level default style contract during `novel-init` so the workflow consistently writes toward a Chinese male-audience web-serial baseline instead of relying on ad hoc alignment during chapter planning and drafting.

**Architecture:** Keep `CLAUDE.md` as the single project entry point, but upgrade it from a pure directory guide into a workflow contract. `novel-init` writes the default style baseline into `CLAUDE.md`, `novel-plan` turns that baseline into chapter-planning checks, `novel-write` turns it into prose-selection and merge rules, and `novel-discuss` uses it as a guardrail when designing future settings, characters, and relationship beats.

## Problem

The current workflow describes project structure well, but it does not pin down what kind of novel this project is trying to become. As a result:

- `novel-init` creates `CLAUDE.md` as a structural guide only
- later skills do not inherit a stable project-level prose target
- chapter output can drift away from the user’s expected male-audience web-serial feel
- “style” is handled too late, mostly during drafting and final polish

The missing piece is not only “write style into a file”, but “make the whole workflow read and execute that style as a hard default”.

## Chosen Direction

Use **Option 2**:

- `novel-init` writes a default style section into `CLAUDE.md`
- `novel-plan`, `novel-write`, and `novel-discuss` explicitly read and apply it
- the default style acts as the project baseline unless the user later adds stronger project-specific guidance

This is preferred over a `CLAUDE.md`-only documentation change because the user problem is execution drift, not documentation absence.

## Default Style Contract

The baseline should be written in direct, operational language rather than abstract “tone” labels.

### Core Positioning

- The project defaults to a Chinese male-audience web-serial approach
- The protagonist defaults to male
- Narrative priority stays with the protagonist rather than being evenly distributed across ensemble characters

### Protagonist Drive

The protagonist’s key actions ultimately serve “装逼” payoff.

Here, “装逼” should be interpreted operationally as:

- appearing stronger than others
- appearing rarer or more special than others
- making better judgments than others
- gaining treatment, recognition, or opportunities that others do not receive

Cultivation, combat, schemes, wealth accumulation, puzzle-solving, status climbing, and relationship progress are not independent end goals. They are buildup, leverage, or payoff for protagonist-centered dominance and distinction.

### Romance and Supporting Cast Usage

- Romance is not primarily for lyrical introspection
- its main function is to amplify the protagonist’s special treatment
- female-character interactions should highlight attitude differences toward the protagonist versus others
- supporting characters, rivals, antagonists, and bystanders should primarily provide contrast, pressure, witness value, face-slapping targets, or recognition shifts

### Plot Filtering Rule

Any subplot, transition, explanation, banter, slice-of-life material, or emotional padding that does not serve the protagonist’s “装逼 chain” should be cut, merged, or compressed by default.

A scene or beat is high priority only if it serves at least one of these functions:

- builds momentum for the protagonist
- creates dismissal, suppression, or contrast
- prepares a reversal or face-slapping target
- magnifies the protagonist’s strength, status, resources, judgment, or rarity
- causes another character’s attitude to shift toward the protagonist
- delivers new reward, privilege, opportunity, or recognition to the protagonist

### Default Payoff Loop

Single chapters or short chapter runs should preferably form a recognizable payoff loop:

`蓄势 -> 受压/被轻视/形成对比 -> 主角出手或亮底牌 -> 他人震动/改变态度/被打脸 -> 主角获得资源、地位、关系或名望上的兑现`

If a chapter is only a bridge chapter, it still needs to explain what future payoff it is preparing.

## `CLAUDE.md` Structure Change

`novel-init` should extend the generated `CLAUDE.md` with a dedicated section such as:

- `## 默认创作风格基线`
- `### 项目定位`
- `### 主角核心驱动`
- `### 感情戏与配角使用原则`
- `### 情节取舍规则`
- `### 默认爽点循环`

This section should live alongside project overview and directory structure so later skills can reliably find and reuse it.

## Workflow Integration

### `plugins/vibe-noveling/skills/novel-init/SKILL.md`

Responsibilities:

- update initialization instructions so `CLAUDE.md` includes the default style contract
- stop describing `CLAUDE.md` as only a structural guide
- explicitly frame `CLAUDE.md` as both project structure reference and project writing contract

### `plugins/vibe-noveling/skills/novel-plan/SKILL.md`

Responsibilities:

- add a pre-read rule: read the style baseline in `CLAUDE.md` before planning the chapter
- convert the default style into chapter-planning checks
- tighten existing “爽点检查” into a more explicit “装逼兑现度” evaluation

Recommended planning checks:

- what kind of protagonist payoff is this chapter serving
- where does this chapter build pressure, contrast, or suppression
- who provides the comparison or face-slapping function
- what new recognition, resource, privilege, or status does the protagonist gain by the end
- if the chapter is transitional, what next payoff is it preparing
- which lines can be delayed because they do not serve the protagonist’s payoff chain

At the `5W1H` alignment stage, each plot point should also be tested for whether it:

- builds toward protagonist payoff
- creates contrast or reversal space
- directly cashes out protagonist distinction
- wastes space on neutral information without sharpening the protagonist

### `plugins/vibe-noveling/skills/novel-write/SKILL.md`

Responsibilities:

- add prose-level rules that preserve protagonist sharpness and payoff visibility
- ensure multi-style merge prefers lines that keep the protagonist strong, special, and differentially treated
- add a final review check against “flattening” male-audience payoff into safe neutral prose

Recommended drafting and merge preferences:

- prefer lines that show the protagonist judging faster or better than others
- prefer moments where others doubt, dismiss, or underestimate the protagonist before being corrected by reality
- prefer female-character or key-character reactions that highlight differential treatment
- prefer explicit payoff nodes involving reward, recognition, privilege, or status gain
- compress safe but non-sharpening sentences

### `plugins/vibe-noveling/skills/novel-discuss/SKILL.md`

Responsibilities:

- keep future setting and character design aligned with the project baseline
- use the baseline as a light guardrail instead of a heavy writing template

Recommended discussion guardrails:

- ask how a new character serves the protagonist’s payoff chain
- ask how romance or emotional beats amplify protagonist specialness
- ask whether a rival, antagonist, or supporting character creates pressure, contrast, or a face-slapping platform
- warn when an interesting setting idea consumes too much narrative space without serving protagonist payoff

## Compatibility Rules

The style baseline is the project default, not an absolute ban on later customization.

Priority order:

1. Initialization baseline in `CLAUDE.md`
2. Later explicit project-level additions in `CLAUDE.md`
3. Chapter-level temporary preferences that do not contradict the project baseline

This allows later project-specific flavor shifts while keeping a stable fallback identity.

## Risk Boundaries

The main risk is over-narrow execution. The design should explicitly state:

- “装逼” is not limited to loud boasting or simplistic face-slapping; it also includes superior judgment, rarity, steadiness, hidden leverage, and privileged access
- “all roads serve protagonist payoff” does not mean all supporting characters must become empty tools
- romance serving protagonist payoff does not mean female characters should become pure props; their independent choices and reactions can still function as amplifiers of protagonist distinction
- cutting irrelevant material does not mean turning bridge chapters into outline summaries; bridge chapters must still build toward the next payoff
- a male-audience baseline does not mean identical pacing in every chapter; setback, delay, or calm beats are allowed when they strengthen later payoff

## Verification

Add or extend static tests to enforce the new contract:

### `tests/test_novel_write_workflow.py`

- assert `novel-init` writes a default style baseline into `CLAUDE.md`
- assert the baseline includes “主角默认男性”, “关键行为最终服务装逼”, and plot-compression rules
- assert `novel-plan` explicitly reads `CLAUDE.md` for project style before planning
- assert `novel-plan` checks whether a chapter serves the protagonist payoff chain and whether a bridge chapter is building toward the next payoff
- assert `novel-write` prefers protagonist sharpness, differentiated treatment, and payoff retention in final merge
- assert `novel-discuss` keeps new design work aligned with the protagonist payoff chain
- assert `README.md` documents that the workflow now carries a default male-audience style baseline from initialization onward

## Outcome

After this change, the workflow should no longer rely on vague genre memory. A new project starts with a declared writing baseline, and later skills inherit that baseline as a concrete execution contract. The result should be tighter alignment between initialization, chapter planning, drafting, and future-setting discussion.
