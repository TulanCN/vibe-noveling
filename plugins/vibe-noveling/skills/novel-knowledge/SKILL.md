---
name: novel-knowledge
description: 当其他 skill 或 agent 需要搜索、更新或重建小说知识图谱时使用。
when_to_use: |
  仅供其他 skill 或 agent 调用，用于实体搜索、关系查询、标签查询、索引重建等底层数据访问。
  高级语义理解和上下文拼装交给 `context-collector`。
user-invocable: false
invokes: {SKILL_DIR}/scripts/knowledge_graph.py
---

# 知识图谱工具

## 调用约定

- 仅供其他 skill 或 agent 调用，不直接面向用户入口
- 本工具负责数据访问，不负责高层语义判断和上下文拼装

## 用途

被其他 skill 调用，搜索和更新小说设定知识库。

## 设计原则

**本工具只负责数据访问**，不包含高级语义理解逻辑。

- ✅ 搜索实体
- ✅ 创建/更新实体
- ✅ 查询关系
- ✅ 按标签查询
- ✅ 从 md 文件重建知识图谱和索引

❌ **不包含**：生成上下文、解析 Event 等高级逻辑（这些由 context-collector agent 完成）

## 推荐工作流

### 创建或编辑实体

**直接编辑 md 文件**，然后运行 `rebuild` 同步知识图谱：

```
1. 编辑 memory/entities/<type>/<name>.md（写好 YAML frontmatter）
2. 运行 rebuild → 自动生成 _graph.json 和 _index.json
```

⚠️ **不要手动编辑 `_graph.json` 或 `_index.json`**，它们应该由 `rebuild` 从 md 文件自动生成。

### 何时运行 rebuild

- 创建新的实体文件后
- 编辑实体的 frontmatter（id、name、tags、relations）后
- 批量修改多个实体后
- `novel-sync` 完成一致性检查后

### 依赖

- **PyYAML**：用于解析嵌套的 YAML frontmatter（relations 等字段）。如果未安装，嵌套 dict 会被错误解析为字符串列表。安装命令：`uv pip install pyyaml`

## 调用方式

使用 Bash 工具执行（相对于项目根目录）：

```bash
python {SKILL_DIR}/scripts/knowledge_graph.py <command> [args]
```

## 支持的命令

### search - 搜索设定

```bash
python {SKILL_DIR}/scripts/knowledge_graph.py search <query>
```

在 memory/ 目录中搜索相关设定，返回匹配的角色、地点、物品等信息。

选项：
- `--type, -t`: 限制搜索类型（character/location/item/faction/concept）
- `--limit, -l`: 返回结果数量（默认 10）
- `--json, -j`: JSON 格式输出

### update - 创建实体文件

```bash
python {SKILL_DIR}/scripts/knowledge_graph.py update <type> <name>
```

创建指定类型的实体文件（如果文件不存在），使用模板生成。不会覆盖已有文件。

**注意**：此命令只创建空模板文件。编辑完成后需要运行 `rebuild` 同步知识图谱。

选项：
- `--json, -j`: JSON 格式输出

### relations - 查询实体关系

```bash
python {SKILL_DIR}/scripts/knowledge_graph.py relations <entity_id>
```

查询指定实体的所有关系（出向和入向）。返回双向关系：
- 出向：该实体指向的其他实体
- 入向：指向该实体的其他实体

### tags - 按标签查询

```bash
python {SKILL_DIR}/scripts/knowledge_graph.py tags <tag>
```

按标签搜索实体。

### rebuild - 从 md 文件重建知识图谱（核心命令）

```bash
python {SKILL_DIR}/scripts/knowledge_graph.py rebuild
```

**扫描所有 `memory/entities/` 下的 md 文件**，从 YAML frontmatter 中提取：
- 实体信息（id、name、type、tags、aliases）
- 关系信息（relations 列表）

然后**重新生成**：
1. `memory/_graph.json` — 知识图谱（实体 + 关系）
2. `memory/_index.json` — 索引（名称索引、标签索引、类型索引）

这是保持知识图谱与实体文件同步的**推荐方式**。

## 实体文件 Frontmatter 格式

每个实体文件的 YAML frontmatter 应包含以下字段：

```yaml
---
id: <唯一标识符，中文，如 苏寒染>
name: <显示名称>
type: <类型：character/location/item/faction/concept>
tags:
  - <标签1>
  - <标签2>
relations:
  - target: <目标实体id>
    relation: <关系类型>
    description: <关系描述>
---
```

### 关系字段说明

- `target`：指向的目标实体 id（必须存在）
- `relation`：关系类型（自由文本，如 `father_of`、`located_in`、`allied_with`）
- `description`：关系描述（自然语言说明）

关系是**双向的**：A → B 的关系会自动生成 B → A 的入向关系。

## 知识库结构

```
memory/
├── entities/
│   ├── characters/    # 角色设定（protagonist/supporting）
│   ├── locations/     # 地点设定（都城、基地、传送门等）
│   ├── factions/      # 势力/门派设定
│   ├── items/         # 物品/法宝设定
│   └── concepts/      # 概念设定（修炼体系等）
├── _graph.json        # 知识图谱（自动生成，勿手动编辑）
├── _index.json        # 索引文件（自动生成，勿手动编辑）
├── past.md            # 已完成剧情
├── future/            # 未来规划目录
└── worldbuilding.md    # 世界观总览
```

## 输出格式

返回 JSON 格式：

```json
{
  "success": true,
  "results": [...]
}
```
