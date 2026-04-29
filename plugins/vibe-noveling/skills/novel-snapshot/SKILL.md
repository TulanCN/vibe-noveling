---
name: novel-snapshot
description: 为当前小说项目创建快照、备份状态或恢复历史版本。
when_to_use: |
  适用于"创建快照""保存进度""备份项目""打版本""存个档""恢复快照""回滚"等请求。
---
# 小说项目快照管理

使用 Python 脚本 `scripts/snapshot.py` 管理快照。

## 操作

### 创建快照

```bash
python {SKILL_DIR}/scripts/snapshot.py create "描述"
```

复制 memory/、chapters/、events/ 到 `.snapshots/{日期-描述}/`。

### 恢复快照

```bash
python {SKILL_DIR}/scripts/snapshot.py list           # 列出可用快照
python {SKILL_DIR}/scripts/snapshot.py restore "快照名" # 恢复（自动备份当前状态）
```

### 列出快照

```bash
python {SKILL_DIR}/scripts/snapshot.py list
```

## 用户确认

- 创建前：确认描述和将复制的目录
- 恢复前：确认目标快照，⚠️ 提醒当前状态会被自动备份

## 建议时机

- 开始写新章节前、大幅修改大纲后、修改核心设定前、完成重要剧情后（必需）
- 完成重要章节后、每日工作结束时、尝试新思路前（推荐）
