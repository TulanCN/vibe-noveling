import random

from generator_core import NameData, collect_unique_results, combine_unique, pick_one, roll_rarity, scan_existing_entities

FACTION_KINDS = ("宗门", "宫阙", "山门", "联盟", "城邦", "族群", "现代组织", "邪教")
FACTION_ORIGINS = ("orthodox", "commercial", "northern", "zhongfang", "youming")

KIND_SUFFIXES = {
    "宗门": ["宗", "门", "派", "府", "阁", "观"],
    "宫阙": ["宫", "殿", "阙", "府"],
    "山门": ["山门", "峰", "岭", "谷", "山"],
    "联盟": ["盟", "会", "联"],
    "城邦": ["城", "堡", "寨", "垣", "府"],
    "族群": ["部", "族", "氏", "裔"],
    "现代组织": ["署", "处", "局", "部", "院", "所", "团", "司", "会"],
    "邪教": ["教", "宗", "会", "殿", "门"],
}

DOMAIN_WORDS = {
    "general": [],
    "war": ["镇", "锋", "卫", "巡", "征", "戍", "守"],
    "trade": ["商", "市", "通", "贸", "汇", "运", "行"],
    "craft": ["工", "铸", "造", "机", "巧", "营"],
    "knowledge": ["文", "典", "策", "律", "学", "衡"],
    "medical": ["药", "医", "灵", "养", "济", "和"],
}

ZHONGFANG_REGION_WORDS = ["函谷", "河洛", "安澜", "东岭", "前线", "北港", "南川"]
ZHONGFANG_CORE_WORDS = ["工程", "联防", "后勤", "巡检", "通讯", "供能", "转运", "开拓", "协作", "拓荒"]
COMMERCIAL_WORDS = ["商", "市", "舟", "平码", "云帆", "鲁班", "宝", "丰", "源", "衡", "汇", "通"]
NORTHERN_WORDS = ["寒", "霜", "雪", "冰", "狼", "乌兰", "塔", "阿尔沁", "荒", "原", "骨", "北境"]
YOUMING_WORDS = ["幽", "冥", "蚀", "魇", "骨", "渊", "黄泉", "夜", "厄", "噬"]


def _choose_origin_pools(data, origin, domain):
    domain_words = DOMAIN_WORDS.get(domain, [])
    if origin == "zhongfang":
        primary = combine_unique(ZHONGFANG_REGION_WORDS, ZHONGFANG_CORE_WORDS, domain_words)
        secondary = combine_unique(domain_words, ZHONGFANG_CORE_WORDS, ["甲", "营", "站", "务", "协"])
        place = combine_unique(["岭", "港", "哨", "垒", "站", "区"], data.sect["place_words"])
    elif origin == "commercial":
        primary = combine_unique(COMMERCIAL_WORDS, domain_words, data.sect["neutral_words"], data.shared["materials"])
        secondary = combine_unique(domain_words, ["宝", "平码", "云帆", "商", "衡", "利", "源", "通"])
        place = combine_unique(["港", "渡", "埠", "平码", "津"], data.sect["place_words"])
    elif origin == "northern":
        primary = combine_unique(NORTHERN_WORDS, data.sect["neutral_words"], data.shared["beasts"])
        secondary = combine_unique(domain_words, ["狼", "霜", "雪", "乌", "兰", "荒", "原"])
        place = combine_unique(["原", "荒", "岭", "峰", "泽"], data.sect["place_words"])
    elif origin == "youming":
        primary = combine_unique(YOUMING_WORDS, data.sect["demonic_words"], domain_words)
        secondary = combine_unique(["夜", "鬼", "血", "骨", "渊", "狱"], data.sect["demonic_words"], domain_words)
        place = combine_unique(["渊", "谷", "殿", "窟", "城"], data.sect["place_words"])
    else:
        primary = combine_unique(data.sect["righteous_words"], data.shared["celestial"], domain_words)
        secondary = combine_unique(data.sect["neutral_words"], data.shared["nature"], data.shared["qualities"], domain_words)
        place = combine_unique(["霄", "岳", "霞", "岚", "月", "星"], data.sect["place_words"])
    return primary, secondary, place


def _build_faction_name(data, kind, origin, domain):
    primary, secondary, place = _choose_origin_pools(data, origin, domain)
    suffix = pick_one(KIND_SUFFIXES[kind])

    if kind == "现代组织":
        head = pick_one(primary)
        middle_pool = combine_unique(secondary, ZHONGFANG_CORE_WORDS if origin == "zhongfang" else COMMERCIAL_WORDS)
        middle = pick_one(middle_pool)
        name = head + middle + suffix
    elif kind == "族群":
        head = pick_one(primary)
        if random.random() < 0.5:
            head += pick_one(combine_unique(secondary, data.shared["beasts"]))
        name = head + suffix
    elif kind == "城邦":
        first = pick_one(combine_unique(primary, place))
        second = pick_one(combine_unique(secondary, place))
        name = first + second + suffix
    elif kind == "联盟":
        first = pick_one(primary)
        if random.random() < 0.4:
            first += pick_one(combine_unique(secondary, place))
        name = first + suffix
    elif kind == "山门":
        first = pick_one(combine_unique(primary, secondary))
        second = pick_one(place)
        name = first + second if suffix in {"峰", "岭", "谷", "山"} else first + second + suffix
    else:
        first = pick_one(primary)
        second = pick_one(combine_unique(secondary, place))
        name = first + second + suffix

    if len(name) > 1 and name[-2:] == suffix * 2:
        name = name[:-len(suffix)]
    return name


def generate_faction_name(kind="宗门", origin="orthodox", domain="general", count=1, exclude_existing=True):
    data = NameData()
    existing = scan_existing_entities() if exclude_existing else set()
    if origin not in FACTION_ORIGINS:
        raise ValueError(f"不支持的 faction origin: {origin}")
    if kind not in FACTION_KINDS:
        raise ValueError(f"不支持的 faction kind: {kind}")

    def builder():
        rarity_key, rarity_cn = roll_rarity()
        return {
            "name": _build_faction_name(data, kind, origin, domain),
            "kind": kind,
            "origin": origin,
            "domain": domain,
            "rarity": rarity_key,
            "rarity_cn": rarity_cn,
        }

    return collect_unique_results(count, builder, existing=existing, max_attempts=max(count * 60, 180))


def generate_sect_name(style="正道", count=1, exclude_existing=True, kind="宗门", origin=None, domain="general"):
    if origin is None:
        if style == "魔道":
            origin = "youming"
            kind = "邪教"
        elif style == "中立":
            origin = "commercial"
            kind = "城邦"
        else:
            origin = "orthodox"
    return generate_faction_name(kind=kind, origin=origin, domain=domain, count=count, exclude_existing=exclude_existing)
