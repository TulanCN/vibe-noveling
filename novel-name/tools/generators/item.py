from generator_core import NameData, get_rarity_index, pick_one, roll_rarity, scan_existing_entities, pad_results

ITEM_ORIGINS = ("zhongfang_infra", "cultivation_common", "artifact_rare", "youming_tool")
ITEM_MODEL = {
    "zhongfang_infra": {
        "阵法": {"communication": ["通讯阵", "回讯阵", "联络阵", "讯传阵"], "household": ["净水阵", "照明阵", "取暖阵"], "farming": ["滴灌阵", "催生阵", "护田阵"], "medical": ["补灵阵", "安神阵", "清秽阵"], "military": ["警示阵", "封锁阵", "驱兽阵"], "trade": ["供能阵", "仓储阵", "换电阵"]},
        "器具": {"communication": ["通讯石板", "灵讯匣", "传讯盘"], "household": ["灵能热壶", "净水壶", "照明灯"], "farming": ["滴灌匣", "育苗盘", "测土尺"], "medical": ["补灵匣", "疗伤包", "药温盒"], "military": ["警示牌", "巡检盘", "阵控匣"], "trade": ["换电匣", "储灵箱", "配电盘"]},
        "电池": {"communication": ["通讯电池", "灵讯电池"], "household": ["家用灵池", "热壶电池"], "farming": ["滴灌电池", "田用灵池"], "medical": ["医用灵池", "补灵电池"], "military": ["野战灵池", "巡逻电池"], "trade": ["标准灵池", "储备灵池", "换电电池"]},
        "店铺品牌": {"trade": ["鲁班坊", "灵工坊", "换电坊"], "communication": ["讯联坊", "通灵铺"]},
    },
    "cultivation_common": {"法宝": ["青魄铃", "照岳盘", "引灵佩", "听风珠", "归元镜"], "丹药": ["回春丹", "益气丸", "凝神露", "培元散", "清心丹"], "符箓": ["护身符", "传讯符", "净秽符", "追风符", "定身符"], "材料": ["灵木芯", "寒铁砂", "青玉髓", "赤铜片", "月华露"], "典籍": ["阵法初解", "炼丹手札", "驭兽要录", "静心诀解", "剑道杂录"]},
    "artifact_rare": {"法宝": ["太玄铃", "九曜盘", "照岳钟", "流光伞", "镇海印"], "丹药": ["太清还元丹", "九转凝魄丹", "玉露归元丸"], "符箓": ["天罡护命符", "玄霄遁影符", "太乙镇邪符"], "材料": ["星陨玄铁", "太阴寒髓", "赤霄灵晶"], "典籍": ["上清剑经", "太虚阵典", "九曜真解"]},
    "youming_tool": {"法宝": ["蚀灵针", "冥骨铃", "幽魇幡", "噬魂匣"], "丹药": ["蚀心散", "冥血丸", "噬灵丹"], "符箓": ["幽蚀符", "冥锁符", "摄魂符"], "材料": ["阴蚀骨", "冥血砂", "腐魂晶"], "典籍": ["冥蚀秘录", "噬魂残卷", "幽骨邪典"]},
}


def _generate_artifact_name(subtype_data, data, ri):
    item_words = subtype_data.get("weapons", []) + subtype_data.get("accessories", []) + subtype_data.get("defensive", []) + subtype_data.get("tools", [])
    if ri <= 1:
        return pick_one(item_words)
    if ri <= 2:
        return pick_one(subtype_data.get("prefixes_rare", [])) + pick_one(item_words)
    if ri <= 4:
        return pick_one(data.shared["colors"]) + pick_one(subtype_data.get("prefixes_rare", [])) + pick_one(item_words)
    return pick_one(subtype_data.get("prefixes_legendary", [])) + pick_one(item_words)


def _generate_pill_name(subtype_data, data, ri):
    effects = subtype_data["effects"]
    all_effects = sum(effects.values(), []) if isinstance(effects, dict) else effects
    forms = subtype_data["forms"]
    if ri <= 1:
        return pick_one(all_effects) + pick_one(forms)
    if ri <= 3:
        return pick_one(data.shared["colors"]) + pick_one(all_effects) + pick_one(forms)
    return pick_one(data.alchemy.get("age_prefixes", ["千年"])) + pick_one(all_effects) + pick_one(forms)


def _generate_talisman_name(subtype_data, data, ri):
    effects = subtype_data["effects"]
    forms = subtype_data["forms"]
    if ri <= 1:
        return pick_one(effects) + pick_one(forms[:7])
    if ri <= 3:
        return pick_one(data.shared["colors"]) + pick_one(effects) + pick_one(forms[:7])
    return pick_one(subtype_data.get("materials", ["灵纸"])) + pick_one(effects) + pick_one(forms)


def _generate_material_name(subtype_data, data, ri):
    all_materials = []
    for v in subtype_data.values():
        if isinstance(v, list):
            all_materials.extend(v)
    prefixes = subtype_data.get("quality_prefixes", [])
    if ri <= 1:
        return pick_one(all_materials)
    if ri <= 3:
        return pick_one(prefixes) + pick_one(all_materials)
    return pick_one(data.shared["colors"]) + pick_one(prefixes) + pick_one(all_materials)


def _generate_book_name(subtype_data, data, ri):
    subjects = subtype_data["subjects"]
    forms = subtype_data["forms"]
    prefixes = subtype_data.get("quality_prefixes", [])
    if ri <= 1:
        return pick_one(subjects) + pick_one(forms[:10])
    if ri <= 3:
        return pick_one(prefixes) + pick_one(subjects) + pick_one(forms[:10])
    return pick_one(prefixes) + pick_one(subjects) + pick_one(forms)


def _generate_generic_item_name(subtype_data, data, ri):
    all_words = []
    for v in subtype_data.values():
        if isinstance(v, list):
            all_words.extend(v)
    return pick_one(all_words) if ri <= 1 else pick_one(data.shared["colors"]) + pick_one(all_words)


def generate_item_name(rarity="仙品", count=1, item_type=None, exclude_existing=True, origin=None, usage="trade"):
    data = NameData()
    existing = scan_existing_entities() if exclude_existing else set()
    results = []
    origin = origin or "cultivation_common"
    if origin in ITEM_ORIGINS:
        model = ITEM_MODEL[origin]
        use_types = [item_type] if item_type and item_type in model else list(model.keys())
    else:
        use_types = [item_type] if item_type and item_type in data.item else list(data.item.keys())
    attempts = 0
    max_attempts = max(count * 10, 30)
    while len(results) < count and attempts < max_attempts:
        attempts += 1
        rarity_key, rarity_cn = roll_rarity(force_level=rarity)
        current_type = pick_one(use_types)
        if origin in ITEM_ORIGINS:
            usage_pool = ITEM_MODEL[origin][current_type]
            names = usage_pool.get(usage, sum(usage_pool.values(), [])) if isinstance(usage_pool, dict) else usage_pool
            name = pick_one(names)
        else:
            ri = get_rarity_index(rarity_key)
            subtype_data = data.item[current_type]
            if current_type == "法宝":
                name = _generate_artifact_name(subtype_data, data, ri)
            elif current_type == "丹药":
                name = _generate_pill_name(subtype_data, data, ri)
            elif current_type == "符箓":
                name = _generate_talisman_name(subtype_data, data, ri)
            elif current_type == "材料":
                name = _generate_material_name(subtype_data, data, ri)
            elif current_type == "典籍":
                name = _generate_book_name(subtype_data, data, ri)
            else:
                name = _generate_generic_item_name(subtype_data, data, ri)
        if not exclude_existing or name not in existing:
            results.append({"name": name, "type": current_type, "origin": origin, "usage": usage, "rarity": rarity_key, "rarity_cn": rarity_cn})
            if exclude_existing:
                existing.add(name)
    return pad_results(results, count)
