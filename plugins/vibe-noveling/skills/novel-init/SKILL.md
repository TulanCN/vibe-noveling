---
name: novel-init
description: |
  初始化新的小说创作项目。当用户需要开始新小说、设置创作环境、建立项目结构时触发。

  【必须触发】用户说：初始化小说、新建小说项目、开始写小说、创建小说、novel-init、新建一个修真小说项目、帮我搭建小说项目、开始一个新的故事。

  【关键区分】如果用户已经有项目在进行→用其他skills；如果用户要创建全新的项目结构→用本技能。

  支持多种小说类型：修真/仙侠、玄幻、都市、科幻、历史等，创建完整的目录结构和初始配置文件。
---
# 小说项目初始化

## 目标

为中国网络小说创作建立完整的项目结构和工作流基础，确保后续创作有良好的组织。

## 执行流程

### 第一步：确认项目类型

先询问用户要创作什么类型的小说：

```
📱 欢迎使用小说创作工作流！

请选择你要创作的小说类型：
A. 修真/仙侠（修炼升级、门派争斗、逆天改命）
B. 玄幻/奇幻（异世界、魔法体系、种族战争）
C. 都市/现代（都市异能、商战、重生）
D. 科幻/未来（星际、赛博朋克、末世）
E. 其他类型（请描述）

请输入选择（A/B/C/D/E）：
```

### 第二步：询问小说标题

```
📖 你的小说叫什么名字？
（例如：《万古仙尊》）
```

### 第三步：创建目录结构

```
project/
├── CLAUDE.md              # 项目说明（包含项目基本信息）
├── memory/                  # 长期记忆
│   ├── _graph.json         # 知识图谱（实体+关系索引）
│   ├── _index.json         # 记忆索引（名称/标签/类型索引）
│   ├── entities/           # 实体文件目录
│   │   ├── README.md       # 实体格式规范
│   │   ├── characters/     # 角色（主角/配角/反派）
│   │   ├── locations/      # 地点
│   │   ├── factions/       # 势力门派
│   │   ├── items/          # 物品法宝
│   │   └── concepts/       # 概念（修炼体系、物品体系等）
│   ├── worldbuilding.md    # 世界观总览（一份综合文档）
│   ├── world-design-progress.md # 世界观构建进度（引导式设计用）
│   ├── past.md             # 已完成剧情总结
│   ├── future/             # 未来规划目录
│   │   ├── 00-index.md
│   │   ├── 10-book.md
│   │   ├── 20-threads.md
│   │   ├── 30-volumes/
│   │   ├── 40-arcs/
│   │   └── 90-sync-tracker.md
│   └── setting-todo.md     # 设定待办清单
├── chapters/               # 章节目录（正文+大纲）
├── templates/               # 模板文件
└── .snapshots/              # 版本快照
```

**设计原则：**

- 具体设定（角色、地点、势力、物品、体系）→ 放入 `entities/` 知识图谱
- 世界观总览 → 一份 `worldbuilding.md` 综合文档
- 关系和索引 → `_graph.json` + `_index.json`
- 剧情时间线 → `past.md`（已完成）+ `future/`（待发生规划）

### 第四步：初始化核心文件

创建 `memory/_graph.json`：

```json
{
  "version": "1.0",
  "entities": {},
  "relations": []
}
```

创建 `memory/_index.json`：

```json
{
  "version": "1.0",
  "name_index": {},
  "tag_index": {},
  "type_index": {
    "character": [],
    "location": [],
    "faction": [],
    "item": [],
    "concept": []
  }
}
```

创建 `memory/entities/README.md`（实体格式规范，内容见附录）

创建 `memory/past.md`：

```markdown
# 已完成剧情

记录当前写作进度之前已经发生的剧情摘要。

> 使用说明：按时间顺序排列，边写边更新，保持最新状态。

## 剧情概要

（项目刚开始，暂无已完成的剧情）

## 已揭示伏笔

（暂无）

## 角色状态变化

（暂无）
```

创建 `memory/future/` 目录，并初始化以下文件：

- `memory/future/00-index.md`
- `memory/future/10-book.md`
- `memory/future/20-threads.md`
- `memory/future/30-volumes/`
- `memory/future/40-arcs/`
- `memory/future/90-sync-tracker.md`
- `memory/setting-todo.md`

最小初始化要求：

- `00-index.md`：说明 future/ 的读取顺序和各文件职责
- `10-book.md`：预留终极目标、故事母型、全书节奏蓝图
- `20-threads.md`：预留长期线程总表
- `90-sync-tracker.md`：预留章节伏笔追踪表
- `setting-todo.md`：记录待补完设定

**时间线管理原则：**

- `past.md` - 已完成（回顾用，随写作进度更新）
- `future/` - 未发生（规划用，按全书 / 分卷 / arc / 追踪分层维护）
- 两者相互对应，形成完整的剧情时间线

创建 `memory/world-design-progress.md`（世界观构建进度追踪，供 novel-discuss 引导模式使用）：

```markdown
# 世界观构建进度

> 由 novel-init 创建，novel-discuss 维护。每次讨论一个模块并标记完成。

## 构建清单

- [ ] **世界本质** — 定义这个世界是什么
- [ ] **能力体系** — 力量/魔法/技术规则 [可选：纯现实题材可跳过]
- [ ] **社会形态** — 社会组织与文化
- [ ] **势力格局** — 主要组织与关系
- [ ] **地理环境** — 物理世界与关键地点
- [ ] **历史背景** — 塑造现状的过去
- [ ] **经济与物品** — 资源、贸易、技术
- [ ] **核心矛盾** — 驱动故事的张力

---

## 设计记录

### 世界本质
**状态**：待设计
**关键决定**：

### 能力体系
**状态**：待设计
**关键决定**：

### 社会形态
**状态**：待设计
**关键决定**：

### 势力格局
**状态**：待设计
**关键决定**：

### 地理环境
**状态**：待设计
**关键决定**：

### 历史背景
**状态**：待设计
**关键决定**：

### 经济与物品
**状态**：待设计
**关键决定**：

### 核心矛盾
**状态**：待设计
**关键决定**：
```

**世界观构建进度说明：**

- `world-design-progress.md` - 世界观各模块的设计进度（novel-discuss 引导模式使用）
- 每完成一个模块的讨论，标记 `[x]` 并填写关键决定
- 详细设定写入对应的 entity 文件，此文件仅作进度索引

### 第五步：创建模板文件

自动创建基础模板：

- `templates/chapter-template.md`
- `templates/character-template.md`

### 第六步：创建项目说明文件

创建 `CLAUDE.md` 文件，帮助后续创作时快速了解项目结构：

```markdown
# CLAUDE.md

本文件为 Claude Code 提供项目结构说明，避免每次创作时重复探索。

## 项目概述
这是一个中国网络小说创作工作流工具，使用 Claude Code 的 skills 和 agents 模块化管理小说创作过程。

## 目录结构说明

### memory/ - 长期记忆（设定）
- `_graph.json` - 知识图谱（实体+关系索引）
- `_index.json` - 记忆索引（名称/标签/类型索引）
- `entities/` - 实体文件目录
  - `characters/` - 角色设定（主角/配角/反派）
  - `locations/` - 地点设定
  - `factions/` - 势力门派设定
  - `items/` - 物品法宝设定
  - `concepts/` - 概念设定（修炼体系、物品体系等）
- `worldbuilding.md` - 世界观总览（一份综合文档）
- `world-design-progress.md` - 世界观构建进度（引导式设计用）
- `past.md` - 已完成剧情总结（回顾用，随写作进度更新）
- `future/` - 未来规划目录（规划用，按全书 / 分卷 / arc 分层维护）
- `setting-todo.md` - 设定待办清单（仅记录待补完设定）

### chapters/ - 章节目录
按分卷/分章目录存放章节产物，例如 `chapters/vol-01/ch-0001/正文.md`、`chapters/vol-01/ch-0001/大纲.md`

### templates/ - 模板文件
- `chapter-template.md` - 章节正文模板
- `character-template.md` - 角色设定模板

### .snapshots/ - 版本快照
版本备份目录，用于回滚和恢复。

## 可用 Skills

- `/novel-init` — 初始化新项目
- `/novel-snapshot` — 创建快照
- `/novel-rollback` — 回滚到历史版本
- `/novel-discuss` — 设计角色、构建世界观、讨论剧情走向
- `/novel-plan` — 规划下一章剧情
- `/novel-write` — 章节创作

## 可用 Agents

- consistency-guard — 一致性守护者
- context-collector — 上下文收集器

## Python 工具（通过 Skill 调用）

```
# 生成名称（使用 novel-name skill）
使用 Skill 工具：skill="novel-name", args="character --type 修士 --count 5"

# 搜索设定（使用 novel-knowledge skill）
使用 Skill 工具：skill="novel-knowledge", args="search <query>"

# 更新设定（使用 novel-knowledge skill）
使用 Skill 工具：skill="novel-knowledge", args="update <type> <name> --content <content>"
```

```

## 输出确认

初始化完成后，显示：

```
✅ 小说项目初始化完成！

📚 项目信息：
   标题：《xxx》
   类型：修真小说

📁 已创建目录结构：
   memory/      - 设定文件
   chapters/    - 分卷/分章章节目录（如 chapters/vol-01/ch-0001/正文.md）
   templates/   - 模板文件
   .snapshots/  - 版本管理

🚀 推荐工作流：
   1. /novel-discuss 构建世界观（引导式，按模块逐步设计）
   2. /novel-discuss 设计角色
   3. /novel-bookplan  规划全书大纲（卷结构+伏笔）
   4. /novel-plan      规划下一章剧情
   5. /novel-write     开始创作第一章

💡 小贴士：
   - 项目信息已写入 CLAUDE.md，每次对话自动加载
   - 使用 /novel-snapshot 定期保存进度
```

## 验收清单

- [ ] 目录结构完整
- [ ] CLAUDE.md 包含项目信息
- [ ] 模板文件已创建
- [ ] 下一步工作流清晰
