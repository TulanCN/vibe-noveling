# vibe-noveling 仓库协作说明

本文件面向两类读者：

- AI coding agent：进入仓库后快速理解哪里该改、哪里不要乱动、改完如何验证。
- 人类贡献者：在不通读全部历史文档的前提下，快速掌握这个仓库的维护方式。

这不是最终小说项目里的运行时说明，而是这个插件仓库本身的协作手册。

## 仓库定位

`vibe-noveling` 是一个面向 Claude Code 的中文网文创作工作流插件仓库。核心资产不是传统应用代码，而是：

- Skills 提示词契约
- Agents 协作提示词
- 少量 Python 工具脚本
- README、设计文档和静态回归测试

因此，这个仓库的“行为”经常由文案决定。很多看起来只是措辞调整的改动，实际上会改变工作流契约，必须像改代码一样谨慎处理。

## 先看哪里

处理任务前，优先确认这几个位置：

- `README.md`
  当前对外说明、仓库结构、开发验证命令都在这里。
- `plugins/vibe-noveling/`
  发布产物主路径。要发布到 marketplace 的 skills、agents、plugin metadata 都在这里。
- `tests/test_novel_write_workflow.py`
  静态断言测试，负责守住关键提示词契约和目录约定。
- `docs/plans/`
  工作流演进历史。涉及流程变更时，先搜索是否已有设计文档或相关上下文。

## 目录职责

### 发布相关

- `plugins/vibe-noveling/.claude-plugin/plugin.json`
  插件元数据。
- `plugins/vibe-noveling/agents/`
  内置子 Agent 提示词。
- `plugins/vibe-noveling/skills/`
  发布版 Skills、reference 文档和脚本工具。

### 仓库级辅助文件

- `.claude-plugin/marketplace.json`
  marketplace 清单。
- `README.md`
  面向使用者和贡献者的总说明。
- `docs/plans/`
  设计与实施记录。
- `tests/`
  回归测试。

### 本地开发目录

- `.claude/`
  本地 Claude Code 开发布局，路径形态接近安装后的使用环境。

重要：`plugins/vibe-noveling/` 和 `.claude/` 不要默认当成永远同步的镜像。这个仓库里它们可能存在差异。改动前先确认当前任务到底应该落在发布目录、开发目录，还是两边都要处理。

## 默认编辑策略

如果没有更具体的任务说明，按下面的优先级操作：

1. 涉及发布行为、skill 契约、agent 提示词的改动，优先编辑 `plugins/vibe-noveling/` 下的文件。
2. 涉及对外文档、安装方式、工作流说明的改动，同时更新 `README.md`。
3. 涉及工作流行为变化、输出格式变化、关键词契约变化的改动，同时更新 `tests/test_novel_write_workflow.py`。
4. 涉及较大的流程调整或设计决策，补充 `docs/plans/` 文档，保持设计历史可追溯。
5. 只有在任务明确要求，或本地开发流程确实依赖 `.claude/` 目录时，才同步修改 `.claude/` 下的副本。

## 高频改动模式

### 改 Skill 行为

通常需要一起检查：

- `plugins/vibe-noveling/skills/<skill>/SKILL.md`
- 该 skill 下的 `references/`、`tools/`、`scripts/`
- `README.md`
- `tests/test_novel_write_workflow.py`
- 如有必要，`docs/plans/*.md`

注意大小写：发布目录里通常是 `SKILL.md`，本地 `.claude/skills/...` 里常见的是 `skill.md`。

### 改 Agent 行为

通常需要一起检查：

- `plugins/vibe-noveling/agents/*.md`
- 引用该 agent 的 skill 文档
- `README.md`
- 相关静态断言测试

### 改元数据或发布信息

通常需要一起检查：

- `plugins/vibe-noveling/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `README.md` 中的版本、能力描述、安装说明

## 验证方式

这个仓库当前最重要的验证是静态契约测试和关键文案检索。

常用命令：

```bash
python3 -m unittest tests/test_novel_write_workflow.py -v
```

```bash
rg -n "故事大纲|故事梗概|剧情思路卡|叙述式可写场景纲要|大纲 AI 味检测|正文阶段内部切分|按内部写作单元逐个合并|自动合并生成最终稿" \
  README.md \
  plugins/vibe-noveling/skills/novel-plan/SKILL.md \
  plugins/vibe-noveling/skills/novel-plan/references/output.md \
  plugins/vibe-noveling/skills/novel-write/SKILL.md
```

如果改动触及 Python 脚本，也要按改动范围补做针对性执行或最小手动验证。

## 文档和测试的关系

这里的测试不是在测传统业务逻辑，而是在测“提示词契约是否还成立”。因此：

- 不要把测试失败简单理解成“文案太死板”
- 先判断是你真的改了工作流，还是无意破坏了既有契约
- 如果确实有意调整行为，要同步更新 README、Skill 文案、reference 文档和测试断言

很多改动都需要四处联动：`plugins/...`、`README.md`、`tests/`、`docs/plans/`。

## 不要顺手改的内容

除非任务明确要求，否则不要随手修改这些内容：

- `.omc/`
  本地状态缓存。
- `plugins/.snapshots/`
  用户/调试快照。
- `plugins/vibe-noveling/skills/novel-knowledge/.venv/`
  本地 Python 虚拟环境。
- 各类 `__pycache__/`
  生成产物。

## 提交前自检

准备收尾前，至少做这几件事：

1. 看一眼 `git status --short`，确认没有误碰无关文件。
2. 回读修改后的提示词，确认新增规则没有和 README 或测试中的既有契约冲突。
3. 如果是行为变更，运行 `python3 -m unittest tests/test_novel_write_workflow.py -v`。
4. 如果你修改了发布描述或版本信息，检查两个 plugin 元数据文件是否需要同步。

## 当前仓库的一条实用判断

当你犹豫“这是不是只是文档改动”时，优先按“可能影响工作流契约”处理。这个仓库里，文档、提示词、参考文档和测试本来就是同一套产品行为的不同投影。
