#!/usr/bin/env python3
"""
中文小说字数统计工具

统计方式：
- 中文字数：统计所有中文字符（不含标点、空格、换行）
- 总字符数：包含标点的字符数
- 实际字数：符合网文平台统计标准的字数

使用方式：
    python tools/word_counter.py                    # 统计全部章节
    python tools/word_counter.py volumes/vol-01     # 统计指定卷
    python tools/word_counter.py --chapter 11       # 统计指定章节
    python tools/word_counter.py --range 1-10       # 统计章节范围
"""

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple


class WordCount(NamedTuple):
    """字数统计结果"""
    chinese_chars: int  # 中文字符数（不含标点）
    total_chars: int    # 总字符数（含标点）
    platform_count: int # 平台字数（网文平台统计标准）


def count_chinese_words(text: str) -> WordCount:
    """
    统计中文小说字数

    统计规则（符合主流网文平台标准）：
    1. 中文字符：每个汉字算 1 字
    2. 英文/数字：连续的英文或数字算 0.5 字
    3. 标点符号：一般不计入
    4. 空格/换行：不计入
    """
    # 移除空白字符
    text_no_space = re.sub(r'\s+', '', text)

    # 统计中文字符（Unicode 范围：\u4e00-\u9fff）
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text_no_space))

    # 统计英文和数字（连续的算一组）
    english_groups = re.findall(r'[a-zA-Z]+', text_no_space)
    numbers = re.findall(r'[0-9]+', text_no_space)

    # 英文/数字按 0.5 字计算（网文平台常用标准）
    en_num_count = (len(english_groups) + len(numbers)) * 0.5

    # 平台字数 = 中文字符 + 英文/数字折算
    platform_count = int(chinese_chars + en_num_count)

    # 总字符数（不含空白，但含标点）
    total_chars = len(text_no_space)

    return WordCount(
        chinese_chars=chinese_chars,
        total_chars=total_chars,
        platform_count=platform_count
    )


def find_chapter_files(base_path: Path) -> list[Path]:
    """查找所有章节文件"""
    files = []
    # 匹配模式：volumes/vol-XX/chapters/XXX-章节名/正文.md
    for vol_dir in sorted(base_path.glob("volumes/vol-*")):
        for chapter_dir in sorted(vol_dir.glob("chapters/*")):
            content_file = chapter_dir / "正文.md"
            if content_file.exists():
                files.append(content_file)
    return files


def extract_chapter_number(path: Path) -> int:
    """从路径中提取章节编号"""
    match = re.search(r'/(\d+)-', str(path))
    if match:
        return int(match.group(1))
    return 0


def format_count(count: int) -> str:
    """格式化字数显示"""
    if count >= 10000:
        return f"{count/10000:.1f}万"
    return str(count)


def main():
    parser = argparse.ArgumentParser(description="中文小说字数统计")
    parser.add_argument("path", nargs="?", default=".", help="统计路径（默认当前目录）")
    parser.add_argument("--chapter", "-c", type=int, help="统计指定章节")
    parser.add_argument("--range", "-r", type=str, help="统计章节范围（如 1-10）")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示每章详情")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    base_path = Path(args.path)

    # 查找章节文件
    all_files = find_chapter_files(base_path)

    if not all_files:
        print("未找到章节文件", file=sys.stderr)
        sys.exit(1)

    # 过滤章节
    if args.chapter:
        all_files = [f for f in all_files if extract_chapter_number(f) == args.chapter]
    elif args.range:
        try:
            start, end = map(int, args.range.split('-'))
            all_files = [f for f in all_files if start <= extract_chapter_number(f) <= end]
        except ValueError:
            print("范围格式错误，应为：1-10", file=sys.stderr)
            sys.exit(1)

    if not all_files:
        print("未找到匹配的章节", file=sys.stderr)
        sys.exit(1)

    # 统计
    results = []
    total = WordCount(0, 0, 0)

    for file_path in sorted(all_files, key=extract_chapter_number):
        text = file_path.read_text(encoding='utf-8')
        count = count_chinese_words(text)
        results.append({
            "chapter": extract_chapter_number(file_path),
            "path": str(file_path),
            "count": count
        })
        total = WordCount(
            total.chinese_chars + count.chinese_chars,
            total.total_chars + count.total_chars,
            total.platform_count + count.platform_count
        )

    # 输出
    if args.json:
        import json
        output = {
            "total": {
                "chinese_chars": total.chinese_chars,
                "total_chars": total.total_chars,
                "platform_count": total.platform_count,
                "chapter_count": len(results)
            },
            "chapters": results
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        if args.verbose:
            print("=" * 60)
            print(f"{'章节':<8} {'中文字数':<10} {'总字符':<10} {'平台字数':<10}")
            print("=" * 60)
            for r in results:
                c = r["count"]
                print(f"第{r['chapter']:03d}章   {c.chinese_chars:<10} {c.total_chars:<10} {c.platform_count:<10}")
            print("=" * 60)

        print(f"\n📊 字数统计")
        print(f"   章节数量：{len(results)} 章")
        print(f"   中文字数：{format_count(total.chinese_chars)} 字")
        print(f"   总字符数：{format_count(total.total_chars)} 字")
        print(f"   平台字数：{format_count(total.platform_count)} 字（网文平台标准）")

        if len(results) > 1:
            avg = total.platform_count // len(results)
            print(f"   平均每章：{avg} 字")


if __name__ == "__main__":
    main()
