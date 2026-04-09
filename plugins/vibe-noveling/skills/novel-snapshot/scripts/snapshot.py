#!/usr/bin/env python3
"""
小说项目快照管理工具

功能：
1. 创建快照：复制 memory/、chapters/、events/ 到 .snapshots/日期-描述/
2. 恢复快照：先备份当前状态，再恢复指定快照
3. 列出快照：显示所有可用快照
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# 要备份的目录
BACKUP_DIRS = ["memory", "chapters", "events"]
SNAPSHOTS_DIR = ".snapshots"


def get_project_root() -> Path:
    """获取项目根目录

    优先级：
    1. 环境变量 SNAPSHOT_PROJECT_ROOT（显式指定）
    2. git 仓库根目录（git rev-parse --show-toplevel）
    3. 当前工作目录（cwd）
    """
    # 1. 环境变量显式指定
    env_root = os.environ.get("SNAPSHOT_PROJECT_ROOT")
    if env_root:
        root = Path(env_root).resolve()
        if root.is_dir():
            return root

    # 2. git 仓库根目录
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return Path(result.stdout.strip()).resolve()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # 3. 回退到当前工作目录
    return Path.cwd().resolve()


def get_snapshots_dir() -> Path:
    """获取快照目录"""
    return get_project_root() / SNAPSHOTS_DIR


def list_snapshots() -> list[dict]:
    """列出所有快照"""
    snapshots_dir = get_snapshots_dir()
    if not snapshots_dir.exists():
        return []

    snapshots = []
    for snapshot in sorted(snapshots_dir.iterdir(), reverse=True):
        if snapshot.is_dir() and not snapshot.name.startswith('.'):
            metadata_file = snapshot / "metadata.json"
            metadata = {}
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            snapshots.append({
                "name": snapshot.name,
                "path": str(snapshot),
                "metadata": metadata
            })
    return snapshots


def create_snapshot(description: str) -> dict:
    """创建快照

    Args:
        description: 快照描述（用于命名）

    Returns:
        结果字典，包含 success、message、snapshot_path 等
    """
    project_root = get_project_root()
    snapshots_dir = get_snapshots_dir()

    # 确保快照目录存在
    snapshots_dir.mkdir(parents=True, exist_ok=True)

    # 生成快照名称：日期-描述
    date_str = datetime.now().strftime("%Y-%m-%d")
    # 清理描述中的特殊字符
    safe_desc = "".join(c for c in description if c.isalnum() or c in ('-', '_', ' ')).strip()
    safe_desc = safe_desc.replace(' ', '-')[:50]  # 限制长度

    snapshot_name = f"{date_str}-{safe_desc}"
    snapshot_path = snapshots_dir / snapshot_name

    # 如果已存在同名快照，添加时间戳后缀
    if snapshot_path.exists():
        time_str = datetime.now().strftime("%H%M%S")
        snapshot_name = f"{snapshot_name}-{time_str}"
        snapshot_path = snapshots_dir / snapshot_name

    # 创建快照目录
    snapshot_path.mkdir(parents=True)

    # 复制目录
    copied_dirs = []
    for dir_name in BACKUP_DIRS:
        src = project_root / dir_name
        if src.exists():
            dst = snapshot_path / dir_name
            shutil.copytree(src, dst)
            copied_dirs.append(dir_name)

    # 创建元数据
    metadata = {
        "name": snapshot_name,
        "createdAt": datetime.now().isoformat(),
        "description": description,
        "dirs": copied_dirs
    }

    with open(snapshot_path / "metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return {
        "success": True,
        "message": f"快照创建成功",
        "snapshot_path": str(snapshot_path),
        "snapshot_name": snapshot_name,
        "copied_dirs": copied_dirs
    }


def restore_snapshot(snapshot_name: str) -> dict:
    """恢复快照

    逻辑：先备份当前状态，再恢复指定快照

    Args:
        snapshot_name: 要恢复的快照名称

    Returns:
        结果字典
    """
    project_root = get_project_root()
    snapshots_dir = get_snapshots_dir()

    # 检查快照是否存在
    snapshot_path = snapshots_dir / snapshot_name
    if not snapshot_path.exists():
        return {
            "success": False,
            "message": f"快照 '{snapshot_name}' 不存在"
        }

    # 先创建当前状态的备份
    backup_desc = f"恢复前自动备份"
    backup_result = create_snapshot(backup_desc)

    if not backup_result["success"]:
        return {
            "success": False,
            "message": f"创建备份失败: {backup_result['message']}"
        }

    # 恢复快照内容
    restored_dirs = []
    for dir_name in BACKUP_DIRS:
        src = snapshot_path / dir_name
        if src.exists():
            dst = project_root / dir_name
            # 删除当前目录
            if dst.exists():
                shutil.rmtree(dst)
            # 复制快照目录
            shutil.copytree(src, dst)
            restored_dirs.append(dir_name)

    return {
        "success": True,
        "message": f"快照恢复成功",
        "restored_dirs": restored_dirs,
        "backup_name": backup_result["snapshot_name"]
    }


def main():
    parser = argparse.ArgumentParser(description="小说项目快照管理工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 创建快照
    create_parser = subparsers.add_parser("create", help="创建快照")
    create_parser.add_argument("description", help="快照描述")

    # 恢复快照
    restore_parser = subparsers.add_parser("restore", help="恢复快照")
    restore_parser.add_argument("snapshot_name", help="快照名称")

    # 列出快照
    subparsers.add_parser("list", help="列出所有快照")

    args = parser.parse_args()

    if args.command == "create":
        result = create_snapshot(args.description)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "restore":
        result = restore_snapshot(args.snapshot_name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "list":
        snapshots = list_snapshots()
        if not snapshots:
            print("暂无快照")
        else:
            print(f"共有 {len(snapshots)} 个快照：\n")
            for s in snapshots:
                meta = s["metadata"]
                desc = meta.get("description", "无描述")
                created = meta.get("createdAt", "未知时间")
                print(f"  📸 {s['name']}")
                print(f"     描述：{desc}")
                print(f"     时间：{created}")
                print()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
