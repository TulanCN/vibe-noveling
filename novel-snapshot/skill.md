---
name: novel-snapshot
description: |
  创建和恢复小说项目的版本快照。当用户需要保存当前进度、创建备份、恢复历史版本时触发。

  【必须触发】用户说：创建快照、保存进度、备份项目、novel-snapshot、打版本、存个档、恢复快照、回滚、novel-rollback、回到之前、撤销修改。

  支持两种操作：
  - 创建快照：复制 memory/、chapters/、events/ 到 .snapshots/日期-描述/
  - 恢复快照：先自动备份当前状态，再恢复指定快照
---

# 小说项目快照管理

## 概述

使用 Python 脚本管理快照，确保文件操作安全可靠。

## 可用操作

### 1. 创建快照

用户说：创建快照、保存进度、备份项目、打版本、存个档

**执行步骤：**

1. 询问用户快照描述
2. 运行脚本创建快照

```bash
python {SKILL_DIR}/scripts/snapshot.py create "快照描述"
```

**输出示例：**
```json
{
  "success": true,
  "snapshot_name": "2026-03-14-完成第三章",
  "snapshot_path": ".snapshots/2026-03-14-完成第三章",
  "copied_dirs": ["memory", "chapters", "events"]
}
```

### 2. 恢复快照

用户说：恢复快照、回滚、回到之前、撤销修改

**执行步骤：**

1. 列出可用快照
2. 用户选择要恢复的快照
3. 确认操作
4. 运行脚本恢复

```bash
# 先列出快照
python {SKILL_DIR}/scripts/snapshot.py list

# 恢复指定快照（会自动备份当前状态）
python {SKILL_DIR}/scripts/snapshot.py restore "2026-03-14-完成第三章"
```

**恢复逻辑：**
1. 自动创建当前状态的备份（命名：日期-恢复前自动备份）
2. 将快照内容复制到工作区
3. 返回备份名称，以防用户想撤销

### 3. 列出快照

```bash
python {SKILL_DIR}/scripts/snapshot.py list
```

## 快照目录结构

```
.snapshots/
├── 2026-03-13-初始设定/
│   ├── metadata.json
│   ├── memory/
│   ├── chapters/
│   └── events/
├── 2026-03-14-完成第三章/
│   ├── metadata.json
│   ├── memory/
│   ├── chapters/
│   └── events/
└── 2026-03-14-恢复前自动备份/
    ├── metadata.json
    ├── memory/
    ├── chapters/
    └── events/
```

## 元数据格式

每个快照包含 `metadata.json`：

```json
{
  "name": "2026-03-14-完成第三章",
  "createdAt": "2026-03-14T18:30:00",
  "description": "完成第三章",
  "dirs": ["memory", "chapters", "events"]
}
```

## 用户确认

**创建快照时：**
```
📸 准备创建快照

描述：[用户输入的描述]
将复制：memory/、chapters/、events/

确认创建？(y/n)
```

**恢复快照时：**
```
🔄 准备恢复快照

目标快照：2026-03-13-初始设定
⚠️ 当前状态将自动备份为：2026-03-14-恢复前自动备份

确认恢复？(y/n)
```

## 输出格式

**创建成功：**
```
✅ 快照创建成功！

📸 快照信息：
   名称：2026-03-14-完成第三章
   描述：完成第三章
   时间：2026-03-14 18:30:00

💾 位置：.snapshots/2026-03-14-完成第三章/
```

**恢复成功：**
```
✅ 快照恢复成功！

🔄 恢复信息：
   恢复的快照：2026-03-13-初始设定
   已恢复目录：memory/、chapters/、events/

💾 当前状态已备份到：.snapshots/2026-03-14-恢复前自动备份/
（如需撤销，可恢复此备份）
```

## 建议的快照时机

```
📸 建议在这些时候创建快照：

必需快照：
  ✅ 开始写新章节前
  ✅ 大幅修改大纲后
  ✅ 修改核心设定前
  ✅ 完成重要剧情后

推荐快照：
  📝 完成重要章节后
  📝 每日工作结束时
  📝 尝试新思路前
```
