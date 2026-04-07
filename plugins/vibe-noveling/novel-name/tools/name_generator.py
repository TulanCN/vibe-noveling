#!/usr/bin/env python3
"""CLI entrypoint for novel-name generators."""

import argparse
import json
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from generators import (
    CHARACTER_ORIGINS,
    CHARACTER_TONES,
    CREATURE_BIOMES,
    DAO_ORIGINS,
    FACTION_KINDS,
    FACTION_ORIGINS,
    ITEM_ORIGINS,
    LOCATION_CULTURES,
    TECHNIQUE_ORIGINS,
    generate_alchemy_name,
    generate_character_name,
    generate_creature_name,
    generate_dao_name,
    generate_faction_name,
    generate_item_name,
    generate_location_name,
    generate_sect_name,
    generate_technique_name,
)

__all__ = [
    "generate_character_name",
    "generate_technique_name",
    "generate_faction_name",
    "generate_sect_name",
    "generate_item_name",
    "generate_location_name",
    "generate_dao_name",
    "generate_creature_name",
    "generate_alchemy_name",
]


def build_parser():
    parser = argparse.ArgumentParser(
        description="修真小说命名生成器 v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python name_generator.py character --origin zhongfang --gender 男 --length 3 --count 5
  python name_generator.py technique --origin zhongfang --element 土 --category defense --count 5
  python name_generator.py faction --kind 现代组织 --origin zhongfang --count 5
  python name_generator.py item --origin zhongfang_infra --item-type 阵法 --usage communication --count 5
  python name_generator.py creature --biome corrupted --count 5
  python name_generator.py location --culture northern_tribe --category 城市 --count 5
  python name_generator.py alchemy --count 5
  python name_generator.py dao --origin youming --tone ominous --count 5
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="生成类型")

    p = subparsers.add_parser("character", help="生成角色名")
    p.add_argument("--type", choices=["修士", "凡人", "妖族"], default="修士")
    p.add_argument("--gender", choices=["男", "女"], default="男")
    p.add_argument("--style", choices=["古典", "霸气", "柔和"], default=None)
    p.add_argument("--origin", choices=list(CHARACTER_ORIGINS), default=None)
    p.add_argument("--tone", choices=list(CHARACTER_TONES), default=None)
    p.add_argument("--length", type=int, choices=[2, 3, 4], default=None)
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--exclude-existing", action="store_true", default=True)
    p.add_argument("--allow-existing", action="store_true")

    p = subparsers.add_parser("technique", help="生成功法名")
    p.add_argument("--origin", choices=list(TECHNIQUE_ORIGINS), default="traditional")
    p.add_argument("--element", choices=["金", "木", "水", "火", "土", "暗", "空间", "通用"], default=None)
    p.add_argument("--category", choices=["attack", "defense", "movement", "utility", "formation"], default="attack")
    p.add_argument("--length", choices=["short", "medium"], default="medium")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--exclude-existing", action="store_true", default=True)
    p.add_argument("--allow-existing", action="store_true")

    p = subparsers.add_parser("sect", help="生成门派名")
    p.add_argument("--style", choices=["正道", "魔道", "中立"], default="正道")
    p.add_argument("--kind", choices=list(FACTION_KINDS), default="宗门")
    p.add_argument("--origin", choices=list(FACTION_ORIGINS), default=None)
    p.add_argument("--domain", default="general")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--exclude-existing", action="store_true", default=True)
    p.add_argument("--allow-existing", action="store_true")

    p = subparsers.add_parser("faction", help="生成势力/组织名")
    p.add_argument("--kind", choices=list(FACTION_KINDS), default="宗门")
    p.add_argument("--origin", choices=list(FACTION_ORIGINS), default="orthodox")
    p.add_argument("--domain", default="general")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--exclude-existing", action="store_true", default=True)
    p.add_argument("--allow-existing", action="store_true")

    p = subparsers.add_parser("item", help="生成物品名")
    p.add_argument("--rarity", default="灵品")
    p.add_argument("--origin", choices=list(ITEM_ORIGINS), default="cultivation_common")
    p.add_argument("--item-type", choices=["法宝", "丹药", "符箓", "材料", "典籍", "阵法", "器具", "电池", "店铺品牌"], default=None)
    p.add_argument("--usage", choices=["household", "military", "trade", "farming", "medical", "communication"], default="trade")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--exclude-existing", action="store_true", default=True)
    p.add_argument("--allow-existing", action="store_true")

    p = subparsers.add_parser("creature", help="生成灵兽名")
    p.add_argument("--category", choices=["草木", "鱼", "兽", "鸟", "虫", "爬虫"], default=None)
    p.add_argument("--biome", choices=list(CREATURE_BIOMES), default="mountain")
    p.add_argument("--rank", choices=["common", "spirit", "rare", "ancient"], default="common")
    p.add_argument("--temper", choices=["gentle", "predatory", "ominous"], default="gentle")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--exclude-existing", action="store_true", default=True)
    p.add_argument("--allow-existing", action="store_true")

    p = subparsers.add_parser("location", help="生成地点名")
    p.add_argument("--category", choices=["城市", "山岳", "水域", "秘境", "大陆"], default=None)
    p.add_argument("--culture", choices=list(LOCATION_CULTURES), default="orthodox")
    p.add_argument("--tone", choices=["grand", "practical", "mysterious"], default="grand")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--exclude-existing", action="store_true", default=True)
    p.add_argument("--allow-existing", action="store_true")

    p = subparsers.add_parser("alchemy", help="生成丹药名")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--exclude-existing", action="store_true", default=True)
    p.add_argument("--allow-existing", action="store_true")

    p = subparsers.add_parser("dao", help="生成法号/道号名")
    p.add_argument("--gender", choices=["男", "女"], default="男")
    p.add_argument("--origin", choices=list(DAO_ORIGINS), default="orthodox")
    p.add_argument("--tone", choices=["dignified", "aloof", "gentle", "ominous"], default="dignified")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--exclude-existing", action="store_true", default=True)
    p.add_argument("--allow-existing", action="store_true")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    exclude = not getattr(args, "allow_existing", False)
    if args.command == "character":
        results = generate_character_name(char_type=args.type, count=args.count, gender=args.gender, style=args.style, exclude_existing=exclude, origin=args.origin, tone=args.tone, length=args.length)
    elif args.command == "technique":
        results = generate_technique_name(element=args.element, count=args.count, exclude_existing=exclude, origin=args.origin, category=args.category, length=args.length)
    elif args.command == "sect":
        results = generate_sect_name(style=args.style, count=args.count, exclude_existing=exclude, kind=args.kind, origin=args.origin, domain=args.domain)
    elif args.command == "faction":
        results = generate_faction_name(kind=args.kind, origin=args.origin, domain=args.domain, count=args.count, exclude_existing=exclude)
    elif args.command == "item":
        results = generate_item_name(rarity=args.rarity, count=args.count, item_type=args.item_type, exclude_existing=exclude, origin=args.origin, usage=args.usage)
    elif args.command == "creature":
        results = generate_creature_name(category=args.category, count=args.count, exclude_existing=exclude, biome=args.biome, rank=args.rank, temper=args.temper)
    elif args.command == "location":
        results = generate_location_name(category=args.category, count=args.count, exclude_existing=exclude, culture=args.culture, tone=args.tone)
    elif args.command == "alchemy":
        results = generate_alchemy_name(count=args.count, exclude_existing=exclude)
    elif args.command == "dao":
        results = generate_dao_name(count=args.count, gender=args.gender, exclude_existing=exclude, origin=args.origin, tone=args.tone)
    else:
        parser.print_help()
        sys.exit(1)

    output = {
        "command": args.command,
        "params": {k: v for k, v in vars(args).items() if k not in ("command", "exclude_existing", "allow_existing") and v is not None},
        "results": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
