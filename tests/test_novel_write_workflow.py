import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text()
WRITER_ZHOUZI = (ROOT / "plugins/vibe-noveling/agents/writer-zhouzi.md").read_text()
WRITER_DAZHONGMA = (ROOT / "plugins/vibe-noveling/agents/writer-dazhongma.md").read_text()
CONTEXT_COLLECTOR = (ROOT / "plugins/vibe-noveling/agents/context-collector.md").read_text()
WRITE_SKILL = (ROOT / "plugins/vibe-noveling/skills/novel-write/SKILL.md").read_text()
EVENT_CANVAS = (ROOT / "plugins/vibe-noveling/skills/novel-discuss/references/event-canvas.md").read_text()


class NovelWriteWorkflowTests(unittest.TestCase):
    def test_readme_no_longer_mentions_write_stage_ssot_for_writers(self):
        self.assertNotIn("writer 先用 SSoT 为 20 个剧情点做章内分布规划", README)
        self.assertNotIn("writer 在章内用 SSoT 先做分布规划", README)

    def test_writer_agents_no_longer_embed_write_stage_ssot_contract(self):
        for content in (WRITER_ZHOUZI, WRITER_DAZHONGMA):
            self.assertNotIn("SSoT 章内防趋同执行规约", content)
            self.assertNotIn("四层分布规划", content)
            self.assertNotIn("先分桶，再写作", content)

    def test_novel_write_no_longer_uses_html_confirmation(self):
        """novel-write 不再使用 HTML 确认和 Opus 试写"""
        self.assertNotIn("chapter-plan-viewer.html", WRITE_SKILL)
        self.assertNotIn("Opus试写", WRITE_SKILL)
        self.assertNotIn("HTML 确认", WRITE_SKILL)

    def test_skill_md_mentions_scene_chain_format(self):
        self.assertIn("场景链", WRITE_SKILL)
        self.assertIn("<环境> [动机]（动作）结果", WRITE_SKILL)

    def test_chapter_directory_uses_event_based_numbering(self):
        """章节目录使用 E{event_num}-{seq} 事件级编号"""
        new_convention = "chapters/e{event_padded}/ch-{chapter_seq}"
        old_convention = "chapters/vol-{v}/ch-{c}"
        for content, name in [
            (WRITE_SKILL, "novel-write/SKILL.md"),
            (CONTEXT_COLLECTOR, "context-collector.md"),
        ]:
            self.assertIn(new_convention, content, f"{name}: 缺少新目录约定 {new_convention}")
            self.assertNotIn(old_convention, content, f"{name}: 仍包含旧目录约定 {old_convention}")

    def test_event_canvas_has_scene_chain_in_chapter_split(self):
        """事件画布章节拆分直接产出场景链"""
        self.assertIn("章节拆分", EVENT_CANVAS)
        self.assertIn("场景链", EVENT_CANVAS)
        self.assertIn("<环境> [动机]（动作）结果", EVENT_CANVAS)
        self.assertIn("E{num}-0", EVENT_CANVAS)

    def test_novel_plan_no_longer_exists(self):
        """novel-plan 已合并到 event-canvas + novel-write"""
        plan_skill = ROOT / "plugins/vibe-noveling/skills/novel-plan"
        self.assertFalse(plan_skill.exists(), "novel-plan 目录应该已被删除")


if __name__ == "__main__":
    unittest.main()
