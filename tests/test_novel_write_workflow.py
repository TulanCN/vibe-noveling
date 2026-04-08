import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NOVEL_PLAN = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-plan" / "SKILL.md"
NOVEL_WRITE = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-write" / "SKILL.md"
NOVEL_MASTER = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-master" / "SKILL.md"
README = REPO_ROOT / "README.md"


class NovelWriteWorkflowTests(unittest.TestCase):
    def test_novel_plan_uses_concise_third_person_outline(self) -> None:
        content = NOVEL_PLAN.read_text(encoding="utf-8")

        self.assertIn("第三人称精简剧情纲要", content)
        self.assertIn("不再输出剧情点切分", content)
        self.assertNotIn("将选定的方案细切为 10-20 个剧情点", content)
        self.assertNotIn("> ✏️ 写作提示", content)

    def test_novel_write_defaults_to_all_styles(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")

        self.assertIn("默认创作全部 4 种写作风格", content)
        self.assertIn("按风格逐个开启写作 Agent", content)
        self.assertIn("自动合并生成最终稿", content)
        self.assertNotIn("默认并行创作全部 4 种写作风格", content)
        self.assertNotIn("为每种风格 dispatch 一个 `general-purpose` Agent，并行写作。", content)
        self.assertNotIn("用户选择 2-3 种写作风格", content)
        self.assertNotIn("用户手动合并最终稿", content)

    def test_novel_write_derives_internal_units_and_outputs_continuous_chapter(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")

        self.assertIn("先在正文阶段内部切分写作单元", content)
        self.assertIn("写作单元只供写作阶段使用，不回写 outline", content)
        self.assertIn("最终稿输出为连续章节正文", content)
        self.assertNotIn("最终合并稿也必须保留剧情点切分", content)

    def test_novel_write_merges_final_draft_unit_by_unit(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")

        self.assertIn("按内部写作单元顺序逐个合并", content)
        self.assertIn("每次只处理当前写作单元在 4 个风格版本中的对应内容", content)
        self.assertIn("当前写作单元合并完成后，再进入下一个写作单元", content)
        self.assertIn("最终稿输出为连续章节正文", content)

    def test_readme_describes_concise_outline_and_internal_splitting(self) -> None:
        content = README.read_text(encoding="utf-8")

        self.assertIn("默认全风格逐个启动写作 Agent + 自动合并", content)
        self.assertIn("按内部写作单元逐个合并", content)
        self.assertIn("自动合并生成最终稿", content)
        self.assertIn("精简剧情纲要", content)
        self.assertIn("正文阶段内部切分", content)
        self.assertNotIn("默认全风格并行写作 + 自动合并", content)
        self.assertNotIn("场景化大纲", content)

    def test_novel_master_adds_postwrite_style_correction_rules(self) -> None:
        content = NOVEL_MASTER.read_text(encoding="utf-8")

        self.assertIn("正文后文风矫正", content)
        self.assertIn("删除用数字硬撑专业感", content)
        self.assertIn("删掉“不是……，而是……”这类先否定再肯定的句式", content)
        self.assertIn("删除不承担推进的平淡比喻", content)
        self.assertIn("少用嘴角、手指等细节偷渡内心", content)
        self.assertNotIn("嘴角动了一下", content)
        self.assertNotIn("凌绝尘的手指收紧了一下", content)

    def test_novel_write_runs_postwrite_style_correction_on_final_review(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")

        self.assertIn("定点修正 AI 味的正文后矫正", content)
        self.assertIn("这一步只在最终稿复检时强制执行", content)
        self.assertIn("不提前统一抹平 4 个中间稿的风格差异", content)


if __name__ == "__main__":
    unittest.main()
