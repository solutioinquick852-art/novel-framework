# AI网文小说写作框架 - 数据结构设计

**版本：** 1.0  
**日期：** 2026-03-11

---

## 1. 项目目录结构

```
novel-project/
├── .novel/                        # 框架配置目录
│   ├── config.yaml               # 主配置文件
│   ├── whitelist.txt             # 英文白名单
│   └── templates/                # 章节模板
│       ├── battle.md             # 战斗章节模板
│       ├── daily.md              # 日常章节模板
│       ├── climax.md             # 高潮章节模板
│       └── transition.md         # 过渡章节模板
│
├── data/                          # 数据目录
│   ├── characters/               # 角色数据
│   │   ├── main/                 # 主角
│   │   │   ├── ye_fan.yaml       # 叶凡
│   │   │   └── lin_yao.yaml      # 林瑶
│   │   └── support/              # 配角
│   │       ├── elder_zhang.yaml  # 张长老
│   │       └── ...
│   │
│   ├── stats/                    # 数值系统
│   │   ├── snapshots/            # 状态快照
│   │   │   ├── ch_001-010.yaml   # 第1-10章快照
│   │   │   ├── ch_011-020.yaml   # 第11-20章快照
│   │   │   └── ...
│   │   └── formulas.yaml         # 计算公式定义
│   │
│   ├── foreshadowing/            # 伏笔管理
│   │   ├── active.yaml           # 活跃伏笔
│   │   ├── completed.yaml        # 已完成伏笔
│   │   └── archive/              # 伏笔详情档案
│   │       ├── fs_001.yaml       # 单个伏笔详情
│   │       └── ...
│   │
│   ├── world/                    # 世界观设定
│   │   ├── geography.yaml        # 地理设定
│   │   ├── factions.yaml         # 势力设定
│   │   ├── cultivation.yaml      # 修炼体系
│   │   ├── items.yaml            # 物品库
│   │   ├── skills.yaml           # 技能库
│   │   └── history.yaml          # 历史事件
│   │
│   └── memory/                   # 记忆系统
│       ├── summaries/            # 章节摘要
│       │   ├── ch_001.md         # 第1章摘要
│       │   ├── ch_002.md
│       │   └── ...
│       ├── timeline.yaml         # 事件时间线
│       └── relations.yaml        # 角色关系图
│
├── content/                       # 内容目录
│   ├── volumes/                  # 分卷
│   │   ├── vol_01/               # 第一卷
│   │   │   ├── ch_001.md         # 第1章
│   │   │   ├── ch_002.md         # 第2章
│   │   │   └── ...
│   │   ├── vol_02/               # 第二卷
│   │   └── ...
│   │
│   ├── outlines/                 # 大纲
│   │   ├── main_outline.md       # 主线大纲
│   │   ├── vol_01_outline.md     # 第一卷大纲
│   │   ├── character_arc.md      # 角色成长线
│   │   └── world_arc.md          # 世界发展线
│   │
│   └── drafts/                   # 草稿
│       └── temp.md
│
├── reports/                       # 报告目录
│   ├── stats/                    # 统计报告
│   │   ├── word_count.md         # 字数统计
│   │   ├── word_count.json       # 详细数据
│   │   └── chapter_stats.yaml    # 章节统计
│   │
│   ├── quality/                  # 质量检查
│   │   ├── language_check.md     # 语言检查报告
│   │   └── consistency_check.md  # 一致性检查
│   │
│   └── foreshadowing/            # 伏笔状态
│       └── status.md             # 状态报告
│
├── tools/                         # 工具脚本
│   ├── count_words.py            # 字数统计
│   ├── check_language.py         # 语言检查
│   ├── validate_stats.py         # 数值验证
│   ├── check_foreshadowing.py    # 伏笔检查
│   ├── auto_commit.sh            # Git自动提交
│   ├── generate_prompt.py        # 提示词生成
│   └── report.py                 # 报告生成
│
├── .gitignore
├── README.md                      # 项目说明
└── requirements.txt               # Python依赖
```

---

## 2. 核心数据格式

### 2.1 配置文件 (config.yaml)

```yaml
# .novel/config.yaml

# ==================== 小说信息 ====================
novel:
  title: "天道至尊"
  author: "作者名"
  genre: "玄幻"              # 玄幻/都市/科幻/仙侠/历史
  target_words: 3000000      # 目标字数
  status: "ongoing"          # ongoing/completed/hiatus

# ==================== AI配置 ====================
ai:
  model: "claude-3-opus"
  temperature: 0.8
  max_tokens: 4000
  
  # 生成参数
  generation:
    chapter_min_words: 2500
    chapter_max_words: 4000
    style_hints:
      - "对话自然"
      - "节奏紧凑"
      - "描写生动"

# ==================== 语言规范 ====================
language:
  primary: "zh-CN"
  allow_english: false
  whitelist: ".novel/whitelist.txt"
  
  # 自动修正
  auto_fix:
    enabled: true
    replace_map:
      "HP": "生命值"
      "MP": "法力值"

# ==================== 自动化配置 ====================
automation:
  # Git自动提交
  auto_commit:
    enabled: true
    delay: 5                 # 延迟秒数
    branch: "main"
    
  # 字数统计
  auto_count:
    enabled: true
    update_interval: 60      # 秒

# ==================== 数值系统 ====================
stats:
  snapshot_interval: 10      # 每10章生成快照
  auto_validate: true        # 自动验证一致性
  
  # 数值范围限制
  limits:
    level_max: 100
    hp_max: 999999
    mp_max: 999999

# ==================== 伏笔系统 ====================
foreshadowing:
  reminder_threshold: 20     # 超过20章未揭示时提醒
  importance_levels:
    critical: 30             # 重要伏笔30章内必须揭示
    major: 60
    minor: 100

# ==================== 记忆系统 ====================
memory:
  working_capacity: 5        # 工作记忆章节数
  summary_max_length: 500    # 摘要最大字数
```

### 2.2 角色数据格式

```yaml
# data/characters/main/ye_fan.yaml

# ==================== 基本信息 ====================
id: "char_ye_fan"
name: "叶凡"
role: "protagonist"          # protagonist/antagonist/support
first_appear: 1

# ==================== 角色设定 ====================
profile:
  full_name: "叶凡"
  age: 18
  gender: "男"
  origin: "青云镇"
  
  appearance: |
    身材修长，剑眉星目，气质不凡。
    常穿一袭青衫，腰间挂着神秘玉佩。
  
  personality:
    traits: ["坚毅", "果断", "重情义", "谨慎"]
    speech_style: "简洁有力，不喜废话"
  
  background: |
    青云镇叶家少主，自幼天赋异禀。
    十八岁成人礼上觉醒失败，被视为废物。
    实则被神秘传承选中，开启逆天崛起之路。

# ==================== 当前状态 ====================
current_state:
  chapter: 50                    # 最新更新章节
  cultivation_level: "筑基中期"
  faction: "天剑宗·内门弟子"
  location: "天剑宗"
  
  # 状态标记
  status_effects:
    - name: "天道传承"
      permanent: true
    - name: "玉佩守护"
      permanent: true

# ==================== 成长轨迹 ====================
growth:
  milestones:
    - chapter: 1
      event: "觉醒天道传承"
      changes:
        - "获得神秘玉佩"
        - "开启修炼之路"
    
    - chapter: 5
      event: "突破炼气期"
      changes:
        - "修为达到炼气一层"
        - "习得基础剑法"
    
    - chapter: 20
      event: "加入天剑宗"
      changes:
        - "成为外门弟子"
        - "获得宗门功法"

# ==================== 重要物品 ====================
items:
  - id: "item_jade_pendant"
    name: "神秘玉佩"
    obtained_chapter: 1
    description: "传承自上古，来历不明"
    foreshadowing_id: "fs_001"    # 关联伏笔
    importance: "critical"
  
  - id: "item_tianjian"
    name: "天道剑"
    obtained_chapter: 48
    description: "天剑宗传承神器"
    importance: "major"

# ==================== 关系网络 ====================
relationships:
  - target_id: "char_lin_yao"
    type: "lover"
    since_chapter: 15
    description: "青梅竹马，相互扶持"
  
  - target_id: "char_elder_zhang"
    type: "mentor"
    since_chapter: 20
    description: "宗门引路人"
  
  - target_id: "char_antagonist_1"
    type: "enemy"
    since_chapter: 30
    description: "杀父仇人"
```

### 2.3 数值快照格式

```yaml
# data/stats/snapshots/ch_041-050.yaml

# ==================== 快照范围 ====================
range:
  start: 41
  end: 50

# ==================== 角色数值 ====================
characters:
  ye_fan:
    # 第41章状态
    chapter_41:
      level: 42
      cultivation: "筑基初期"
      realm_power: 4200         # 境界战力
      
      # 基础属性
      attributes:
        hp: 6500
        mp: 3200
        attack: 480
        defense: 250
        speed: 180
        spirit: 320
      
      # 技能列表
      skills:
        - id: "skill_flame_slash"
          name: "烈焰斩"
          level: 5
          damage_formula: "attack * 2.8 + level * 15"
          mp_cost: 50
          cooldown: 3
        
        - id: "skill_wind_step"
          name: "疾风步"
          level: 4
          effect: "闪避率+15%，速度+30"
          mp_cost: 20
          duration: 5
      
      # 装备
      equipment:
        weapon: "青钢剑"
        armor: "天剑宗内门道袍"
        accessory: "神秘玉佩"
    
    # 第50章状态
    chapter_50:
      level: 48
      cultivation: "筑基中期"
      realm_power: 5800
      
      attributes:
        hp: 8000
        mp: 4000
        attack: 650
        defense: 320
        speed: 210
        spirit: 400
      
      # 变更记录
      changes:
        - chapter: 45
          type: "突破"
          description: "突破筑基中期，全属性提升"
          stat_changes:
            hp: "+1500"
            attack: "+170"
        
        - chapter: 48
          type: "装备"
          description: "获得天剑宗传承之剑'天道剑'"
          stat_changes:
            attack: "+120"

# ==================== 公式引用 ====================
formula_refs:
  - "data/stats/formulas.yaml"
```

### 2.4 伏笔数据格式

```yaml
# data/foreshadowing/active.yaml

# ==================== 活跃伏笔列表 ====================
foreshadowing:
  # ===== 伏笔 FS-001 =====
  - id: "fs_001"
    type: "道具"                    # 道具/角色/事件/设定
    title: "神秘玉佩的真正用途"
    importance: "critical"          # critical/major/minor
    
    # 埋设信息
    planted:
      chapter: 1
      description: "叶凡在遗迹中获得神秘玉佩"
      context: "觉醒仪式失败后，神秘老者赠送"
    
    # 强化记录
    hints:
      - chapter: 5
        content: "玉佩在叶凡危急时刻发热，提供保护"
        subtlety: "subtle"          # subtle/moderate/obvious
      
      - chapter: 20
        content: "玉佩与传承功法产生共鸣"
        subtlety: "moderate"
      
      - chapter: 40
        content: "玉佩显示出部分功能，但核心用途仍未揭示"
        subtlety: "moderate"
    
    # 揭示计划
    reveal:
      target_range: [80, 120]       # 计划揭示章节范围
      planned_chapter: null         # 实际揭示章节
      reveal_type: "climax"         # climax/gradual/sudden
      description: "在最终大战中揭示玉佩是上古天道传承的核心"
    
    # 状态
    status: "active"                # active/hinted/ready/completed
    last_hint_chapter: 40
    chapters_since_planted: 9
    urgency: "high"                 # low/medium/high/critical
    
    # 元数据
    created: "2026-03-01"
    last_updated: "2026-03-11"
    notes: "这是最重要的主线伏笔，必须在高潮时揭示"
  
  # ===== 伏笔 FS-002 =====
  - id: "fs_002"
    type: "角色"
    title: "神秘老者的真实身份"
    importance: "major"
    
    planted:
      chapter: 1
      description: "神秘老者在觉醒仪式后出现"
    
    hints:
      - chapter: 3
        content: "老者对叶家先祖非常熟悉"
        subtlety: "subtle"
    
    reveal:
      target_range: [150, 200]
      planned_chapter: null
      reveal_type: "gradual"
    
    status: "active"
    chapters_since_planted: 49
    urgency: "medium"
```

### 2.5 章节文件格式

```markdown
---
# ==================== 章节元数据 ====================
chapter: 1
title: "觉醒"
volume: 1
word_count: 3200
status: "final"                  # draft/review/final
created: "2026-03-01"
modified: "2026-03-11"

# ==================== 标签 ====================
tags:
  - "开篇"
  - "觉醒"
  - "传承"

# ==================== 伏笔关联 ====================
foreshadowing:
  planted:                        # 本章埋下的伏笔
    - id: "fs_001"
      type: "道具"
      description: "神秘玉佩"
    - id: "fs_002"
      type: "角色"
      description: "神秘老者身份"
  revealed: []                    # 本章揭示的伏笔

# ==================== 角色出场 ====================
characters:
  involved:                       # 出场角色
    - "叶凡"
    - "叶家主"
    - "神秘老者"
  new:                            # 新登场角色
    - "神秘老者"

# ==================== 数值变更 ====================
stats_changes:
  ye_fan:
    cultivation: "凡人"
    note: "觉醒失败，但获得天道传承"
---

# 第一章 觉醒

青云镇，叶家大院。

今天是叶家一年一度的成人礼，也是家族子弟觉醒天赋的日子。

广场上，数百名家族成员齐聚一堂。十八岁的叶凡站在队伍中，神色平静，但紧握的拳头暴露了他内心的紧张。

"下一个，叶凡！"族老的声音响起。

叶凡深吸一口气，走向广场中央的觉醒石...

<!-- 章节内容省略 -->

---

<!--
框架注释（不会出现在最终输出中）：

本章要点：
- 埋下伏笔 fs_001（神秘玉佩）
- 埋下伏笔 fs_002（神秘老者）
- 叶凡初始状态已记录

下章预告：
- 叶凡开始探索玉佩的秘密
- 第一次修炼尝试
- 与林瑶的重逢
-->
```

### 2.6 世界观设定格式

```yaml
# data/world/cultivation.yaml

# ==================== 修炼体系 ====================
system:
  name: "天道修炼体系"
  type: "等级制"
  description: "吸收天地灵气，修炼己身，最终超脱天道"

# ==================== 境界划分 ====================
realms:
  - name: "凡人"
    level: 0
    description: "未开始修炼的普通人"
    power_range: [1, 10]
  
  - name: "炼气期"
    level: 1
    stages: ["初期", "中期", "后期", "巅峰"]
    description: "吸收天地灵气，淬炼肉身"
    power_range: [10, 100]
    lifespan: 150
    
    breakthrough:
      to_next: "筑基期"
      requirements:
        - "修为达到炼气巅峰"
        - "需要筑基丹或特殊机缘"
      success_rate:
        base: 30
        with_pill: 70
        with_opportunity: 90
  
  - name: "筑基期"
    level: 2
    stages: ["初期", "中期", "后期", "巅峰"]
    description: "铸造道基，凝练真元"
    power_range: [100, 1000]
    lifespan: 300
    
    abilities:
      - "御剑飞行"
      - "神识初现"
  
  - name: "金丹期"
    level: 3
    stages: ["初期", "中期", "后期", "巅峰"]
    description: "凝聚金丹，寿元大增"
    power_range: [1000, 10000]
    lifespan: 800
  
  # ... 更多境界

# ==================== 特殊体质 ====================
constitutions:
  - id: "const_heavenly_dao"
    name: "天道体"
    rarity: "unique"
    description: "天生与天道亲和，修炼速度极快"
    effects:
      cultivation_speed: 10.0
      breakthrough_bonus: 50
    special_abilities:
      - "天道感应"
      - "天劫减免"
```

---

## 3. 报告格式

### 3.1 字数统计报告

```yaml
# reports/stats/chapter_stats.yaml

# ==================== 统计时间 ====================
generated_at: "2026-03-11T10:00:00"
version: 1

# ==================== 总体统计 ====================
summary:
  total_words: 156789
  total_chapters: 50
  target_words: 3000000
  progress_percent: 5.23
  average_per_chapter: 3135

# ==================== 分卷统计 ====================
volumes:
  vol_01:
    name: "第一卷：崛起"
    chapters: 50
    words: 156789
    average: 3135
    status: "ongoing"

# ==================== 最近章节 ====================
recent_chapters:
  - chapter: 50
    title: "突破筑基中期"
    words: 3456
    date: "2026-03-11"
  
  - chapter: 49
    title: "传承之剑"
    words: 3210
    date: "2026-03-10"

# ==================== 趋势分析 ====================
trends:
  daily_average_7d: 3200
  weekly_total: 22400
  estimated_completion: "2027-06-15"
```

### 3.2 语言检查报告

```markdown
# 语言检查报告

**检查时间：** 2026-03-11 10:00:00  
**检查范围：** content/volumes/vol_01/  

---

## 总体情况

- **检查章节数：** 50
- **通过章节数：** 48
- **问题章节数：** 2
- **通过率：** 96%

---

## 问题详情

### 第23章 (ch_023.md)

**问题数：** 3

| 行号 | 内容 | 类型 |
|------|------|------|
| 45 | `system` | 非白名单英文 |
| 67 | `data` | 非白名单英文 |
| 89 | `process` | 非白名单英文 |

**建议修改：**
- `system` → "系统"
- `data` → "数据"
- `process` → "过程"

### 第35章 (ch_035.md)

**问题数：** 1

| 行号 | 内容 | 类型 |
|------|------|------|
| 123 | `function` | 非白名单英文 |

---

## 白名单状态

当前白名单包含 25 个术语：
HP, MP, EXP, LV, BUG, GG, ID, NPC, BOSS, AOE, DOT, CD, ...
```

---

## 4. 数据迁移策略

### 4.1 版本控制

所有数据文件使用 Git 版本控制：

```bash
# 初始化项目
git init
git add .
git commit -m "初始化小说项目"

# 日常提交
git add content/volumes/vol_01/ch_051.md
git commit -m "添加第51章：xxx | 当前字数：160,000"
git push
```

### 4.2 备份策略

```bash
# 自动备份脚本
# tools/backup.sh

#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR="backups/$DATE"

mkdir -p $BACKUP_DIR
cp -r data $BACKUP_DIR/
cp -r content $BACKUP_DIR/
cp -r .novel $BACKUP_DIR/

# 保留最近30天的备份
find backups -type d -mtime +30 -exec rm -rf {} \;
```

### 4.3 数据迁移

当数据格式升级时：

```yaml
# .novel/migrations/001_initial.yaml
version: 1
description: "初始版本"
date: "2026-03-11"

# 迁移脚本会在首次运行时创建所有必要文件
```

---

**文档状态：** ✅ 完成  
**下一步：** CLI命令设计 (CLI_DESIGN.md)
