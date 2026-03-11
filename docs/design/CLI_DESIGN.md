# AI网文小说写作框架 - CLI命令设计

**版本：** 1.0  
**日期：** 2026-03-11

---

## 1. 命令概览

### 1.1 命令结构

```bash
novel <command> [options] [arguments]
```

### 1.2 命令列表

| 命令 | 功能 | 优先级 |
|------|------|--------|
| `novel init` | 初始化新项目 | P0 |
| `novel stats` | 数值系统管理 | P0 |
| `novel fs` | 伏笔管理 | P0 |
| `novel char` | 角色管理 | P1 |
| `novel count` | 字数统计 | P1 |
| `novel check` | 质量检查 | P1 |
| `novel gen` | 提示词生成 | P1 |
| `novel report` | 生成报告 | P2 |
| `novel world` | 世界观管理 | P2 |

---

## 2. 核心命令详解

### 2.1 `novel init` - 初始化项目

**功能：** 创建新的小说项目

**用法：**
```bash
# 在当前目录初始化
novel init

# 指定项目名称
novel init --name "我的小说"

# 指定目录
novel init --path /path/to/project

# 从模板创建
novel init --template xuanhuan
```

**选项：**
| 选项 | 简写 | 说明 |
|------|------|------|
| `--name` | `-n` | 小说名称 |
| `--path` | `-p` | 项目路径 |
| `--template` | `-t` | 使用模板（xuanhuan/urban/scifi） |
| `--author` | `-a` | 作者名称 |
| `--force` | `-f` | 强制覆盖已存在的项目 |

**输出：**
```
✓ 创建项目结构
✓ 生成配置文件
✓ 创建示例数据

项目初始化完成！
路径：./my-novel
下一步：编辑 .novel/config.yaml 配置小说信息
```

**生成的文件：**
```
my-novel/
├── .novel/
│   ├── config.yaml
│   └── whitelist.txt
├── data/
│   ├── characters/
│   ├── stats/
│   ├── foreshadowing/
│   ├── world/
│   └── memory/
├── content/
│   ├── volumes/
│   └── outlines/
├── reports/
└── tools/
```

---

### 2.2 `novel stats` - 数值系统管理

**功能：** 管理角色数值和状态快照

#### 子命令

##### `novel stats get` - 获取数值

```bash
# 获取角色当前数值
novel stats get ye_fan

# 获取指定章节的数值
novel stats get ye_fan --chapter 50

# 获取所有角色数值
novel stats get --all

# JSON格式输出
novel stats get ye_fan --format json
```

**输出示例：**
```
角色：叶凡
章节：50

【基础属性】
等级: 48
境界: 筑基中期
生命值: 8000
法力值: 4000
攻击力: 650
防御力: 320
速度: 210
精神: 400

【技能】
- 烈焰斩 Lv.5 (伤害: 1820)
- 疾风步 Lv.4 (效果: 闪避+15%, 速度+30)
- 天道剑法 Lv.2 (伤害: 2600)

【装备】
- 武器: 天道剑 (+120攻击)
- 防具: 天剑宗内门道袍 (+50防御)
- 饰品: 神秘玉佩
```

##### `novel stats update` - 更新数值

```bash
# 更新单个属性
novel stats update ye_fan --set hp=8500

# 批量更新
novel stats update ye_fan --set hp=8500,attack=680,defense=350

# 从文件更新
novel stats update ye_fan --file updates.yaml

# 记录变更原因
novel stats update ye_fan --set level=49 --reason "第51章突破"
```

##### `novel stats snapshot` - 生成快照

```bash
# 手动生成快照
novel stats snapshot --chapter 50

# 生成指定范围的快照
novel stats snapshot --range 41-50

# 验证快照一致性
novel stats snapshot --validate
```

##### `novel stats calc` - 计算数值

```bash
# 计算技能伤害
novel stats calc damage --attacker ye_fan --skill "烈焰斩" --target enemy_001

# 使用自定义公式
novel stats calc --formula "attack * 2.5 + level * 15" --char ye_fan

# 批量计算
novel stats calc damage --all-skills --char ye_fan
```

##### `novel stats validate` - 验证一致性

```bash
# 验证所有数值
novel stats validate

# 验证指定角色
novel stats validate ye_fan

# 验证指定章节范围
novel stats validate --range 41-50

# 详细输出
novel stats validate --verbose
```

**输出示例：**
```
数值一致性检查

✓ 叶凡: 第41-50章数值一致
✓ 林瑶: 第41-50章数值一致
⚠ 反派A: 第45章数值跳跃异常
  - 第44章: 等级=30, 攻击=200
  - 第45章: 等级=30, 攻击=500
  - 建议: 检查是否有遗漏的升级描述

发现 1 个问题，请检查后确认
```

---

### 2.3 `novel fs` - 伏笔管理

**功能：** 管理伏笔的完整生命周期

#### 子命令

##### `novel fs list` - 列出伏笔

```bash
# 列出所有活跃伏笔
novel fs list

# 只显示特定类型
novel fs list --type 道具

# 只显示特定状态
novel fs list --status active

# 按重要性排序
novel fs list --sort importance

# JSON格式
novel fs list --format json
```

**输出示例：**
```
活跃伏笔 (共5个)

ID      | 类型 | 标题                    | 章节 | 状态    | 紧急度
--------|------|------------------------|------|---------|--------
fs_001  | 道具 | 神秘玉佩的真正用途      | 1→49 | active  | ⚠️ 高
fs_002  | 角色 | 神秘老者的真实身份      | 1→49 | active  | 中
fs_003  | 事件 | 叶家灭门真相           | 10→49| active  | ⚠️ 高
fs_004  | 设定 | 修炼体系的秘密         | 5→49 | active  | 低
fs_005  | 道具 | 传承之剑的来历         | 48→49| active  | 中

需要关注：
- fs_001: 已埋设49章，接近揭示范围(80-120)
- fs_003: 已埋设39章，应在近期强化
```

##### `novel fs plant` - 埋下伏笔

```bash
# 交互式埋下伏笔
novel fs plant

# 快速埋下
novel fs plant \
  --type 道具 \
  --title "神秘玉佩的真正用途" \
  --chapter 1 \
  --description "叶凡在遗迹中获得神秘玉佩" \
  --importance critical \
  --reveal-range 80-120
```

##### `novel fs hint` - 添加强化

```bash
# 添加伏笔强化
novel fs hint fs_001 \
  --chapter 50 \
  --content "玉佩在战斗中发光，似乎有自主意识"

# 批量添加
novel fs hint fs_001 --file hints.yaml
```

##### `novel fs reveal` - 揭示伏笔

```bash
# 标记伏笔已揭示
novel fs reveal fs_001 --chapter 100

# 揭示并记录详情
novel fs reveal fs_001 \
  --chapter 100 \
  --description "玉佩是上古天道传承的核心载体"
```

##### `novel fs remind` - 获取提醒

```bash
# 获取当前应提醒的伏笔
novel fs remind --chapter 50

# 获取即将到期的伏笔
novel fs remind --urgent

# 获取需要强化的伏笔
novel fs remind --need-hint
```

**输出示例：**
```
伏笔提醒 - 第50章

【紧急】需要揭示 (target < 70)
  (无)

【警告】需要强化 (超过20章未强化)
  - fs_001: 神秘玉佩 - 距上次强化已25章
  - fs_003: 叶家灭门真相 - 距上次强化已30章

【提示】即将到期 (target 70-90)
  - fs_006: 某配角的秘密 - 计划在第80章揭示

建议操作：
  novel fs hint fs_001 --chapter 50 --content "..."
  novel fs hint fs_003 --chapter 50 --content "..."
```

##### `novel fs report` - 状态报告

```bash
# 生成完整报告
novel fs report

# 输出到文件
novel fs report --output reports/foreshadowing/status.md

# 只显示统计
novel fs report --summary
```

---

### 2.4 `novel char` - 角色管理

**功能：** 管理角色信息

```bash
# 列出所有角色
novel char list

# 查看角色详情
novel char get ye_fan

# 创建新角色
novel char create --name "张三" --role support

# 更新角色信息
novel char update ye_fan --set "cultivation_level=筑基后期"

# 更新角色关系
novel char relation ye_fan lin_yao --type lover --since 15

# 查看角色时间线
novel char timeline ye_fan
```

---

### 2.5 `novel count` - 字数统计

**功能：** 统计小说字数

```bash
# 统计总字数
novel count

# 详细统计
novel count --detail

# 按卷统计
novel count --by-volume

# 生成报告
novel count --report

# 实时监控模式
novel count --watch
```

**输出示例：**
```
字数统计
========

总计：156,789 字 (50章)
目标：3,000,000 字
进度：5.23%

分卷统计：
  第一卷：156,789 字 (50章)

最近7天：22,400 字
日均：3,200 字
预计完成：2027-06-15

字数分布：
  最短章节：2,100 字 (第5章)
  最长章节：4,200 字 (第20章)
  平均章节：3,136 字
```

---

### 2.6 `novel check` - 质量检查

**功能：** 检查章节质量

```bash
# 检查所有章节
novel check

# 检查语言规范
novel check --language

# 检查数值一致性
novel check --stats

# 检查指定章节
novel check --chapters 40-50

# 生成报告
novel check --report
```

**输出示例：**
```
质量检查报告
============

【语言检查】
✓ 通过：48/50 章 (96%)

问题章节：
  ch_023.md: 3个非白名单英文单词
  ch_035.md: 1个非白名单英文单词

【数值检查】
✓ 通过：49/50 章 (98%)

问题：
  ch_045: 叶凡攻击力跳跃 (480→650)，缺少说明

【伏笔检查】
⚠️ 需要关注：
  - fs_001: 超过20章未强化
  - fs_003: 超过20章未强化

总体评分：B+ (87/100)
```

---

### 2.7 `novel gen` - 提示词生成

**功能：** 生成AI写作提示词

```bash
# 生成第51章提示词
novel gen 51

# 使用特定模板
novel gen 51 --template battle

# 包含特定角色
novel gen 51 --chars ye_fan,lin_yao

# 包含特定伏笔
novel gen 51 --foreshadowing fs_001,fs_003

# 输出到文件
novel gen 51 --output prompt.md

# 复制到剪贴板
novel gen 51 --copy
```

**输出示例：**
```
# 写作任务：第51章

## 基础规范
- 严格使用中文
- 保持与前文一致
- 字数：2500-4000字

## 角色数值

### 叶凡
- 等级：48
- 境界：筑基中期
- 生命值：8000
- 攻击力：650
- 技能：烈焰斩(Lv5), 疾风步(Lv4), 天道剑法(Lv2)

### 林瑶
- 等级：45
- 境界：筑基初期
- 生命值：5500
- 攻击力：380

## 伏笔提醒

### [重要] 神秘玉佩的真正用途 (fs_001)
- 埋设于第1章，已49章未揭示
- 目标揭示范围：80-120章
- 建议：本章适当强化

### [重要] 叶家灭门真相 (fs_003)
- 埋设于第10章，已39章未揭示
- 建议：本章适当强化

## 前文摘要

第50章：叶凡突破筑基中期，获得天剑宗传承之剑...

## 章节要求

[根据模板或用户输入生成]

---
提示词已生成，共约2000 tokens
```

---

### 2.8 `novel report` - 生成报告

**功能：** 生成各类报告

```bash
# 生成所有报告
novel report

# 生成字数报告
novel report --words

# 生成质量报告
novel report --quality

# 生成伏笔报告
novel report --foreshadowing

# 生成完整报告
novel report --full
```

---

## 3. 全局选项

### 3.1 通用选项

| 选项 | 简写 | 说明 |
|------|------|------|
| `--help` | `-h` | 显示帮助 |
| `--version` | `-V` | 显示版本 |
| `--project` | `-p` | 指定项目路径 |
| `--quiet` | `-q` | 静默模式 |
| `--verbose` | `-v` | 详细输出 |
| `--format` | `-f` | 输出格式（text/json/yaml） |
| `--config` | `-c` | 指定配置文件 |

### 3.2 输出格式

```bash
# 文本格式（默认）
novel stats get ye_fan

# JSON格式
novel stats get ye_fan --format json

# YAML格式
novel stats get ye_fan --format yaml
```

---

## 4. 工具脚本

### 4.1 自动提交脚本

```bash
# tools/auto_commit.sh

#!/bin/bash
# Git自动提交工具

PROJECT_ROOT=$(dirname "$0")/..
cd "$PROJECT_ROOT"

# 获取最新章节
LATEST_CH=$(ls -1 content/volumes/*/ch_*.md | tail -1 | grep -oP 'ch_\K\d+')

# 获取字数
WORD_COUNT=$(python3 tools/count_words.py --quick)

# 生成提交信息
COMMIT_MSG="更新至第${LATEST_CH}章 | 当前字数：${WORD_COUNT}"

# 提交
git add -A
git commit -m "$COMMIT_MSG"
git push

echo "✓ 已提交：$COMMIT_MSG"
```

### 4.2 批量检查脚本

```bash
# tools/check_all.sh

#!/bin/bash
# 批量检查工具

echo "开始检查..."

# 语言检查
echo "【1/3】语言检查..."
python3 tools/check_language.py

# 数值验证
echo "【2/3】数值验证..."
python3 tools/validate_stats.py

# 伏笔检查
echo "【3/3】伏笔检查..."
python3 tools/check_foreshadowing.py

echo "检查完成！"
```

---

## 5. 配置文件

### 5.1 别名配置

```yaml
# .novel/aliases.yaml

# 命令别名
aliases:
  s: stats
  f: foreshadowing
  c: char
  w: count
  g: gen
  
# 快捷命令
shortcuts:
  "quick-stats": "stats get --quick"
  "hint-all": "fs remind --need-hint"
  "check-recent": "check --chapters recent"
```

### 5.2 钩子配置

```yaml
# .novel/hooks.yaml

# 章节保存后钩子
on_chapter_save:
  - "count --update"
  - "check --language"
  
# 伏笔揭示后钩子
on_foreshadowing_reveal:
  - "fs report --summary"
  
# 数值更新后钩子
on_stats_update:
  - "stats validate"
```

---

## 6. 使用示例

### 6.1 日常写作流程

```bash
# 1. 查看当前状态
novel count
novel fs remind

# 2. 生成提示词
novel gen 51 --copy

# 3. [写作...]

# 4. 保存后检查
novel check --chapters 51

# 5. 更新数值
novel stats update ye_fan --set level=49 --reason "第51章升级"

# 6. 更新伏笔
novel fs hint fs_001 --chapter 51 --content "..."

# 7. 生成报告
novel report
```

### 6.2 批量操作

```bash
# 批量检查所有章节
novel check --all

# 批量生成快照
novel stats snapshot --range 1-100

# 批量导出数值
novel stats export --all --format json --output stats.json
```

---

**文档状态：** ✅ 完成  
**下一步：** 开发实现阶段
