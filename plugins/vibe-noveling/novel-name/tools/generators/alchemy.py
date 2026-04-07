from generator_core import NameData, get_rarity_index, pick_one, roll_rarity, scan_existing_entities, pad_results


def generate_alchemy_name(count=1, exclude_existing=True):
    data = NameData()
    existing = scan_existing_entities() if exclude_existing else set()
    results = []
    attempts = 0
    max_attempts = max(count * 10, 30)
    while len(results) < count and attempts < max_attempts:
        attempts += 1
        rarity_key, rarity_cn = roll_rarity()
        ri = get_rarity_index(rarity_key)
        all_effects = []
        for effect_list in data.alchemy["effects"].values():
            all_effects.extend(effect_list)
        forms = data.alchemy["forms"]
        grade_names = data.alchemy.get("grade_names", [])
        age_prefixes = data.alchemy.get("age_prefixes", [])
        if ri <= 1:
            name = pick_one(all_effects) + pick_one(forms)
        elif ri <= 3:
            quality = pick_one(grade_names[:5])
            name = quality + pick_one(all_effects) + pick_one(forms)
        else:
            age = pick_one(age_prefixes)
            name = age + pick_one(all_effects) + pick_one(forms)
        if not exclude_existing or name not in existing:
            results.append({"name": name, "rarity": rarity_key, "rarity_cn": rarity_cn})
            if exclude_existing:
                existing.add(name)
    return pad_results(results, count)
