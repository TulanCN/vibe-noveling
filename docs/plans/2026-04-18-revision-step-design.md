# 返修环节设计

**日期**: 2026-04-18

## 背景

正文写作交付后，需要一个强制的人机协作返修环节：用户在正文中标记问题点，AI 按标记规则处理。

## 决策

### 流程位置

在 Step 10（交付）和原 Step 11（确认同步）之间插入 **Step 11：返修**，原确认同步顺延为 Step 12。返修是强制环节，用户必须经过返修（或确认无需返修）才能进入同步。

### 实现方式

返修由主 session 直接执行，读取 `references/revision-rules.md` 作为唯一规则来源。不创建独立 agent。

理由：
- 返修规则较多（四种标记 + 各自进阶操作），但主 session 已有完整的正文上下文，内联执行更连贯
- 减少不必要的 agent 派发开销
- 与 AI 味检测保持一致架构（两者都由主 session 直接执行）

### 标记约定

| 标记 | 名称 | 操作 |
|---|---|---|
| `**加粗**` | 润滑 | 补过渡、让句子顺滑 |
| `*斜体*` | 合并 | 多短句合并为长句 |
| `~~删除线~~` | 清理重写 | 删掉标记内容，重写所在句子 |
| `` `行内代码` `` | 扩写 | 一句话展开为多句 |

### 返修后不做 AI 味复查

返修只涉及局部修改，不做完整的 28 项 AI 味复查。返修后直接交付让用户确认。

### 循环返修

用户可多次标记 → 返修，直到满意后才确认同步。

## 新增文件

- `plugins/vibe-noveling/skills/novel-write/references/revision-rules.md` — 返修规则参考文件

## 修改文件

- `plugins/vibe-noveling/skills/novel-write/SKILL.md` — 流程图、Step 8（AI 味检测改为内联）、Step 11（返修改为内联）、核心特性、关键原则、完成确认模板
- `README.md` — 技能表、Agents 表、工作流图、正文写作说明

## 删除文件

- `plugins/vibe-noveling/agents/revision-handler.md` — 返修不再使用独立 agent
- `plugins/vibe-noveling/agents/ai-smell-guard.md` — AI 味检测不再使用独立 agent
