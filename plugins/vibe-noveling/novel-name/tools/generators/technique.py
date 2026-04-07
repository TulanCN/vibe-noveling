from generator_core import NameData, pick_one, roll_rarity, scan_existing_entities, pad_results

TECHNIQUE_ORIGINS = ("zhongfang", "youming", "traditional")

ZHONGFANG_TECHNIQUE_STEMS = {
    "attack": {"金": ["裂锋", "断金", "破甲", "锋切"], "木": ["缠藤", "木刺", "束枝", "裂蔓"], "水": ["激流", "寒潮", "破浪", "凝汐"], "火": ["爆炎", "炽焰", "燃火", "灼流"], "土": ["裂地", "落岩", "崩丘", "震岳"], "空间": ["裂空", "折域", "断界"], "暗": ["镇影", "压煞"], "通用": ["强袭", "突击", "破障"]},
    "defense": {"金": ["固甲", "坚锋", "御刃"], "木": ["护藤", "木障", "生壁"], "水": ["水幕", "凝冰", "护潮"], "火": ["炎幕", "热障", "燃盾"], "土": ["坚壁", "固岩", "镇岳", "厚土"], "空间": ["界障", "折幕"], "暗": ["蔽影", "沉幕"], "通用": ["护体", "稳元", "防冲"]},
    "movement": {"金": ["迅锋", "疾掠"], "木": ["穿林", "踏枝"], "水": ["踏浪", "浮波", "流身"], "火": ["焰步", "流火"], "土": ["移岩", "遁地", "踏岳"], "空间": ["折空", "跃界", "短移"], "暗": ["潜影", "遁影"], "通用": ["疾行", "轻身", "瞬步"]},
    "utility": {"金": ["锐感", "辨矿"], "木": ["催生", "植养", "养木"], "水": ["净水", "聚流", "润泽"], "火": ["控温", "点火", "熔炼"], "土": ["稳基", "整地", "筑台"], "空间": ["纳物", "缩距", "定点"], "暗": ["匿息", "遮感"], "通用": ["补灵", "稳神", "通讯", "照明"]},
    "formation": {"金": ["警戒", "封锁"], "木": ["催生", "育苗"], "水": ["净水", "滴灌"], "火": ["供热", "照明"], "土": ["固阵", "筑基"], "空间": ["传送", "定位"], "暗": ["隐匿", "遮蔽"], "通用": ["通讯", "补灵", "供能", "驱兽"]},
}
TRADITIONAL_TECHNIQUE = {"prefixes": ["清霄", "归元", "玄衡", "太虚", "青岚", "凌霄", "昭月", "苍梧", "流云", "听雪"], "attack": ["剑诀", "刀法", "掌法", "拳经", "指诀"], "defense": ["心法", "护体诀", "罡气法", "御守诀"], "movement": ["步", "身法", "遁法", "游诀"], "utility": ["养神诀", "静心法", "观息诀", "归元法"], "formation": ["阵经", "阵图", "布阵诀", "结界法"]}
YOUMING_TECHNIQUE = {"attack": ["火弹", "骨刃", "蚀刺", "冥手", "噬魂爪"], "defense": ["冥幕", "阴障", "骨盾", "暗壳"], "movement": ["潜行", "遁影", "幽步", "暗跃"], "utility": ["蚀灵咒", "摄魂术", "蔽息法", "腐心诀"], "formation": ["噬阵", "蚀界", "幽封", "冥锁"]}


def _normalize_element(element):
    return element if element in {"金", "木", "水", "火", "土", "暗", "空间", "通用"} else "通用"


def generate_technique_name(element=None, count=1, exclude_existing=True, origin="traditional", category="attack", length="medium"):
    existing = scan_existing_entities() if exclude_existing else set()
    results = []
    if origin not in TECHNIQUE_ORIGINS:
        raise ValueError(f"不支持的 technique origin: {origin}")
    element = _normalize_element(element)
    attempts = 0
    max_attempts = max(count * 10, 30)
    while len(results) < count and attempts < max_attempts:
        attempts += 1
        rarity_key, rarity_cn = roll_rarity()
        if origin == "zhongfang":
            stems = ZHONGFANG_TECHNIQUE_STEMS.get(category, ZHONGFANG_TECHNIQUE_STEMS["attack"])
            stem = pick_one(stems.get(element, stems["通用"]))
            suffix = pick_one(["术", "法", "诀"] if length == "short" else ["术", "法", "诀", "阵法"])
            name = stem + suffix
        elif origin == "youming":
            prefix = pick_one(["幽", "冥", "暗"])
            core = pick_one(YOUMING_TECHNIQUE.get(category, YOUMING_TECHNIQUE["attack"]))
            suffix = "" if core.endswith(("术", "法", "诀", "弹", "手", "爪")) else pick_one(["术", "法", "诀", "咒"])
            name = prefix + core + suffix
        else:
            prefix = pick_one(TRADITIONAL_TECHNIQUE["prefixes"])
            suffix = pick_one(TRADITIONAL_TECHNIQUE.get(category, TRADITIONAL_TECHNIQUE["attack"]))
            name = prefix + suffix
        if not exclude_existing or name not in existing:
            results.append({"name": name, "element": element, "origin": origin, "category": category, "rarity": rarity_key, "rarity_cn": rarity_cn})
            if exclude_existing:
                existing.add(name)
    return pad_results(results, count)
