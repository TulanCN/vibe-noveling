# 章节级合并配置 + 并发数配置

日期：2026-04-16

## 背景

`novel-write` 第六步的合并逻辑写死在 SKILL.md 中，包括 5 条风格优先规则、15 条合并约束和最终稿偏好段。用户希望按章节指定合并逻辑（如打斗章偏好肘子、文戏章偏好大仲马）。此外，writer subagent 的并发数也写死为 1，用户希望能选择并发数。

## 设计决策

### 1. 合并配置外部化

- 将合并规则从 SKILL.md 内联抽出为 `references/merge-rules.md`
- SKILL.md 只保留 6 条不可覆盖的硬约束（结构性规则），其余通过引用读取
- 合并 prompt 模板中的风格偏好类规则全部引导到 references 文件

### 2. 章节级配置

- 新增"第二步 C：合并配置"，在剧情点细切后、正式写作前执行
- 如果 `合并配置.md` 不存在，主动询问用户合并偏好，给出基于大纲的建议
- 用户确认后生成 `合并配置.md`；跳过则使用默认规则
- Override 优先级：章节配置 > 默认规则 > 不可覆盖硬约束

### 3. 并发数配置

- 在"第三步"新增"3.1 并发数确认"
- 向用户提供 1/2/3/5 并发选项，默认 1
- 第四步根据并发数分批调度 writer subagent

## 改动文件

| 文件 | 操作 |
|------|------|
| `plugins/vibe-noveling/skills/novel-write/references/merge-rules.md` | 新增 |
| `plugins/vibe-noveling/skills/novel-write/SKILL.md` | 修改 |
| `docs/plans/2026-04-16-chapter-merge-config-design.md` | 新增（本文件） |
