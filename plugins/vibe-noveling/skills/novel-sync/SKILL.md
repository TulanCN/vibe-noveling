---
name: novel-sync
description: |
  同步状态。当章节通过一致性检查后，需要更新知识图谱和剧情摘要时触发。

  【必须触发】用户说：同步、sync、更新状态、检查通过后更新、章节完成同步、novel-sync、更新知识图谱、更新past、同步一下、已合并 ch-xxxx.md、我合并完了。

  【关键区分】如果用户要写正文→用novel-write；如果用户要检查一致性→用novel-check；如果用户要更新检查通过后的状态→用本技能。
---

# 状态同步

## 目标

在章节**通过一致性检查后**，同步更新知识图谱、剧情摘要、伏笔状态，确保项目状态与正文进度一致。

## 工作流位置

```
novel-write（创作正文）
      ↓
novel-check（检查一致性）
      ↓
人工审核（用户确认）
      ↓
novel-sync（更新状态）← 你在这里
      ↓
novel-write（下一章）
```

**重要**：必须先完成一致性检查并通过人工审核后再执行同步。

## 使用方式

```
/novel-sync chapter 11    # 同步第11章完成后的状态
/novel-sync               # 同步最新完成的章节
/novel-sync full          # 全面同步（重建索引）
```

## 执行流程

### 第一步：确认同步范围（主 session 交互）

使用 AskUserQuestion 展示同步范围：

```
同步类型：{章节}
目标：{目标章节}

将更新：past.md、future/ 线程与追踪文件、知识图谱索引（可选：新实体）、CLAUDE.md（创作进度）
```

### 第二步：派发 subagent 执行同步

用户确认后，**使用 Agent 工具派发一个 subagent** 完成所有文件更新工作。主 session 不直接操作文件。

**subagent prompt 模板：**

```
你是一个小说状态同步助手。请按以下步骤完成同步工作。

同步范围：{同步类型}，目标：{目标章节}

## 任务清单

### 1. 更新剧情摘要（past.md）
- 优先读取章节文件 `chapters/ch-{chapter_padded}.md`（例如 `chapters/ch-0011.md`）
- 若不存在，再回退读取 `chapters/{chapter}.md`（兼容旧命名）
- 提取核心事件、关键情节、角色变化、伏笔埋设
- 追加摘要到 memory/past.md（格式参考已有条目）
- 摘要控制在 100 字以内

### 2. 更新伏笔状态（future/）

#### 2.1 主线线程总表
- 读取 `memory/future/20-threads.md`
- 检查本章是否让某条长期线程进入新状态（如 `Draft → Active`、`Active → PaidOff`）
- 如有变化，更新线程表中的状态与备注
- 如本章产生新的长期线程，再追加到线程表中

#### 2.2 章节伏笔追踪表（新增）
- 读取 `memory/future/90-sync-tracker.md`
- 读取当前章 outline 文件 `chapters/ch-{chapter_padded}-outline.md`
- 提取「伏笔计划」表格中的所有伏笔
- **转移待回收伏笔**：对于状态为「⏳ 待回收」且**尚未移交**的伏笔：
  - 追加到 `memory/future/90-sync-tracker.md`（如果文件不存在则创建）
  - 在 outline 的伏笔计划中将该伏笔标记为「🔄 已移交追踪表」
- **清理已回收伏笔**：对于状态为「✅ 已回收」的伏笔：
  - 在追踪表中找到对应条目（章节=回收来源章，伏笔描述匹配）
  - **从追踪表中删除**这些条目（伏笔已闭环）
  - 在 outline 的伏笔计划中将该伏笔标记为「✅ 已同步」
- 追踪表始终保持只包含**尚未回收**的伏笔

### 3. 实体变更检测
- 扫描章节内容，识别新实体（地点/物品/势力）
- 如果发现新实体，创建 memory/entities/ 下的对应文件
- 更新现有实体文件的状态变更（境界/关系/位置等）

### 4. 重建知识图谱索引
- 使用 Skill 工具：skill="novel-knowledge", args="rebuild"

### 5. 更新 CLAUDE.md 创作进度
- 统计 chapters/ 目录下 .md 文件数量 → 已完成章节
- 读取最新章节大纲 `chapters/ch-{chapter_padded}-outline.md` → 当前章节标题
- 使用 Edit 工具替换 CLAUDE.md 中 ## 创作进度 下方的内容

## 输出要求

完成后返回一份同步摘要，包含：
- 各文件操作结果
- 发现的新实体/状态变更
- 最终的创作进度信息
```

**Agent 工具调用方式：**

```
使用 Agent 工具：
- subagent_type: "general-purpose"
- mode: "bypassPermissions"
- run_in_background: false（需要拿到结果）
- prompt: {上面的 subagent prompt 模板，填充具体参数}
```

**重要：**
- 所有文件读写、编辑、知识图谱更新都在 subagent 中完成
- 主 session 只负责交互和展示结果
- subagent 完成后，主 session 展示同步报告

### 第三步：展示同步报告（主 session 展示）

subagent 返回结果后，主 session 整理展示：

```markdown
✅ 同步完成报告

**同步时间**：2026-03-13 19:30:00
**同步范围**：第 11 章

## 更新内容

- memory/past.md → 追加（添加第 11 章摘要）
- memory/future/20-threads.md → 更新（长期线程状态变更）
- memory/future/90-sync-tracker.md → 更新（章节伏笔追踪）
- 知识图谱索引 → 重建（实体数量不变）
- CLAUDE.md → 更新（创作进度：已完成 11 章）

## 当前状态

- 已完成章节：11 章
- 总字数：约 33,000 字
- 待回收伏笔：4 个

## 下一步建议

- `/novel-write 12` 创作第 12 章
- `/novel-plan` 规划下一章
```

## 同步时机

必须同步：
- 完成重要章节后
- 发现伏笔需要调整时
- 需要新增重要角色/地点时

可选同步：
- 每完成一个章节
- 每完成一卷

## 关键原则

1. **增量更新** - 只追加新内容，不删除历史
2. **用户确认** - 创建新实体前询问用户
3. **保持简洁** - 摘要控制在 100 字以内
4. **状态一致** - 确保索引与文件一致

## ⚠️ 重要约束：内容边界

### 章节完成后的内容去向

- 剧情摘要 → `past.md`
- **角色成长** → **角色设定文件** + `past.md`
- 伏笔埋设/回收 → `memory/future/20-threads.md` + `memory/future/90-sync-tracker.md`
- 新实体 → `memory/entities/`

### 章节完成后，允许更新角色设定

章节写完后，**可以且应该**更新角色设定文件的以下内容：

- ✅ 境界变化（如"炼气一层 → 炼气四层"）
- ✅ 身份变化（如"外门弟子 → 内门弟子"）
- ✅ 关系变化（如"敌人 → 朋友"）
- ✅ 获得物品/功法（如"获得青木剑"）
- ✅ 认知变化（如"知道修真界存在"）

### 但不能写未来规划

- ❌ 不写"计划在下一章突破"
- ❌ 不写"成长轨迹：Vol-02 达到金丹"（这是规划，写 `memory/future/`）
- ❌ 不写尚未发生的剧情

### 示例

**章节完成后同步更新**：

```
✅ 正确做法（第11章写完后）：
   1. past.md 添加第11章摘要
   2. 苏寒染.md 更新：
      - 境界：炼气三层 → 炼气四层
      - 关系：王师兄（敌人 → 化敌为友）
   3. future/ 更新线程状态与章节追踪

❌ 错误做法：
   - 苏寒染.md 写"计划在第12章突破炼气五层"
```

## 与其他 Skill 的关系

```
novel-write（完成正文）
      ↓
novel-check（检查一致性）← 必须先执行
      ↓
人工审核（用户确认）← 必须先执行
      ↓
novel-sync（更新状态）← 你在这里
      ↓
[继续创作下一章]
```

## 文件结构

```
memory/
├── past.md          # 已完成剧情摘要（本 skill 更新）
├── future/
│   ├── 20-threads.md      # 长期线程状态（本 skill 可更新）
│   └── 90-sync-tracker.md # 章节伏笔追踪（本 skill 更新）
├── _graph.json      # 知识图谱索引（本 skill 重建）
├── _index.json      # 记忆索引（本 skill 重建）
└── entities/        # 实体设定文件（本 skill 可创建）
CLAUDE.md            # 创作进度（本 skill 更新）
```
