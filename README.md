# Vibe Noveling

**用 Claude Code 写小说的专业工作流工具包。**

一套完整的中文网络小说创作工作流，基于 Claude Code 的自定义 Skill + Agent 体系构建。从项目初始化到章节发布，覆盖小说创作的全流程。

## 特性

- **11 个专业技能 + 2 个内置子 Agent** — 覆盖初始化、讨论、规划、写作、检查、同步全流程
- **知识图谱驱动** — 自动管理角色、地点、物品、势力等设定，支持搜索和关系追踪
- **Save the Cat 剧情架构** — 内置 15 节拍故事母型，支持全书/分卷/单章三层规划
- **默认全风格逐个启动写作 Agent + 自动合并** — 基于精简剧情纲要在正文阶段内部切分，按风格顺序拉起 4 个写作 Agent，并按内部写作单元逐个合并，避免把写作和合并都堆成一次性大请求
- **AI 味检测 + 反常规检查** — 内置文本质检系统，消除 AI 写作痕迹
- **命名生成器** — 支持角色、功法、门派、物品等 8 类命名，带稀有度体系
- **进度可视化** — 自动生成字数统计饼图
- **快照管理** — 安全的版本备份与回滚
- **文档与回归测试同步维护** — `docs/plans/` 记录流程设计演进，`tests/` 用静态断言守住提示词契约

## 技能一览

| 技能 | 触发词 | 说明 |
|------|--------|------|
| `/novel-init` | 初始化、新建小说 | 创建完整的项目结构和目录 |
| `/novel-discuss` | 讨论、设计角色、世界观 | 苏格拉底式对话，支持世界观/角色/物品/势力/体系设计 |
| `/novel-bookplan` | 全书大纲、卷结构 | Save the Cat 15 节拍全书架构规划 |
| `/novel-plan` | 规划下一章 | 单章第三人称精简剧情纲要 + Opus 正文测试 |
| `/novel-write` | 写章节、创作正文 | 默认全风格逐个启动写作 Agent，并按内部写作单元逐个合并最终稿 |
| `/novel-sync` | 同步、更新状态 | 章节完成后更新知识图谱 |
| `/novel-master` | （自动集成） | 风格控制器：AI 味检测 + 反常规检查 |
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
/novel-plan          →  逐章精简剧情纲要
    ↓
/novel-write         →  正文阶段内部切分 + 默认全风格逐个启动写作 Agent + 按内部写作单元逐个合并 + 内置一致性检查
    ↓
生成最终稿          →  自动合并生成最终稿，并保留各风格中间稿供回看
    ↓
/novel-sync          →  同步更新知识图谱
    ↓
/novel-snapshot      →  创建版本快照（随时）
/novel-progress      →  查看创作进度（随时）
```

## 安装

### 方式一：Claude Plugin Marketplace（推荐）

在 Claude Code 中直接安装：

```bash
/plugin marketplace add TulanCN/vibe-noveling
/plugin install vibe-noveling@vibe-noveling
```

安装后 11 个技能和 2 个内置子 Agent 自动可用，支持自动更新。

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
│   ├── ch-XXXX-outline.md     # 精简剧情纲要
│   ├── ch-XXXX.md             # 章节正文
│   └── ch-XXXX-context.md     # 章节上下文
├── .snapshots/                # 版本快照
└── templates/                 # 模板文件
```

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
│           │   └── tools/
│           ├── novel-sync/
│           ├── novel-master/
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
rg -n "第三人称精简剧情纲要|正文阶段内部切分|按内部写作单元逐个合并|自动合并生成最终稿" \
  README.md \
  plugins/vibe-noveling/skills/novel-plan/SKILL.md \
  plugins/vibe-noveling/skills/novel-plan/references/output.md \
  plugins/vibe-noveling/skills/novel-write/SKILL.md
```

## 设计文档

- `docs/plans/2026-04-07-outline-format-redesign*.md`：记录 `novel-plan` 从旧版章节大纲格式转为第三人称精简剧情纲要的设计与实施。
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
