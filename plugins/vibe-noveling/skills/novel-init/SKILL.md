---
name: novel-init
description: 初始化一个新的小说项目，建立目录结构和基础创作契约。
when_to_use: |
  适用于"初始化小说""新建小说项目""开始写小说""创建小说"等请求。
  已有项目进入后续创作阶段改用其他 skills。
---
# 小说项目初始化

## 步骤

### 1. 确认项目类型

问用户什么类型（修真仙侠/玄幻奇幻/都市现代/科幻未来/其他）。

### 2. 确认书名

### 3. 创建目录结构

```
project/
├── CLAUDE.md
├── memory/
│   ├── _graph.json / _index.json           ← 知识图谱，由 rebuild 自动生成
│   ├── entities/{characters,locations,factions,items,concepts}/
│   ├── worldbuilding.md                    ← 世界观总览
│   ├── world-design-progress.md            ← 世界观构建进度（novel-discuss 维护）
│   ├── past.md                             ← 已完成剧情
│   ├── future/{00-index,10-book,20-threads,30-volumes,40-events,90-sync-tracker}.md
│   └── setting-todo.md                     ← 设定待办
├── chapters/
├── templates/
└── .snapshots/
```

### 4. 初始化核心文件

创建最小化初始文件：
- `_graph.json`：`{"version":"1.0","entities":{},"relations":[]}`
- `_index.json`：`{"version":"1.0","name_index":{},"tag_index":{},"type_index":{...}}`
- `entities/README.md`：实体文件格式规范
- `past.md`：空初始状态
- `future/00-index.md`：说明各文件职责和读取顺序
- `world-design-progress.md`：8 个模块的构建清单（世界本质/能力体系/社会形态/势力格局/地理环境/历史背景/经济物品/核心矛盾），初始全部待设计
- `worldbuilding.md`：空世界观总览
- `setting-todo.md`：空待办清单

### 5. 创建模板文件

`templates/chapter-template.md`、`templates/character-template.md`

### 6. 创建 CLAUDE.md

CLAUDE.md 必须包含以下 section，具体内容由用户回答决定，不要填入预设值：

```markdown
# CLAUDE.md

## 项目概述
[书名]、[类型]

## 小说宪法
> 本小说创作的最高准则。剧情设计、详略讨论、正文合并均须服从。
> 讨论中可随时修正，修正后立即更新本节。

### 灵魂
[小说的基调，一句话]

### 爽感公式
- 来源：[实力碾压/身份反转/角色成长/差别待遇 等]
- 递进节奏：[爆发型/渐进型/过山车型]

### 叙事纹理
- 节奏倾向：
- 文字质感：
- 信息密度：

### 主角光谱
- 主角吸引力来源：
- 主角与读者的关系：[仰望感/代入感/共情感]

### 作者人格
- 叙事姿态：
- 价值底色：
- 情感温度：
- 幽默方式：
- 信息习惯：

### 绝对红线
[不可逾越的规则，每条一行]

### 风格锚点
[参考作品或风格，每条一行]

## 创作进度
- 当前卷：Vol-01
- 当前章节：第 1 章（待规划）

## 目录结构说明
[简要说明 memory/ chapters/ templates/ .snapshots/ 的用途]

## 可用 Skills
- /novel-discuss — 讨论创意、角色、世界观
- /novel-bookplan — 规划全书与分卷节奏
- /novel-plan — 规划下一章
- /novel-write — 章节创作
- /novel-sync — 同步知识图谱
- /novel-progress — 查看进度
- /novel-snapshot — 创建/恢复快照
```

宪法中的每个条目都需要和用户确认后填入，不要编造默认值。如果用户不想某项现在定，写"待定"。

### 7. 完成提示

```text
✅ 项目初始化完成

📁 目录：memory/ chapters/ templates/ .snapshots/
📄 CLAUDE.md 已写入项目信息

🚀 推荐流程：
   1. /novel-discuss 构建世界观 + 设计角色
   2. /novel-bookplan 规划全书大纲
   3. /novel-plan 规划第一章
   4. /novel-write 开始创作
```
