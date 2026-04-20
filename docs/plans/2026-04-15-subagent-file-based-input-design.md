# subagent 文件化输入 + 通用规则下沉设计

**日期**：2026-04-15

**背景**

当前 `novel-write` 在调用 writer subagent 时，通过 prompt 模板把所有动态内容（上下文摘要、大纲、20 个剧情点、Opus 约束）内联展开到每次调用中。5 个 writer subagent 各展开一次，合并 prompt 再展开一次剧情点，导致同一份内容重复传递 5-6 次。

同时，通用写作规则（节奏控制、句式规则、视角规则等）写在 prompt 模板中，对所有风格完全相同，每次调用都重复传递。

**问题**

1. Token 浪费：剧情点、上下文、大纲等内容被内联展开 5-6 次
2. 维护负担：通用写作规则在 prompt 模板中，修改时需要同时考虑其对所有风格的影响
3. 上下文缓存已有落盘文件（`上下文.md`），但模板中仍同时内联了一份，冗余

**方案**

### 一、动态内容落盘

- 剧情点细切完成后写入 `剧情点.md`，不再通过 `{writing_units_summary}` 占位符内联
- Opus 约束提炼后写入 `写作约束.md`，不再通过 `{opus_constraints_summary}` 占位符内联
- 大纲和上下文已有对应文件（`大纲.md`、`上下文.md`），subagent 直接读取
- prompt 模板只传文件路径列表，不展开内容

### 二、通用写作规则下沉 agent 文件

- 将节奏控制、句式规则、视角规则、输出格式、结构边界、自检、冗余清理等通用规则从 prompt 模板移出
- 追加到 5 个 writer agent 的 `.md` 定义文件中（`## 通用写作规则` 段落）
- 各 agent 文件自包含风格人格 + 通用规则，prompt 模板不再夹带静态规则

**改动文件**

- `plugins/vibe-noveling/skills/novel-write/SKILL.md`：落盘指令 + prompt 模板瘦身
- `plugins/vibe-noveling/agents/writer-hemingway.md`：追加通用写作规则
- `plugins/vibe-noveling/agents/writer-maibaoxiaolangjun.md`：追加通用写作规则
- `plugins/vibe-noveling/agents/writer-zhouzi.md`：追加通用写作规则
- `plugins/vibe-noveling/agents/writer-dazhongma.md`：追加通用写作规则
- `plugins/vibe-noveling/agents/writer-banter.md`：追加通用写作规则

**效果**

- 每个 writer subagent 的 prompt 体积大幅缩小（从 ~4000 token 降至 ~200 token）
- 通用规则与风格规则共存于 agent 文件，维护更集中
- 剧情点只存一份文件，所有 subagent 和合并 agent 按需读取
