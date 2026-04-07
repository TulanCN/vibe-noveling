from generator_core import NameData, pick_one, pick_random, roll_rarity, scan_existing_entities

CHARACTER_ORIGINS = ("zhongfang", "cultivator", "villain", "civilian")
CHARACTER_TONES = ("写实", "古雅", "凌厉", "温润")


def _resolve_character_model(char_type="修士", gender="男", style=None, origin=None, tone=None):
    resolved_origin = origin
    resolved_tone = tone
    if not resolved_origin:
        if char_type == "凡人":
            resolved_origin = "civilian"
        elif char_type == "妖族":
            resolved_origin = "villain"
        else:
            resolved_origin = "cultivator"

    if not resolved_tone:
        if style == "古典":
            resolved_tone = "古雅"
        elif style == "霸气":
            resolved_tone = "凌厉"
        elif style == "柔和":
            resolved_tone = "温润"
        elif resolved_origin in ("zhongfang", "civilian"):
            resolved_tone = "写实"
        elif resolved_origin == "villain":
            resolved_tone = "凌厉"
        else:
            resolved_tone = "古雅"
    return resolved_origin, resolved_tone


def _build_character_pool(data, gender, origin, tone):
    source = data.names_female if gender == "女" else data.names_male
    pool = []
    origin_key_map = {
        "zhongfang": "modern",
        "cultivator": "cultivator",
        "villain": "villain",
        "civilian": "civilian",
    }
    pool.extend(source.get(origin_key_map[origin], []))
    tone_key_map = {
        "写实": "tone_grounded",
        "古雅": "tone_refined",
        "凌厉": "tone_sharp",
        "温润": "tone_warm",
    }
    pool.extend(source.get(tone_key_map[tone], []))
    if gender == "女" and tone in ("古雅", "温润"):
        pool.extend(source.get("gentle", []))
        pool.extend(source.get("flora", []))
    if origin == "zhongfang":
        pool.extend(source.get("modern", []))
    return list(dict.fromkeys(pool))


def _build_character_pair_pool(data, gender, origin, tone):
    source = data.names_female if gender == "女" else data.names_male
    pool = []
    origin_key_map = {
        "zhongfang": "modern_pairs",
        "cultivator": "cultivator_pairs",
        "villain": "villain_pairs",
        "civilian": "civilian_pairs",
    }
    base_key = origin_key_map.get(origin)
    if base_key:
        pool.extend(source.get(base_key, []))
    if tone == "温润":
        pool.extend(source.get("modern_pairs", [])[:10])
        pool.extend(source.get("cultivator_pairs", [])[:10])
    elif tone == "古雅":
        pool.extend(source.get("cultivator_pairs", []))
    elif tone == "写实":
        pool.extend(source.get("modern_pairs", []))
    elif tone == "凌厉":
        pool.extend(source.get("villain_pairs", []))
    return list(dict.fromkeys(pool))


def _pick_character_surname(data, origin, total_length, use_compound=False):
    surnames = list(data.surnames["common_surnames"])
    if origin == "zhongfang":
        surnames = data.surnames.get("zhongfang_priority", []) + surnames[:60]
    elif origin == "cultivator":
        surnames = data.surnames.get("cultivator_priority", []) + surnames
    elif origin == "villain":
        surnames = data.surnames.get("villain_priority", []) + data.surnames.get("rare_surnames", []) + surnames
    if use_compound or total_length == 4:
        compound = data.surnames.get("compound_surnames", [])
        if origin in ("cultivator", "villain"):
            compound = data.surnames.get("rare_surnames", []) + compound
        if compound:
            return pick_one(list(dict.fromkeys(compound)))
    return pick_one(list(dict.fromkeys(surnames)))


def _should_use_compound_surname(origin, total_length):
    if total_length != 4:
        return False
    import random
    if origin == "zhongfang":
        return random.random() < 0.85
    if origin == "civilian":
        return random.random() < 0.2
    return random.random() < 0.55


def _dedupe_chars(chars):
    return list(dict.fromkeys(chars))


def _is_awkward_character_name(full_name, surname, given_name, origin):
    if not given_name:
        return True
    if len(set(given_name)) == 1 and len(given_name) > 1:
        return True
    if any(a == b for a, b in zip(given_name, given_name[1:])):
        return True
    forbidden_pairs = ("玄冥", "冥幽", "绝灭", "霸天", "弑神", "狂龙", "血煞")
    if any(pair in full_name for pair in forbidden_pairs):
        return True
    if origin == "zhongfang" and any(ch in set("冥魇煞刹弑") for ch in full_name):
        return True
    if origin == "civilian" and any(ch in set("霄渊魇刃烬") for ch in full_name):
        return True
    return False


def _generate_given_name(pool, total_length, surname, origin, gender, tone):
    given_length = total_length - len(surname)
    if given_length <= 0:
        raise ValueError("姓名总字数必须大于姓氏长度")

    def pick_chars(char_pool, count):
        if origin == "zhongfang" and count == 2:
            first_pool = [ch for ch in char_pool if ch not in "军国伟强福贵财寿"] or char_pool
            second_pool = [ch for ch in char_pool if ch not in "军国建民"] or char_pool
            return pick_one(first_pool) + pick_one(second_pool)
        return "".join(pick_random(char_pool, count))

    if given_length == 1:
        return pick_one(pool)
    if given_length == 2:
        pair_pool = _build_character_pair_pool(NameData(), gender, origin, tone)
        import random
        use_pair_probability = 0.72
        if origin == "cultivator":
            use_pair_probability = 0.9
        elif origin in ("zhongfang", "civilian"):
            use_pair_probability = 0.85
        if pair_pool and random.random() < use_pair_probability:
            for _ in range(20):
                given_name = pick_one(pair_pool)
                if len(given_name) == 2 and not _is_awkward_character_name(surname + given_name, surname, given_name, origin):
                    return given_name
        for _ in range(30):
            given_name = "".join(_dedupe_chars(list(pick_chars(pool, given_length))))
            if len(given_name) == given_length and not _is_awkward_character_name(surname + given_name, surname, given_name, origin):
                return given_name
        return pick_chars(pool, given_length)
    if given_length == 3:
        for _ in range(30):
            given_name = "".join(_dedupe_chars(list(pick_chars(pool, given_length))))
            if len(given_name) == given_length and not _is_awkward_character_name(surname + given_name, surname, given_name, origin):
                return given_name
        return pick_chars(pool, given_length)
    raise ValueError("当前角色名仅支持 2-4 字全名")


def generate_character_name(char_type="修士", count=1, gender="男", style=None,
                            exclude_existing=True, origin=None, tone=None, length=None):
    data = NameData()
    existing = scan_existing_entities() if exclude_existing else set()
    results = []
    resolved_origin, resolved_tone = _resolve_character_model(
        char_type=char_type, gender=gender, style=style, origin=origin, tone=tone
    )
    if resolved_origin not in CHARACTER_ORIGINS:
        raise ValueError(f"不支持的 origin: {resolved_origin}")
    if resolved_tone not in CHARACTER_TONES:
        raise ValueError(f"不支持的 tone: {resolved_tone}")
    if length is not None and length not in (2, 3, 4):
        raise ValueError("角色姓名总字数仅支持 2、3、4")

    attempts = 0
    max_attempts = max(count * 20, 40)
    import random
    while len(results) < count and attempts < max_attempts:
        attempts += 1
        rarity_key, rarity_cn = roll_rarity()
        if length is None:
            if resolved_origin == "zhongfang":
                total_length = random.choices([3, 4], weights=[9, 1])[0]
            elif resolved_origin == "civilian":
                total_length = random.choices([2, 3], weights=[2, 8])[0]
            elif resolved_origin == "villain":
                total_length = random.choices([2, 3, 4], weights=[4, 5, 1])[0]
            else:
                total_length = random.choices([2, 3, 4], weights=[1, 7, 2])[0]
        else:
            total_length = length
        surname = _pick_character_surname(data, resolved_origin, total_length, _should_use_compound_surname(resolved_origin, total_length))
        if len(surname) >= total_length:
            continue
        pool = _build_character_pool(data, gender, resolved_origin, resolved_tone)
        given_name = _generate_given_name(pool, total_length, surname, resolved_origin, gender, resolved_tone)
        full_name = surname + given_name
        if full_name in existing or _is_awkward_character_name(full_name, surname, given_name, resolved_origin):
            continue
        results.append({
            "name": full_name,
            "surname": surname,
            "given_name": given_name,
            "type": char_type,
            "origin": resolved_origin,
            "tone": resolved_tone,
            "length": len(full_name),
            "rarity": rarity_key,
            "rarity_cn": rarity_cn,
        })
        existing.add(full_name)
    return results
