# AI网文小说写作框架 - 用户界面设计

**文档版本：** 1.0  
**设计日期：** 2026-03-11  
**设计师：** Worker (Designer Agent)

---

## 1. 设计原则

### 1.1 核心原则

1. **CLI优先**：主要使用命令行工具，简单高效
2. **配置驱动**：通过YAML配置文件控制行为
3. **渐进式复杂度**：新手简单，专家强大
4. **可读性优先**：所有输出都是人类可读的文本格式
5. **版本控制友好**：配置和数据都使用文本文件

### 1.2 用户画像

| 用户类型 | 特征 | 主要需求 |
|---------|------|---------|
| **新手作家** | 不熟悉技术工具 | 简单的命令、详细的帮助 |
| **技术作家** | 熟悉CLI和Git | 高效的工具链、自动化 |
| **专业作家** | 大量写作需求 | 完整功能、可定制性 |

---

## 2. CLI命令设计

### 2.1 命令结构

```bash
novel <command> [options] [arguments]
```

### 2.2 核心命令

#### 2.2.1 项目管理

```bash
# 初始化新项目
novel init <project-name> [--template=玄幻|都市|科幻]

# 查看项目状态
novel status

# 显示项目信息
novel info
```

**输出示例：**

```
$ novel status

小说项目：《天道至尊》
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 总体进度
  总字数：152,340
  目标字数：3,000,000
  完成度：5.1%
  当前章节：第48章

📚 分卷统计
  第一卷·觉醒篇 (1-30章)：89,234字
  第二卷·成长篇 (31-60章)：63,106字

📌 待处理伏笔
  🔴 高优先级：2个
  🟡 中优先级：5个
  🟢 低优先级：8个

✅ 质量状态
  语言检查：通过
  数值一致性：通过
  最后更新：2026-03-11 10:30
```

#### 2.2.2 章节管理

```bash
# 新建章节
novel new <chapter-num> [--title="章节标题"]

# 查看章节
novel show <chapter-num>

# 编辑章节（打开编辑器）
novel edit <chapter-num>

# 检查章节
novel check <chapter-num> [--fix]
```

**输出示例：**

```
$ novel check 48

🔍 检查第48章...

✅ 语言检查
  未发现非白名单英文

✅ 数值一致性
  叶凡.攻击力：650 (与前文一致)
  林瑶.等级：42 (与前文一致)

⚠️ 伏笔提醒
  [FS-001] 神秘玉佩
    埋设于第1章，已过47章未揭示
    计划揭示：第80-120章
    建议：近期可考虑添加提示

  [FS-002] 神秘老者
    埋设于第3章，已过45章未揭示
    计划揭示：第150-200章

📊 章节统计
  字数：3,245
  段落数：42
  对话比例：38%

✅ 检查完成！发现 1 个提醒
```

#### 2.2.3 角色管理

```bash
# 查看角色列表
novel character list [--role=protagonist|support|antagonist]

# 查看角色详情
novel character show <character-id>

# 更新角色信息
novel character update <character-id> [--attr=key:value]

# 查看角色数值历史
novel character stats <character-id> [--chapter=N]
```

**输出示例：**

```
$ novel character show ye_fan

👤 角色档案：叶凡
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 基本信息
  角色：主角
  首次出场：第1章
  年龄：18岁
  性别：男

🎯 当前状态 (第48章)
  修炼境界：筑基中期
  所属势力：天剑宗·内门弟子
  位置：天剑宗·内门峰

⚔️ 数值属性
  等级：48
  生命值：8,000
  法力值：4,000
  攻击力：650
  防御力：320

🔥 已习得技能
  烈焰斩 (Lv.5) - 伤害: 1820
  疾风步 (Lv.4) - 闪避率+15%
  天剑诀 (Lv.3) - 伤害: 2600

📦 持有物品
  天道剑 (神器)
  神秘玉佩 (未知)

📖 成长轨迹
  第1章：觉醒天道传承
  第20章：突破炼气期
  第45章：突破筑基中期

⚠️ 关联伏笔
  [FS-001] 神秘玉佩的真正用途
```

#### 2.2.4 伏笔管理

```bash
# 查看伏笔列表
novel foreshadowing list [--status=active|completed] [--importance=high|medium|low]

# 查看伏笔详情
novel foreshadowing show <fs-id>

# 添加伏笔
novel foreshadowing add --type=道具|角色|事件|设定 \
  --title="标题" \
  --planted=章节号 \
  --target=目标章节范围 \
  --importance=high|medium|low \
  --desc="描述"

# 添加伏笔提示
novel foreshadowing hint <fs-id> --chapter=N --content="提示内容"

# 标记伏笔已揭示
novel foreshadowing reveal <fs-id> --chapter=N --content="揭示内容"
```

**输出示例：**

```
$ novel foreshadowing list --status=active

📌 活跃伏笔列表
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 高优先级 (2个)
  [FS-001] 神秘玉佩的真正用途
    类型：道具 | 埋设：第1章 | 已过：47章
    计划揭示：第80-120章
    状态：⏳ 待处理

  [FS-005] 叶凡的真实身世
    类型：角色 | 埋设：第15章 | 已过：33章
    计划揭示：第100-150章
    状态：⏳ 待处理

🟡 中优先级 (5个)
  [FS-002] 神秘老者的身份
    类型：角色 | 埋设：第3章 | 已过：45章
    计划揭示：第150-200章
    状态：✅ 进度正常

  [FS-003] 天剑宗的秘密
    类型：设定 | 埋设：第18章 | 已过：30章
    计划揭示：第80-100章
    状态：⚠️ 接近提醒阈值
    ...

📊 统计
  总计：15个
  已完成：3个 (20%)
  活跃：12个 (80%)
  平均已埋设：28章
```

#### 2.2.5 数值管理

```bash
# 查看数值快照
novel stats snapshot [--chapter=N]

# 更新角色数值
novel stats update <character-id> \
  --chapter=N \
  --attrs="hp:8000,mp:4000,attack:650"

# 计算技能伤害
novel stats calculate \
  --attacker=ye_fan \
  --skill=烈焰斩 \
  --target=enemy_001 \
  --chapter=48

# 验证数值一致性
novel stats validate [--chapter=N]
```

**输出示例：**

```
$ novel stats calculate --attacker=ye_fan --skill=烈焰斩 --chapter=48

⚔️ 伤害计算
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 攻击者：叶凡 (第48章)
  基础攻击力：650
  技能等级：烈焰斩 Lv.5

🎯 技能信息
  名称：烈焰斩
  公式：attack * 2.8 + level * 15
  
📊 计算过程
  基础伤害 = 650 * 2.8 = 1820
  等级加成 = 48 * 15 = 720
  最终伤害 = 1820 + 720 = 2540

💡 结果
  预计伤害：2,540
  暴击伤害：3,810 (按1.5倍计算)
```

#### 2.2.6 提示词生成

```bash
# 生成写作提示词
novel prompt generate <chapter-num> \
  [--template=battle|daily|climax] \
  [--output=prompt.txt]

# 预览上下文注入
novel prompt preview <chapter-num> \
  [--max-tokens=8000]
```

**输出示例：**

```
$ novel prompt generate 49

📝 生成第49章提示词
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 上下文收集完成
  工作记忆：1,245 tokens
  角色数值：523 tokens
  伏笔信息：312 tokens
  世界观：198 tokens
  前文摘要：892 tokens
  ─────────────────
  总计：3,170 tokens / 8,000 限制

📋 注入内容预览
  ✅ 基础写作要求
  ✅ 语言规范要求
  ✅ 活跃角色：叶凡、林瑶、李长老
  ✅ 待处理伏笔：FS-001, FS-003
  ✅ 相关世界观：天剑宗、筑基期
  ✅ 第48章摘要

💾 提示词已保存到：.novel/prompts/ch_049.txt
```

#### 2.2.7 统计报告

```bash
# 生成字数统计报告
novel report words [--output=markdown|html|json]

# 生成伏笔报告
novel report foreshadowing [--output=markdown]

# 生成质量报告
novel report quality [--chapter=N]

# 生成综合报告
novel report all [--output-dir=./reports]
```

**输出示例：**

```
$ novel report words

📊 字数统计报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
生成时间：2026-03-11 10:45:32

📈 总体进度
┌─────────────────────────────────────┐
│ ████████░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│ 152,340 / 3,000,000 (5.1%)          │
└─────────────────────────────────────┘

📚 分卷统计
  第一卷·觉醒篇
    章节：1-30章
    字数：89,234 (58.6%)
    平均：2,974字/章

  第二卷·成长篇
    章节：31-48章
    字数：63,106 (41.4%)
    平均：3,321字/章

📊 近期趋势
  最近7天：+12,450字
  平均速度：1,778字/天
  预计完成：2028年8月

💾 报告已保存到：
  - reports/stats/word_count.md
  - reports/stats/word_count.json
```

#### 2.2.8 工具命令

```bash
# 语言检查
novel lint <file-or-chapter> [--whitelist-add=word]

# Git操作
novel git commit [--message="message"]
novel git push
novel git status

# 备份
novel backup [--output=backup.tar.gz]

# 数据迁移
novel migrate --from=v1 --to=v2
```

---

## 3. 配置文件设计

### 3.1 全局配置 (config.yaml)

```yaml
# 小说基本信息
novel:
  title: "天道至尊"
  author: "作者名"
  genre: "玄幻"
  target_words: 3000000
  
# AI配置
ai:
  model: "claude-3-opus"
  temperature: 0.8
  max_tokens: 4000
  
# 语言规范
language:
  primary: "zh-CN"
  allow_english: false
  whitelist_file: "whitelist.txt"
  
# 自动化配置
automation:
  auto_commit: true
  commit_delay: 5
  auto_count_words: true
  
# 记忆系统
memory:
  working_memory_size: 5  # 最近N章
  summary_enabled: true
  
# 数值系统
stats:
  snapshot_interval: 10  # 每N章生成快照
  
# 伏笔系统
foreshadowing:
  reminder_threshold: 20  # 超过N章未揭示提醒
  
# 可选功能
advanced:
  vector_search: false
  web_ui: false
```

### 3.2 英文白名单 (whitelist.txt)

```
# 允许使用的英文术语
# 格式：单词 (可选注释)

HP
MP
EXP
LV
BUG
GG
ID
NPC
BOSS
AOE  # 范围攻击
DOT  # 持续伤害
CD   # 冷却时间
DPS  # 每秒伤害
```

### 3.3 角色配置 (data/characters/main/ye_fan.yaml)

```yaml
# 角色基本信息
id: "char_ye_fan"
name: "叶凡"
role: "protagonist"
first_appear: 1

# 角色设定
profile:
  age: 18
  gender: "男"
  appearance: "身材修长，剑眉星目，气质不凡"
  personality: ["坚毅", "果断", "重情义"]
  background: "青云镇叶家少主，天赋异禀"
  
# 当前状态
current_state:
  chapter: 48
  cultivation_level: "筑基中期"
  faction: "天剑宗·内门弟子"
  location: "天剑宗·内门峰"
  
# 数值属性
attributes:
  level: 48
  hp: 8000
  mp: 4000
  attack: 650
  defense: 320
  speed: 180
  
# 技能列表
skills:
  - id: "skill_001"
    name: "烈焰斩"
    level: 5
    type: "攻击"
    damage_formula: "attack * 2.8 + level * 15"
    cooldown: 0
    cost: 200
    
  - id: "skill_002"
    name: "疾风步"
    level: 4
    type: "辅助"
    effect: "闪避率+15%，持续5回合"
    cooldown: 3
    cost: 150
    
# 重要物品
items:
  - id: "item_001"
    name: "天道剑"
    type: "神器"
    obtained_chapter: 35
    description: "天剑宗传承神器，威力无穷"
    attributes:
      attack_bonus: 200
      
  - id: "item_002"
    name: "神秘玉佩"
    type: "未知"
    obtained_chapter: 1
    description: "传承自上古，来历不明"
    foreshadowing_id: "fs_001"
```

### 3.4 伏笔配置 (data/foreshadowing/active.yaml)

```yaml
foreshadowing:
  - id: "fs_001"
    type: "道具"
    title: "神秘玉佩的真正用途"
    planted_chapter: 1
    importance: "critical"
    
    description: "叶凡在遗迹中获得的神秘玉佩，来历不明"
    
    hints:
      - chapter: 5
        content: "玉佩在叶凡危急时刻发热"
      - chapter: 20
        content: "玉佩与传承功法产生共鸣"
      - chapter: 45
        content: "玉佩对某个禁地产生反应"
        
    reveal:
      target_range: [80, 120]
      planned_content: "玉佩是上古天道传承的钥匙"
      
    status: "active"
    last_updated: 45
```

---

## 4. 用户交互流程

### 4.1 新项目初始化流程

```
用户：novel init 我的第一本小说 --template=玄幻

系统：
┌──────────────────────────────────────┐
│ 🎉 创建新小说项目                      │
│                                       │
│ 项目名称：我的第一本小说               │
│ 模板类型：玄幻                         │
│                                       │
│ 正在创建项目结构...                    │
│ ✅ 创建配置文件                        │
│ ✅ 创建数据目录                        │
│ ✅ 创建内容目录                        │
│ ✅ 创建工具目录                        │
│ ✅ 生成示例文件                        │
│                                       │
│ 📝 接下来：                            │
│ 1. 编辑 .novel/config.yaml 设置小说信息│
│ 2. 编辑 data/characters/ 添加角色     │
│ 3. 编辑 data/world/ 添加世界观        │
│ 4. 运行 novel new 1 创建第一章        │
│                                       │
│ 💡 提示：运行 novel help 查看所有命令  │
└──────────────────────────────────────┘
```

### 4.2 日常写作流程

```
┌─────────────────────────────────────────────────────────┐
│                    日常写作流程                          │
└─────────────────────────────────────────────────────────┘

1️⃣ 查看状态
   $ novel status
   → 了解当前进度、待处理伏笔

2️⃣ 生成提示词
   $ novel prompt generate <下一章号>
   → 获取包含上下文的提示词

3️⃣ AI生成/人工写作
   → 使用提示词让AI生成，或自己写作

4️⃣ 保存章节
   $ novel save <章节号> --file=章节文件
   → 或直接编辑 content/volumes/vol_XX/ch_XXX.md

5️⃣ 质量检查
   $ novel check <章节号>
   → 自动检查语言、数值、伏笔

6️⃣ 更新数据
   $ novel stats update <角色ID> --chapter=N --attrs="..."
   $ novel foreshadowing hint <FS-ID> --chapter=N --content="..."
   → 更新数值和伏笔状态

7️⃣ 自动提交
   → 系统自动检测文件变化并提交到Git
```

### 4.3 伏笔管理流程

```
┌─────────────────────────────────────────────────────────┐
│                    伏笔管理流程                          │
└─────────────────────────────────────────────────────────┘

埋设伏笔
  $ novel foreshadowing add \
    --type=道具 \
    --title="神秘玉佩的真正用途" \
    --planted=1 \
    --target=80-120 \
    --importance=high \
    --desc="叶凡获得的神秘玉佩"
  → 系统记录伏笔，后续自动提醒

添加提示
  $ novel foreshadowing hint fs_001 \
    --chapter=20 \
    --content="玉佩与传承功法产生共鸣"
  → 记录伏笔的强化

查看提醒
  $ novel foreshadowing list --status=active
  → 系统自动显示超过阈值的伏笔

揭示伏笔
  $ novel foreshadowing reveal fs_001 \
    --chapter=100 \
    --content="玉佩是上古天道传承的钥匙"
  → 标记伏笔完成
```

---

## 5. 错误处理与提示

### 5.1 友好的错误提示

```
❌ 错误：未找到章节文件

找不到第50章的文件。
路径：content/volumes/vol_02/ch_050.md

💡 建议：
  1. 运行 novel new 50 创建新章节
  2. 检查文件路径是否正确
  3. 运行 novel status 查看当前进度
```

### 5.2 警告提示

```
⚠️ 警告：伏笔长时间未处理

[FS-001] 神秘玉佩的真正用途
  埋设于第1章，已过47章未揭示
  计划揭示范围：第80-120章
  当前章节：第48章

💡 建议：
  1. 在近期章节中添加提示
  2. 或调整计划揭示范围
  3. 运行 novel foreshadowing show fs_001 查看详情
```

### 5.3 进度反馈

```
⏳ 正在处理...

[1/5] 读取章节内容...
[2/5] 提取角色信息...
[3/5] 检查数值一致性...
[4/5] 验证伏笔状态...
[5/5] 生成检查报告...

✅ 处理完成！
```

---

## 6. 可视化界面（可选）

### 6.1 Web界面概述

如果实现Web界面，建议使用以下技术栈：
- **后端**：FastAPI (Python)
- **前端**：Vue.js 3 + Element Plus
- **图表**：ECharts

### 6.2 主要页面

#### 6.2.1 仪表板

```
┌─────────────────────────────────────────────────────────┐
│  📊 写作仪表板                    《天道至尊》  第48章    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📈 总体进度                        📚 章节统计           │
│  ┌────────────────────┐           ┌──────────────────┐  │
│  │ ████████░░░░░░░░░░ │           │ 第一卷：30章     │  │
│  │ 152K / 3000K (5%)  │           │ 第二卷：18章     │  │
│  └────────────────────┘           │ 总计：48章       │  │
│                                    └──────────────────┘  │
│  📌 伏笔状态                        📊 最近7天            │
│  ┌────────────────────┐           ┌──────────────────┐  │
│  │ 🔴 高优：2          │           │ +12,450字        │  │
│  │ 🟡 中优：5          │           │ 日均：1,778字    │  │
│  │ 🟢 低优：8          │           │ 完成度：5.1%     │  │
│  └────────────────────┘           └──────────────────┘  │
│                                                          │
│  🎯 待办事项                                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │ □ [FS-001] 神秘玉佩 - 建议在近5章内添加提示        │ │
│  │ □ [FS-003] 天剑宗秘密 - 接近提醒阈值               │ │
│  │ □ 角色数值更新 - 叶凡突破后需要更新数值            │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### 6.2.2 角色管理页面

```
┌─────────────────────────────────────────────────────────┐
│  👥 角色管理                                              │
├─────────────────────────────────────────────────────────┤
│  筛选：[全部▼] [主角] [配角] [反派]    🔍 搜索角色...    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ 👤 叶凡   │  │ 👤 林瑶   │  │ 👤 李长老 │              │
│  │ 主角      │  │ 配角      │  │ 配角      │              │
│  │ Lv.48    │  │ Lv.42    │  │ Lv.??    │              │
│  │ 筑基中期  │  │ 筑基初期  │  │ 金丹期    │              │
│  └──────────┘  └──────────┘  └──────────┘              │
│                                                          │
│  点击查看详情 →                                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### 6.2.3 伏笔时间线

```
┌─────────────────────────────────────────────────────────┐
│  📌 伏笔时间线                                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  章节：1 ──────────────────── 48 ──────────── 100 ───→  │
│        │                      │                │        │
│  FS-001 埋设                  当前位置         计划揭示  │
│        ●━━━━━━━━━━━━━━━━━━━━━▶                 ○        │
│        │                      │                          │
│        └─ 提示1 (ch.5)        └─ 已过47章 ⚠️            │
│        └─ 提示2 (ch.20)                                  │
│        └─ 提示3 (ch.45)                                  │
│                                                          │
│  FS-002 埋设                                  计划揭示   │
│        ●━━━━━━━━━━━━━━━━━━━━━▶                           │
│        │                                                 │
│        └─ 进度正常 ✅                                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 7. 快捷操作

### 7.1 命令别名

```bash
# 可在 .bashrc 或 .zshrc 中添加别名
alias n='novel'
alias ns='novel status'
alias nc='novel check'
alias np='novel prompt generate'
alias nf='novel foreshadowing list'
```

### 7.2 快捷键（如果实现TUI）

```
Ctrl+S     保存当前章节
Ctrl+C     检查当前章节
Ctrl+P     生成提示词
Ctrl+F     查看伏笔
Ctrl+N     新建章节
?          显示帮助
q          退出
```

---

## 8. 帮助系统

### 8.1 命令帮助

```bash
$ novel help

novel - AI网文小说写作框架

用法：
  novel <command> [options] [arguments]

命令：
  项目管理：
    init        初始化新项目
    status      查看项目状态
    info        显示项目信息
    
  章节管理：
    new         新建章节
    show        查看章节
    edit        编辑章节
    check       检查章节
    
  角色管理：
    character   角色相关操作
    
  伏笔管理：
    foreshadowing  伏笔相关操作
    
  数值管理：
    stats       数值相关操作
    
  提示词：
    prompt      生成写作提示词
    
  报告：
    report      生成统计报告
    
  工具：
    lint        语言检查
    git         Git操作
    backup      备份项目

选项：
  -h, --help     显示帮助信息
  -v, --version  显示版本号
  --verbose      显示详细输出

更多信息：
  novel help <command>  查看命令详细帮助
  novel docs            打开在线文档
```

### 8.2 上下文帮助

```bash
$ novel new --help

novel new - 新建章节

用法：
  novel new <chapter-num> [options]

参数：
  chapter-num    章节号（必需）

选项：
  --title=TITLE     章节标题
  --template=TYPE   使用模板 (battle|daily|climax)
  --volume=N        指定卷号

示例：
  novel new 1
  novel new 31 --title="新的开始" --volume=2
  novel new 100 --template=battle

提示：
  - 新章节会自动创建在正确的卷目录下
  - 如果不指定标题，会生成默认标题
  - 使用模板可以快速开始写作
```

---

## 9. 国际化考虑

### 9.1 多语言支持

虽然小说内容主要是中文，但CLI界面可以考虑支持多语言：

```yaml
# .novel/locale.yaml
language: zh-CN

messages:
  status:
    total_words: "总字数"
    target_words: "目标字数"
    completion: "完成度"
    
  foreshadowing:
    active: "活跃"
    completed: "已完成"
    overdue: "超期"
```

---

## 10. 总结

### 10.1 设计亮点

1. **CLI优先**：简单高效，适合技术用户
2. **丰富的视觉反馈**：使用emoji和颜色增强可读性
3. **智能提醒**：主动提示伏笔、数值等问题
4. **渐进式复杂度**：新手可以用基础命令，专家可以用高级功能
5. **配置驱动**：灵活可定制
6. **可选Web界面**：满足不同用户需求

### 10.2 实施优先级

**Phase 1 (P0):**
- [x] 核心CLI命令（init, status, new, check）
- [x] 基础配置文件
- [x] 帮助系统

**Phase 2 (P1):**
- [x] 完整命令集（character, foreshadowing, stats）
- [x] 提示词生成
- [x] 报告生成

**Phase 3 (P2):**
- [x] Web界面（可选）
- [x] 可视化图表
- [x] 高级交互功能

---

**文档状态：** ✅ 完成  
**下一步：** 数据结构设计

---

*此文档由 Worker (Designer Agent) 设计*  
*版本：1.0*  
*日期：2026-03-11*
