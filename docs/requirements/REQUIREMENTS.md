# AI网文小说写作框架系统 - 需求分析文档

**项目代号：** NovelAI-Framework  
**文档版本：** 1.0  
**创建日期：** 2026-03-11  
**负责人：** Worker (Deep Agent)

---

## 目录

1. [项目概述](#1-项目概述)
2. [背景研究](#2-背景研究)
3. [核心需求分析](#3-核心需求分析)
4. [技术架构建议](#4-技术架构建议)
5. [文件结构设计](#5-文件结构设计)
6. [数据格式规范](#6-数据格式规范)
7. [自动化流程设计](#7-自动化流程设计)
8. [实施路线图](#8-实施路线图)
9. [风险评估与应对](#9-风险评估与应对)

---

## 1. 项目概述

### 1.1 项目目标

构建一个完整的AI网文小说写作框架系统，使AI能够：
- 撰写数百万字的长篇连贯小说
- 维护复杂的数值系统一致性
- 遵循语言规范（纯中文，允许通用游戏术语）
- 高效管理伏笔系统
- 自动化字数统计与上传流程

### 1.2 核心价值

- **质量保证：** 通过系统性框架确保小说质量，避免常见AI写作问题
- **效率提升：** 减少人工干预，自动化重复性任务
- **一致性维护：** 确保长篇作品中剧情、数值、设定的前后一致
- **可扩展性：** 支持不同类型网文（玄幻、都市、科幻等）

### 1.3 项目范围

**包含：**
- 框架核心系统（记忆、数值、伏笔、语言检查）
- 文件结构与数据格式设计
- 自动化工具链（字数统计、Git上传）
- 示例模板与配置

**不包含：**
- 具体小说内容创作
- 商业化发布平台集成
- 读者互动功能

---

## 2. 背景研究

### 2.1 现有AI写作工具分析

#### 2.1.1 主流AI写作平台

| 工具名称 | 优势 | 劣势 | 启发点 |
|---------|------|------|--------|
| **NovelAI** | 专注小说生成，风格多样 | 长篇连贯性差，无数值系统 | 风格标签系统值得借鉴 |
| **AI Dungeon** | 交互式叙事，记忆系统 | 记忆容量有限，容易遗忘 | 简单记忆机制可扩展 |
| **Sudowrite** | 故事弧线管理 | 短篇为主，缺乏长篇支持 | 故事结构规划思路 |
| **GPT系列** | 通用能力强 | 长篇一致性差，无专门系统 | 作为基础生成引擎 |
| **Claude** | 长上下文支持好 | 同样缺乏专门框架 | 适合作为核心模型 |

#### 2.1.2 关键发现

1. **记忆瓶颈：** 现有工具普遍受限于上下文窗口，难以处理超长文本
2. **数值盲区：** 几乎没有工具专门处理数值系统（修炼等级、技能伤害等）
3. **伏笔缺失：** 缺乏系统性的伏笔追踪机制
4. **语言控制弱：** 难以严格约束输出语言（如纯中文）

### 2.2 知识图谱与记忆系统研究

#### 2.2.1 长文本记忆解决方案

**方案对比：**

| 方案 | 原理 | 优势 | 劣势 | 适用性 |
|------|------|------|------|--------|
| **滑动窗口** | 只保留最近N个token | 实现简单 | 丢失早期信息 | ❌ 不适合 |
| **摘要链** | 分段摘要，摘要再摘要 | 压缩率高 | 信息损失严重 | ⚠️ 部分适用 |
| **向量数据库** | 将文本向量化存储，相似性检索 | 可检索长历史 | 需要额外检索步骤 | ✅ 推荐 |
| **知识图谱** | 提取实体关系，图结构存储 | 结构化，易查询 | 构建成本高 | ✅ 强烈推荐 |
| **分层记忆** | 工作记忆+长期记忆+档案 | 模拟人类记忆 | 设计复杂 | ✅ 推荐 |

#### 2.2.2 推荐架构：混合记忆系统

```
┌─────────────────────────────────────────────────┐
│                 工作记忆层                        │
│  (当前章节 + 最近5章摘要 + 活跃角色状态)            │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│                 知识图谱层                        │
│  (角色关系、世界设定、事件时间线)                   │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│                 向量检索层                        │
│  (所有历史章节的向量表示，支持语义检索)              │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│                 档案存储层                        │
│  (完整历史记录，按需查询)                         │
└─────────────────────────────────────────────────┘
```

### 2.3 数值系统研究

#### 2.3.1 网文常见数值类型

1. **角色属性系统**
   - 等级、生命值、魔法值
   - 力量、敏捷、智力、体质
   - 修炼境界、功法层数

2. **技能系统**
   - 技能等级、冷却时间、消耗
   - 伤害计算公式
   - 效果持续时间

3. **物品系统**
   - 装备属性、强化等级
   - 丹药效果、持续时间
   - 价格体系

4. **经济系统**
   - 货币类型、汇率
   - 收入支出记录

#### 2.3.2 数值一致性挑战

- **跨章节引用：** 第10章设定的数值，第100章需要一致
- **动态变化：** 角色升级、装备更新导致的数值变化
- **计算依赖：** 伤害 = 基础攻击 × 技能倍率 × 暴击系数

#### 2.3.3 推荐方案：状态快照 + 变更日志

```yaml
# 角色状态快照示例
character_snapshots:
  - chapter: 10
    character: "叶凡"
    attributes:
      level: 15
      hp: 1500
      mp: 800
      attack: 120
      defense: 80
    skills:
      - name: "烈焰斩"
        level: 3
        damage_formula: "attack * 2.5 + level * 10"
    
  - chapter: 50
    character: "叶凡"
    attributes:
      level: 45
      hp: 8000
      mp: 4000
      attack: 650
      defense: 320
    changes_since_last:
      - "获得神器'天道剑'，攻击+200"
      - "突破筑基期，全属性+50%"
```

### 2.4 伏笔管理系统研究

#### 2.4.1 伏笔类型分析

1. **道具伏笔：** 获得神秘物品，后期揭示用途
2. **角色伏笔：** 配角的隐藏身份
3. **事件伏笔：** 早期事件的后续影响
4. **设定伏笔：** 世界观的逐步揭示

#### 2.4.2 伏笔生命周期

```
埋下伏笔 → 周期提醒 → 适度强化 → 适时揭示 → 标记完成
```

#### 2.4.3 伏笔追踪系统设计

```yaml
# 伏笔管理示例
foreshadowing:
  - id: "FS-001"
    type: "道具"
    planted_chapter: 10
    description: "叶凡在遗迹中获得神秘玉佩"
    hints:
      - chapter: 25
        content: "玉佩在危险时发出微光"
      - chapter: 60
        content: "玉佩与古老传承产生共鸣"
    target_reveal: "第100-120章之间"
    reveal_status: "pending"
    importance: "critical"
    
  - id: "FS-002"
    type: "角色"
    planted_chapter: 5
    description: "神秘老者救下叶凡，身份不明"
    target_reveal: "第200章"
    reveal_status: "pending"
    importance: "major"
```

---

## 3. 核心需求分析

### 3.1 功能需求 (Functional Requirements)

#### FR-001: 长篇连贯性保障系统 [P0]

**描述：** 确保数百万字长篇小说的剧情连贯性，避免前后矛盾。

**详细说明：**
- 自动提取和维护角色信息、关系、状态
- 追踪事件时间线和因果关系
- 检测并提示潜在的矛盾冲突
- 维护世界观设定的一致性

**验收标准：**
- AC-001-1: 系统能自动提取每章的角色信息并更新角色库
- AC-001-2: 检测到矛盾时（如角色死亡后又出现）发出警告
- AC-001-3: 提供时间线可视化工具
- AC-001-4: 支持手动标记和查询设定信息

**技术要点：**
- 使用知识图谱存储角色关系和事件
- 使用向量数据库存储章节内容，支持语义检索
- 实现自动矛盾检测算法

#### FR-002: 数值系统一致性管理 [P0]

**描述：** 维护角色数值、技能、物品等数据的一致性，支持自动计算。

**详细说明：**
- 定义数值类型和计算公式
- 自动跟踪数值变化历史
- 在写作时提供最新数值参考
- 支持数值查询和验证

**验收标准：**
- AC-002-1: 系统能存储和管理至少100个角色的完整数值数据
- AC-002-2: 支持自定义伤害公式和计算
- AC-002-3: 每次生成新章节时自动注入最新数值
- AC-002-4: 数值变化有完整的变更日志

**技术要点：**
- 使用YAML/JSON存储数值数据
- 实现公式解析和计算引擎
- 提供数值快照和差异对比功能

#### FR-003: 语言规范控制 [P1]

**描述：** 确保AI输出严格遵循中文语言规范，不出现非预期的英文。

**详细说明：**
- 默认只使用中文
- 允许配置白名单术语（如BUG、GG、HP、MP等）
- 自动检测并提示非白名单英文
- 提供术语表管理功能

**验收标准：**
- AC-003-1: 99%以上的输出为纯中文（不含白名单术语）
- AC-003-2: 检测到非白名单英文时发出警告
- AC-003-3: 支持动态添加/删除白名单术语
- AC-003-4: 提供语言检查报告

**技术要点：**
- 正则表达式检测英文单词
- 白名单配置文件
- 可选：集成中文分词和语法检查

#### FR-004: 高效字数统计 [P1]

**描述：** 自动统计小说字数，无需AI计算，减少token消耗。

**详细说明：**
- 自动统计总字数、章节字数
- 支持按卷、按篇分类统计
- 生成统计报告
- 字数目标跟踪

**验收标准：**
- AC-004-1: 统计准确率100%
- AC-004-2: 支持实时统计（文件保存时自动更新）
- AC-004-3: 生成可视化统计图表
- AC-004-4: 支持导出统计报告（Markdown/HTML）

**技术要点：**
- Python/Shell脚本实现
- 监听文件变化自动触发
- 使用图表库生成可视化

#### FR-005: 自动化GitHub上传 [P1]

**描述：** 自动将小说内容上传到GitHub，AI只需更新本地文件。

**详细说明：**
- 监听文件变化，自动提交
- 规范化提交信息（章节编号、字数等）
- 支持分支管理（草稿/发布）
- 冲突检测和处理

**验收标准：**
- AC-005-1: 文件保存后5秒内自动提交
- AC-005-2: 提交信息格式统一规范
- AC-005-3: 支持回滚到历史版本
- AC-005-4: 支持多人协作（可选）

**技术要点：**
- Git自动化脚本
- 文件监听（inotify/fswatch）
- 提交信息模板

#### FR-006: 伏笔管理系统 [P0]

**描述：** 系统性管理伏笔的埋设、追踪和揭示。

**详细说明：**
- 支持伏笔注册和分类
- 根据章节进度提醒待揭示伏笔
- 记录伏笔的强化和揭示历史
- 支持伏笔重要性分级

**验收标准：**
- AC-006-1: 支持至少1000个伏笔的管理
- AC-006-2: 根据当前章节自动提示相关伏笔
- AC-006-3: 支持伏笔完成度统计
- AC-006-4: 提供伏笔可视化（时间线/网络图）

**技术要点：**
- YAML/JSON存储伏笔数据
- 章节进度触发提醒机制
- 可选：图形化展示工具

#### FR-007: 世界观设定库 [P1]

**描述：** 维护完整的世界观设定，供AI写作时参考。

**详细说明：**
- 地理设定（地图、国家、城市）
- 势力设定（宗门、组织、国家）
- 修炼体系/能力体系
- 物品/装备/丹药库
- 历史事件时间线

**验收标准：**
- AC-007-1: 支持分类存储不同类型设定
- AC-007-2: 提供快速检索功能
- AC-007-3: 支持设定间的关联（如物品归属势力）
- AC-007-4: 设定变更时记录版本历史

**技术要点：**
- 结构化数据存储（YAML/JSON）
- 提供查询接口
- 版本控制

#### FR-008: 章节模板系统 [P2]

**描述：** 提供可定制的章节模板，加速写作过程。

**详细说明：**
- 预设模板（战斗章、日常章、转折章等）
- 支持自定义模板
- 模板包含结构提示和风格标签
- 支持模板变量替换

**验收标准：**
- AC-008-1: 提供至少5种预设模板
- AC-008-2: 支持模板的创建、编辑、删除
- AC-008-3: 模板支持变量（如章节号、标题）
- AC-008-4: 支持模板导入导出

**技术要点：**
- Markdown模板
- 变量替换引擎
- 模板库管理

#### FR-009: 写作提示注入系统 [P1]

**描述：** 在AI生成时自动注入必要的上下文信息。

**详细说明：**
- 根据章节号自动注入相关伏笔
- 注入角色的最新状态和数值
- 注入世界观设定（按相关性）
- 注入前文摘要和剧情走向

**验收标准：**
- AC-009-1: 自动识别并注入最相关的信息
- AC-009-2: 注入信息不超过上下文限制
- AC-009-3: 支持手动调整注入策略
- AC-009-4: 注入过程可追溯

**技术要点：**
- 信息检索和排序算法
- Token计数和截断策略
- 配置化的注入规则

#### FR-010: 质量检查工具 [P2]

**描述：** 自动检查章节质量，提示潜在问题。

**详细说明：**
- 语言规范检查（英文检测）
- 数值一致性检查
- 剧情矛盾检测
- 风格一致性检查
- 生成检查报告

**验收标准：**
- AC-010-1: 检测准确率>90%
- AC-010-2: 检查时间<10秒/章
- AC-010-3: 提供详细的问题定位
- AC-010-4: 支持忽略特定类型的检查

**技术要点：**
- 规则引擎
- 自然语言处理（可选）
- 报告生成器

### 3.2 非功能需求 (Non-Functional Requirements)

#### NFR-001: 性能要求 [P1]

- 字数统计：<1秒/百万字
- 数值查询：<100ms
- 伏笔检索：<200ms
- 文件提交：<5秒
- 质量检查：<10秒/章

#### NFR-002: 可扩展性 [P1]

- 支持至少1000章小说
- 支持至少100个角色
- 支持至少1000个伏笔
- 支持至少10000个设定项

#### NFR-003: 易用性 [P1]

- 文件结构清晰易懂
- 配置文件使用YAML/JSON，易于编辑
- 提供详细的文档和示例
- 错误提示友好明确

#### NFR-004: 可维护性 [P2]

- 代码模块化，职责清晰
- 提供完善的日志
- 支持配置热更新
- 数据备份和恢复机制

#### NFR-005: 兼容性 [P2]

- 支持主流操作系统（Linux, macOS, Windows）
- 支持主流AI模型（GPT-4, Claude, etc.）
- 输出格式兼容主流阅读器
- 支持Markdown格式

---

## 4. 技术架构建议

### 4.1 整体架构

```
┌────────────────────────────────────────────────────────┐
│                     用户接口层                          │
│  (CLI命令 / 配置文件 / 可选Web界面)                      │
└────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────┐
│                    核心框架层                           │
│  ┌─────────────┬─────────────┬──────────────────────┐ │
│  │ 记忆系统    │ 数值系统     │ 伏笔系统              │ │
│  │ (Memory)    │ (Stats)     │ (Foreshadowing)      │ │
│  └─────────────┴─────────────┴──────────────────────┘ │
│  ┌─────────────┬─────────────┬──────────────────────┐ │
│  │ 语言检查    │ 世界观库     │ 模板系统              │ │
│  │ (Linter)    │ (World)     │ (Template)           │ │
│  └─────────────┴─────────────┴──────────────────────┘ │
└────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────┐
│                    数据存储层                           │
│  ┌─────────────┬─────────────┬──────────────────────┐ │
│  │ 文件系统    │ 知识图谱     │ 向量数据库            │ │
│  │ (YAML/MD)   │ (Neo4j)     │ (Chroma/FAISS)       │ │
│  └─────────────┴─────────────┴──────────────────────┘ │
└────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────┐
│                    自动化工具层                         │
│  ┌─────────────┬─────────────┬──────────────────────┐ │
│  │ 字数统计    │ Git自动提交  │ 质量检查              │ │
│  │ (Counter)   │ (AutoPush)  │ (Checker)            │ │
│  └─────────────┴─────────────┴──────────────────────┘ │
└────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────┐
│                    AI接口层                            │
│  (提示词生成 / 上下文注入 / 结果解析)                    │
└────────────────────────────────────────────────────────┘
```

### 4.2 技术栈建议

#### 4.2.1 核心技术

| 组件 | 推荐技术 | 备选方案 | 理由 |
|------|---------|---------|------|
| **配置管理** | YAML | JSON, TOML | 可读性好，支持注释 |
| **数据存储** | 文件系统 + SQLite | 纯文件系统 | 简单可靠，易于备份 |
| **知识图谱** | Neo4j (可选) | NetworkX | 大型项目可选Neo4j |
| **向量数据库** | Chroma | FAISS, Pinecone | 轻量级，易于本地部署 |
| **自动化脚本** | Python + Shell | Node.js | 生态丰富，易于维护 |
| **文件监听** | inotify (Linux) / fswatch (macOS) | watchdog | 高效可靠 |
| **Git操作** | GitPython | Subprocess调用 | Python原生，易于集成 |

#### 4.2.2 可选增强

| 组件 | 技术 | 用途 |
|------|------|------|
| **Web界面** | Flask/FastAPI + Vue.js | 可视化管理 |
| **图表可视化** | ECharts / D3.js | 统计图表、关系图 |
| **全文搜索** | ElasticSearch | 快速检索（可选） |
| **CI/CD** | GitHub Actions | 自动化测试和部署 |

### 4.3 数据流设计

```
用户写作请求
    ↓
[1] 解析章节号和上下文需求
    ↓
[2] 从记忆系统检索相关信息
    ├─→ 角色状态（数值系统）
    ├─→ 活跃伏笔（伏笔系统）
    ├─→ 世界观设定（设定库）
    └─→ 前文摘要（向量检索）
    ↓
[3] 构建提示词
    ├─→ 基础指令（语言规范等）
    ├─→ 注入上下文
    └─→ 应用模板
    ↓
[4] 调用AI生成
    ↓
[5] 质量检查
    ├─→ 语言规范检查
    ├─→ 数值一致性检查
    └─→ 剧情矛盾检测
    ↓
[6] 保存和更新
    ├─→ 保存章节文件
    ├─→ 更新数值快照
    ├─→ 更新伏笔状态
    └─→ 更新知识图谱
    ↓
[7] 自动化处理
    ├─→ 字数统计
    └─→ Git自动提交
```

---

## 5. 文件结构设计

### 5.1 项目根目录结构

```
novel-project/
├── .novel/                    # 框架配置和元数据
│   ├── config.yaml           # 全局配置
│   ├── whitelist.txt         # 英文白名单
│   └── templates/            # 章节模板
│       ├── battle.md
│       ├── daily.md
│       └── climax.md
│
├── data/                      # 数据文件
│   ├── characters/           # 角色数据
│   │   ├── main/
│   │   │   └── ye_fan.yaml   # 主角：叶凡
│   │   └── support/
│   │       └── lin_yao.yaml  # 配角：林瑶
│   │
│   ├── world/                # 世界观设定
│   │   ├── geography.yaml    # 地理设定
│   │   ├── factions.yaml     # 势力设定
│   │   ├── cultivation.yaml  # 修炼体系
│   │   ├── items.yaml        # 物品库
│   │   └── history.yaml      # 历史事件
│   │
│   ├── stats/                # 数值系统
│   │   ├── snapshots/        # 角色状态快照
│   │   │   ├── ch_001-010.yaml
│   │   │   └── ch_011-020.yaml
│   │   └── formulas.yaml     # 计算公式定义
│   │
│   ├── foreshadowing/        # 伏笔管理
│   │   ├── active.yaml       # 活跃伏笔
│   │   ├── completed.yaml    # 已揭示伏笔
│   │   └── archive/          # 伏笔详情
│   │       ├── fs_001.yaml
│   │       └── fs_002.yaml
│   │
│   └── memory/               # 记忆系统
│       ├── summaries/        # 章节摘要
│       │   ├── ch_001.md
│       │   └── ch_002.md
│       ├── timeline.yaml     # 事件时间线
│       └── relations.yaml    # 角色关系图
│
├── content/                   # 小说内容
│   ├── volumes/              # 分卷
│   │   ├── vol_01/
│   │   │   ├── ch_001.md
│   │   │   ├── ch_002.md
│   │   │   └── ...
│   │   └── vol_02/
│   ├── outlines/             # 大纲
│   │   ├── main_outline.md   # 主线大纲
│   │   ├── vol_01_outline.md # 分卷大纲
│   │   └── character_arc.md  # 角色成长线
│   └── drafts/               # 草稿
│       └── temp.md
│
├── reports/                   # 报告输出
│   ├── stats/                # 统计报告
│   │   ├── word_count.md
│   │   └── chapter_stats.yaml
│   ├── quality/              # 质量检查报告
│   │   └── ch_001_check.md
│   └── foreshadowing/        # 伏笔状态报告
│       └── status.md
│
├── tools/                     # 工具脚本
│   ├── count_words.py        # 字数统计
│   ├── check_language.py     # 语言检查
│   ├── validate_stats.py     # 数值验证
│   ├── auto_commit.sh        # Git自动提交
│   └── generate_prompt.py    # 提示词生成
│
├── .gitignore
├── README.md                  # 项目说明
└── requirements.txt           # Python依赖（如有）
```

### 5.2 关键文件格式示例

#### 5.2.1 全局配置 (config.yaml)

```yaml
# 小说基本信息
novel:
  title: "天道至尊"
  author: "作者名"
  genre: "玄幻"
  target_words: 3000000  # 目标字数
  
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
  commit_delay: 5  # 秒
  auto_count_words: true
  
# 数值系统
stats:
  snapshot_interval: 10  # 每10章生成一次快照
  
# 伏笔系统
foreshadowing:
  reminder_threshold: 20  # 超过20章未揭示时提醒
```

#### 5.2.2 角色数据 (characters/main/ye_fan.yaml)

```yaml
# 角色基本信息
id: "char_ye_fan"
name: "叶凡"
role: "protagonist"
first_appear: 1  # 首次出场章节

# 角色设定
profile:
  age: 18
  gender: "男"
  appearance: "身材修长，剑眉星目，气质不凡"
  personality: ["坚毅", "果断", "重情义"]
  background: "青云镇叶家少主，天赋异禀"
  
# 当前状态（最新）
current_state:
  chapter: 50
  cultivation_level: "筑基中期"
  faction: "天剑宗·内门弟子"
  
# 成长轨迹
growth:
  - chapter: 1
    event: "觉醒天道传承"
    changes: ["获得神秘玉佩", "开启修炼之路"]
    
  - chapter: 20
    event: "突破炼气期"
    changes: ["修为达到炼气巅峰", "习得烈焰斩"]
    
# 重要物品
items:
  - id: "item_jade_pe pendant"
    name: "神秘玉佩"
    obtained_chapter: 1
    description: "传承自上古，来历不明"
    foreshadowing_id: "fs_001"
```

#### 5.2.3 伏笔管理 (foreshadowing/active.yaml)

```yaml
# 活跃伏笔列表
foreshadowing:
  - id: "fs_001"
    type: "道具"
    title: "神秘玉佩的真正用途"
    planted_chapter: 1
    importance: "critical"  # critical, major, minor
    
    # 提示信息
    hints:
      - chapter: 5
        content: "玉佩在叶凡危急时刻发热"
      - chapter: 20
        content: "玉佩与传承功法产生共鸣"
        
    # 揭示计划
    reveal:
      target_range: [80, 120]  # 计划在第80-120章揭示
      importance: "critical"
      
    # 状态
    status: "active"  # active, ready_to_reveal, completed
    last_hint_chapter: 20
    chapters_since_planted: 49
    
  - id: "fs_002"
    type: "角色"
    title: "神秘老者的身份"
    planted_chapter: 3
    importance: "major"
    reveal:
      target_range: [150, 200]
    status: "active"
    chapters_since_planted: 47
```

#### 5.2.4 数值快照 (stats/snapshots/ch_041-050.yaml)

```yaml
# 第41-50章角色数值快照
snapshot_range:
  start_chapter: 41
  end_chapter: 50
  
characters:
  ye_fan:
    chapter_41:
      level: 42
      cultivation: "筑基初期"
      hp: 6500
      mp: 3200
      attack: 480
      defense: 250
      skills:
        - name: "烈焰斩"
          level: 5
          damage: "attack * 2.8 + level * 15"
        - name: "疾风步"
          level: 4
          effect: "闪避率+15%"
          
    chapter_50:
      level: 48
      cultivation: "筑基中期"
      hp: 8000
      mp: 4000
      attack: 650
      defense: 320
      changes:
        - chapter: 45
          type: "突破"
          description: "突破筑基中期，全属性提升"
        - chapter: 48
          type: "装备"
          description: "获得天剑宗传承之剑，攻击+120"
```

---

## 6. 数据格式规范

### 6.1 章节文件格式

```markdown
---
chapter: 1
title: "觉醒"
word_count: 3200
status: "final"  # draft, review, final
created: "2026-03-11"
modified: "2026-03-11"
tags: ["开篇", "觉醒", "传承"]
foreshadowing_planted: ["fs_001"]
foreshadowing_revealed: []
characters_involved: ["叶凡", "叶家主", "神秘老者"]
---

# 第一章 觉醒

[正文内容...]

<!-- 
框架注释（不会出现在最终输出中）：
- 本章埋下伏笔：fs_001（神秘玉佩）
- 叶凡初始数值已记录
- 下章预告：叶凡开始修炼
-->
```

### 6.2 设定文件格式规范

#### 6.2.1 地理设定 (world/geography.yaml)

```yaml
# 世界地理设定
world:
  name: "天道大陆"
  
  regions:
    - id: "reg_east"
      name: "东域"
      description: "修仙文明最繁荣的区域"
      countries:
        - id: "country_tianlang"
          name: "天狼国"
          capital: "天狼城"
          major_cities:
            - "青云镇"
            - "白石城"
            
  locations:
    - id: "loc_qingyun"
      name: "青云镇"
      type: "town"
      region: "东域.天狼国"
      description: "叶凡的家乡，看似普通的小镇"
      importance: "major"
      first_appear: 1
```

#### 6.2.2 势力设定 (world/factions.yaml)

```yaml
# 势力设定
factions:
  - id: "faction_tianjian"
    name: "天剑宗"
    type: "宗门"
    rank: "一流"  # 顶级、一流、二流、三流
    
    location: "东域.天狼国.天剑山"
    
    structure:
      leader:
        title: "宗主"
        current: "剑圣·李无极"
        
      hierarchy:
        - "宗主"
        - "长老"
        - "内门弟子"
        - "外门弟子"
        - "杂役弟子"
        
    relations:
      - target: "魔道宗"
        type: "敌对"
        intensity: "high"
      - target: "天狼皇室"
        type: "合作"
        intensity: "medium"
        
    notable_members:
      - character_id: "char_ye_fan"
        status: "内门弟子"
        join_chapter: 15
```

### 6.3 摘要文件格式

```markdown
# 第一章摘要

## 主要事件
1. 叶凡在成人礼上觉醒失败
2. 神秘老者出现，赐予玉佩
3. 叶凡回家后发现玉佩的异常

## 角色状态变化
- 叶凡：未觉醒 → 获得神秘传承
- 叶家主：失望 → 疑惑

## 重要信息
- 伏笔：神秘玉佩（fs_001）
- 伏笔：神秘老者身份（fs_002）

## 下一章预告
叶凡开始探索玉佩的秘密，踏上修炼之路
```

---

## 7. 自动化流程设计

### 7.1 字数统计自动化

#### 7.1.1 统计脚本 (tools/count_words.py)

```python
#!/usr/bin/env python3
"""
字数统计工具
功能：
1. 统计总字数
2. 分卷/分章统计
3. 生成报告
4. 目标进度跟踪
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime

class WordCounter:
    def __init__(self, project_root):
        self.root = Path(project_root)
        self.content_dir = self.root / "content" / "volumes"
        self.config = self.load_config()
        
    def count_chapter(self, file_path):
        """统计单个章节字数"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 移除YAML front matter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2]
            # 统计中文字符
            chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
            # 统计英文单词（可选）
            # ...
            return chinese_chars
            
    def count_all(self):
        """统计所有章节"""
        results = {
            "total": 0,
            "volumes": {},
            "last_updated": datetime.now().isoformat()
        }
        
        for vol_dir in self.content_dir.iterdir():
            if vol_dir.is_dir():
                vol_name = vol_dir.name
                vol_count = 0
                chapters = {}
                
                for chapter_file in sorted(vol_dir.glob("ch_*.md")):
                    count = self.count_chapter(chapter_file)
                    chapters[chapter_file.name] = count
                    vol_count += count
                    
                results["volumes"][vol_name] = {
                    "total": vol_count,
                    "chapters": chapters
                }
                results["total"] += vol_count
                
        return results
        
    def generate_report(self, output_path):
        """生成统计报告"""
        results = self.count_all()
        target = self.config.get('novel', {}).get('target_words', 0)
        
        report = f"""# 字数统计报告

**生成时间：** {results['last_updated']}

## 总体进度

- **总字数：** {results['total']:,}
- **目标字数：** {target:,}
- **完成度：** {results['total']/target*100:.1f}%

## 分卷统计

"""
        for vol_name, vol_data in results['volumes'].items():
            report += f"### {vol_name}\n"
            report += f"- **字数：** {vol_data['total']:,}\n"
            report += f"- **章节数：** {len(vol_data['chapters'])}\n\n"
            
        # 保存JSON数据
        json_path = output_path.with_suffix('.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        # 保存Markdown报告
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        return results

if __name__ == "__main__":
    counter = WordCounter(".")
    counter.generate_report(Path("reports/stats/word_count.md"))
    print("字数统计完成！")
```

### 7.2 Git自动提交流程

#### 7.2.1 自动提交脚本 (tools/auto_commit.sh)

```bash
#!/bin/bash
# Git自动提交工具
# 监听文件变化，自动提交到仓库

PROJECT_ROOT="/path/to/novel-project"
WATCH_DIRS=("content" "data")
COMMIT_DELAY=5  # 秒

# 提交信息生成函数
generate_commit_msg() {
    local changed_files=$1
    local word_count=$(python3 tools/count_words.py --quick)
    
    # 获取最新章节号
    local latest_ch=$(ls -1 content/volumes/*/ch_*.md | tail -1 | grep -oP 'ch_\K\d+')
    
    echo "更新至第${latest_ch}章 | 当前字数：${word_count}"
}

# 主循环
inotifywait -m -r -e modify,create,delete "${WATCH_DIRS[@]}" --format '%w%f' | 
while read file; do
    # 延迟提交，避免频繁提交
    sleep $COMMIT_DELAY
    
    # 检查是否有其他更改
    if git diff --quiet; then
        continue
    fi
    
    # 生成提交信息
    CHANGED_FILES=$(git diff --name-only)
    COMMIT_MSG=$(generate_commit_msg "$CHANGED_FILES")
    
    # 执行提交
    git add -A
    git commit -m "$COMMIT_MSG"
    git push
    
    echo "[$(date)] 已自动提交：$COMMIT_MSG"
done
```

### 7.3 质量检查流程

#### 7.3.1 语言检查工具 (tools/check_language.py)

```python
#!/usr/bin/env python3
"""
语言规范检查工具
检测非预期的英文单词
"""

import re
import yaml
from pathlib import Path

class LanguageChecker:
    def __init__(self, project_root):
        self.root = Path(project_root)
        self.whitelist = self.load_whitelist()
        
    def load_whitelist(self):
        """加载英文白名单"""
        whitelist_file = self.root / ".novel" / "whitelist.txt"
        if whitelist_file.exists():
            with open(whitelist_file, 'r', encoding='utf-8') as f:
                return set(line.strip() for line in f if line.strip())
        return set()
        
    def check_file(self, file_path):
        """检查单个文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 移除YAML front matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]
                
        # 移除代码块（如果有）
        content = re.sub(r'```[\s\S]*?```', '', content)
        
        # 查找所有英文单词
        english_words = re.findall(r'\b[a-zA-Z]+\b', content)
        
        # 过滤白名单
        violations = []
        for word in english_words:
            if word not in self.whitelist:
                violations.append(word)
                
        return violations
        
    def check_chapter(self, chapter_path):
        """检查章节并生成报告"""
        violations = self.check_file(chapter_path)
        
        if violations:
            report = f"""# 语言检查报告：{chapter_path.name}

**检查时间：** {datetime.now().isoformat()}

## 发现问题

检测到以下非白名单英文单词：

"""
            # 统计词频
            from collections import Counter
            word_freq = Counter(violations)
            
            for word, count in word_freq.most_common():
                report += f"- `{word}`: {count}次\n"
                
            return report
        else:
            return None

if __name__ == "__main__":
    import sys
    checker = LanguageChecker(".")
    chapter = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    
    if chapter:
        report = checker.check_chapter(chapter)
        if report:
            print(report)
        else:
            print("✓ 语言检查通过")
```

### 7.4 提示词生成流程

#### 7.4.1 上下文注入工具 (tools/generate_prompt.py)

```python
#!/usr/bin/env python3
"""
提示词生成工具
根据章节号自动注入必要的上下文
"""

import yaml
from pathlib import Path

class PromptGenerator:
    def __init__(self, project_root):
        self.root = Path(project_root)
        self.config = self.load_config()
        
    def get_active_foreshadowing(self, chapter_num):
        """获取当前应该关注的伏笔"""
        fs_file = self.root / "data" / "foreshadowing" / "active.yaml"
        with open(fs_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        active_fs = []
        for fs in data.get('foreshadowing', []):
            # 检查是否应该提醒
            planted = fs['planted_chapter']
            target = fs['reveal']['target_range']
            
            # 如果接近揭示范围，优先级提高
            if chapter_num >= target[0] - 20:
                fs['priority'] = 'high'
            elif chapter_num - planted > 20:
                fs['priority'] = 'medium'
            else:
                fs['priority'] = 'low'
                
            active_fs.append(fs)
            
        # 按优先级排序
        active_fs.sort(key=lambda x: (
            x['priority'] == 'high',
            x['importance'] == 'critical'
        ), reverse=True)
        
        return active_fs[:5]  # 最多返回5个
        
    def get_character_stats(self, chapter_num, character_ids):
        """获取角色最新数值"""
        # 找到最新的快照文件
        snapshot_dir = self.root / "data" / "stats" / "snapshots"
        snapshots = sorted(snapshot_dir.glob("ch_*.yaml"))
        
        # 找到最接近但不超过当前章节的快照
        latest_snapshot = None
        for snap in snapshots:
            # 解析文件名中的章节范围
            match = re.search(r'ch_(\d+)-(\d+)', snap.name)
            if match:
                start, end = int(match.group(1)), int(match.group(2))
                if start <= chapter_num:
                    latest_snapshot = snap
                    
        if latest_snapshot:
            with open(latest_snapshot, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            stats = {}
            for char_id in character_ids:
                if char_id in data.get('characters', {}):
                    # 获取最接近当前章节的状态
                    char_data = data['characters'][char_id]
                    latest_chapter = max(
                        int(ch) for ch in char_data.keys() 
                        if int(ch) <= chapter_num
                    )
                    stats[char_id] = char_data[f'chapter_{latest_chapter}']
                    
            return stats
        return {}
        
    def generate_prompt(self, chapter_num, template_type="default"):
        """生成完整的提示词"""
        # 加载模板
        template_file = self.root / ".novel" / "templates" / f"{template_type}.md"
        with open(template_file, 'r', encoding='utf-8') as f:
            template = f.read()
            
        # 收集上下文
        foreshadowing = self.get_active_foreshadowing(chapter_num)
        # ... 获取其他上下文
        
        # 构建提示词
        prompt = f"""# 写作任务：第{chapter_num}章

## 基础要求
- 严格使用中文，不要出现英文（游戏术语除外）
- 保持与前文的一致性
- 字数目标：3000-4000字

## 伏笔提醒
"""
        for fs in foreshadowing:
            prompt += f"- 【{fs['type']}】{fs['title']}\n"
            prompt += f"  埋设于第{fs['planted_chapter']}章，计划揭示范围：{fs['reveal']['target_range']}\n"
            
        # 添加模板内容
        prompt += f"\n## 章节结构\n{template}\n"
        
        return prompt

if __name__ == "__main__":
    import sys
    chapter_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    generator = PromptGenerator(".")
    prompt = generator.generate_prompt(chapter_num)
    print(prompt)
```

---

## 8. 实施路线图

### 8.1 阶段划分

#### 阶段1：基础框架 (2-3周)

**目标：** 搭建基础文件结构和核心工具

**任务清单：**
- [ ] 创建标准文件结构
- [ ] 实现配置管理系统
- [ ] 实现字数统计工具
- [ ] 实现语言检查工具
- [ ] 实现Git自动提交
- [ ] 编写基础文档

**交付物：**
- 可运行的基础框架
- 配置文件模板
- 工具使用文档

#### 阶段2：核心系统 (3-4周)

**目标：** 实现记忆、数值、伏笔三大核心系统

**任务清单：**
- [ ] 实现角色数据管理
- [ ] 实现数值快照系统
- [ ] 实现伏笔管理系统
- [ ] 实现世界观设定库
- [ ] 实现提示词生成器
- [ ] 集成测试

**交付物：**
- 完整的数据管理系统
- 上下文注入工具
- 系统测试报告

#### 阶段3：高级功能 (2-3周)

**目标：** 实现高级功能和优化

**任务清单：**
- [ ] 实现知识图谱（可选）
- [ ] 实现向量检索（可选）
- [ ] 实现质量检查工具
- [ ] 实现章节模板系统
- [ ] 性能优化
- [ ] 用户界面（可选）

**交付物：**
- 高级功能模块
- 性能测试报告
- 用户手册

#### 阶段4：实战测试 (2-4周)

**目标：** 通过实际写作测试验证框架

**任务清单：**
- [ ] 选择测试小说题材
- [ ] 初始化项目
- [ ] 完成至少50章测试写作
- [ ] 收集问题和反馈
- [ ] 修复bug和优化
- [ ] 完善文档

**交付物：**
- 测试项目
- 问题清单和解决方案
- 最终版本框架

### 8.2 技术里程碑

| 里程碑 | 目标 | 验收标准 |
|--------|------|---------|
| M1 | 基础工具可用 | 字数统计、语言检查、自动提交全部正常工作 |
| M2 | 数据系统可用 | 角色、数值、伏笔数据可正常增删改查 |
| M3 | 上下文注入可用 | 提示词生成器能正确注入相关信息 |
| M4 | 质量检查可用 | 能检测出90%以上的常见问题 |
| M5 | 完整系统可用 | 完成一次50章以上的完整测试 |

---

## 9. 风险评估与应对

### 9.1 技术风险

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|---------|
| **AI上下文限制** | 高 | 高 | 1. 使用摘要和检索而非全文；2. 优先级排序信息；3. 使用长上下文模型 |
| **数值计算复杂** | 中 | 中 | 1. 简化公式系统；2. 提供预计算值；3. 使用计算引擎 |
| **伏笔遗漏** | 中 | 高 | 1. 自动提醒机制；2. 可视化展示；3. 定期审查 |
| **性能问题** | 低 | 中 | 1. 优化算法；2. 使用索引；3. 异步处理 |

### 9.2 使用风险

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|---------|
| **学习成本高** | 中 | 中 | 1. 详细文档；2. 示例项目；3. 视频教程 |
| **配置复杂** | 中 | 低 | 1. 默认配置；2. 配置向导；3. 配置验证工具 |
| **数据丢失** | 低 | 高 | 1. Git版本控制；2. 自动备份；3. 数据验证 |
| **AI质量问题** | 高 | 高 | 1. 人工审核；2. 多轮优化；3. 质量检查工具 |

### 9.3 应急预案

#### 数据恢复
- 所有数据使用Git版本控制
- 每日自动备份到云端
- 提供数据恢复工具

#### 系统降级
- 核心功能可独立运行
- 可选功能可随时禁用
- 提供手动操作接口

---

## 附录

### A. 参考资料

1. **AI写作相关**
   - [NovelAI Documentation](https://docs.novelai.net/)
   - [AI Dungeon Guides](https://guide.aidungeon.io/)
   
2. **知识图谱相关**
   - Neo4j Graph Database
   - Knowledge Graph Construction
   
3. **长文本处理**
   - Long-Context Transformers
   - Hierarchical Memory Networks
   
4. **网文创作**
   - 网文创作技巧与规范
   - 修炼体系设计参考

### B. 术语表

| 术语 | 定义 |
|------|------|
| **知识图谱** | 结构化的知识表示方法，用图的形式存储实体和关系 |
| **向量数据库** | 存储向量嵌入的数据库，支持相似性检索 |
| **上下文注入** | 在AI生成时自动添加相关背景信息的技术 |
| **状态快照** | 某一时刻角色数值的完整记录 |
| **伏笔** | 提前埋设的线索，在后续章节揭示 |

### C. 配置模板

#### C.1 基础配置模板

```yaml
# config.yaml - 基础配置模板
novel:
  title: "小说标题"
  author: "作者"
  genre: "类型"
  target_words: 1000000
  
ai:
  model: "claude-3-opus"
  temperature: 0.8
  
language:
  primary: "zh-CN"
  allow_english: false
  
automation:
  auto_commit: true
  auto_count: true
```

#### C.2 英文白名单模板

```
# whitelist.txt - 允许的英文术语
HP
MP
EXP
LV
BUG
GG
ID
NPC
BOSS
AOE
DOT
CD
```

---

**文档状态：** ✅ 完成  
**下一步：** 提交给designer-agent进行架构设计

---

*此文档由Deep Agent生成，版本1.0*
