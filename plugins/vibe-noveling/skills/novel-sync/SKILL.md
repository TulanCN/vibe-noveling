---
name: novel-sync
description: 章节完成后回写知识图谱与剧情摘要。
when_to_use: |
  适用于"同步""sync""更新状态""更新知识图谱""更新past"等请求。
  仅在正文通过返修确认后执行；正文创作用 novel-write。
---
# 状态同步

章节写完、检查过、确认过，把状态落回项目记忆。

工作流位置：novel-write → novel-revise → 人工确认 → **novel-sync** → 下一章

## 执行流程

### 1. 确认同步范围（主 session）

用 AskUserQuestion 确认目标章节和将更新的文件（past.md、future/线程与追踪、知识图谱索引、CLAUDE.md 创作进度）。

### 2. 派发 subagent 执行

用户确认后，派发 subagent 完成以下工作。subagent prompt：

```
你是小说状态同步助手。同步第 {N} 章。

### 任务清单

1. **更新剧情摘要**：读 `chapters/vol-{v}/ch-{c}/正文.md`，提取核心事件和关键变化，追加 ≤100 字摘要到 memory/past.md

2. **更新伏笔状态**：
   - 读 `20-threads.md`，本章让某条线程进入新状态（Draft→Active→PaidOff）则更新
   - 读 `90-sync-tracker.md`，从大纲伏笔计划中：
     - 待回收未移交的 → 追加到追踪表，大纲中标记"已移交追踪表"
     - 已回收的 → 从追踪表删除，大纲中标记"已同步"

3. **实体变更检测**：扫描章节找新实体（地点/物品/势力），发现则创建 entity 文件。更新已有实体的状态变更（境界/关系/位置等）

4. **重建知识图谱**：`skill="novel-knowledge", args="rebuild"`

5. **更新 CLAUDE.md 创作进度**：统计已完成章节数，读取最新章节大纲的标题（仍为"待定"则不写标题），替换创作进度 section
```

### 3. 展示同步报告

subagent 返回后，主 session 展示摘要：更新了哪些文件、发现的新实体/状态变更、当前进度。

## 约束

- 剧情摘要 → past.md（已完成），角色成长 → 角色设定文件 + past.md，伏笔 → threads + sync-tracker，新实体 → entities/
- ✅ 允许更新角色设定：境界变化、身份变化、关系变化、获得物品/功法、认知变化
- ❌ 不能在设定文件中写未来规划（"计划下一章突破"等），那属于 future/

## 禁止

- 跳过人工确认直接同步
- 在设定文件中写未来规划
- 删除 past.md 历史内容
