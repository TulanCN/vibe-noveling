---
name: novel-name
description: 当其他 skill 或 agent 需要批量生成中文风格名称候选时使用。
when_to_use: |
  仅供其他 skill 或 agent 调用，用于生成角色名、功法名、门派名、物品名、灵兽名、地点名、丹药名、法号名等候选。
  需要项目级去重、稀有度控制或风格化命名时优先使用本工具。
user-invocable: true
invokes: {SKILL_DIR}/tools/name_generator.py
---
# 命名生成器 v2

## 调用约定

- 仅供其他 skill 或 agent 调用，不直接面向用户入口
- 负责出候选名字，不负责决定哪个名字最终落地

## 用途

为小说生成各类中国风格名称。支持 8 类命名、7 级稀有度体系、项目实体去重。

角色命名支持多种风格：

- `zhongfang`：中方/现代真实姓名风格
- `cultivator`：修真本地角色风格
- `villain`：反派/幽冥系冷硬风格
- `civilian`：普通人/凡俗姓名风格
- 支持通过 `--length 2|3|4` 明确指定姓名总字数

## 命名方式（双通道）

### 优先通道：SSoT 直接生成

默认使用 SSoT（String Seed of Thought）方式生成名字。

**步骤**：

1. **读取去重数据**：扫描 `memory/entities/` 下已有实体，提取所有已有名字作为排除列表
2. **生成种子字符串**：在心里生成一个复杂随机字符串（至少 20 字符），拆成多段，每段独立驱动一个创作决策。映射方式：片段 ASCII 求和 mod 选项数，得到选项索引
3. **基于种子组合名字**：按照下方各类型的驱动链执行，调用者已明确指定的参数直接作为约束，未指定的由种子片段驱动
4. **去重验证**：生成的名字不能与排除列表中已有名字重复；若冲突则用种子的下一段重新生成
5. **分配稀有度**：基于种子字符串的哈希值分配稀有度等级
6. **种子选择过程在 thinking 中完成，不暴露给用户**
7. **每次用户说"换一批""再来一批""重新生成"时，必须生成全新的随机字符串，不允许复用上一次的字符串**

**优势**：名字更有整体感，不是机械拼装；风格自然；每次生成都有差异性；不依赖外部词库

#### SSoT 驱动链定义

每个名字用 3 段种子片段驱动。每个片段的映射方式：ASCII 求和 mod 选项数。

**character（角色名）**：
- 片段 A → 姓氏类型：大姓 / 中等姓 / 稀姓 / 复姓（4）
- 片段 B → 名字气质：写实 / 古雅 / 凌厉 / 温润 / 清冷 / 烟火气（6）
- 片段 C → 名字长度：2字 / 3字 / 4字（3）
- 调用者指定了 origin 则按 origin 的风格倾向选姓；指定了 tone 则覆盖片段 B；指定了 length 则覆盖片段 C；指定了 gender 则作为硬约束

**technique（功法名）**：
- 片段 A → 元素倾向：金 / 木 / 水 / 火 / 土 / 暗 / 空间 / 通用（8）
- 片段 B → 功法类型：攻击 / 防御 / 身法 / 辅助 / 阵法（5）
- 片段 C → 命名风格：古典玄奥 / 霸气直白 / 朴素写实 / 诗意意象（4）
- 调用者指定了 element 则覆盖片段 A；指定了 category 则覆盖片段 B

**faction / sect（势力名）**：
- 片段 A → 阵营气质：正道清正 / 魔道肃杀 / 中立超然 / 世俗烟火 / 隐世幽深（5）
- 片段 B → 组织形态：宗门 / 家族 / 帮会 / 朝廷机构 / 散修联盟（5）
- 片段 C → 命名风格：宏大气象 / 古朴厚重 / 凌厉锋锐 / 低调内敛（4）
- 调用者指定了 style/kind/origin 则对应覆盖

**item（物品名）**：
- 片段 A → 物品类型：法宝 / 丹药 / 符箓 / 材料 / 典籍 / 阵法 / 器具（7）
- 片段 B → 稀有度倾向：凡品 / 良品 / 上品 / 极品 / 秘宝（5）
- 片段 C → 命名风格：写实功能 / 玄妙意境 / 古朴传承 / 霸气威压（4）
- 调用者指定了 item-type 则覆盖片段 A；指定了 origin 则约束命名风格

**creature（灵兽名）**：
- 片段 A → 物种类别：草木 / 鱼 / 兽 / 鸟 / 虫 / 爬虫（6）
- 片段 B → 气质：温顺 / 凶猛 / 诡异 / 庄严 / 灵动（5）
- 片段 C → 命名风格：写实形态 / 玄妙意象 / 古意山海 / 恐怖压迫（4）
- 调用者指定了 category/biome/temper 则对应覆盖

**location（地点名）**：
- 片段 A → 地点类型：城市 / 山岳 / 水域 / 秘境 / 大陆（5）
- 片段 B → 文化气质：正道清修 / 商镇繁华 / 边塞粗犷 / 幽冥诡谲 / 隐世桃源（5）
- 片段 C → 命名风格：宏大 / 实用 / 神秘 / 古朴（4）
- 调用者指定了 category/culture/tone 则对应覆盖

**alchemy（丹药名）**：
- 片段 A → 功效方向：疗伤 / 增灵 / 突破 / 解毒 / 延寿 / 化形（6）
- 片段 B → 品级倾向：下品 / 中品 / 上品 / 极品（4）
- 片段 C → 命名风格：写实功效 / 玄妙意象 / 古方传承 / 霸气夸张（4）

**dao（法号/道号）**：
- 片段 A → 风格来源：正道 / 隐修 / 幽冥 / 散修 / 佛门（5）
- 片段 B → 气质：端庄 / 清冷 / 温和 / 凌厉 / 飘渺 / 威严（6）
- 片段 C → 性别：男 / 女（2）
- 调用者指定了 origin/tone/gender 则对应覆盖

### 备用通道：Python 脚本生成

当 SSoT 方式生成的名字不满意、需要更精确的风格控制、或需要大批量生成时，使用 Python 脚本作为备选：

```bash
python3 {SKILL_DIR}/tools/name_generator.py <type> [options]
```

## 稀有度体系

每个生成的名字自动携带稀有度等级：

| 稀有度 | 中文名 | 概率 | 效果 |
|--------|--------|------|------|
| common | 凡品 | ~65% | 简短名(2-4字) |
| uncommon | 良品 | ~20% | 稍长(3-5字) |
| rare | 上品 | ~8% | 有色彩/灵气前缀 |
| epic | 极品 | ~4% | 多前缀组合 |
| legendary | 秘宝 | ~2% | 年份/品级前缀 |
| mythic | 灵宝 | ~1% | 完整修饰链 |
| exotic | 古宝 | ~0.5% | 山海经风格词 |

SSoT 通道通过种子字符串的哈希值分配稀有度；Python 通道由脚本自动分配。

## 支持的名称类型（8 类）

### character - 角色名

SSoT 通道参数映射：
- `--origin` → 种子片段 A 驱动姓氏库风格选择（中方/修真/反派/凡俗）
- `--tone` → 种子片段 B 驱动名字用字气质（写实/古雅/凌厉/温润）
- `--length` → 种子片段 C 驱动姓名总字数（2/3/4）
- `--gender` → 直接作为约束条件

Python 通道：

```bash
# 中方/现代中文姓名（推荐）
python3 {SKILL_DIR}/tools/name_generator.py character --origin zhongfang --gender 男 --length 3 --count 5
python3 {SKILL_DIR}/tools/name_generator.py character --origin zhongfang --gender 女 --length 3 --count 5

# 修真本地角色
python3 {SKILL_DIR}/tools/name_generator.py character --origin cultivator --gender 男 --tone 古雅 --length 3 --count 5

# 反派/幽冥系
python3 {SKILL_DIR}/tools/name_generator.py character --origin villain --gender 男 --tone 凌厉 --length 2 --count 5

# 普通人/凡俗角色
python3 {SKILL_DIR}/tools/name_generator.py character --origin civilian --gender 男 --length 3 --count 5
```

### technique - 功法名

Python 通道：

```bash
python3 {SKILL_DIR}/tools/name_generator.py technique --origin zhongfang --element 土 --category defense --count 5
python3 {SKILL_DIR}/tools/name_generator.py technique --origin youming --category attack --count 5
```

### faction / sect - 势力名

Python 通道：

```bash
python3 {SKILL_DIR}/tools/name_generator.py faction --kind 现代组织 --origin zhongfang --count 5
python3 {SKILL_DIR}/tools/name_generator.py faction --kind 宗门 --origin orthodox --count 5
python3 {SKILL_DIR}/tools/name_generator.py sect --style 正道 --count 5
```

### item - 物品名

Python 通道：

```bash
python3 {SKILL_DIR}/tools/name_generator.py item --origin zhongfang_infra --item-type 阵法 --usage communication --count 5
python3 {SKILL_DIR}/tools/name_generator.py item --origin cultivation_common --item-type 法宝 --count 5
```

### creature - 灵兽名

Python 通道：

```bash
python3 {SKILL_DIR}/tools/name_generator.py creature --biome water --count 5
python3 {SKILL_DIR}/tools/name_generator.py creature --biome corrupted --count 5
```

### location - 地点名

Python 通道：

```bash
python3 {SKILL_DIR}/tools/name_generator.py location --culture orthodox --category 城市 --count 5
python3 {SKILL_DIR}/tools/name_generator.py location --culture water_trade --category 水域 --count 5
```

### alchemy - 丹药名

Python 通道：

```bash
python3 {SKILL_DIR}/tools/name_generator.py alchemy --count 5
```

### dao - 法号/道号名

Python 通道：

```bash
python3 {SKILL_DIR}/tools/name_generator.py dao --origin orthodox --tone dignified --count 5
python3 {SKILL_DIR}/tools/name_generator.py dao --origin youming --tone ominous --count 5
```

## 去重功能

所有通道默认自动去重：扫描 `memory/entities/` 下已有实体，生成的名字会跳过重名。同一批次内也会自动避免重复候选。

SSoT 通道：在生成名字前先读取已有实体列表，生成时实时排除。Python 通道：由脚本自动处理。

## 输出格式

无论哪种通道，最终输出格式统一：

```json
{
  "method": "ssot | python",
  "command": "character",
  "params": {"origin": "zhongfang", "gender": "男", "length": 3, "count": 5},
  "results": [
    {"name": "周启川", "surname": "周", "given_name": "启川", "type": "修士", "origin": "zhongfang", "tone": "写实", "length": 3, "rarity": "uncommon", "rarity_cn": "良品"}
  ]
}
```

## 数据文件

词库数据分离到 `data/` 目录：

```
data/
├── shared.json        # 共享词库（元素/神兽/颜色/数字/动作/道佛词）
├── surnames.json      # 姓氏库（单姓/复姓/稀有姓）
├── names_male.json    # 男性名字用字（按风格分类）
├── names_female.json  # 女性名字用字（按风格分类）
├── names_middle.json  # 辈分/中间字
├── technique.json     # 功法专用词（后缀/兵器/模板）
├── sect.json          # 门派专用词（后缀/风格词）
├── item.json          # 物品专用词（各子类型词库）
├── creature.json      # 灵兽专用词（分类词库）
├── location.json      # 地点专用词（分类词库）
├── alchemy.json       # 丹药专用词（功效/剂型/品级）
├── dao.json           # 法号专用词
└── strange.json       # 山海经古词（高稀有度用）
```

## 用户确认流程

生成名字后，**必须**使用 AskUserQuestion 工具询问用户确认。

### 确认问题格式

```
问题：请选择您满意的名字（可多选），或选择调整方向重新生成：
选项：
1. [名字1] ([rarity_cn]) - 保留
2. [名字2] ([rarity_cn]) - 保留
3. [名字3] ([rarity_cn]) - 保留
4. [名字4] ([rarity_cn]) - 保留
5. [名字5] ([rarity_cn]) - 保留
6. 调整方向重新生成 - 如果都不满意
```

### 交互流程

1. **生成名字**：执行命令生成 5 个候选名字
2. **展示结果**：清晰列出所有生成的名字及稀有度和简要说明
3. **用户确认**：使用 AskUserQuestion 让用户选择
4. **处理结果**：
   - 如果用户选择了具体名字 → 保留这些名字，返回给调用方
   - 如果用户选择"调整方向" → 询问调整方向，然后重新生成

### 用户选择调整方向时

**使用 AskUserQuestion 询问具体调整方向：**

```
问题：请选择您希望的调整方向：
选项：
1. 更古典 - 更有古风韵味
2. 更霸气 - 更有气势感
3. 更柔和 - 更温婉含蓄
4. 更神秘 - 更有仙气/神秘感
5. 其他方向 - 自定义要求
```

根据用户选择调整参数，重新生成名字，**然后重复确认流程（再次使用 AskUserQuestion）**。

## 在其他 skill 中使用

默认使用 SSoT 通道。当 SSoT 结果不满意时，切换到 Python 通道。

**SSoT 通道调用流程**：

1. 扫描 `memory/entities/` 获取已有名字排除列表
2. 在 thinking 中生成随机字符串，基于片段驱动名字创作
3. 依靠 LLM 自身知识库生成名字，不读取词库文件
4. 输出统一 JSON 格式（method 字段为 "ssot"）
5. 用 AskUserQuestion 让用户确认

**Python 通道调用示例**：

```bash
# 角色名
python3 {SKILL_DIR}/tools/name_generator.py character --origin zhongfang --gender 男 --length 3 --count 5

# 门派名
python3 {SKILL_DIR}/tools/name_generator.py sect --style 正道 --count 3

# 功法名
python3 {SKILL_DIR}/tools/name_generator.py technique --element 火 --count 3
```

## 根据小说类型映射

- 修真/仙侠 → 修士，正道/魔道门派
- 玄幻/奇幻 → 修士，正道/魔道门派
- 都市/现代 → 凡人，中立门派
- 科幻/未来 → 凡人，中立门派
