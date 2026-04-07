#!/usr/bin/env python3
"""Shared utilities for novel-name generators."""

import json
import random
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename: str) -> dict:
    filepath = DATA_DIR / filename
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


class NameData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def _ensure_loaded(self):
        if not self._loaded:
            self.shared = load_json("shared.json")
            self.surnames = load_json("surnames.json")
            self.names_male = load_json("names_male.json")
            self.names_female = load_json("names_female.json")
            self.names_middle = load_json("names_middle.json")
            self.technique = load_json("technique.json")
            self.sect = load_json("sect.json")
            self.item = load_json("item.json")
            self.creature = load_json("creature.json")
            self.location = load_json("location.json")
            self.alchemy = load_json("alchemy.json")
            self.dao = load_json("dao.json")
            self.strange = load_json("strange.json")
            self._loaded = True

    def __getattr__(self, name):
        self._ensure_loaded()
        return object.__getattribute__(self, name)


RARITY_LEVELS = [
    ("common", "凡品", 1.0, (2, 4)),
    ("uncommon", "良品", 0.35, (3, 5)),
    ("rare", "上品", 0.15, (3, 5)),
    ("epic", "极品", 0.075, (4, 6)),
    ("legendary", "秘宝", 0.03, (4, 7)),
    ("mythic", "灵宝", 0.012, (5, 8)),
    ("exotic", "古宝", 0.005, (5, 9)),
]

OLD_RARITY_MAP = {
    "凡品": "common",
    "灵品": "uncommon",
    "上品": "rare",
    "极品": "epic",
    "仙品": "legendary",
    "神品": "mythic",
}


def roll_rarity(force_level: str = None) -> tuple:
    if force_level:
        for key, cn, _, _ in RARITY_LEVELS:
            if key == force_level or cn == force_level:
                return (key, cn)
        if force_level in OLD_RARITY_MAP:
            mapped = OLD_RARITY_MAP[force_level]
            for key, cn, _, _ in RARITY_LEVELS:
                if key == mapped:
                    return (key, cn)
        return ("common", "凡品")

    r = random.random()
    for key, cn, threshold, _ in reversed(RARITY_LEVELS):
        if r <= threshold:
            return (key, cn)
    return ("common", "凡品")


def get_rarity_index(key: str) -> int:
    for i, (k, _, _, _) in enumerate(RARITY_LEVELS):
        if k == key:
            return i
    return 0


def scan_existing_entities(project_root: Path = None) -> set:
    names = set()
    if project_root is None:
        current = Path(__file__).resolve()
        for parent in [current] + list(current.parents):
            if (parent / "memory" / "entities").is_dir():
                project_root = parent
                break
    if project_root and (project_root / "memory" / "entities").is_dir():
        entities_dir = project_root / "memory" / "entities"
        for subdir in entities_dir.iterdir():
            if subdir.is_dir():
                for f in subdir.glob("*.md"):
                    names.add(f.stem)
                    try:
                        content = f.read_text(encoding="utf-8")
                    except OSError:
                        continue
                    match = re.search(r"^name:\s*(.+?)\s*$", content, flags=re.MULTILINE)
                    if match:
                        names.add(match.group(1).strip().strip("\"'"))
    return names


def pick_random(data_list, count=1, exclude=None):
    if exclude is None:
        exclude = set()
    pool = [x for x in data_list if x not in exclude]
    if not pool:
        return data_list[:count] if count <= len(data_list) else random.choices(data_list, k=count)
    return random.sample(pool, min(count, len(pool))) if count <= len(pool) else random.choices(pool, k=count)


def pick_one(data_list, exclude=None):
    return pick_random(data_list, 1, exclude)[0]


def pad_results(results, count):
    return results[:count]


def combine_unique(*groups):
    merged = []
    for group in groups:
        if not group:
            continue
        merged.extend(group)
    return list(dict.fromkeys(merged))


def render_pattern(pattern: str, values: dict) -> str:
    parts = []
    for token in pattern.split(" + "):
        token = token.strip()
        if token.startswith("[") and token.endswith("]"):
            parts.append(values.get(token[1:-1], ""))
        elif token:
            parts.append(token)
    return "".join(part for part in parts if part)


def looks_awkward(name: str) -> bool:
    if not name:
        return True
    if any(a == b for a, b in zip(name, name[1:])):
        return True
    forbidden_pairs = (
        "宗宗",
        "门门",
        "教教",
        "盟盟",
        "城城",
        "谷谷",
        "山山",
        "海海",
        "湖湖",
        "洞洞",
        "境境",
        "界界",
    )
    return any(pair in name for pair in forbidden_pairs)


def collect_unique_results(count, builder, existing=None, max_attempts=None):
    blocked = set(existing or set())
    results = []
    attempts = 0
    limit = max_attempts or max(count * 40, 120)

    while len(results) < count and attempts < limit:
        attempts += 1
        candidate = builder()
        if not candidate:
            continue
        name = candidate.get("name")
        if not name or name in blocked or looks_awkward(name):
            continue
        results.append(candidate)
        blocked.add(name)

    return results
