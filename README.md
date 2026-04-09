# Vibe Noveling

**用 Claude Code 写小说的专业工作流工具包。**

一套完整的中文网络小说创作工作流，基于 Claude Code 的自定义 Skill + Agent 体系构建。从项目初始化到章节发布，覆盖小说创作的全流程。

## 特性

- **10 个专业技能 + 2 个内置子 Agent** — 覆盖初始化、讨论、规划、写作、检查、同步全流程
- **知识图谱驱动** — 自动管理角色、地点、物品、势力等设定，支持搜索和关系追踪
- **Save the Cat 剧情架构** — 内置 15 节拍故事母型，支持全书/分卷/单章三层规划
- **逐点澄清后再落大纲** — `/novel-plan` 会先澄清每个小剧情点的 5W1H，再把确认后的推进链压成可手改的精简剧情纲要
- **默认全风格逐个启动写作 Agent + 自动合并** — 基于精简剧情纲要在正文阶段内部切分，按风格顺序拉起 4 个写作 Agent，并按内部写作单元逐个合并，避免把写作和合并都堆成一次性大请求
- **规划期强制反思 + 爽点检查** — `novel-plan` 内置结构层自检，先在大纲阶段拦住平淡和失效推进
- **正文期 AI 味检测** — `novel-write` 内置 20 项文本质检与最终稿文风矫正
- **命名生成器** — 支持角色、功法、门派、物品等 8 类命名，带稀有度体系
- **进度可视化** — 自动生成字数统计饼图
- **快照管理** — 安全的版本备份与回滚
- **文档与回归测试同步维护** — `docs/plans/` 记录流程设计演进，`tests/` 用静态断言守住提示词契约

## 技能一览

| 技能 | 触发词 | 说明 |
|------|--------|------|
| `/novel-init` | 初始化、新建小说 | 创建完整的项目结构和目录 |
| `/novel-discuss` | 讨论、设计角色、世界观 | 苏格拉底式对话，支持世界观/角色/物品/势力/体系设计 |
| `/novel-bookplan` | 全书大纲、卷结构 | Save the Cat 15 节拍全书架构规划，按卷与节拍规划，不预设章节数 |
| `/novel-plan` | 规划下一章 | 先澄清每个小剧情点的 5W1H，再生成单章第三人称精简剧情纲要 + Opus 正文测试，并内置规划期强制反思与爽点检查 |
| `/novel-write` | 写章节、创作正文 | 默认全风格逐个启动写作 Agent，并按内部写作单元逐个合并最终稿，内置 20 项 AI 味检测与最终稿文风矫正 |
| `/novel-sync` | 同步、更新状态 | 章节完成后更新知识图谱 |
| `/novel-knowledge` | （内部调用） | 知识图谱：搜索/创建/更新实体 |
| `/novel-name` | 命名、取名 | 8 类命名生成器（Python 脚本） |
| `/novel-snapshot` | 快照、备份 | 项目版本快照管理 |
| `/novel-progress` | 进度、字数 | 创作进度可视化（HTML 饼图） |

## 内置 Agents

| Agent | 用途 |
|------|------|
| `context-collector` | 为 `novel-plan` / `novel-write` 收集并缓存章节上下文 |
| `consistency-guard` | 为 `novel-write` 提供一致性检查，替代已废弃的独立检查 skill |

## 工作流

```
/novel-init          →  初始化项目
    ↓
/novel-discuss       →  设计世界观、角色、设定
    ↓
/novel-bookplan      →  全书架构与卷规划（可选）
    ↓
/novel-plan          →  先澄清每个小剧情点的 5W1H，再生成逐章精简剧情纲要 + 内置规划期强制反思与爽点检查
    ↓
/novel-write         →  正文阶段内部切分 + 默认全风格逐个启动写作 Agent + 按内部写作单元逐个合并 + 内置 AI 味检测与一致性检查
    ↓
生成最终稿          →  自动合并生成最终稿，并保留各风格中间稿供回看
    ↓
/novel-sync          →  同步更新知识图谱
    ↓
/novel-snapshot      →  创建版本快照（随时）
/novel-progress      →  查看创作进度（随时）
```

## 当前小说创作流程说明

这套工作流现在分成 7 个阶段，核心原则是：设定先落长期记忆，结构先落 `future/`，单章先做 `5W1H` 对齐，再进入正文创作。

### 1. 初始化项目：`/novel-init`

先创建标准项目骨架，包括：

- `memory/` 长期记忆与知识图谱
- `memory/future/` 全书、分卷、arc、线程规划
- `chapters/vol-xx/ch-xxxx/` 章节目录
- `CLAUDE.md` 当前项目说明

这是后续所有 skill 的共同上下文基础。

### 2. 讨论设定与剧情方向：`/novel-discuss`

当你需要设计世界观、角色、势力、物品、体系，或者讨论接下来怎么写时，先用 `/novel-discuss`。

当前流程里，`/novel-discuss` 不只是“聊天”：

- 会先按话题选择讨论 reference
- 再按动作读取最小相关上下文
- 不再默认全量扫描整个 `memory/`
- 设定类结论会写回对应实体文件或长期记忆
- 已确认的未来剧情、卷计划、arc 方向会同步写入 `memory/future/`
- 还没定下来的备选方案只保留在讨论里，不会提前污染正式规划

如果你讨论的是未来剧情方向，它还会多做一层两段式收束：

- 先用苏格拉底式方式讨论未来剧情方向
- 当方向开始收束时，再用显式 `5W1H` 澄清选中方案
- 这一步服务于 future/ 输入，不替代 `/novel-plan` 的章节级对齐卡

也就是说，它负责把“想法”变成后面 `novel-bookplan` / `novel-plan` 可读取的稳定输入。

### 3. 规划全书与分卷：`/novel-bookplan`

如果项目还没有成型的全书节奏蓝图，或者你刚补完一批会影响主线的设定，就先跑 `/novel-bookplan`。

它当前负责的是全书和分卷层，不直接给章节编号：

- 识别或确认故事母型
- 规划全书 beat 和主线线程
- 规划每一卷的职责段、卷内位置、关键状态变化
- 把结果写入 `memory/future/`

它不预设总章节数，也不提前决定“第几章发生什么”，这些章位决策留给单章规划阶段。

### 4. 规划单章：`/novel-plan`

`/novel-plan` 现在是“先对齐，再落纲”的流程，而不是直接吐一版章节大纲。

它会按这个顺序工作：

1. 读取 `memory/future/`、上一章大纲和 `past.md`，先确定本章节奏定位
2. 生成章节任务卡，确认本章主任务、必须推进的线、允许延期的线、建议收尾点
3. 把选定走向拆成 3-8 个小剧情点
4. 逐点澄清 `Who / What / Why / Where / When / How`
5. 先输出 `小剧情点对齐卡` 给你确认
6. 确认后再压成第三人称精简剧情纲要，写入 `chapters/vol-{volume_padded}/ch-{chapter_padded}/大纲.md`
7. 默认继续生成 `上下文.md`，并用 Opus 做一次试写，反推结构问题

这里有两个重要边界：

- `5W1H` 对齐卡只在对话里用来澄清，不回写到最终 `大纲.md`
- 如果 Opus 试写暴露结构断点，优先回到 `/novel-plan --revise`，而不是硬进正文

### 5. 写正文：`/novel-write`

`/novel-write` 接的是已经确认好的精简大纲，而不是自己重做结构。

它现在的正文流程是：

1. 读取 `大纲.md`、`上下文.md`、`Opus报告.md`
2. 在正文阶段内部切分写作单元，这个切分只在执行层使用，不回写 outline
3. 按固定顺序逐个启动 4 个风格写作 Agent，而不是一次性全并发
4. 保留各风格中间稿
5. 再按内部写作单元顺序逐个合并，输出连续章节正文 `正文.md`
6. 完成后做一致性检查和最终复检

所以现在的设计是：结构收敛发生在 `novel-plan`，落文与风格吸收发生在 `novel-write`，两边职责分开。

### 6. 同步结果：`/novel-sync`

章节正文确认后，用 `/novel-sync` 把本章结果同步回项目状态：

- 更新 `memory/past.md`
- 更新 `memory/future/` 中已兑现、延期或状态变化的条目
- 更新知识图谱和实体关系

这样下一次再跑 `/novel-plan` 时，读取到的是已经推进过的最新状态，而不是停留在旧计划。

### 7. 辅助工具：`/novel-snapshot` 与 `/novel-progress`

这两个不是主线流程，但建议常用：

- `/novel-snapshot`：在大改大纲、重写章节、批量补设定前后做快照
- `/novel-progress`：查看当前正文、章节产物和字数进度

### 一条典型路径

一个常见的实际循环会是这样：

`/novel-init` → `/novel-discuss` → `/novel-bookplan` → `/novel-plan` → `Opus 试写`

如果试写发现结构不顺：

`/novel-plan --revise` → 再试写 → `/novel-write` → `/novel-sync`

如果中途补了重要设定或长期主线方向：

先回 `/novel-discuss` 或 `/novel-bookplan`，把上游结构更新完，再继续单章规划。

## 安装

### 方式一：Claude Plugin Marketplace（推荐）

在 Claude Code 中直接安装：

```bash
/plugin marketplace add TulanCN/vibe-noveling
/plugin install vibe-noveling@vibe-noveling
```

安装后 10 个技能和 2 个内置子 Agent 自动可用，支持自动更新。

### 方式二：手动复制

```bash
# 1. 克隆仓库
git clone https://github.com/TulanCN/vibe-noveling.git

# 2. 复制 Skills
cp -r vibe-noveling/plugins/vibe-noveling/skills/* 你的项目/.claude/skills/

# 3. 复制 Agents
mkdir -p 你的项目/.claude/agents
cp -r vibe-noveling/plugins/vibe-noveling/agents/* 你的项目/.claude/agents/
```

### 方式三：符号链接（适合开发调试）

```bash
ln -s /path/to/vibe-noveling/plugins/vibe-noveling/skills/novel-init .claude/skills/novel-init
ln -s /path/to/vibe-noveling/plugins/vibe-noveling/skills/novel-discuss .claude/skills/novel-discuss
# ... 对每个 skill 重复

ln -s /path/to/vibe-noveling/plugins/vibe-noveling/agents/context-collector.md .claude/agents/context-collector.md
ln -s /path/to/vibe-noveling/plugins/vibe-noveling/agents/consistency-guard.md .claude/agents/consistency-guard.md
```

## 使用前提

- [Claude Code CLI](https://claude.ai/code) 已安装
- Python 3.10+（用于命名生成器、知识图谱、进度图表等脚本）
- PyYAML（知识图谱依赖）：`pip install pyyaml`

## 项目结构

安装后的标准项目结构：

```
your-novel/
├── CLAUDE.md                  # 项目说明
├── memory/                    # 长期记忆（设定）
│   ├── _graph.json            # 知识图谱（自动生成）
│   ├── _index.json            # 索引文件（自动生成）
│   ├── entities/              # 实体文件
│   │   ├── characters/        # 角色设定
│   │   ├── locations/         # 地点设定
│   │   ├── factions/          # 势力设定
│   │   ├── items/             # 物品设定
│   │   └── concepts/          # 概念设定
│   ├── past.md                # 已完成剧情
│   └── future/                # 未来规划
│       ├── 00-index.md
│       ├── 10-book.md         # 全书锚点
│       ├── 20-threads.md      # 主线线程
│       ├── 30-volumes/        # 分卷蓝图
│       └── 40-arcs/           # arc 规划
├── chapters/                  # 章节目录
│   └── vol-01/
│       └── ch-0001/
│           ├── 大纲.md        # 精简剧情纲要
│           ├── 上下文.md      # 章节上下文
│           ├── Opus试写.md    # 试写正文
│           ├── Opus报告.md    # 反推报告
│           ├── 海明威.md      # 风格中间稿
│           └── 正文.md        # 最终正文
├── .snapshots/                # 版本快照
└── templates/                 # 模板文件
```

例如最终正文路径为 `chapters/vol-01/ch-0001/正文.md`。

## 快速开始

```bash
# 1. 在 Claude Code 中初始化新项目
/novel-init

# 2. 讨论和设计你的世界
/novel-discuss

# 3. 规划第一章
/novel-plan

# 4. 开始写作
/novel-write 01

# 5. 确认最终稿并同步
/novel-sync chapter 1

# 6. 查看进度
/novel-progress
```

## 仓库结构

```
vibe-noveling/
├── .claude-plugin/
│   └── marketplace.json       # Plugin marketplace 清单
├── docs/
│   └── plans/                 # 工作流调整与实现计划
├── plugins/
│   └── vibe-noveling/          # 插件根目录
│       ├── .claude-plugin/
│       │   └── plugin.json     # 插件元数据
│       ├── agents/             # 子 Agent（上下文收集 / 一致性守护）
│       └── skills/
│           ├── novel-init/
│           ├── novel-discuss/
│           │   └── references/
│           ├── novel-bookplan/
│           │   └── references/
│           ├── novel-plan/
│           │   └── references/
│           ├── novel-write/
│           │   ├── references/
│           │   └── tools/
│           ├── novel-sync/
│           ├── novel-knowledge/
│           │   └── scripts/
│           ├── novel-name/
│           │   ├── data/
│           │   └── tools/
│           ├── novel-snapshot/
│           │   └── scripts/
│           └── novel-progress/
│               └── scripts/
├── tests/
│   └── test_novel_write_workflow.py
├── README.md
└── LICENSE
```

Skill 文件中使用 `{SKILL_DIR}` 作为占位符，表示该 Skill 的安装目录。实际使用时会解析为：

```
.claude/skills/{skill-name}/
```

例如 `{SKILL_DIR}/references/world-design.md` 实际对应 `.claude/skills/novel-discuss/references/world-design.md`。

## 开发与验证

```bash
# 运行提示词契约回归测试
python3 -m unittest tests/test_novel_write_workflow.py -v

# 快速检查核心文案是否保持一致
rg -n "先澄清每个小剧情点的 5W1H|第三人称精简剧情纲要|正文阶段内部切分|按内部写作单元逐个合并|自动合并生成最终稿" \
  README.md \
  plugins/vibe-noveling/skills/novel-plan/SKILL.md \
  plugins/vibe-noveling/skills/novel-plan/references/output.md \
  plugins/vibe-noveling/skills/novel-write/SKILL.md
```

## 设计文档

- `docs/plans/2026-04-07-outline-format-redesign*.md`：记录 `novel-plan` 从旧版章节大纲格式转为第三人称精简剧情纲要的设计与实施。
- `docs/plans/2026-04-08-novel-plan-5w1h-alignment*.md`：记录 `novel-plan` 在生成精简大纲前新增小剧情点 `5W1H` 对齐卡的设计与实施。
- `docs/plans/2026-04-07-postwrite-style-correction*.md`：记录最终稿复检阶段的正文后文风矫正规则。
- `docs/plans/2026-04-08-pointwise-merge*.md`：记录 `novel-write` 按内部写作单元逐个合并最终稿的流程调整。

## 支持的小说类型

- 修真 / 仙侠
- 玄幻 / 奇幻
- 都市 / 现代
- 科幻 / 未来
- 历史 / 古言
- 其他类型（自定义）

## 许可证

[MIT](LICENSE)

## 致谢

- 基于 [Claude Code](https://claude.ai/code) 自定义 Skill 体系
- 剧情架构参考 [Save the Cat! Writes a Novel](https://www.savethecat.com/) 的 15 节拍法
