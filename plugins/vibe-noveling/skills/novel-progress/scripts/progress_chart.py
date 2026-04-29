#!/usr/bin/env python3
from __future__ import annotations

"""小说创作进度可视化 — 扫描项目文件，生成字数占比饼图 HTML。"""

import argparse
import math
import os
import re
import webbrowser
from pathlib import Path

# 项目根目录（此脚本位于 plugins/vibe-noveling/skills/novel-progress/scripts/）
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent

# 文件分类规则：(分类名, glob_pattern 列表)
CATEGORIES = [
    ("大纲", ["chapters/vol-*/ch-*/大纲.md"]),
    ("设定文件", ["memory/**/*.md"]),
    ("正文", ["chapters/vol-*/ch-*/正文.md"]),
]

# 正文分类需要排除的文件（避免被大纲文件误匹配）
EXCLUDE_PATTERNS = ["大纲.md"]

# 饼图配色
COLORS = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336", "#00BCD4", "#795548"]

# Markdown 语法标记（不计入字数）
MD_MARKERS = re.compile(r"^#{1,6}\s|^[-*+>]\s|^\|.*\|[-:|]*$|^---$|`{1,3}[^`]*`{1,3}|\*{1,3}[^*]*\*{1,3}")


def count_chars(filepath: Path) -> int:
    """统计文件中的有效字数（中文字符 + 标点 + 数字 + 英文字母，排除 Markdown 语法和空白）。"""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return 0

    # 跳过 YAML frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            text = text[end + 3:]

    count = 0
    for line in text.splitlines():
        stripped = MD_MARKERS.sub("", line).strip()
        for ch in stripped:
            if ch.isspace():
                continue
            # 计数所有非空白、非 Markdown 语法字符
            count += 1
    return count


def classify_file(filepath: Path) -> str | None:
    """判断文件属于哪个分类，返回分类名或 None。"""
    rel = filepath.relative_to(PROJECT_ROOT).as_posix()

    # 正文分类：匹配分卷/分章目录下的 正文.md
    if re.match(r"chapters/vol-\d+/ch-\d+/正文\.md$", rel):
        return "正文"

    # 大纲分类
    if re.match(r"chapters/vol-\d+/ch-\d+/大纲\.md$", rel):
        return "大纲"

    # 设定文件分类
    if rel.startswith("memory/") and rel.endswith(".md"):
        return "设定文件"
    if re.match(r"chapters/vol-\d+/ch-\d+/上下文\.md$", rel):
        return "设定文件"

    return None


def scan_project() -> dict[str, list[tuple[str, int]]]:
    """扫描项目，返回 {分类名: [(文件名, 字数), ...]}。"""
    result: dict[str, list[tuple[str, int]]] = {}

    for root, _dirs, files in os.walk(PROJECT_ROOT):
        # 跳过隐藏目录、node_modules、.venv 等
        parts = Path(root).relative_to(PROJECT_ROOT).parts
        if any(p.startswith(".") or p in ("node_modules", "__pycache__", ".venv") for p in parts):
            continue

        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = Path(root) / fname
            category = classify_file(fpath)
            if category is None:
                continue

            char_count = count_chars(fpath)
            if char_count == 0:
                continue

            rel_name = fpath.relative_to(PROJECT_ROOT).as_posix()
            result.setdefault(category, []).append((rel_name, char_count))

    return result


def generate_html(data: dict[str, list[tuple[str, int]]]) -> str:
    """根据统计数据生成完整的 HTML 页面。"""

    # 汇总
    categories = []
    total = 0
    for cat_name, files in data.items():
        cat_total = sum(c for _, c in files)
        categories.append((cat_name, cat_total, files))
        total += cat_total

    # 排序：字数多的在前
    categories.sort(key=lambda x: x[1], reverse=True)

    # 生成饼图 SVG 路径
    def pie_path(data_points, cx, cy, r):
        """生成 SVG pie chart path。"""
        paths = []
        start_angle = -math.pi / 2  # 从 12 点方向开始
        for i, (label, value, _) in enumerate(data_points):
            if value == 0:
                continue
            angle = (value / total) * 2 * math.pi
            end_angle = start_angle + angle

            x1 = cx + r * math.cos(start_angle)
            y1 = cy + r * math.sin(start_angle)
            x2 = cx + r * math.cos(end_angle)
            y2 = cy + r * math.sin(end_angle)

            large_arc = 1 if angle > math.pi else 0

            d = f"M {cx} {cy} L {x1:.2f} {y1:.2f} A {r} {r} 0 {large_arc} 1 {x2:.2f} {y2:.2f} Z"
            color = COLORS[i % len(COLORS)]
            pct = value / total * 100

            paths.append(f'<path d="{d}" fill="{color}" stroke="white" stroke-width="2"/>')

            # 标签位置
            mid_angle = start_angle + angle / 2
            label_r = r * 0.65
            lx = cx + label_r * math.cos(mid_angle)
            ly = cy + label_r * math.sin(mid_angle)

            label_text = f"{label}\n{value:,}字 ({pct:.1f}%)"
            paths.append(
                f'<text x="{lx:.2f}" y="{ly:.2f}" text-anchor="middle" dominant-baseline="central" '
                f'fill="white" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">'
                f'<tspan x="{lx:.2f}" dy="-0.6em">{label}</tspan>'
                f'<tspan x="{lx:.2f}" dy="1.2em">{value:,}字 ({pct:.1f}%)</tspan>'
                f"</text>"
            )

            start_angle = end_angle
        return "\n    ".join(paths)

    pie_svg = pie_path(categories, 150, 150, 120)

    # 详细表格行
    table_rows = []
    for idx, (cat_name, cat_total, files) in enumerate(categories):
        pct = cat_total / total * 100 if total > 0 else 0
        color = COLORS[idx % len(COLORS)]
        file_count = len(files)
        file_lines = "\n".join(
            f'<tr class="detail-row" data-cat="{idx}"><td>{f}</td><td class="num">{c:,}</td></tr>'
            for f, c in sorted(files, key=lambda x: x[1], reverse=True)
        )
        table_rows.append(
            f"""
        <tr class="category-row" onclick="toggle({idx})" style="cursor:pointer">
            <td colspan="2">
                <span class="color-dot" style="background:{color}"></span>
                <strong>{cat_name}</strong>
                <span class="pct">{pct:.1f}%</span>
                <span class="file-count">{file_count} 个文件</span>
                <span class="arrow" id="arrow-{idx}">&#9654;</span>
            </td>
            <td class="num">{cat_total:,}</td>
        </tr>
        {file_lines}"""
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>小说创作进度</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        font-family: system-ui, -apple-system, sans-serif;
        background: #f8f9fa;
        color: #333;
        padding: 2rem;
    }}
    .container {{ max-width: 800px; margin: 0 auto; }}
    h1 {{
        text-align: center;
        margin-bottom: 2rem;
        font-size: 1.8rem;
        color: #1a1a1a;
    }}
    .summary {{
        text-align: center;
        margin-bottom: 2rem;
        font-size: 1.1rem;
        color: #666;
    }}
    .summary strong {{ color: #333; font-size: 1.4rem; }}
    .chart-section {{
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    th {{
        background: #f0f0f0;
        padding: 0.75rem 1rem;
        text-align: left;
        font-weight: 600;
        font-size: 0.9rem;
        color: #666;
    }}
    th:last-child {{ text-align: right; }}
    td {{ padding: 0.5rem 1rem; border-top: 1px solid #f0f0f0; font-size: 0.95rem; }}
    td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
    .category-row td {{ padding: 0.75rem 1rem; background: #fafafa; font-size: 1rem; }}
    .detail-row {{ display: none; }}
    .detail-row td {{ padding: 0.4rem 1rem 0.4rem 2.5rem; color: #888; font-size: 0.85rem; }}
    .color-dot {{
        display: inline-block;
        width: 12px; height: 12px;
        border-radius: 50%;
        margin-right: 0.5rem;
        vertical-align: middle;
    }}
    .pct {{
        float: right;
        color: #999;
        font-weight: normal;
        font-size: 0.9rem;
    }}
    .file-count {{
        color: #bbb;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }}
    .arrow {{
        float: right;
        color: #ccc;
        font-size: 0.7rem;
        margin-right: 0.3rem;
        transition: transform 0.2s;
        display: inline-block;
    }}
    .arrow.open {{ transform: rotate(90deg); }}
</style>
</head>
<body>
<div class="container">
    <h1>小说创作进度</h1>
    <div class="summary">总计 <strong>{total:,}</strong> 字</div>
    <div class="chart-section">
        <svg width="300" height="300" viewBox="0 0 300 300">
            {pie_svg}
        </svg>
    </div>
    <table>
        <thead><tr><th>文件</th><th></th><th>字数</th></tr></thead>
        <tbody>
            {''.join(table_rows)}
        </tbody>
    </table>
</div>
<script>
function toggle(catId) {{
    var rows = document.querySelectorAll('.detail-row[data-cat="' + catId + '"]');
    var arrow = document.getElementById('arrow-' + catId);
    var visible = rows[0] && rows[0].style.display !== 'none';
    rows.forEach(function(r) {{ r.style.display = visible ? 'none' : 'table-row'; }});
    arrow.classList.toggle('open');
}}
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="小说创作进度可视化")
    parser.add_argument("--output", "-o", default=None, help="输出 HTML 路径（默认：项目根目录 progress.html）")
    parser.add_argument("--open", default="true", choices=["true", "false"], help="是否自动打开浏览器")
    args = parser.parse_args()

    data = scan_project()

    if not data:
        print("未找到任何可统计的文件。")
        return

    html = generate_html(data)

    output_path = Path(args.output) if args.output else PROJECT_ROOT / "progress.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"进度报告已生成：{output_path}")

    if args.open == "true":
        webbrowser.open(f"file://{output_path}")


if __name__ == "__main__":
    main()
