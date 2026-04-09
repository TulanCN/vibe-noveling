import unittest
import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NOVEL_INIT = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-init" / "SKILL.md"
NOVEL_DISCUSS = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-discuss" / "SKILL.md"
NOVEL_DISCUSS_CONTEXT_ROUTING = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-discuss" / "references" / "context-routing.md"
NOVEL_PLAN = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-plan" / "SKILL.md"
NOVEL_PLAN_OUTPUT = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-plan" / "references" / "output.md"
NOVEL_BOOKPLAN = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-bookplan" / "SKILL.md"
BOOKPLAN_HIERARCHY = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-bookplan" / "references" / "stc-hierarchy.md"
NOVEL_WRITE = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-write" / "SKILL.md"
NOVEL_WRITE_AI_SMELL = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-write" / "references" / "ai-smell-checklist.md"
NOVEL_SYNC = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-sync" / "SKILL.md"
NOVEL_PROGRESS = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-progress" / "SKILL.md"
NOVEL_PROGRESS_SCRIPT = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-progress" / "scripts" / "progress_chart.py"
CONTEXT_COLLECTOR = REPO_ROOT / "plugins" / "vibe-noveling" / "agents" / "context-collector.md"
NOVEL_PLAN_PLANNING_CHECKS = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-plan" / "references" / "planning-checks.md"
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
        self.assertIn("先自然讨论", content)
        self.assertIn("当用户明显偏向某个方案后，再切入显式 `5W1H`", content)
        self.assertIn("只针对当前选中的方向", content)
        self.assertIn("当前判断", content)
        self.assertIn("待确认", content)
        self.assertIn("一次只追一个维度", content)
        self.assertIn("不替代 `novel-plan` 的章节级 `5W1H`", content)

    def test_novel_discuss_routes_context_by_topic_and_action(self) -> None:
        discuss = NOVEL_DISCUSS.read_text(encoding="utf-8")
        routing = NOVEL_DISCUSS_CONTEXT_ROUTING.read_text(encoding="utf-8")

        self.assertIn("references/context-routing.md", discuss)
        self.assertNotIn("无论哪种话题，都先读取现有设定", discuss)
        self.assertNotIn("无论哪种话题，都先读取现有设定避免重复或矛盾", discuss)

        self.assertIn("默认不全量扫描 `memory/`", routing)
        self.assertIn("只读取当前话题所需的最小相关上下文", routing)
        self.assertIn("先判定动作，再决定最小上下文包", routing)
        self.assertIn("判断不清时，先追问对象或范围", routing)
        self.assertIn("未来剧情讨论", routing)
        self.assertIn("编辑已有实体", routing)
        self.assertIn("自洽性审查", routing)

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

    def test_novel_plan_confirms_opus_issues_one_by_one(self) -> None:
        content = NOVEL_PLAN.read_text(encoding="utf-8")
        output = NOVEL_PLAN_OUTPUT.read_text(encoding="utf-8")

        self.assertIn("逐个确认", content)
        self.assertIn("一次只问一个问题", content)
        self.assertIn("2-3 个修法选项", content)
        self.assertIn("当前问题未确认前，不进入下一个问题", content)
        self.assertIn("待确认问题未清空前，不直接鼓励用户进入 `/novel-write`", content)
        self.assertIn("Opus报告.md 仍保存完整报告", content)

        self.assertIn("逐个确认", output)
        self.assertIn("一次只处理 1 个问题", output)
        self.assertIn("2-3 个修法选项", output)
        self.assertIn("完整保存到 `chapters/vol-{volume_padded}/ch-{chapter_padded}/Opus报告.md`", output)

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

    def test_readme_describes_discuss_future_5w1h_flow(self) -> None:
        content = README.read_text(encoding="utf-8")

        self.assertIn("先用苏格拉底式方式讨论未来剧情方向", content)
        self.assertIn("当方向开始收束时，再用显式 `5W1H` 澄清选中方案", content)
        self.assertIn("这一步服务于 future/ 输入，不替代 `/novel-plan` 的章节级对齐卡", content)

    def test_readme_describes_discuss_minimal_context_loading(self) -> None:
        content = README.read_text(encoding="utf-8")

        self.assertIn("先按话题选择讨论 reference", content)
        self.assertIn("再按动作读取最小相关上下文", content)
        self.assertIn("不再默认全量扫描整个 `memory/`", content)

    def test_readme_removes_novel_master_and_reassigns_checks(self) -> None:
        content = README.read_text(encoding="utf-8")

        self.assertNotIn("`/novel-master`", content)
        self.assertNotIn("novel-master/", content)
        self.assertIn("规划期强制反思", content)
        self.assertIn("爽点检查", content)
        self.assertIn("AI 味检测", content)

    def test_novel_plan_owns_planning_checks(self) -> None:
        content = NOVEL_PLAN.read_text(encoding="utf-8")
        planning_checks = NOVEL_PLAN_PLANNING_CHECKS.read_text(encoding="utf-8")

        self.assertNotIn("novel-master", content)
        self.assertIn("内置规划期强制反思、爽点检查和反常规检查", content)
        self.assertIn("references/planning-checks.md", content)
        self.assertIn("剧情点级强制反思", planning_checks)
        self.assertIn("爽感循环是否完整", planning_checks)
        self.assertIn("章末是否有钩子", planning_checks)
        self.assertIn("信息释放是否有节奏", planning_checks)
        self.assertIn("情节可预测性", planning_checks)
        self.assertIn("角色反应戏剧性", planning_checks)
        self.assertIn("冲突激烈程度", planning_checks)
        self.assertIn("转折意外性", planning_checks)

    def test_novel_write_owns_ai_smell_checks(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")
        ai_smell = NOVEL_WRITE_AI_SMELL.read_text(encoding="utf-8")

        self.assertNotIn("novel-master", content)
        self.assertIn("内置 20 个 AI 味检测项", content)
        self.assertIn("references/ai-smell-checklist.md", content)
        self.assertIn("最终稿文风矫正", content)
        self.assertIn("写作完成后，逐条检查以下 20 个 AI 味检测项。", ai_smell)
        self.assertIn("### 检测项 20：剧情反思 / 水字数检查", ai_smell)
        self.assertIn("### 检测项 17：删掉“不是……，而是……”这类先否定再肯定的句式", ai_smell)
        self.assertIn("这一步只在最终稿复检时强制执行", content)
        self.assertIn("不提前统一抹平 4 个中间稿的风格差异", content)


if __name__ == "__main__":
    unittest.main()
