# 返修环节设计

**日期**: 2026-04-18

## 背景

正文写作交付后，需要一个强制的人机协作返修环节：用户在正文中标记问题点，AI 按标记规则处理。

## 决策

### 流程位置

在 Step 10（交付）和原 Step 11（确认同步）之间插入 **Step 11：返修**，原确认同步顺延为 Step 12。返修是强制环节，用户必须经过返修（或确认无需返修）才能进入同步。

### 实现方式

创建独立的 `revision-handler` agent 处理返修，不内联到主 skill。理由：
- 返修规则较多（四种标记 + 各自进阶操作），独立 agent 职责清晰
- 与 `ai-smell-guard` 的架构模式一致

### 标记约定

| 标记 | 名称 | 操作 |
|---|---|---|
| `**加粗**` | 润滑 | 补过渡、让句子顺滑 |
| `*斜体*` | 合并 | 多短句合并为长句 |
| `~~删除线~~` | 清理重写 | 删掉标记内容，重写所在句子 |
| `` `行内代码` `` | 扩写 | 一句话展开为多句 |

### 返修后不做 AI 味复查

返修只涉及局部修改，不做完整的 27 项 AI 味复查。返修后直接交付让用户确认。

### 循环返修

用户可多次标记 → 返修，直到满意后才确认同步。

## 新增文件

- `plugins/vibe-noveling/skills/novel-write/references/revision-rules.md` — 返修规则参考文件
- `plugins/vibe-noveling/agents/revision-handler.md` — 返修处理 agent

## 修改文件

- `plugins/vibe-noveling/skills/novel-write/SKILL.md` — 流程图、Step 10A、核心特性、关键原则、完成确认模板
- `README.md` — 技能表、Agents 表、工作流图、正文写作说明、快速开始示例
