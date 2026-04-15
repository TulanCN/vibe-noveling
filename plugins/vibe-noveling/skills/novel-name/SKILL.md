---
name: novel-name
description: 当其他 skill 或 agent 需要批量生成中文风格名称候选时使用。
when_to_use: |
  仅供其他 skill 或 agent 调用，用于生成角色名、功法名、门派名、物品名、灵兽名、地点名、丹药名、法号名等候选。
  需要项目级去重、稀有度控制或风格化命名时优先使用本工具。
user-invocable: false
invokes: {SKILL_DIR}/tools/name_generator.py
---
# 命名生成器 v2

## 调用约定

- 仅供其他 skill 或 agent 调用，不直接面向用户入口
- 负责出候选名字，不负责决定哪个名字最终落地

## 用途

调用本 skill 目录下的 `tools/name_generator.py` 为小说生成各类中国风格名称。
支持 8 类命名、7 级稀有度体系、共享词库、项目实体去重。
`faction`、`location`、`dao`、`creature` 已改为数据驱动拼装，不再依赖极小硬编码候选表。

角色命名支持多种风格的项目化模型：

- 支持 `zhongfang` 中方/现代真实姓名风格
- 支持 `cultivator` 修真本地角色风格
- 支持 `villain` 反派/幽冥系冷硬风格
- 支持 `civilian` 普通人/凡俗姓名风格
- 支持通过 `--length 2|3|4` 明确指定姓名总字数

## 调用方式

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

## 支持的名称类型（8 类）

### character - 角色名

```bash
# 中方/现代中文姓名（推荐）
python3 {SKILL_DIR}/tools/name_generator.py character --origin zhongfang --gender 男 --length 3 --count 5
python3 {SKILL_DIR}/tools/name_generator.py character --origin zhongfang --gender 女 --length 3 --count 5

# 修真本地角色
python3 {SKILL_DIR}/tools/name_generator.py character --origin cultivator --gender 男 --tone 古雅 --length 3 --count 5
python3 {SKILL_DIR}/tools/name_generator.py character --origin cultivator --gender 女 --tone 温润 --length 3 --count 5

# 反派/幽冥系
python3 {SKILL_DIR}/tools/name_generator.py character --origin villain --gender 男 --tone 凌厉 --length 2 --count 5
python3 {SKILL_DIR}/tools/name_generator.py character --origin villain --gender 女 --tone 凌厉 --length 3 --count 5

# 普通人/凡俗角色
python3 {SKILL_DIR}/tools/name_generator.py character --origin civilian --gender 男 --length 3 --count 5

# 兼容旧接口（仍可用）
python3 {SKILL_DIR}/tools/name_generator.py character --type 修士 --count 5
python3 {SKILL_DIR}/tools/name_generator.py character --type 修士 --style 古典 --count 5
python3 {SKILL_DIR}/tools/name_generator.py character --type 凡人 --count 5
```

### 角色名参数说明

- `--origin`
  - `zhongfang`：中方/现代中文真实姓名，适合军方、联络员、后勤、研究人员
  - `cultivator`：修真本地人名，古风但不悬浮
  - `villain`：冷硬、压迫感更强，适合幽冥教或危险角色
  - `civilian`：普通人、镇民、路人、小人物
- `--tone`
  - `写实`：更像现实姓名
  - `古雅`：偏古风、文气
  - `凌厉`：偏锋利、冷硬
  - `温润`：偏柔和、亲近
- `--length`
  - 指姓名总字数，不是名的字数
  - `2`：如“灵心”“崔绝”
  - `3`：如“苏寒染”“顾青崖”
  - `4`：如复姓四字名“司徒清禾”

### technique - 功法名

```bash
# 中方标准化功法
python3 {SKILL_DIR}/tools/name_generator.py technique --origin zhongfang --element 土 --category defense --count 5

# 幽冥教功法
python3 {SKILL_DIR}/tools/name_generator.py technique --origin youming --category attack --count 5

# 传统宗门功法
python3 {SKILL_DIR}/tools/name_generator.py technique --origin traditional --category movement --count 5
```

### faction / sect - 势力名

```bash
# 新接口：组织/势力
python3 {SKILL_DIR}/tools/name_generator.py faction --kind 现代组织 --origin zhongfang --count 5
python3 {SKILL_DIR}/tools/name_generator.py faction --kind 宗门 --origin orthodox --count 5
python3 {SKILL_DIR}/tools/name_generator.py faction --kind 邪教 --origin youming --count 5

# 旧接口仍可用
python3 {SKILL_DIR}/tools/name_generator.py sect --style 正道 --count 5
python3 {SKILL_DIR}/tools/name_generator.py sect --style 魔道 --count 5
python3 {SKILL_DIR}/tools/name_generator.py sect --style 中立 --count 5
```

### item - 物品名（支持子类型）

```bash
# 中方基础设施 / 工程化物品
python3 {SKILL_DIR}/tools/name_generator.py item --origin zhongfang_infra --item-type 阵法 --usage communication --count 5
python3 {SKILL_DIR}/tools/name_generator.py item --origin zhongfang_infra --item-type 器具 --usage medical --count 5

# 常规修真物品
python3 {SKILL_DIR}/tools/name_generator.py item --origin cultivation_common --item-type 法宝 --count 5

# 稀有法宝 / 幽冥工具
python3 {SKILL_DIR}/tools/name_generator.py item --origin artifact_rare --item-type 法宝 --count 5
python3 {SKILL_DIR}/tools/name_generator.py item --origin youming_tool --item-type 符箓 --count 5
```

### creature - 灵兽名（新增）

```bash
# 按生态区域命名
python3 {SKILL_DIR}/tools/name_generator.py creature --biome water --count 5
python3 {SKILL_DIR}/tools/name_generator.py creature --biome jungle --count 5
python3 {SKILL_DIR}/tools/name_generator.py creature --biome corrupted --count 5
```

### location - 地点名（新增）

```bash
# 按文化圈命名
python3 {SKILL_DIR}/tools/name_generator.py location --culture orthodox --category 城市 --count 5
python3 {SKILL_DIR}/tools/name_generator.py location --culture water_trade --category 水域 --count 5
python3 {SKILL_DIR}/tools/name_generator.py location --culture northern_tribe --category 城市 --count 5
python3 {SKILL_DIR}/tools/name_generator.py location --culture zhongfang_base --category 城市 --count 5
```

### alchemy - 丹药名（新增）

```bash
python3 {SKILL_DIR}/tools/name_generator.py alchemy --count 5
```

### dao - 法号/道号名（新增）

```bash
python3 {SKILL_DIR}/tools/name_generator.py dao --origin orthodox --tone dignified --count 5
python3 {SKILL_DIR}/tools/name_generator.py dao --origin female_cultivator --tone gentle --count 5
python3 {SKILL_DIR}/tools/name_generator.py dao --origin youming --tone ominous --count 5
```

## 去重功能

默认自动扫描 `memory/entities/` 下已有实体，生成的名字会跳过重名。
同一批次内也会自动避免重复候选；如果可用组合不足，会返回更少结果，而不会复制已有名字凑数。
去重同时读取文件名和 frontmatter 里的 `name:` 字段：

```bash
# 默认开启去重
python3 {SKILL_DIR}/tools/name_generator.py character --type 修士 --count 5

# 允许重名（不推荐）
python3 {SKILL_DIR}/tools/name_generator.py character --type 修士 --count 5 --allow-existing
```

## 输出格式

返回 JSON 格式。角色结果会额外包含 `origin`、`tone`、`length` 字段：

```json
{
  "command": "character",
  "params": {"origin": "zhongfang", "gender": "男", "length": 3, "count": 5},
  "results": [
    {"name": "周启川", "surname": "周", "given_name": "启川", "type": "修士", "origin": "zhongfang", "tone": "写实", "length": 3, "rarity": "uncommon", "rarity_cn": "良品"},
    {"name": "顾清禾", "surname": "顾", "given_name": "清禾", "type": "修士", "origin": "cultivator", "tone": "古雅", "length": 3, "rarity": "common", "rarity_cn": "凡品"}
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

当需要生成名字时，执行对应的命令并解析 JSON 输出，**然后必须进行用户确认**：

1. **生成中方角色名**：

   ```bash
   python3 {SKILL_DIR}/tools/name_generator.py character --origin zhongfang --gender 男 --length 3 --count 5
   ```

2. **生成修真本地角色名**：

   ```bash
   python3 {SKILL_DIR}/tools/name_generator.py character --origin cultivator --gender 女 --tone 古雅 --length 3 --count 5
   ```

3. **生成反派名**：

   ```bash
   python3 {SKILL_DIR}/tools/name_generator.py character --origin villain --tone 凌厉 --length 2 --count 5
   ```

4. **生成正道门派名**：

   ```bash
   python3 {SKILL_DIR}/tools/name_generator.py sect --style 正道 --count 3
   ```

5. **生成火属性功法名**：

   ```bash
   python3 {SKILL_DIR}/tools/name_generator.py technique --element 火 --count 3
   ```

6. **生成灵兽名**：

   ```bash
   python3 {SKILL_DIR}/tools/name_generator.py creature --category 兽 --count 3
   ```

7. **生成地点名**：

   ```bash
   python3 {SKILL_DIR}/tools/name_generator.py location --category 山岳 --count 3
   ```

## 根据小说类型映射

- 修真/仙侠 → 修士，正道/魔道门派
- 玄幻/奇幻 → 修士，正道/魔道门派
- 都市/现代 → 凡人，中立门派
- 科幻/未来 → 凡人，中立门派
