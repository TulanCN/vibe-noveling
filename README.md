# Vibe Noveling

**用 Claude Code 写小说的专业工作流工具包。**

一套完整的中文网络小说创作工作流，基于 Claude Code 的自定义 Skill + Agent 体系构建。从项目初始化到章节发布，覆盖小说创作的全流程。

针对GLM-5/GLM-5.1模型深度定制优化，其他模型的使用体验欢迎补充到ISSUE。

**注意，使用时，请关闭Claude Code的思考模式！**

**注意，使用时，请关闭Claude Code的思考模式！**

**注意，使用时，请关闭Claude Code的思考模式！**

## 特性

- **13 个专业技能 + 4 个内置子 Agent** — 覆盖初始化、讨论、规划、写作、返修、同步全流程；其中 `booming` 负责剧情爆破，`fuck-it` 负责单章同终点加戏
- **知识图谱驱动** — 自动管理角色、地点、物品、势力等设定，支持搜索和关系追踪
- **Save the Cat 剧情架构** — 内置 15 节拍故事母型，支持全书/分卷/单章三层规划
- **手动剧情爆破模式** — `booming` 主要给 `novel-discuss` 用；当你觉得剧情太平、不够炸、想强行掀桌时，先用 `booming`；默认给 10 套高烈度爆破走向（每套一句话梗概），至少两套必须真正掀桌
- **同终点单章加戏模式** — `fuck-it` 主要给 `novel-discuss` 用；当你不想改本章结束目标、只想把单章内部写得更戏剧、更夸张、更有漫画感时，先用 `fuck-it`；默认给 3 套同终点强化方案，但会先过一遍内置的 15 种单章加戏方向，再从中挑 3 种，且每套都必须有漫画感
- **事件讨论 + 场景链规划** — `/novel-discuss` 事件画布从根问题出发，产出事件故事大纲、章节拆分（每章直接含场景链）、派生标注；场景链将直接作为 novel-write 的写作输入
- **正文创作** — `/novel-write` 从事件卡读场景链 → 强制反思 → 写作 → 后处理（一致性校验 + AI 味检测 + 润色）
- **正文期 AI 味检测 + 润色阶段** — `novel-write` 写作前强制反思从源头防 AI 腔，完成后读取 `ai-smell-checklist.md` 执行 10 项 AI 味检测与整句重写修正，通过后再做独立润色
- **强制返修环节** — 交付后用户在正文中标记问题点（加粗=扩写、删除线=简写、斜体=润色），运行 `/novel-revise` 为每个标记生成 3 种 SSoT 驱动的改写候选，用户挑选后立即写入，可循环多轮
- **命名生成器** — 支持角色、功法、门派、物品等 8 类命名，带稀有度体系
- **进度可视化** — 自动生成字数统计饼图
- **快照管理** — 安全的版本备份与回滚
- **文档与回归测试同步维护** — `docs/plans/` 记录流程设计演进，`tests/` 用静态断言守住提示词契约

## 技能一览

| 技能                 | 触发词                 | 说明                                                                                                      |
| -------------------- | ---------------------- | --------------------------------------------------------------------------------------------------------- |
| `/novel-init`      | 初始化、新建小说       | 创建完整的项目结构和目录                                                                                  |
| `/novel-discuss`   | 讨论、设计角色、世界观 | 苏格拉底式对话，支持世界观/角色/物品/势力/体系设计                                                        |
| `/booming`         | booming、太平了、不够炸 | 独立触发的剧情爆破模式，但主要给 `novel-discuss` 用；默认给 10 套一句话梗概式高烈度爆破走向，至少两套必须真正掀桌，用户确认后再交给事件讨论落正式大纲 |
| `/fuck-it`         | fuck it、fuck-it、单章加戏 | 同终点单章加戏模式，主要给 `novel-discuss` 用；不改本章结束目标，默认给 3 套同终点强化方案，但会先过一遍内置的 15 种单章加戏方向，再从中挑 3 种，而且每套都必须有漫画感，选中后直接收束进当前事件讨论 |
| `/novel-bookplan`  | 全书大纲、卷结构       | Save the Cat 15 节拍全书架构规划，按卷与节拍规划，不预设章节数                                            |
| `/novel-write`     | 写章节、创作正文       | 从事件卡读场景链 → 强制反思（四维定调 + 预判翻车点 + 核心瞬间 + 禁用句式）→ 写作 → 后处理（一致性校验 + AI 味检测 10 项 + 独立润色）；交付后提示用户运行 `/novel-revise` 返修或 `/novel-sync` 同步 |
| `/novel-revise`    | 返修、处理标记         | 用户在正文中标记问题点（加粗=扩写、删除线=简写、斜体=润色），为每个标记生成 3 种 SSoT 驱动的改写候选，用户挑选后立即写入文件 |
| `/novel-sync`      | 同步、更新状态         | 返修完成后更新知识图谱                                                                        |
| `/novel-knowledge` | （内部调用）           | 知识图谱：搜索/创建/更新实体                                                                              |
| `/novel-name`      | 命名、取名             | 8 类命名生成器（Python 脚本）                                                                             |
| `/novel-snapshot`  | 快照、备份             | 项目版本快照管理                                                                                          |
| `/novel-progress`  | 进度、字数             | 创作进度可视化（HTML 饼图）                                                                               |

## 内置 Agents

| Agent                 | 用途                                                          |
| --------------------- | ------------------------------------------------------------- |
| `context-collector` | 为 `novel-write` 收集并缓存章节上下文      |
| `consistency-guard` | 为 `novel-write` 提供一致性检查，替代已废弃的独立检查 skill |
| `writer-zhouzi` | 为 `novel-write` 产出会说话的肘子风底稿，负责现代快节奏战斗与临场决断 |
| `writer-dazhongma` | 为 `novel-write` 产出大仲马风高光稿，负责精密布局与戏剧交锋 |

## 工作流

```
/novel-init          →  初始化项目
    ↓
/novel-discuss       →  设计世界观、角色、设定
    ↓
/novel-bookplan      →  全书架构与卷规划（可选）
    ↓
/novel-discuss（事件画布）→  事件定位 → 故事大纲 → 章节拆分 + 场景链 → 派生标注 → 写入事件卡
    ↓
/novel-write         →  从事件卡读场景链 → 强制反思 → 写作 → 后处理
    ↓
生成最终稿           →  后处理通过后正文落盘
    ↓
/novel-revise        →  用户在正文中标记问题点（**加粗**=扩写、~~删除线~~=简写、*斜体*=润色），SSoT 驱动为每个标记生成 3 种改写候选，用户挑选后立即写入文件，可循环多轮
    ↓
/novel-sync          →  同步更新知识图谱
    ↓
/novel-snapshot      →  创建版本快照（随时）
/novel-progress      →  查看创作进度（随时）
```

## 当前小说创作流程说明

这套工作流现在分成 6 个阶段，核心原则是：设定先落长期记忆，结构先落 `future/`，场景链在事件讨论中确认后不再额外确认，直接进入正文创作。`booming` 是插在剧情讨论阶段里的可选爆破分支，`fuck-it` 是插在剧情讨论阶段里的同终点加戏分支，它们都不是默认主流程节点。

### 1. 初始化项目：`/novel-init`

先创建标准项目骨架，包括：

- `memory/` 长期记忆与知识图谱
- `memory/future/` 全书、分卷、事件、线程规划
- `chapters/vol-xx/ch-xxxx/` 章节目录
- `CLAUDE.md` 当前项目说明 + 默认创作风格基线

这是后续所有 skill 的共同上下文基础。

当前默认创作风格基线按中国男频网络小说处理：

- 主角默认男性
- 剧情优先服务主角装逼兑现，而不是平均分配群像资源
- 与主角装逼无关的剧情默认砍掉、合并或压缩

也就是说，`CLAUDE.md` 不再只是目录说明，还会把项目级写法约束固定下来，供 `novel-write` 和 `novel-discuss` 持续复用。

### 2. 讨论设定与剧情方向：`/novel-discuss`

当你需要设计世界观、角色、势力、物品、体系，或者讨论接下来怎么写时，先用 `/novel-discuss`。

当前流程里，`/novel-discuss` 不只是“聊天”：

- 会先按话题选择讨论 reference
- 再按动作读取最小相关上下文
- 不再默认全量扫描整个 `memory/`
- 设定类结论会写回对应实体文件或长期记忆
- 已确认的未来剧情、卷计划、事件 方向会同步写入 `memory/future/`
- 还没定下来的备选方案只保留在讨论里，不会提前污染正式规划

如果你讨论的是未来剧情方向，它还会多做一层两段式收束：

- 先用苏格拉底式方式讨论未来剧情方向
- 当方向开始收束时，再用显式 `5W1H` 澄清选中方案
- 这一步服务于 future/ 输入，不替代 `/novel-discuss` 的章节级场景链

也就是说，它负责把”想法”变成后面 `novel-bookplan` 可读取的稳定输入。

如果你在这一阶段明确觉得剧情太平、不够炸、想强行掀桌，可以在讨论过程中直接切到 `booming`：

- `booming` 主要给 `novel-discuss` 用
- 它不是默认主流程节点，而是讨论阶段里的高烈度爆破分支
- 当你觉得剧情太平、不够炸、想强行掀桌时，先用 `booming`
- 默认给 10 套一句话梗概式高烈度爆破走向
- 至少两套必须真正掀桌
- 用户确认后再交给事件讨论落正式大纲

它的定位不是替代 `/novel-discuss`，而是在讨论阶段把“还不够狠”的方向强行推过安全线。

适合它处理的典型场景：

- 这一章太顺了，缺少真正的损失
- 反派压迫感不够，像例行公事
- 伏笔埋很久了，但一直没敢引爆
- 你想让故事突然改命、改局、改关系，但又不想自己先收手

如果你不想改章末结果，只是想把这一章内部写得更戏剧、更夸张、更有漫画感，可以切到 `fuck-it`：

- `fuck-it` 主要给 `novel-discuss` 用
- 它不改本章结束目标，只放大抵达这个终点之前的冲突、表演力和场面感
- 当你觉得这一章过程太平、太顺、太像普通过桥时，先用 `fuck-it`
- 先过一遍内置的 15 种单章加戏方向，再从中挑 3 种
- 这 3 套同终点强化方案每套都必须有漫画感
- 选中后直接收束进当前事件讨论

它的定位不是替代 `/booming`，而是在不改章末目标的前提下，把单章内部推进链强行提气、抬压、加戏。

### 3. 规划全书与分卷：`/novel-bookplan`

如果项目还没有成型的全书节奏蓝图，或者你刚补完一批会影响主线的设定，就先跑 `/novel-bookplan`。

它当前负责的是全书和分卷层，不直接给章节编号：

- 识别或确认故事母型
- 规划全书 beat 和主线线程
- 规划每一卷的职责段、卷内位置、关键状态变化
- 把结果写入 `memory/future/`

它不预设总章节数，也不提前决定”第几章发生什么”，章节级规划由事件讨论产出。

### 4. 写正文：`/novel-write`

`/novel-write` 从事件卡中读取本章的场景链，而不是自己重做结构。

流程：
1. 读事件卡，提取本章场景链
2. **写作前强制反思**（thinking 中完成，不输出）：四维定调 → 预判翻车点 → 核心瞬间 → 禁用句式
3. 从场景链直接展开为具象正文，以反思结论为内置约束
4. 后处理：一致性校验 → AI 味检测（完整 10 项）→ 独立润色
5. 交付后提示用户进行返修和同步

关键边界：
- 上下文读到 `memory/past.md` 就停
- 结构问题不在正文阶段硬修——回事件讨论改事件卡

所以现在的设计是：结构收敛发生在 `novel-discuss` 的事件画布阶段（产出场景链）；`novel-write` 从事件卡读场景链，做强制反思从源头防 AI 腔，再把场景链展开为血肉，交付后由用户决定是否需要返修。

### 5.5. 返修正文：`/novel-revise`

正文交付后，用户可以在正文中标记问题点，运行 `/novel-revise` 进行返修。

标记约定：

- `**加粗**` = 扩写（一句话太干，想多写点）
- `~~删除线~~` = 简写（太啰嗦，需要压缩）
- `*斜体*` = 润色（句子不顺/散/卡，需要调整）

返修流程：

1. 用户在正文中标记问题点
2. 运行 `/novel-revise`
3. 对每个标记，用 SSoT 驱动生成 3 种不同策略的改写候选
4. 用户挑选最满意的版本（或输入自定义改写）
5. 选定后立即写入文件
6. 重复直到所有标记处理完毕
7. 返修完成后运行 `/novel-sync` 同步知识图谱

核心原则：人最不可取代的部分是品味。AI 生成所有候选策略，人来判断用哪个。SSoT 确保每个候选版本写法不同，避免趋同。

### 6. 同步结果：`/novel-sync`

章节正文确认后，用 `/novel-sync` 把本章结果同步回项目状态：

- 更新 `memory/past.md`
- 更新 `memory/future/` 中已兑现、延期或状态变化的条目
- 更新知识图谱和实体关系

这样下一次再跑 `/novel-write` 时，读取到的是已经推进过的最新状态，而不是停留在旧计划。

### 7. 辅助工具：`/novel-snapshot` 与 `/novel-progress`

这两个不是主线流程，但建议常用：

- `/novel-snapshot`：在大改大纲、重写章节、批量补设定前后做快照
- `/novel-progress`：查看当前正文、章节产物和字数进度

### 一条典型路径

一个常见的实际循环会是这样：

`/novel-init` → `/novel-discuss` → `/novel-bookplan` → `/novel-write`

如果在 `/novel-discuss` 阶段觉得剧情太平、不够炸，可以临时切到 `booming`，再把选中的爆破方向送回事件讨论。

如果章末目标已经定了，但你只想把本章内部写得更戏剧、更夸张、更有漫画感，可以在 `/novel-discuss` 阶段临时切到 `fuck-it`，选中后直接收束进当前事件讨论。

如果试写发现结构不顺：

回事件讨论修订场景链 → 再试写 → `/novel-write` → `/novel-revise` → `/novel-sync`

如果中途补了重要设定或长期主线方向：

先回 `/novel-discuss` 或 `/novel-bookplan`，把上游结构更新完，再继续章节写作。

## 安装

### 方式一：Claude Plugin Marketplace（推荐）

在 Claude Code 中直接安装：

```bash
/plugin marketplace add TulanCN/vibe-noveling
/plugin install vibe-noveling@vibe-noveling
```

安装后 13 个技能和 4 个内置子 Agent 自动可用，支持自动更新。

**注意，请关闭Claude Code的思考模式，避免过度思考导致剧情丧失了创造性。**

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
ln -s /path/to/vibe-noveling/plugins/vibe-noveling/agents/writer-zhouzi.md .claude/agents/writer-zhouzi.md
ln -s /path/to/vibe-noveling/plugins/vibe-noveling/agents/writer-dazhongma.md .claude/agents/writer-dazhongma.md
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
│       └── 40-events/           # 事件 规划
├── chapters/                  # 章节目录
│   └── e01/
│       └── ch-01/
│           └── 正文.md        # 正文
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

# 3. 事件讨论（产出场景链）
/novel-discuss

# 4. 开始写作
/novel-write 01

# 5. 在正文中标记问题点，运行返修
/novel-revise 01

# 6. 确认最终稿并同步
/novel-sync chapter 1

# 7. 查看进度
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
│       ├── agents/             # 子 Agent（上下文收集 / 一致性守护 / 2 个 writer subagent）
│       └── skills/
│           ├── novel-init/
│           ├── novel-discuss/
│           │   └── references/
│           ├── booming/
│           ├── fuck-it/
│           ├── novel-bookplan/
│           │   └── references/
│           ├── novel-write/
│           │   ├── references/
│           │   └── tools/
│           ├── novel-revise/
│           │   └── references/
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
rg -n "事件定位|故事大纲|场景链|四通道|fuck it|fuck-it|本章结束目标|AI 味检测|强制反思" \
  README.md \
  plugins/vibe-noveling/skills/booming/SKILL.md \
  plugins/vibe-noveling/skills/fuck-it/SKILL.md \
  plugins/vibe-noveling/skills/novel-write/SKILL.md \
  plugins/vibe-noveling/skills/novel-discuss/references/event-canvas.md
```

## 设计文档

- `docs/plans/2026-04-07-outline-format-redesign*.md`：记录 `novel-plan` 从旧版章节大纲格式转为第三人称精简剧情纲要的设计与实施。
- `docs/plans/2026-04-28-novel-plan-story-outline-design.md`：记录 `novel-plan` 从 SSoT 发散 + 5W1H 填表改为故事大纲 + 逐步澄清流程的设计。
- `docs/plans/2026-04-29-novel-plan-narrative-outline.md`：记录 `novel-plan` 故事梗概落盘、场景纲要改为叙述式段落、新增大纲 AI 味检测的设计。
- `docs/plans/2026-04-07-postwrite-style-correction*.md`：记录合并后正文 AI 味检测阶段的正文后文风矫正规则。
- `docs/plans/2026-04-08-pointwise-merge*.md`：记录 `novel-write` 早期从整章合并改为细粒度逐段合并的流程调整。
- `docs/plans/2026-04-13-booming*.md`：记录 `booming` 作为手动剧情爆破模式接入工作流的设计与实施。
- `docs/plans/2026-04-14-fuck-it*.md`：记录 `fuck-it` 作为同终点单章加戏模式接入工作流的设计与实施。
- `docs/plans/2026-04-13-novel-write-plotpoint-review*.md`：记录 `novel-write` 改为 20 个剧情点显性核对版、逐点择优并标记来源的流程调整。

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
