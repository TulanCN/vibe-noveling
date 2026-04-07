import random

from generator_core import NameData, collect_unique_results, combine_unique, pick_one, roll_rarity, scan_existing_entities

CREATURE_BIOMES = ("northern", "mountain", "water", "jungle", "farmland", "corrupted")

BIOME_WORDS = {
    "northern": ["霜", "雪", "寒", "冰", "北", "狼", "原"],
    "mountain": ["岩", "峰", "崖", "松", "云", "石", "岭"],
    "water": ["潮", "沧", "汐", "涟", "泽", "镜", "波"],
    "jungle": ["藤", "榕", "雾", "木", "岚", "毒", "泽"],
    "farmland": ["谷", "田", "禾", "泥", "渠", "圃", "牧"],
    "corrupted": ["蚀", "腐", "冥", "幽", "疫", "毒", "暗"],
}

TEMPER_WORDS = {
    "gentle": ["灵", "青", "玉", "云", "和", "宁"],
    "predatory": ["裂", "狂", "噬", "猎", "猛", "厉"],
    "ominous": ["幽", "冥", "蚀", "毒", "影", "疫"],
}

RANK_PREFIXES = {
    "common": [],
    "spirit": ["灵", "玄", "玉", "青", "银"],
    "rare": ["太古", "上古", "洪荒", "九天", "圣"],
    "ancient": ["太古", "洪荒", "亘古", "上古", "失落"],
}


def _default_category_for_biome(biome):
    return {
        "water": "鱼",
        "jungle": "兽",
        "farmland": "兽",
        "northern": "兽",
        "corrupted": "爬虫",
        "mountain": "兽",
    }[biome]


def _build_creature_pools(data, category, biome, rank, temper):
    category_data = data.creature[category]
    biome_words = BIOME_WORDS[biome]
    temper_words = TEMPER_WORDS[temper]

    prefixes = combine_unique(category_data["prefixes"], biome_words, temper_words, RANK_PREFIXES.get(rank, []))
    modifiers = combine_unique(category_data["modifiers"], biome_words, temper_words)
    roots = combine_unique(category_data["roots"])

    if category == "兽":
        roots = combine_unique(roots, data.shared["beasts"])
    if rank == "ancient":
        roots = combine_unique(roots, data.strange["ancient_beasts"])
        modifiers = combine_unique(modifiers, data.strange["ancient_descriptors"])

    return prefixes, modifiers, roots


def _build_creature_name(data, category, biome, rank, temper):
    prefixes, modifiers, roots = _build_creature_pools(data, category, biome, rank, temper)
    root = pick_one(roots)
    modifier = pick_one(modifiers)

    if rank == "common":
        if random.random() < 0.45:
            return modifier + root
        return pick_one(BIOME_WORDS[biome]) + root
    if rank == "spirit":
        if random.random() < 0.4:
            return pick_one(prefixes) + root
        return modifier + root
    if rank == "ancient":
        if root in data.strange["ancient_beasts"] and random.random() < 0.5:
            return pick_one(RANK_PREFIXES["ancient"]) + root
    return pick_one(prefixes) + modifier + root


def generate_creature_name(category=None, count=1, exclude_existing=True, biome=None, rank="common", temper="gentle"):
    data = NameData()
    existing = scan_existing_entities() if exclude_existing else set()
    biome = biome or "mountain"
    if biome not in CREATURE_BIOMES:
        raise ValueError(f"不支持的 biome: {biome}")
    if rank not in {"common", "spirit", "rare", "ancient"}:
        raise ValueError(f"不支持的 rank: {rank}")
    if temper not in {"gentle", "predatory", "ominous"}:
        raise ValueError(f"不支持的 temper: {temper}")

    category = category or _default_category_for_biome(biome)
    if category not in data.creature:
        raise ValueError(f"不支持的 category: {category}")

    def builder():
        rarity_key, rarity_cn = roll_rarity()
        return {
            "name": _build_creature_name(data, category, biome, rank, temper),
            "category": category,
            "biome": biome,
            "rank": rank,
            "temper": temper,
            "rarity": rarity_key,
            "rarity_cn": rarity_cn,
        }

    return collect_unique_results(count, builder, existing=existing, max_attempts=max(count * 60, 180))
