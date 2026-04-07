import random

from generator_core import NameData, collect_unique_results, combine_unique, pick_one, roll_rarity, scan_existing_entities

LOCATION_CULTURES = ("orthodox", "water_trade", "southern_jungle", "northern_tribe", "zhongfang_base", "mystic_realm")

CULTURE_PREFIXES = {
    "orthodox": ["承", "清", "昭", "望", "太", "玄", "灵", "玉"],
    "water_trade": ["潮", "沧", "汀", "浦", "津", "烟", "云", "渡"],
    "southern_jungle": ["榕", "藤", "木", "岚", "雾", "药", "苍", "南"],
    "northern_tribe": ["寒", "霜", "雪", "冰", "乌兰", "塔", "苏赫", "北"],
    "zhongfang_base": ["函谷", "河洛", "安澜", "东岭", "前线", "北港"],
    "mystic_realm": ["幻", "蜃", "空", "虚", "忘", "沉", "镜", "灵墟"],
}

CULTURE_MODIFIERS = {
    "orthodox": ["天", "霄", "岳", "宁", "都", "阙", "清", "华"],
    "water_trade": ["平码", "航", "商", "潮", "湾", "汀", "泊", "平码"],
    "southern_jungle": ["榕", "藤", "雾", "泽", "林", "岚", "瘴", "草"],
    "northern_tribe": ["狼", "荒", "原", "骨", "哲", "尔沁", "川", "原"],
    "zhongfang_base": ["基地", "据点", "前哨", "站", "库", "区", "港", "实验"],
    "mystic_realm": ["幻", "蜃", "空", "虚", "镜", "禁", "封", "梦"],
}

TONE_WORDS = {
    "grand": ["天", "圣", "神", "太", "上", "昭", "玉", "承"],
    "practical": ["新", "旧", "东", "西", "南", "北", "前", "后"],
    "mysterious": ["幽", "玄", "幻", "虚", "禁", "封", "隐", "迷"],
}

ZHONGFANG_ROOTS = {
    "城市": ["基地", "据点", "前哨", "站", "港", "区"],
    "山岳": ["哨山", "岭", "山", "峰"],
    "水域": ["引水渠", "水站", "港", "湾"],
    "秘境": ["封控区", "试验秘库", "库区", "隔离带"],
    "大陆": ["前线", "防区", "战区", "域"],
}

CATEGORY_ROOTS = {
    "城市": ["城", "都", "镇", "邑", "州", "府", "堡", "寨", "关", "港", "营"],
    "山岳": ["山", "峰", "岭", "岳", "谷", "崖", "峦"],
    "水域": ["海", "湖", "潭", "渊", "江", "河", "溪", "泽", "湾", "洲", "泉"],
    "秘境": ["秘境", "禁地", "遗迹", "洞天", "福地", "遗界", "古战场"],
    "大陆": ["大陆", "域", "界", "天下", "寰宇", "八荒", "九州", "三界"],
}


def _base_pools(data, category, culture, tone):
    base = data.location[category]
    roots = combine_unique(CATEGORY_ROOTS[category], base["roots"])
    tone_words = TONE_WORDS.get(tone, [])

    if culture == "orthodox":
        prefixes = combine_unique(CULTURE_PREFIXES[culture], base["prefixes"], data.sect["righteous_words"], data.shared["celestial"], tone_words)
        modifiers = combine_unique(CULTURE_MODIFIERS[culture], base["modifiers"], data.sect["neutral_words"], data.shared["nature"], tone_words)
    elif culture == "water_trade":
        prefixes = combine_unique(CULTURE_PREFIXES[culture], ["潮", "沧", "烟", "云", "渡", "津"], ["舟", "帆", "商"])
        modifiers = combine_unique(CULTURE_MODIFIERS[culture], ["潮", "湾", "泊", "商", "航", "平码"])
    elif culture == "southern_jungle":
        prefixes = combine_unique(CULTURE_PREFIXES[culture], data.shared["elements"]["木"], ["榕", "藤", "苍", "木", "药"])
        modifiers = combine_unique(CULTURE_MODIFIERS[culture], data.shared["elements"]["木"], ["泽", "林", "岚", "药", "百草", "瘴"])
    elif culture == "northern_tribe":
        prefixes = combine_unique(CULTURE_PREFIXES[culture], ["乌", "兰", "苏", "赫", "塔"], data.shared["beasts"])
        modifiers = combine_unique(CULTURE_MODIFIERS[culture], ["寒", "霜", "雪", "原", "荒"])
    elif culture == "zhongfang_base":
        practical_tone = tone_words if tone == "practical" else []
        prefixes = combine_unique(CULTURE_PREFIXES[culture], ["东", "西", "南", "北", "一号", "二号"], practical_tone)
        modifiers = combine_unique(CULTURE_MODIFIERS[culture], ["实验", "联防", "供能", "巡检"], practical_tone)
        roots = combine_unique(ZHONGFANG_ROOTS[category], roots)
    elif culture == "mystic_realm":
        prefixes = combine_unique(CULTURE_PREFIXES[culture], data.shared["qualities"], ["蜃", "镜", "梦", "空"], tone_words)
        modifiers = combine_unique(CULTURE_MODIFIERS[culture], data.shared["qualities"], ["蜃", "镜", "梦", "虚"], tone_words)
    else:
        prefixes = combine_unique(CULTURE_PREFIXES[culture], base["prefixes"], tone_words)
        modifiers = combine_unique(CULTURE_MODIFIERS[culture], base["modifiers"], tone_words)

    return prefixes, modifiers, roots


def _build_location_name(data, category, culture, tone):
    prefixes, modifiers, roots = _base_pools(data, category, culture, tone)
    prefix = pick_one(prefixes)
    modifier = pick_one(modifiers)
    root = pick_one(roots)

    if category == "秘境":
        if random.random() < 0.5:
            return prefix + modifier + root
        return modifier + root
    if category == "大陆":
        if random.random() < 0.4:
            return prefix + root
        return prefix + modifier + root
    if category == "城市" and culture == "zhongfang_base":
        return prefix + root
    if category == "水域" and random.random() < 0.3:
        return modifier + root
    return prefix + modifier + root


def generate_location_name(category=None, count=1, exclude_existing=True, culture=None, tone="grand"):
    data = NameData()
    existing = scan_existing_entities() if exclude_existing else set()
    culture = culture or "orthodox"
    if culture not in LOCATION_CULTURES:
        raise ValueError(f"不支持的 culture: {culture}")
    category = category or "城市"
    if category not in data.location:
        raise ValueError(f"不支持的 category: {category}")

    def builder():
        rarity_key, rarity_cn = roll_rarity()
        return {
            "name": _build_location_name(data, category, culture, tone),
            "category": category,
            "culture": culture,
            "tone": tone,
            "rarity": rarity_key,
            "rarity_cn": rarity_cn,
        }

    return collect_unique_results(count, builder, existing=existing, max_attempts=max(count * 60, 180))
