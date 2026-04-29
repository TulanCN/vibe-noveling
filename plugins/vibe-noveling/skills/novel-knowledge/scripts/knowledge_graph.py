#!/usr/bin/env python3
"""
知识图谱工具 - knowledge_graph.py

纯数据访问工具，提供基础的搜索和索引功能。

功能:
1. 搜索知识图谱: python {SKILL_DIR}/scripts/knowledge_graph.py search <query>
2. 创建/更新对象: python {SKILL_DIR}/scripts/knowledge_graph.py update <type> <name>
3. 查询关系: python {SKILL_DIR}/scripts/knowledge_graph.py relations <entity_id>
4. 按标签查询: python {SKILL_DIR}/scripts/knowledge_graph.py tags <tag>
5. 重建索引: python {SKILL_DIR}/scripts/knowledge_graph.py rebuild
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
MEMORY_DIR = PROJECT_ROOT / "memory"
ENTITIES_DIR = MEMORY_DIR / "entities"
EVENTS_DIR = PROJECT_ROOT / "events"

# 图谱和索引文件路径
GRAPH_FILE = MEMORY_DIR / "_graph.json"
INDEX_FILE = MEMORY_DIR / "_index.json"


def load_graph() -> Dict[str, Any]:
    """加载知识图谱"""
    if GRAPH_FILE.exists():
        with open(GRAPH_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": "1.0", "entities": {}, "relations": []}


def load_index() -> Dict[str, Any]:
    """加载索引"""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": "1.0", "name_index": {}, "tag_index": {}, "type_index": {}}


def save_graph(graph: Dict[str, Any]) -> None:
    """保存知识图谱"""
    with open(GRAPH_FILE, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)


def save_index(index: Dict[str, Any]) -> None:
    """保存索引"""
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


# 实体类型到目录的映射
ENTITY_TYPE_DIRS = {
    "character": "characters",
    "location": "locations",
    "item": "items",
    "faction": "factions",
    "concept": "concepts",
    "system": "systems",
    "event": "events"
}


def get_known_entities() -> Dict[str, List[str]]:
    """从索引中动态获取已知实体列表（用于辅助搜索）"""
    index = load_index()
    graph = load_graph()

    entities_by_type = {
        "characters": [],
        "locations": [],
        "items": [],
        "factions": []
    }

    # 从图谱中按类型收集实体名称
    for entity_id, entity_info in graph.get("entities", {}).items():
        entity_type = entity_info.get("type", "")
        entity_name = entity_info.get("name", "")

        if entity_type == "character" and entity_name:
            entities_by_type["characters"].append(entity_name)
        elif entity_type == "location" and entity_name:
            entities_by_type["locations"].append(entity_name)
        elif entity_type == "item" and entity_name:
            entities_by_type["items"].append(entity_name)
        elif entity_type == "faction" and entity_name:
            entities_by_type["factions"].append(entity_name)

    return entities_by_type


def get_template(entity_type: str, name: str) -> str:
    """生成实体模板（带 YAML frontmatter）"""
    date = datetime.now().strftime("%Y-%m-%d")
    id_prefix = {
        "character": "char", "location": "loc", "item": "item",
        "faction": "fac", "concept": "con", "system": "sys", "event": "event"
    }.get(entity_type, "entity")

    safe_name = re.sub(r"[^\w\u4e00-\u9fff-]", "_", name)
    entity_id = f"{id_prefix}_{safe_name}"

    templates = {
        "character": f"""---
id: {entity_id}
type: character
name: {name}
aliases: []
tags: [主角]  # 可选: 主角/配角/反派
faction:
realm:
relations: []
---

# {name}

> 一句话身份描述

## 基本信息
- **姓名**: {name}
- **年龄**:
- **身份**:
- **境界**:

## 外貌描写
（待补充）

## 性格特点
（待补充）

## 背景故事
（待补充）
""",
        "location": f"""---
id: {entity_id}
type: location
name: {name}
aliases: []
tags: []
faction:
relations: []
---

# {name}

> 一句话描述

## 基本信息
- **名称**: {name}
- **类型**:
- **位置**:

## 描述
（待补充）

## 相关角色
（待补充）
""",
        "item": f"""---
id: {entity_id}
type: item
name: {name}
aliases: []
tags: []
relations: []
---

# {name}

> 一句话描述

## 基本信息
- **名称**: {name}
- **类型**:
- **持有者**:

## 描述
（待补充）

## 能力/效果
（待补充）
""",
        "faction": f"""---
id: {entity_id}
type: faction
name: {name}
aliases: []
tags: []
relations: []
---

# {name}

> 一句话描述

## 基本信息
- **名称**: {name}
- **类型**: 宗门/组织

## 组织结构
（待补充）

## 核心人物
（待补充）
""",
        "event": f"""---
id: {entity_id}
type: event
name: {name}
tags: []
relations: []
---

# {name}

## Position
- Volume:
- Timeline:

## 起
（待补充）

## 承
（待补充）

## 转
（待补充）

## 合
（待补充）

## Characters Involved
- **Protagonist**:
- **New Characters**:

## Notes
（待补充）
""",
    }
    return templates.get(entity_type, f"# {name}\n\n> 创建时间: {date}\n\n（待补充）\n")


@dataclass
class SearchResult:
    """搜索结果"""
    entity_id: str
    file: str
    title: str
    relevance: float
    snippet: str
    line_number: int
    matches: list


def load_file(filepath: Path) -> tuple[str, list[str]]:
    """加载文件内容"""
    if not filepath.exists():
        return "", []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return content, content.split("\n")


def extract_title(content: str, filepath: Path) -> str:
    """从 markdown 文件中提取标题（跳过 YAML frontmatter）"""
    # 跳过 YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]

    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else filepath.stem


def parse_frontmatter(content: str) -> Dict[str, Any]:
    """解析 YAML frontmatter（支持多行列表）"""
    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    frontmatter_text = parts[1].strip()
    result = {}

    try:
        import yaml
        result = yaml.safe_load(frontmatter_text) or {}
    except ImportError:
        # 回退到简单解析
        current_key = None
        current_list = []

        for line in frontmatter_text.split("\n"):
            stripped = line.strip()

            # 多行列表项
            if stripped.startswith("- ") and current_key:
                current_list.append(stripped[2:].strip().strip("\"'"))
                continue

            # 普通键值对
            if ":" in line and not line.startswith(" "):
                # 保存之前的列表
                if current_key and current_list:
                    result[current_key] = current_list
                    current_list = []

                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                current_key = key

                if not value:
                    current_list = []
                elif value.startswith("[") and value.endswith("]"):
                    items = value[1:-1].strip()
                    if items:
                        result[key] = [i.strip().strip("\"'") for i in items.split(",")]
                    else:
                        result[key] = []
                    current_key = None
                elif value.isdigit():
                    result[key] = int(value)
                    current_key = None
                elif value.lower() in ("true", "false"):
                    result[key] = value.lower() == "true"
                    current_key = None
                else:
                    result[key] = value.strip("\"'")
                    current_key = None

        # 保存最后的列表
        if current_key and current_list:
            result[current_key] = current_list

    return result


def find_section(lines: list[str], start_line: int, context_lines: int = 5) -> str:
    """提取匹配位置周围的上下文片段"""
    start = max(0, start_line - context_lines)
    end = min(len(lines), start_line + context_lines + 1)
    result = []
    for i in range(start, end):
        prefix = ">>> " if i == start_line else "    "
        result.append(f"{prefix}{lines[i]}")
    return "\n".join(result)


def extract_keywords(text: str) -> list[str]:
    """从文本中提取关键词"""
    text = re.sub(r"[^\w\s\u4e00-\u9fff]", " ", text)
    keywords = []
    for match in re.finditer(r"[\u4e00-\u9fff]+", text):
        if len(match.group()) >= 2:
            keywords.append(match.group())
    for match in re.finditer(r"[a-zA-Z]+", text):
        if len(match.group()) >= 2:
            keywords.append(match.group().lower())
    return list(set(keywords))


def calculate_relevance(query_terms: list[str], content: str, title: str, tags: list = None) -> float:
    """计算相关性分数"""
    score = 0.0
    content_lower = content.lower()
    title_lower = title.lower()

    for term in query_terms:
        term_lower = term.lower()
        if term_lower in title_lower:
            score += 10.0
        count = content_lower.count(term_lower)
        score += min(count * 0.5, 5.0)
        if term in title:
            score += 3.0
        if term in content:
            score += 1.0

    # 标签匹配加分
    if tags:
        for term in query_terms:
            for tag in tags:
                if term.lower() in tag.lower():
                    score += 5.0

    return score


def search_in_file(filepath: Path, query_terms: list[str], entity_id: str = None) -> list[SearchResult]:
    """在单个文件中搜索"""
    results = []
    content, lines = load_file(filepath)
    if not content:
        return results

    title = extract_title(content, filepath)
    frontmatter = parse_frontmatter(content)
    tags = frontmatter.get("tags", [])

    base_relevance = calculate_relevance(query_terms, content, title, tags)
    if base_relevance == 0:
        return results

    matched_lines = []
    for i, line in enumerate(lines):
        line_matches = [t for t in query_terms if t.lower() in line.lower()]
        if line_matches:
            matched_lines.append((i, line_matches))

    if not matched_lines:
        return results

    for line_num, line_matches in matched_lines[:3]:
        results.append(SearchResult(
            entity_id=entity_id or filepath.stem,
            file=str(filepath.relative_to(PROJECT_ROOT)),
            title=title,
            relevance=base_relevance + len(line_matches) * 2,
            snippet=find_section(lines, line_num),
            line_number=line_num + 1,
            matches=list(set(line_matches))
        ))
    return results


def get_all_entity_files() -> List[Path]:
    """获取所有实体文件"""
    files = []
    if ENTITIES_DIR.exists():
        for subdir in ENTITIES_DIR.iterdir():
            if subdir.is_dir():
                for f in subdir.rglob("*.md"):
                    if f.name != "README.md":
                        files.append(f)
    return files


def search_knowledge(query: str, search_type: Optional[str] = None, limit: int = 10) -> list[dict]:
    """搜索知识图谱"""
    query_terms = extract_keywords(query)
    if not query_terms:
        return []

    all_results = []

    # 先检查索引，快速查找
    index = load_index()

    # 名称精确匹配
    for term in query_terms:
        if term in index.get("name_index", {}):
            entity_id = index["name_index"][term]
            graph = load_graph()
            if entity_id in graph.get("entities", {}):
                entity_info = graph["entities"][entity_id]
                filepath = MEMORY_DIR / entity_info.get("file", "")
                if filepath.exists():
                    results = search_in_file(filepath, query_terms, entity_id)
                    all_results.extend(results)

    # 搜索实体文件
    entity_files = get_all_entity_files()

    # 按类型过滤
    if search_type:
        type_dir = ENTITY_TYPE_DIRS.get(search_type, search_type)
        entity_files = [f for f in entity_files if type_dir in str(f)]

    for filepath in entity_files:
        results = search_in_file(filepath, query_terms)
        all_results.extend(results)

    # 搜索 events
    if EVENTS_DIR.exists():
        for filepath in EVENTS_DIR.glob("*.md"):
            results = search_in_file(filepath, query_terms)
            all_results.extend(results)

    all_results.sort(key=lambda x: x.relevance, reverse=True)
    return [asdict(r) for r in all_results[:limit]]


def get_entity_relations(entity_id: str) -> Dict[str, Any]:
    """获取实体的所有关系"""
    graph = load_graph()
    relations = {"entity_id": entity_id, "outgoing": [], "incoming": []}

    if entity_id not in graph.get("entities", {}):
        return relations

    for rel in graph.get("relations", []):
        if rel["from"] == entity_id:
            relations["outgoing"].append(rel)
        if rel["to"] == entity_id:
            relations["incoming"].append(rel)

    return relations


def search_by_tag(tag: str) -> List[Dict[str, Any]]:
    """按标签搜索实体"""
    index = load_index()
    graph = load_graph()

    entity_ids = index.get("tag_index", {}).get(tag, [])
    results = []

    for entity_id in entity_ids:
        if entity_id in graph.get("entities", {}):
            results.append(graph["entities"][entity_id])

    return results


def get_entity_filepath(entity_type: str, name: str) -> Path:
    """获取实体文件路径"""
    if entity_type == "event":
        target_dir = EVENTS_DIR
    else:
        subdir = ENTITY_TYPE_DIRS.get(entity_type, entity_type)
        target_dir = ENTITIES_DIR / subdir
        target_dir.mkdir(parents=True, exist_ok=True)

    safe_name = re.sub(r"[^\w\u4e00-\u9fff-]", "_", name)
    return target_dir / f"{safe_name}.md"


def update_entity(entity_type: str, name: str, content: Optional[str] = None) -> dict:
    """创建或更新实体，同时更新知识图谱和索引"""
    filepath = get_entity_filepath(entity_type, name)

    # 1. 创建/更新实体文件
    if content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        action = "updated"
    elif filepath.exists():
        action = "exists"
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(get_template(entity_type, name))
        action = "created"

    # 2. 读取实体文件，解析 frontmatter
    file_content, _ = load_file(filepath)
    frontmatter = parse_frontmatter(file_content)

    # 3. 更新知识图谱
    graph = load_graph()
    entity_id = frontmatter.get("id", filepath.stem)

    graph["entities"][entity_id] = {
        "name": frontmatter.get("name", name),
        "type": frontmatter.get("type", entity_type),
        "tags": frontmatter.get("tags", []),
        "aliases": frontmatter.get("aliases", []),
        "file": str(filepath.relative_to(PROJECT_ROOT)),
        "description": extract_title(file_content, filepath)
    }

    # 处理关系（如果 frontmatter 中有 relations 字段）
    if "relations" in frontmatter:
        relations = frontmatter.get("relations", [])
        if isinstance(relations, list):
            for rel in relations:
                if isinstance(rel, dict) and "target" in rel:
                    graph["relations"].append({
                        "from": entity_id,
                        "to": rel.get("target"),
                        "type": rel.get("relation", "related_to"),
                        "note": rel.get("description", "")
                    })

    save_graph(graph)

    # 4. 更新索引
    index = load_index()

    # 确保 tag_index 存在
    if "tag_index" not in index:
        index["tag_index"] = {}

    # 名称索引
    index["name_index"][frontmatter.get("name", name)] = entity_id

    # 标签索引
    for tag in frontmatter.get("tags", []):
        if tag not in index["tag_index"]:
            index["tag_index"][tag] = []
        if entity_id not in index["tag_index"][tag]:
            index["tag_index"][tag].append(entity_id)

    # 类型索引
    etype = frontmatter.get("type", entity_type)
    if etype not in index["type_index"]:
        index["type_index"][etype] = []
    if entity_id not in index["type_index"][etype]:
        index["type_index"][etype].append(entity_id)

    save_index(index)

    return {"status": "success", "action": action, "type": entity_type,
            "name": name, "entity_id": entity_id,
            "file": str(filepath.relative_to(PROJECT_ROOT))}


def rebuild_index() -> dict:
    """重建知识图谱和索引（从文件系统扫描）"""
    graph = {
        "version": "1.0",
        "entities": {},
        "relations": []
    }
    index = {
        "version": "1.0",
        "name_index": {},
        "tag_index": {},
        "type_index": {},
        "faction_index": {}
    }

    entities_count = 0

    # 1. 扫描实体文件
    if ENTITIES_DIR.exists():
        for subdir in ENTITIES_DIR.iterdir():
            if subdir.is_dir():
                for filepath in subdir.rglob("*.md"):
                    if filepath.name == "README.md":
                        continue

                    content, _ = load_file(filepath)
                    if not content:
                        continue

                    frontmatter = parse_frontmatter(content)
                    entity_id = frontmatter.get("id", filepath.stem)
                    name = frontmatter.get("name", filepath.stem)
                    entity_type = frontmatter.get("type", "")
                    tags = frontmatter.get("tags", [])
                    faction = frontmatter.get("faction", "")
                    aliases = frontmatter.get("aliases", [])

                    # 添加到图谱
                    graph["entities"][entity_id] = {
                        "name": name,
                        "type": entity_type,
                        "tags": tags,
                        "aliases": aliases,
                        "faction": faction,
                        "file": str(filepath.relative_to(PROJECT_ROOT)),
                        "description": extract_title(content, filepath)
                    }

                    # 处理关系
                    if "relations" in frontmatter:
                        relations = frontmatter.get("relations", [])
                        if isinstance(relations, list):
                            for rel in relations:
                                if isinstance(rel, dict) and "target" in rel:
                                    graph["relations"].append({
                                        "from": entity_id,
                                        "to": rel.get("target"),
                                        "type": rel.get("relation", "related_to"),
                                        "note": rel.get("description", "")
                                    })

                    # 更新索引
                    if name:
                        index["name_index"][name] = entity_id
                    for alias in aliases:
                        index["name_index"][alias] = entity_id
                    for tag in tags:
                        if tag not in index["tag_index"]:
                            index["tag_index"][tag] = []
                        if entity_id not in index["tag_index"][tag]:
                            index["tag_index"][tag].append(entity_id)
                    if entity_type:
                        if entity_type not in index["type_index"]:
                            index["type_index"][entity_type] = []
                        if entity_id not in index["type_index"][entity_type]:
                            index["type_index"][entity_type].append(entity_id)
                    if faction:
                        if faction not in index["faction_index"]:
                            index["faction_index"][faction] = []
                        if entity_id not in index["faction_index"][faction]:
                            index["faction_index"][faction].append(entity_id)

                    entities_count += 1

    # 2. 扫描事件文件
    if EVENTS_DIR.exists():
        for filepath in EVENTS_DIR.glob("*.md"):
            content, _ = load_file(filepath)
            if not content:
                continue

            frontmatter = parse_frontmatter(content)
            entity_id = frontmatter.get("id", filepath.stem)
            name = frontmatter.get("name", filepath.stem)
            tags = frontmatter.get("tags", [])

            # 添加到图谱
            graph["entities"][entity_id] = {
                "name": name,
                "type": "event",
                "tags": tags,
                "file": str(filepath.relative_to(PROJECT_ROOT)),
                "description": extract_title(content, filepath)
            }

            # 更新索引
            if name:
                index["name_index"][name] = entity_id
            for tag in tags:
                if tag not in index["tag_index"]:
                    index["tag_index"][tag] = []
                if entity_id not in index["tag_index"][tag]:
                    index["tag_index"][tag].append(entity_id)
            if "event" not in index["type_index"]:
                index["type_index"]["event"] = []
            if entity_id not in index["type_index"]["event"]:
                index["type_index"]["event"].append(entity_id)

            entities_count += 1

    # 3. 保存图谱和索引
    save_graph(graph)
    save_index(index)

    return {"status": "success", "entities_indexed": entities_count}


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="知识图谱工具 - 搜索和管理小说设定",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python {SKILL_DIR}/scripts/knowledge_graph.py search 苏寒染
  python {SKILL_DIR}/scripts/knowledge_graph.py search 凌霄剑宗 -t location
  python {SKILL_DIR}/scripts/knowledge_graph.py update character 张三
  python {SKILL_DIR}/scripts/knowledge_graph.py relations char_苏寒染
  python {SKILL_DIR}/scripts/knowledge_graph.py tags 主角
  python {SKILL_DIR}/scripts/knowledge_graph.py rebuild
"""
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索知识图谱")
    search_parser.add_argument("query", help="搜索查询")
    search_parser.add_argument("--type", "-t", help="限制搜索类型")
    search_parser.add_argument("--limit", "-l", type=int, default=10, help="返回结果数量")
    search_parser.add_argument("--json", "-j", action="store_true", help="输出 JSON")

    # update 命令
    update_parser = subparsers.add_parser("update", help="创建或更新实体")
    update_parser.add_argument("type", help="实体类型")
    update_parser.add_argument("name", help="实体名称")
    update_parser.add_argument("--content", "-c", help="实体内容")
    update_parser.add_argument("--json", "-j", action="store_true", help="输出 JSON")

    # relations 命令
    relations_parser = subparsers.add_parser("relations", help="查询实体关系")
    relations_parser.add_argument("entity_id", help="实体 ID")
    relations_parser.add_argument("--json", "-j", action="store_true", help="输出 JSON")

    # tags 命令
    tags_parser = subparsers.add_parser("tags", help="按标签查询")
    tags_parser.add_argument("tag", help="标签名称")
    tags_parser.add_argument("--json", "-j", action="store_true", help="输出 JSON")

    # rebuild 命令
    rebuild_parser = subparsers.add_parser("rebuild", help="重建索引")
    rebuild_parser.add_argument("--json", "-j", action="store_true", help="输出 JSON")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "search":
        results = search_knowledge(args.query, args.type, args.limit)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        elif results:
            print(f"找到 {len(results)} 个结果:\n")
            for i, r in enumerate(results, 1):
                print(f"【{i}】{r['title']}")
                print(f"    ID: {r.get('entity_id', 'N/A')}")
                print(f"    文件: {r['file']} | 相关性: {r['relevance']:.1f}")
                print(f"    匹配: {', '.join(r['matches'])} | 位置: 第 {r['line_number']} 行\n")
                print(r['snippet'])
                print("-" * 60)
        else:
            print("未找到匹配结果")

    elif args.command == "update":
        result = update_entity(args.type, args.name, args.content)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            action_text = {"created": "已创建", "updated": "已更新", "exists": "已存在"}
            print(f"{action_text.get(result['action'], result['action'])}: {result['name']}")
            print(f"文件: {result['file']}")

    elif args.command == "relations":
        result = get_entity_relations(args.entity_id)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"实体: {args.entity_id}")
            print("=" * 60)
            if result['outgoing']:
                print("出向关系:")
                for rel in result['outgoing']:
                    print(f"  → [{rel['type']}] {rel['to']}" + (f" ({rel.get('note', '')})" if rel.get('note') else ""))
            if result['incoming']:
                print("入向关系:")
                for rel in result['incoming']:
                    print(f"  ← [{rel['type']}] {rel['from']}" + (f" ({rel.get('note', '')})" if rel.get('note') else ""))
            if not result['outgoing'] and not result['incoming']:
                print("无关系记录")

    elif args.command == "tags":
        results = search_by_tag(args.tag)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        elif results:
            print(f"标签 [{args.tag}] 下的实体:\n")
            for i, entity in enumerate(results, 1):
                print(f"{i}. {entity.get('name', 'N/A')} ({entity.get('type', 'N/A')})")
                print(f"   文件: {entity.get('file', 'N/A')}")
                if entity.get('tags'):
                    print(f"   标签: {', '.join(entity['tags'])}")
                print()
        else:
            print(f"未找到标签为 [{args.tag}] 的实体")

    elif args.command == "rebuild":
        result = rebuild_index()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"索引重建完成，已索引 {result['entities_indexed']} 个实体")


if __name__ == "__main__":
    main()
