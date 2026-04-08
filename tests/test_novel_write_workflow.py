import unittest
import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NOVEL_INIT = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-init" / "SKILL.md"
NOVEL_DISCUSS = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-discuss" / "SKILL.md"
NOVEL_PLAN = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-plan" / "SKILL.md"
NOVEL_BOOKPLAN = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-bookplan" / "SKILL.md"
BOOKPLAN_HIERARCHY = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-bookplan" / "references" / "stc-hierarchy.md"
NOVEL_WRITE = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-write" / "SKILL.md"
NOVEL_SYNC = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-sync" / "SKILL.md"
NOVEL_PROGRESS = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-progress" / "SKILL.md"
NOVEL_PROGRESS_SCRIPT = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-progress" / "scripts" / "progress_chart.py"
CONTEXT_COLLECTOR = REPO_ROOT / "plugins" / "vibe-noveling" / "agents" / "context-collector.md"
NOVEL_MASTER = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-master" / "SKILL.md"
README = REPO_ROOT / "README.md"


class NovelWriteWorkflowTests(unittest.TestCase):
    def test_chapter_artifacts_live_in_volume_chapter_directories(self) -> None:
        novel_init = NOVEL_INIT.read_text(encoding="utf-8")
        novel_plan = NOVEL_PLAN.read_text(encoding="utf-8")
        novel_write = NOVEL_WRITE.read_text(encoding="utf-8")
        novel_sync = NOVEL_SYNC.read_text(encoding="utf-8")
        novel_progress = NOVEL_PROGRESS.read_text(encoding="utf-8")
        context_collector = CONTEXT_COLLECTOR.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        self.assertIn("chapters/vol-01/ch-0001/正文.md", novel_init)
        self.assertIn("chapters/vol-{volume_padded}/ch-{chapter_padded}/大纲.md", novel_plan)
        self.assertIn("chapters/vol-{volume_padded}/ch-{chapter_padded}/上下文.md", novel_plan)
        self.assertIn("chapters/vol-{volume_padded}/ch-{chapter_padded}/正文.md", novel_write)
        self.assertIn("chapters/vol-{volume_padded}/ch-{chapter_padded}/上下文.md", context_collector)
        self.assertIn("chapters/vol-{volume_padded}/ch-{chapter_padded}/正文.md", novel_sync)
        self.assertIn("chapters/vol-xx/ch-xxxx/正文.md", novel_progress)
        self.assertIn("chapters/vol-01/ch-0001/正文.md", readme)

        self.assertNotIn("chapters/ch-{chapter_padded}-outline.md", novel_plan)
        self.assertNotIn("chapters/ch-{chapter_padded}-context.md", context_collector)
        self.assertNotIn("chapters/ch-{编号}.md", novel_write)
        self.assertNotIn("chapters/ch-{chapter_padded}.md", novel_sync)

    def test_novel_progress_classifies_volume_chapter_directory_files(self) -> None:
        spec = importlib.util.spec_from_file_location("progress_chart", NOVEL_PROGRESS_SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertEqual(
            module.classify_file(REPO_ROOT / "chapters" / "vol-01" / "ch-0001" / "正文.md"),
            "正文",
        )
        self.assertEqual(
            module.classify_file(REPO_ROOT / "chapters" / "vol-01" / "ch-0001" / "大纲.md"),
            "大纲",
        )
        self.assertEqual(
            module.classify_file(REPO_ROOT / "chapters" / "vol-01" / "ch-0001" / "上下文.md"),
            "设定文件",
        )

    def test_novel_bookplan_avoids_chapter_count_coupling(self) -> None:
        content = NOVEL_BOOKPLAN.read_text(encoding="utf-8")
        hierarchy = BOOKPLAN_HIERARCHY.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        self.assertIn("全书规划阶段不预设章节数", content)
        self.assertIn("职责段 / 卷内位置 / 状态变化", content)
        self.assertNotIn("对应的大致章节范围", content)
        self.assertNotIn("| Beat | 对应卷 | 大致章节 | 关键事件 | 状态 |", content)
        self.assertNotIn("第 1 段（开卷 3-5 章）", content)
        self.assertNotIn("第 1 段（1-4 章）", hierarchy)
        self.assertNotIn("第 2 段（5-10 章）", hierarchy)
        self.assertIn("按卷与节拍规划，不预设章节数", readme)

    def test_novel_discuss_syncs_confirmed_future_decisions(self) -> None:
        content = NOVEL_DISCUSS.read_text(encoding="utf-8")

        self.assertIn("如果讨论结果形成了已确认的未来规划", content)
        self.assertIn("除了写入 `memory/discussions/` 和 `memory/discussions.md`，还必须同步更新 `memory/future/` 对应文件", content)
        self.assertIn("全书级方向 / 终局 / 长期困境", content)
        self.assertIn("长期主线、伏笔、回收条件", content)
        self.assertIn("某一卷的目标、职责段、关键状态变化", content)
        self.assertIn("某个 arc 的中程推进、阶段性对抗、预期转折", content)

    def test_novel_plan_uses_concise_third_person_outline(self) -> None:
        content = NOVEL_PLAN.read_text(encoding="utf-8")

        self.assertIn("第三人称精简剧情纲要", content)
        self.assertIn("不再输出剧情点切分", content)
        self.assertNotIn("将选定的方案细切为 10-20 个剧情点", content)
        self.assertNotIn("> ✏️ 写作提示", content)

    def test_novel_plan_requires_plot_point_5w1h_alignment(self) -> None:
        content = NOVEL_PLAN.read_text(encoding="utf-8")

        self.assertIn("拆成 3-8 个小剧情点", content)
        self.assertIn("Who / What / Why / Where / When / How", content)
        self.assertIn("小剧情点对齐卡", content)
        self.assertIn("先确认对齐卡，再生成正式大纲", content)
        self.assertIn("不写入 `大纲.md`", content)
        self.assertIn("只对新增、改写或受波及的小剧情点重做 `5W1H`", content)

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
        self.assertIn("先澄清每个小剧情点的 5W1H", content)
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
