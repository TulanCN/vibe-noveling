from generator_core import NameData, collect_unique_results, combine_unique, pick_one, render_pattern, roll_rarity, scan_existing_entities

DAO_ORIGINS = ("orthodox", "loose", "ancient", "female_cultivator", "youming")

TONE_ADDITIONS = {
    "dignified": ["守一", "清净", "太玄", "无量", "抱朴"],
    "aloof": ["孤", "寂", "云岫", "无涯", "听雪"],
    "gentle": ["清和", "素月", "慈航", "明净", "妙莲"],
    "ominous": ["九幽", "黄泉", "蚀骨", "冥夜", "无常"],
}

TONE_PLACES = {
    "dignified": ["玉衡", "紫府", "天枢", "太虚", "玄都"],
    "aloof": ["孤峰", "听雪", "云岫", "寒潭", "松涧"],
    "gentle": ["清溪", "莲台", "竹庭", "月汀", "兰洲"],
    "ominous": ["黄泉", "幽都", "冥渊", "忘川", "夜壑"],
}

ROOT_PREFERENCES = {
    "orthodox": ["真人", "道人", "上人", "先生", "居士"],
    "loose": ["散人", "居士", "山人", "隐者", "先生"],
    "ancient": ["尊者", "圣者", "上人", "真人", "祖"],
    "female_cultivator": ["仙", "真人", "居士", "上人", "觉者"],
    "youming": ["道人", "上人", "尊者", "散人", "先生"],
}

ORIGIN_PATTERNS = {
    "orthodox": ["[adjective] + [root]", "[prefix] + [root]", "[prefix] + [name_part] + [root]", "[place_adj] + [root]"],
    "loose": ["[prefix] + [root]", "[place_adj] + [root]", "[prefix] + [name_part] + [root]"],
    "ancient": ["[adjective] + [root]", "[prefix] + [adjective] + [root]", "[place_adj] + [root]"],
    "female_cultivator": ["[prefix] + [root]", "[prefix] + [name_part] + [root]", "[adjective] + [root]"],
    "youming": ["[adjective] + [root]", "[prefix] + [root]", "[prefix] + [name_part] + [root]"],
}


def _build_dao_pools(data, origin, gender, tone):
    female_like = gender == "女" or origin == "female_cultivator"
    prefix_pool = data.dao["prefixes_female"] if female_like else data.dao["prefixes_male"]
    adjective_pool = data.dao["adjectives"]
    name_part_pool = data.dao["daoist"]
    place_pool = combine_unique(data.shared["nature"], data.shared["celestial"], TONE_PLACES.get(tone, []))
    root_pool = combine_unique(ROOT_PREFERENCES[origin], data.dao["roots"])

    if origin == "loose":
        adjective_pool = combine_unique(adjective_pool, ["抱朴", "听风", "松云", "清茶", "竹溪"])
        name_part_pool = combine_unique(name_part_pool, data.shared["nature"])
    elif origin == "ancient":
        adjective_pool = combine_unique(adjective_pool, data.strange["ancient_descriptors"], data.strange["ancient_elements"])
        name_part_pool = combine_unique(name_part_pool, data.strange["ancient_elements"])
    elif origin == "female_cultivator":
        prefix_pool = combine_unique(prefix_pool, ["昭", "静", "清荷", "霜华", "云岫"])
        adjective_pool = combine_unique(adjective_pool, ["素月", "清荷", "静澜", "明和"])
        name_part_pool = combine_unique(name_part_pool, ["素", "月", "莲", "云", "荷", "岫"])
    elif origin == "youming":
        prefix_pool = combine_unique(["幽", "冥", "蚀", "魇", "骨", "夜", "厄", "噬"], data.sect["demonic_words"])
        adjective_pool = combine_unique(TONE_ADDITIONS["ominous"], ["幽冥", "黄泉", "蚀心", "腐魂", "夜魇", "冥夜", "无常"])
        name_part_pool = ["幽", "冥", "骨", "魇", "噬", "蚀", "夜", "血", "魂"]
        place_pool = ["黄泉", "冥渊", "忘川", "幽都", "夜壑"]
        root_pool = ["道人", "上人", "尊者", "散人"]
    else:
        prefix_pool = combine_unique(prefix_pool, data.dao["daoist"], ["守一", "归真", "清虚"])

    adjective_pool = combine_unique(adjective_pool, TONE_ADDITIONS.get(tone, []))
    if tone == "gentle":
        name_part_pool = combine_unique(name_part_pool, data.dao["buddhist"])
    elif tone == "aloof":
        name_part_pool = combine_unique(name_part_pool, ["云", "鹤", "松", "雪", "寂"])
    elif tone == "ominous":
        name_part_pool = combine_unique(name_part_pool, ["夜", "幽", "冥", "血", "骨"])

    return prefix_pool, adjective_pool, name_part_pool, place_pool, root_pool


def _build_dao_name(data, origin, gender, tone):
    prefix_pool, adjective_pool, name_part_pool, place_pool, root_pool = _build_dao_pools(data, origin, gender, tone)
    pattern = pick_one(ORIGIN_PATTERNS[origin])
    values = {
        "prefix": pick_one(prefix_pool),
        "adjective": pick_one(adjective_pool),
        "name_part": pick_one(name_part_pool),
        "place_adj": pick_one(place_pool),
        "root": pick_one(root_pool),
    }
    return render_pattern(pattern, values)


def generate_dao_name(count=1, gender="男", exclude_existing=True, origin="orthodox", tone="dignified"):
    data = NameData()
    existing = scan_existing_entities() if exclude_existing else set()
    if origin not in DAO_ORIGINS:
        raise ValueError(f"不支持的 dao origin: {origin}")
    if tone not in {"dignified", "aloof", "gentle", "ominous"}:
        tone = "dignified"

    def builder():
        rarity_key, rarity_cn = roll_rarity()
        return {
            "name": _build_dao_name(data, origin, gender, tone),
            "origin": origin,
            "tone": tone,
            "rarity": rarity_key,
            "rarity_cn": rarity_cn,
        }

    return collect_unique_results(count, builder, existing=existing, max_attempts=max(count * 60, 180))
