# Vibe Noveling

**用 Claude Code 写小说的专业工作流工具包。**

一套完整的中文网络小说创作技能（Skills），基于 Claude Code 的自定义 Skill 体系构建。从项目初始化到章节发布，覆盖小说创作的全流程。

## 特性

- **13 个专业技能** — 覆盖初始化、讨论、规划、写作、同步全流程
- **知识图谱驱动** — 自动管理角色、地点、物品、势力等设定，支持搜索和关系追踪
- **Save the Cat 剧情架构** — 内置 15 节拍故事母型，支持全书/分卷/单章三层规划
- **多风格并行写作** — 同一剧情点生成多个风格版本供选择
- **AI 味检测 + 反常规检查** — 内置文本质检系统，消除 AI 写作痕迹
- **命名生成器** — 支持角色、功法、门派、物品等 8 类命名，带稀有度体系
- **进度可视化** — 自动生成字数统计饼图
- **快照管理** — 安全的版本备份与回滚

## 技能一览

| 技能 | 触发词 | 说明 |
|------|--------|------|
| `/novel-init` | 初始化、新建小说 | 创建完整的项目结构和目录 |
| `/novel-discuss` | 讨论、设计角色、世界观 | 苏格拉底式对话，支持世界观/角色/物品/势力/体系设计 |
| `/novel-bookplan` | 全书大纲、卷结构 | Save the Cat 15 节拍全书架构规划 |
| `/novel-plan` | 规划下一章 | 单章场景化大纲 + Opus 正文测试 |
| `/novel-write` | 写章节、创作正文 | 多风格并行章节创作 |
| `/novel-sync` | 同步、更新状态 | 章节完成后更新知识图谱 |
| `/novel-master` | （自动集成） | 风格控制器：AI 味检测 + 反常规检查 |
| `/novel-knowledge` | （内部调用） | 知识图谱：搜索/创建/更新实体 |
| `/novel-name` | 命名、取名 | 8 类命名生成器（Python 脚本） |
| `/novel-snapshot` | 快照、备份 | 项目版本快照管理 |
| `/novel-progress` | 进度、字数 | 创作进度可视化（HTML 饼图） |

## 工作流

```
/novel-init          →  初始化项目
    ↓
/novel-discuss       →  设计世界观、角色、设定
    ↓
/novel-bookplan      →  全书架构与卷规划（可选）
    ↓
/novel-plan          →  逐章场景大纲
    ↓
/novel-write         →  多风格并行创作正文
    ↓
用户审阅合并        →  手动挑选最佳版本
    ↓
/novel-sync          →  同步更新知识图谱
    ↓
/novel-snapshot      →  创建版本快照（随时）
/novel-progress      →  查看创作进度（随时）
```

## 安装

### 方式一：Plugin Marketplace（推荐）

```bash
# 添加 marketplace 并安装
/plugin marketplace add TulanCN/vibe-noveling
/plugin install vibe-noveling@vibe-noveling
```

### 方式二：手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/TulanCN/vibe-noveling.git

# 2. 复制技能到你的 Claude Code 项目
cp -r vibe-noveling/plugins/vibe-noveling/* 你的项目/.claude/skills/
```

### 方式三：符号链接（推荐开发时使用）

```bash
# 在你的项目目录下创建符号链接
ln -s /path/to/vibe-noveling/plugins/vibe-noveling/novel-init .claude/skills/novel-init
ln -s /path/to/vibe-noveling/plugins/vibe-noveling/novel-discuss .claude/skills/novel-discuss
# ... 对每个 skill 重复
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
│   ├── ch-XXXX-outline.md     # 场景化大纲
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

# 5. 查看进度
/novel-progress
```

## 仓库结构

```
vibe-noveling/
├── .claude-plugin/
│   └── marketplace.json       # Plugin marketplace 清单
├── plugins/
│   └── vibe-noveling/          # 插件根目录
│       ├── novel-init/
│       ├── novel-discuss/
│       │   └── references/
│       ├── novel-bookplan/
│       │   └── references/
│       ├── novel-plan/
│       │   └── references/
│       ├── novel-write/
│       │   └── tools/
│       ├── novel-sync/
│       ├── novel-master/
│       ├── novel-knowledge/
│       │   └── scripts/
│       ├── novel-name/
│       │   ├── data/
│       │   └── tools/
│       ├── novel-snapshot/
│       │   └── scripts/
│       └── novel-progress/
│           └── scripts/
├── README.md
└── LICENSE
```

Skill 文件中使用 `{SKILL_DIR}` 作为占位符，表示该 Skill 的安装目录。实际使用时会解析为：

```
.claude/skills/{skill-name}/
```

例如 `{SKILL_DIR}/references/world-design.md` 实际对应 `.claude/skills/novel-discuss/references/world-design.md`。

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
