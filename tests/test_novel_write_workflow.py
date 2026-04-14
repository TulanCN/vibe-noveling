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
BOOMING = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "booming" / "SKILL.md"
FUCK_IT = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "fuck-it" / "SKILL.md"
NOVEL_WRITE = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-write" / "SKILL.md"
NOVEL_WRITE_AI_SMELL = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-write" / "references" / "ai-smell-checklist.md"
NOVEL_SYNC = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-sync" / "SKILL.md"
NOVEL_PROGRESS = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-progress" / "SKILL.md"
NOVEL_SNAPSHOT = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-snapshot" / "SKILL.md"
NOVEL_NAME = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-name" / "SKILL.md"
NOVEL_KNOWLEDGE = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-knowledge" / "SKILL.md"
NOVEL_PROGRESS_SCRIPT = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-progress" / "scripts" / "progress_chart.py"
CONTEXT_COLLECTOR = REPO_ROOT / "plugins" / "vibe-noveling" / "agents" / "context-collector.md"
NOVEL_PLAN_PLANNING_CHECKS = REPO_ROOT / "plugins" / "vibe-noveling" / "skills" / "novel-plan" / "references" / "planning-checks.md"
README = REPO_ROOT / "README.md"


class NovelWriteWorkflowTests(unittest.TestCase):
    @staticmethod
    def parse_frontmatter(path: Path) -> dict[str, str]:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            return {}

        end = text.find("\n---\n", 4)
        if end == -1:
            return {}

        lines = text[4:end].splitlines()
        data: dict[str, str] = {}
        index = 0

        while index < len(lines):
            line = lines[index]
            if not line.strip():
                index += 1
                continue

            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()

            if value == "|":
                index += 1
                chunks: list[str] = []
                while index < len(lines):
                    current = lines[index]
                    if current.startswith("  "):
                        chunks.append(current[2:])
                        index += 1
                        continue
                    if not current.strip():
                        chunks.append("")
                        index += 1
                        continue
                    break
                data[key] = "\n".join(chunks).strip()
                continue

            data[key] = value
            index += 1

        return data

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

    def test_booming_skill_commits_to_explosive_plot_routes(self) -> None:
        content = BOOMING.read_text(encoding="utf-8")

        self.assertIn("name: booming", content)
        self.assertIn("【必须触发】用户说：booming", content)
        self.assertIn("主要给 `novel-discuss` 用", content)
        self.assertIn("如果用户只是普通讨论剧情方向，优先用 `novel-discuss`", content)
        self.assertIn("太平了", content)
        self.assertIn("不够炸", content)
        self.assertIn("只负责把剧情炸开", content)
        self.assertIn("默认给出 3 套爆破走向", content)
        self.assertIn("至少一套方案必须真正掀桌", content)
        self.assertIn("某个角色死亡", content)
        self.assertIn("主角遭受重大挫折", content)
        self.assertIn("主角直接死去", content)
        self.assertIn("奇迹般的助力", content)
        self.assertIn("直接达成某个长期目标", content)
        self.assertIn("神秘学、占星术、古代神话恐怖", content)
        self.assertIn("不要主动替作者求稳", content)
        self.assertIn("不要用“其实只是虚惊一场”泄压", content)
        self.assertIn("如果上下文不足，不要先问一串问题", content)
        self.assertIn("给出爆点核心", content)
        self.assertIn("代价与牺牲", content)
        self.assertIn("冲突升级链", content)
        self.assertIn("不可回头点", content)
        self.assertIn("对长期主线的改写", content)
        self.assertIn("用户确认其中一条后，再交给 `novel-plan` 落正式大纲", content)

    def test_readme_mentions_booming_as_manual_explosive_mode(self) -> None:
        content = README.read_text(encoding="utf-8")

        self.assertIn("12 个专业技能 + 2 个内置子 Agent", content)
        self.assertIn("手动剧情爆破模式", content)
        self.assertIn("`booming`", content)
        self.assertIn("主要给 `novel-discuss` 用", content)
        self.assertIn("当你觉得剧情太平、不够炸、想强行掀桌时", content)
        self.assertIn("先用 `booming`", content)
        self.assertIn("默认给 3 套高烈度爆破走向", content)
        self.assertIn("至少一套必须真正掀桌", content)
        self.assertIn("用户确认后再交给 `/novel-plan` 落正式大纲", content)
        self.assertIn("不是默认主流程节点", content)

    def test_fuck_it_skill_amplifies_single_chapter_without_changing_end_goal(self) -> None:
        content = FUCK_IT.read_text(encoding="utf-8")

        self.assertIn("name: fuck-it", content)
        self.assertIn("fuck it", content)
        self.assertIn("fuck-it", content)
        self.assertIn("主要给 `novel-discuss` 和 `novel-plan` 用", content)
        self.assertIn("单章节", content)
        self.assertIn("不改变单章节的结束目标", content)
        self.assertIn("默认给出 3 套方案", content)
        self.assertIn("内置 15 种单章加戏方向", content)
        self.assertIn("先从 15 种方向里筛选", content)
        self.assertIn("再从中选择 3 种", content)
        self.assertIn("本章结束目标（固定）", content)
        self.assertIn("冲突升级链", content)
        self.assertIn("角色表现力放大点", content)
        self.assertIn("漫画感 / 场面感装置", content)
        self.assertIn("每套方案都必须有明确漫画感", content)
        self.assertIn("为什么终点没变但过程更炸", content)
        self.assertIn("公开处刑型", content)
        self.assertIn("身份掀牌型", content)
        self.assertIn("倒计时逼杀型", content)
        self.assertIn("赌注加码型", content)
        self.assertIn("带伤硬撑型", content)
        self.assertIn("如果用户想把后续剧情整体炸开，改用 `booming`", content)
        self.assertIn("如果当前就在 `novel-plan`，直接把选中的方案收束进当前大纲", content)
        self.assertNotIn("至少一套方案要有明显漫画感", content)
        self.assertNotIn("建议至少拉开成三种方向", content)

    def test_readme_mentions_fuck_it_as_same_goal_chapter_amplifier(self) -> None:
        content = README.read_text(encoding="utf-8")

        self.assertIn("12 个专业技能 + 2 个内置子 Agent", content)
        self.assertIn("`fuck-it`", content)
        self.assertIn("同终点单章加戏模式", content)
        self.assertIn("主要给 `novel-discuss` 和 `novel-plan` 用", content)
        self.assertIn("不改本章结束目标", content)
        self.assertIn("默认给 3 套同终点强化方案", content)
        self.assertIn("先过一遍内置的 15 种单章加戏方向", content)
        self.assertIn("再从中挑 3 种", content)
        self.assertIn("每套都必须有漫画感", content)
        self.assertIn("更戏剧、更夸张、更有漫画感", content)
        self.assertIn("如果当前就在 `/novel-plan`，选中后直接收束进当前大纲", content)

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

    def test_novel_init_writes_default_project_style_contract(self) -> None:
        content = NOVEL_INIT.read_text(encoding="utf-8")

        self.assertIn("默认创作风格基线", content)
        self.assertIn("主角默认男性", content)
        self.assertIn("关键行为的终极目标，都是为装逼服务", content)
        self.assertIn("与装逼链条无关的剧情默认砍掉、合并或压缩", content)
        self.assertIn("默认爽点循环", content)

    def test_novel_init_claude_template_uses_formal_style_draft_names(self) -> None:
        content = NOVEL_INIT.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        self.assertIn("`海明威.md` / `卖报小郎君.md` / `火星引力.md` / `大仲马.md` / `吐槽口语风.md`", content)
        self.assertIn("风格中间稿", content)
        self.assertNotIn("test-{风格名}.md", content)

        self.assertIn("│           ├── 海明威.md", readme)
        self.assertIn("│           ├── 卖报小郎君.md", readme)
        self.assertIn("│           ├── 火星引力.md", readme)
        self.assertIn("│           ├── 大仲马.md", readme)
        self.assertIn("│           ├── 吐槽口语风.md", readme)
        self.assertNotIn("test-海明威.md", readme)

    def test_novel_plan_reads_project_style_baseline(self) -> None:
        content = NOVEL_PLAN.read_text(encoding="utf-8")
        planning_checks = NOVEL_PLAN_PLANNING_CHECKS.read_text(encoding="utf-8")

        self.assertIn("先读取 `CLAUDE.md` 的默认创作风格基线", content)
        self.assertIn("本章主任务是否服务主角装逼链条", content)
        self.assertIn("过桥章也要说明在为下一次装逼兑现做什么蓄势", content)
        self.assertIn("哪些内容与主角装逼无关，可以延期", content)

        self.assertIn("主角装逼链条", planning_checks)
        self.assertIn("与下一次装逼兑现无关的过渡", planning_checks)

    def test_novel_write_preserves_protagonist_payoff_sharpness(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")

        self.assertIn("优先保留主角锋芒", content)
        self.assertIn("优先保留主角被区别对待", content)
        self.assertIn("打脸效果", content)
        self.assertIn("默认压缩与主角装逼链条无关的安全句", content)

    def test_novel_discuss_uses_project_style_guardrail(self) -> None:
        content = NOVEL_DISCUSS.read_text(encoding="utf-8")

        self.assertIn("如何服务主角装逼链条", content)
        self.assertIn("如何放大主角特殊性", content)
        self.assertIn("占用太多叙事资源却不服务主角装逼", content)

    def test_readme_describes_default_style_baseline(self) -> None:
        content = README.read_text(encoding="utf-8")

        self.assertIn("默认创作风格基线", content)
        self.assertIn("中国男频网络小说", content)
        self.assertIn("主角默认男性", content)
        self.assertIn("与主角装逼无关的剧情", content)

    def test_novel_plan_uses_dual_outline_structure(self) -> None:
        content = NOVEL_PLAN.read_text(encoding="utf-8")

        self.assertIn("剧情思路卡", content)
        self.assertIn("可写场景纲要", content)
        self.assertIn("本章核心兑现", content)
        self.assertIn("主角状态变化", content)
        self.assertIn("核心冲突链", content)
        self.assertIn("信息释放策略", content)
        self.assertIn("本章边界", content)
        self.assertIn("场景目标", content)
        self.assertIn("触发事件", content)
        self.assertIn("冲突落地", content)
        self.assertIn("转折点", content)
        self.assertIn("落点变化", content)
        self.assertIn("细节锚点", content)
        self.assertNotIn("> ✏️ 写作提示", content)

    def test_novel_plan_requires_plot_point_5w1h_alignment(self) -> None:
        content = NOVEL_PLAN.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        self.assertIn("拆成 3-8 个小剧情点", content)
        self.assertIn("Who / What / Why / Where / When / How", content)
        self.assertIn("小剧情点对齐卡", content)
        self.assertIn("先确认对齐卡，再生成正式大纲", content)
        self.assertIn("不写入 `大纲.md`", content)
        self.assertIn("只对新增、改写或受波及的小剧情点重做 `5W1H`", content)
        self.assertIn("每个小剧情点都必须承担一次不可忽略的净推进", content)
        self.assertIn("一个小剧情点通常只承载一个主目标、一次主冲突落地或一次明确状态变化", content)
        self.assertIn("场景不等于小剧情点", content)
        self.assertIn("如果一个点里包含两次独立转折、跨地点切换或跨时间跳步，就应该拆开", content)
        self.assertIn("如果只是同一次推进里的连续小动作，不要硬拆成多个点", content)

        self.assertIn("每个小剧情点都应该是一段不可忽略的净推进", readme)
        self.assertIn("不是按场景数机械切分，也不是把连续小动作碎成很多点", readme)

    def test_novel_plan_scopes_opening_context_to_arc_search_previous_chapter_and_past(self) -> None:
        content = NOVEL_PLAN.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        self.assertIn("先读取当前所在 `arc` 的剧情设定", content)
        self.assertIn("必须先使用 `novel-knowledge` 搜索", content)
        self.assertIn("上一章 `正文.md`", content)
        self.assertIn("再读取 `memory/past.md`", content)
        self.assertIn("不要因为 `past.md` 中出现的设定名词继续展开读取对应设定文件", content)
        self.assertNotIn("future/ 与上一章 outline 优先于 `past.md`", content)

        self.assertIn("当前 `arc` 的剧情设定", readme)
        self.assertIn("用 `novel-knowledge` 搜索这个 arc 中明确出现的相关设定", readme)
        self.assertIn("上一章 `正文.md`", readme)
        self.assertIn("最后读取 `memory/past.md`", readme)
        self.assertIn("不会因为 `past.md` 里提到的实体继续展开读取其设定文件", readme)

    def test_novel_write_prefers_dual_outline_and_keeps_legacy_fallback(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")

        self.assertIn("优先读取 `可写场景纲要`", content)
        self.assertIn("读取 `剧情思路卡` 作为结构约束", content)
        self.assertIn("若只有旧版 `第三人称精简剧情纲要`，则降级兼容", content)

    def test_novel_write_and_opus_trial_explicitly_reuse_context_cache(self) -> None:
        novel_write = NOVEL_WRITE.read_text(encoding="utf-8")
        novel_plan = NOVEL_PLAN.read_text(encoding="utf-8")
        output = NOVEL_PLAN_OUTPUT.read_text(encoding="utf-8")

        self.assertIn("首先检查 `chapters/vol-{volume_padded}/ch-{chapter_padded}/上下文.md` 是否存在且有效", novel_write)
        self.assertIn("## 上下文缓存文件", novel_write)
        self.assertIn("`chapters/vol-{volume_padded}/ch-{chapter_padded}/上下文.md`", novel_write)
        self.assertIn("如果缓存有效，直接复用缓存内容，不要重新收集", novel_write)
        self.assertIn("如果缓存缺失或失效，才基于最新收集结果填充本节", novel_write)

        self.assertIn("如果存在 `chapters/vol-{volume_padded}/ch-{chapter_padded}/上下文.md`，必须先完整读取其中缓存内容，再开始试写", novel_plan)
        self.assertIn("试写时必须优先复用已有上下文缓存，不要绕过缓存重新临时组织一份 context", novel_plan)
        self.assertIn("如果 context 缺失，允许降级为 outline-only 试写，但报告顶部必须写 `置信度：低`", output)

    def test_novel_write_injects_context_content_from_cache_excerpt(self) -> None:
        novel_write = NOVEL_WRITE.read_text(encoding="utf-8")

        self.assertIn("`{context_content}` 默认直接来自 `chapters/vol-{volume_padded}/ch-{chapter_padded}/上下文.md` 的相关原文或必要摘录", novel_write)
        self.assertIn("不要脱离缓存文件另写一份新的抽象总结", novel_write)
        self.assertIn("只有在长度超限时，才允许压缩为紧凑摘录", novel_write)
        self.assertIn("压缩时必须保留角色语言风格、地点约束、伏笔状态和写作注意事项", novel_write)

    def test_novel_plan_adds_outline_stage_ai_smell_checks(self) -> None:
        content = NOVEL_PLAN.read_text(encoding="utf-8")
        planning_checks = NOVEL_PLAN_PLANNING_CHECKS.read_text(encoding="utf-8")

        self.assertIn("大纲阶段抗 AI 味检查", content)
        self.assertIn("功能说明腔", planning_checks)
        self.assertIn("空泛转场", planning_checks)
        self.assertIn("结果先行", planning_checks)
        self.assertIn("摘要腔", planning_checks)

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

    def test_novel_plan_confirms_chapter_title_before_saving_outline(self) -> None:
        content = NOVEL_PLAN.read_text(encoding="utf-8")
        output = NOVEL_PLAN_OUTPUT.read_text(encoding="utf-8")
        novel_sync = NOVEL_SYNC.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        self.assertIn("正式大纲草稿确认后，再单独处理章节标题", content)
        self.assertIn("先给 2-3 个标题候选", content)
        self.assertIn("如果用户不想现在定标题，允许先记为“待定”", content)
        self.assertIn("未经用户确认，不要擅自生成或写入章节标题", content)

        self.assertIn("# 第 X 章大纲", output)
        self.assertIn("- 章节标题：待定（未确认时）", output)
        self.assertNotIn("# 第 X 章大纲：[标题]", output)

        self.assertIn("若标题仍为“待定”", novel_sync)
        self.assertIn("不要把未确认标题写成当前章节标题", novel_sync)

        self.assertIn("正式大纲草稿确认后，再单独确认章节标题", readme)
        self.assertIn("如果标题还没想好，可以先记为“待定”", readme)

    def test_novel_write_defaults_to_all_styles(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")

        self.assertIn("默认创作全部 5 种写作风格", content)
        self.assertIn("按风格逐个开启写作 Agent", content)
        self.assertIn("吐槽口语风", content)
        self.assertIn("自动合并生成最终稿", content)
        self.assertNotIn("默认并行创作全部 5 种写作风格", content)
        self.assertNotIn("为每种风格 dispatch 一个 `general-purpose` Agent，并行写作。", content)
        self.assertNotIn("用户选择 2-3 种写作风格", content)
        self.assertNotIn("用户手动合并最终稿", content)

    def test_novel_write_derives_twenty_plot_points_and_keeps_visible_titles(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")

        self.assertIn("固定细切为 20 个剧情点", content)
        self.assertIn("恰好 20 个剧情点", content)
        self.assertIn("所有中间稿和最终稿都必须显性保留剧情点标题", content)
        self.assertIn("`【剧情点01：标题】`", content)
        self.assertIn("`【剧情点01：标题｜来源：海明威】`", content)
        self.assertNotIn("不使用“剧情点1 / 剧情点2”标题", content)
        self.assertNotIn("禁止把写作单元标题直接暴露到最终正文中", content)

    def test_novel_write_merges_final_draft_plot_point_by_plot_point(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")

        self.assertIn("按 20 个剧情点顺序逐点择优合并", content)
        self.assertIn("每次只处理当前剧情点在 5 个风格版本中的对应内容", content)
        self.assertIn("每个剧情点只选 1 个主来源版本", content)
        self.assertIn("必须在最终稿剧情点标题中标记来源风格", content)
        self.assertIn("`【剧情点07：雨巷试探｜来源：大仲马】`", content)
        self.assertNotIn("不暴露内部切分结果", content)

    def test_novel_write_biases_final_draft_toward_project_voice(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")
        ai_smell = NOVEL_WRITE_AI_SMELL.read_text(encoding="utf-8")

        self.assertIn("最终稿不是五种风格的平均值", content)
        self.assertIn("更接近当前项目已经人工调整过的正文气质", content)
        self.assertIn("优先保留主线压强、人物活气和网文阅读推进力", content)
        self.assertIn("允许角色即时反应、短促吐槽和带火气的接话", content)
        self.assertIn("允许少量俏皮叙述和轻度作者式调侃", content)
        self.assertIn("允许保留承担推进功能的直给解释", content)
        self.assertIn("不要把最终稿抹平成一个过分安全、过分中性的合并腔", content)

        self.assertIn("短促吐槽", ai_smell)
        self.assertIn("贴着场景的轻俏叙述", ai_smell)
        self.assertIn("承担剧情信息、行动决策或关系变化的直给解释", ai_smell)
        self.assertIn("连续玩梗", ai_smell)
        self.assertIn("脱离视角的作者炫机灵", ai_smell)

    def test_novel_write_adds_banter_style_and_auto_selects_it_in_merge(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        self.assertIn("5. **吐槽口语风", content)
        self.assertIn("5. 吐槽口语", content)
        self.assertIn("自动从吐槽口语风中抽取", content)
        self.assertIn("角色活气不够", content)
        self.assertIn("信息已经对了但读起来发平", content)
        self.assertIn("缺少即时反应", content)
        self.assertIn("不能把紧张场面卸力成段子腔", content)
        self.assertIn("吐槽口语风", readme)
        self.assertIn("5 个写作 Agent", readme)
        self.assertIn("自动从吐槽口语风里选取提气句群", readme)
        self.assertNotIn("残魂互怼", content)
        self.assertNotIn("残魂互怼", readme)

    def test_readme_describes_dual_outline_and_plot_point_review_flow(self) -> None:
        content = README.read_text(encoding="utf-8")

        self.assertIn("默认全风格逐个启动写作 Agent + 自动合并", content)
        self.assertIn("正文阶段细切为固定 20 个剧情点", content)
        self.assertIn("5 个风格稿都显性保留剧情点标题", content)
        self.assertIn("最终稿按剧情点逐点择优", content)
        self.assertIn("在标题处标记来源风格", content)
        self.assertIn("剧情思路卡", content)
        self.assertIn("可写场景纲要", content)
        self.assertIn("先澄清每个小剧情点的 5W1H", content)
        self.assertIn("20 个剧情点", content)
        self.assertNotIn("默认全风格并行写作 + 自动合并", content)
        self.assertNotIn("场景化大纲", content)
        self.assertNotIn("按内部写作单元逐个合并", content)

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
        self.assertIn("内置 27 个 AI 味检测项", content)
        self.assertIn("references/ai-smell-checklist.md", content)
        self.assertIn("最终稿文风矫正", content)
        self.assertIn("写作完成后，逐条检查以下 27 个 AI 味检测项。", ai_smell)
        self.assertIn("### 检测项 21：剧情反思 / 水字数检查", ai_smell)
        self.assertIn("### 检测项 18：删掉“不是……，而是……”这类先否定再肯定的句式", ai_smell)
        self.assertIn("### 检测项 16：破折号滥用", ai_smell)
        self.assertIn("这一步只在最终稿复检时强制执行", content)
        self.assertIn("不提前统一抹平 5 个中间稿的风格差异", content)

    def test_novel_write_absorbs_humanizer_patterns_into_final_review(self) -> None:
        content = NOVEL_WRITE.read_text(encoding="utf-8")
        ai_smell = NOVEL_WRITE_AI_SMELL.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        self.assertIn("检测项 22-27", content)
        self.assertIn("不额外拆出独立 `/humanizer` skill", content)
        self.assertIn("只吸收适合中文网文正文的通用 AI 腔规则", content)

        self.assertIn("### 检测项 22：意义拔高", ai_smell)
        self.assertIn("### 检测项 23：宣传腔", ai_smell)
        self.assertIn("### 检测项 24：伪深刻分析", ai_smell)
        self.assertIn("### 检测项 25：空泛权威", ai_smell)
        self.assertIn("### 检测项 26：强行三连", ai_smell)
        self.assertIn("### 检测项 27：交流残留", ai_smell)
        self.assertIn("不把英文排版习惯当成正文质检重点", ai_smell)
        self.assertNotIn("## 通用 humanizer 补充模式", ai_smell)

        self.assertIn("27 项文本质检", readme)

    def test_public_skill_descriptions_are_trigger_focused(self) -> None:
        public_skills = [
            BOOMING,
            FUCK_IT,
            NOVEL_BOOKPLAN,
            NOVEL_DISCUSS,
            NOVEL_INIT,
            NOVEL_PLAN,
            NOVEL_PROGRESS,
            NOVEL_SNAPSHOT,
            NOVEL_SYNC,
            NOVEL_WRITE,
        ]

        banned_markers = [
            "【必须触发】",
            "【核心功能】",
            "【核心职责】",
            "【关键区分】",
            "【路由规则】",
            "【上下文规则】",
            "【文本质检】",
            "【多风格写作】",
            "【数据来源】",
            "支持两种操作",
        ]

        for path in public_skills:
            frontmatter = self.parse_frontmatter(path)
            description = frontmatter.get("description", "")

            self.assertTrue(description, f"{path} should define a description")
            self.assertIn("when_to_use", frontmatter, f"{path} should define when_to_use")
            self.assertLess(len(description), 120, f"{path} description should stay concise")

            for marker in banned_markers:
                self.assertNotIn(marker, description, f"{path} description should not include {marker}")

    def test_internal_helper_skills_use_user_invocable_flag(self) -> None:
        for path in [NOVEL_NAME, NOVEL_KNOWLEDGE]:
            frontmatter = self.parse_frontmatter(path)

            self.assertEqual(frontmatter.get("user-invocable"), "false")
            self.assertNotIn("internal", frontmatter)
            self.assertIn("when_to_use", frontmatter)


if __name__ == "__main__":
    unittest.main()
