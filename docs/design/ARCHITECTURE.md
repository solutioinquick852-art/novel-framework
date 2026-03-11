# AI网文小说写作框架 - 系统架构设计

**版本：** 1.0  
**日期：** 2026-03-11  
**状态：** 设计阶段

---

## 1. 整体架构

### 1.1 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户层 (User Layer)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   CLI 命令   │  │  配置文件   │  │    Markdown 章节        │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                     核心框架层 (Core Layer)                      │
│  ┌───────────┬───────────┬───────────┬───────────┬───────────┐ │
│  │ 记忆系统   │ 数值系统   │ 伏笔系统   │ 语言检查   │ 世界观库   │ │
│  │ Memory    │ Stats     │ Foreshadow│ Linter    │ World     │ │
│  └───────────┴───────────┴───────────┴───────────┴───────────┘ │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              提示词生成器 (Prompt Generator)               │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                    数据存储层 (Data Layer)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ YAML/JSON   │  │  Markdown   │  │   SQLite (可选)         │ │
│  │ 结构化数据   │  │  章节内容    │  │   索引/缓存             │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                   自动化工具层 (Automation Layer)                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ 字数统计    │  │ Git 自动提交 │  │    质量检查             │ │
│  │ Counter     │  │ AutoCommit  │  │    Checker              │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                      AI 接口层 (AI Layer)                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  上下文注入 → AI 生成 → 结果解析 → 质量检查 → 保存           ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 层次职责

| 层级 | 职责 | 组件 |
|------|------|------|
| **用户层** | 用户交互入口 | CLI、配置文件、Markdown文件 |
| **核心框架层** | 核心业务逻辑 | 记忆、数值、伏笔、语言、世界观、提示词生成 |
| **数据存储层** | 数据持久化 | YAML、Markdown、SQLite |
| **自动化层** | 后台自动化任务 | 统计、提交、检查 |
| **AI接口层** | AI模型交互 | 上下文注入、生成、解析 |

---

## 2. 核心模块设计

### 2.1 记忆系统 (Memory System)

**职责：** 管理长篇小说的上下文信息

**四层架构：**

```
┌────────────────────────────────────┐
│  L1: 工作记忆 (Working Memory)     │  ← 当前章节 + 最近5章摘要
│  容量：~4000 tokens                │
├────────────────────────────────────┤
│  L2: 知识图谱 (Knowledge Graph)    │  ← 角色关系、事件时间线
│  结构化实体关系                    │
├────────────────────────────────────┤
│  L3: 摘要索引 (Summary Index)      │  ← 每章摘要 + 关键词
│  支持快速检索                      │
├────────────────────────────────────┤
│  L4: 完整档案 (Full Archive)       │  ← 所有章节完整内容
│  按需查询                          │
└────────────────────────────────────┘
```

**核心类：**

```python
class MemorySystem:
    def __init__(self, project_root: str):
        self.working_memory = WorkingMemory()
        self.knowledge_graph = KnowledgeGraph()
        self.summary_index = SummaryIndex()
        self.archive = FullArchive()
    
    def get_context(self, chapter_num: int) -> dict:
        """获取指定章节的上下文"""
        pass
    
    def update(self, chapter_num: int, content: str):
        """更新记忆系统"""
        pass
    
    def search(self, query: str) -> list:
        """搜索相关内容"""
        pass
```

### 2.2 数值系统 (Stats System)

**职责：** 管理角色数值、技能、物品等数据

**数据结构：**

```yaml
# data/stats/snapshots/ch_001-010.yaml
range:
  start: 1
  end: 10

characters:
  ye_fan:  # 角色ID
    ch_001:  # 章节快照
      level: 1
      cultivation: "凡人"
      hp: 100
      mp: 0
      attack: 10
      defense: 5
      skills: []
      items: []
    
    ch_005:  # 第5章快照
      level: 5
      cultivation: "炼气一层"
      hp: 200
      mp: 50
      attack: 25
      defense: 12
      skills:
        - name: "基础剑法"
          level: 1
      items:
        - "铁剑"
      changes:  # 变更日志
        - "突破炼气一层"
        - "获得铁剑"
```

**核心类：**

```python
class StatsSystem:
    def __init__(self, project_root: str):
        self.snapshots_dir = Path(project_root) / "data" / "stats" / "snapshots"
        self.formulas = self.load_formulas()
    
    def get_snapshot(self, character_id: str, chapter: int) -> dict:
        """获取角色在指定章节的数值"""
        pass
    
    def update_snapshot(self, character_id: str, chapter: int, data: dict):
        """更新角色数值"""
        pass
    
    def calculate_damage(self, attacker: dict, skill: dict) -> int:
        """计算技能伤害"""
        pass
    
    def validate_consistency(self) -> list:
        """验证数值一致性"""
        pass
```

### 2.3 伏笔系统 (Foreshadowing System)

**职责：** 管理伏笔的生命周期

**伏笔状态：**
- `planted` - 已埋下
- `hinted` - 已强化/提示
- `ready` - 准备揭示
- `revealed` - 已揭示
- `abandoned` - 已放弃

**数据结构：**

```yaml
# data/foreshadowing/active.yaml
foreshadowing:
  - id: "fs_001"
    type: "道具"  # 道具/角色/事件/设定
    title: "神秘玉佩的真正用途"
    
    # 埋设信息
    planted:
      chapter: 1
      description: "叶凡在遗迹中获得神秘玉佩"
    
    # 强化记录
    hints:
      - chapter: 5
        content: "玉佩在危险时发热"
      - chapter: 20
        content: "玉佩与传承功法共鸣"
    
    # 揭示计划
    reveal:
      target_range: [80, 120]
      planned_chapter: null
    
    # 状态
    status: "planted"
    importance: "critical"  # critical/major/minor
    
    # 元数据
    created: "2026-03-11"
    last_updated: "2026-03-11"
```

**核心类：**

```python
class ForeshadowingSystem:
    def __init__(self, project_root: str):
        self.active_file = Path(project_root) / "data" / "foreshadowing" / "active.yaml"
        self.completed_file = Path(project_root) / "data" / "foreshadowing" / "completed.yaml"
    
    def plant(self, fs_data: dict) -> str:
        """埋下新伏笔"""
        pass
    
    def add_hint(self, fs_id: str, chapter: int, content: str):
        """添加伏笔强化"""
        pass
    
    def reveal(self, fs_id: str, chapter: int):
        """揭示伏笔"""
        pass
    
    def get_reminders(self, current_chapter: int) -> list:
        """获取当前应提醒的伏笔"""
        pass
    
    def get_status_report(self) -> dict:
        """获取伏笔状态报告"""
        pass
```

### 2.4 语言检查器 (Language Linter)

**职责：** 检查语言规范，确保纯中文输出

**核心功能：**
- 英文单词检测
- 白名单管理
- 生成检查报告

```python
class LanguageLinter:
    def __init__(self, project_root: str):
        self.whitelist = self.load_whitelist()
    
    def check_file(self, file_path: str) -> dict:
        """检查单个文件"""
        pass
    
    def check_chapter(self, chapter_path: str) -> dict:
        """检查章节"""
        violations = []
        with open(chapter_path, 'r') as f:
            content = f.read()
        
        # 移除 YAML front matter
        # 移除代码块
        
        # 检测英文
        english_words = re.findall(r'\b[a-zA-Z]+\b', content)
        for word in english_words:
            if word not in self.whitelist:
                violations.append(word)
        
        return {
            "file": chapter_path,
            "violations": violations,
            "count": len(violations),
            "passed": len(violations) == 0
        }
```

### 2.5 世界观库 (World Repository)

**职责：** 管理小说世界观设定

**数据结构：**

```yaml
# data/world/cultivation.yaml
system:
  name: "天道修炼体系"
  type: "等级制"
  
  realms:  # 境界
    - name: "凡人"
      level: 0
      description: "未开始修炼"
    - name: "炼气期"
      level: 1
      stages: ["初期", "中期", "后期", "巅峰"]
      description: "吸收天地灵气"
    - name: "筑基期"
      level: 2
      stages: ["初期", "中期", "后期", "巅峰"]
      description: "铸造道基"
    # ... 更多境界
  
  breakthrough_rules:
    - from: "炼气期巅峰"
      to: "筑基期初期"
      requirements:
        - "修为达到炼气巅峰"
        - "筑基丹或机缘"
```

### 2.6 提示词生成器 (Prompt Generator)

**职责：** 为AI生成写作提示词

**核心流程：**

```python
class PromptGenerator:
    def __init__(self, project_root: str):
        self.memory = MemorySystem(project_root)
        self.stats = StatsSystem(project_root)
        self.foreshadowing = ForeshadowingSystem(project_root)
        self.world = WorldRepository(project_root)
    
    def generate(self, chapter_num: int, context: dict = None) -> str:
        """生成章节写作提示词"""
        prompt_parts = []
        
        # 1. 基础指令
        prompt_parts.append(self._base_instructions())
        
        # 2. 角色数值（相关角色）
        if context and "characters" in context:
            prompt_parts.append(self._character_stats(context["characters"], chapter_num))
        
        # 3. 伏笔提醒
        reminders = self.foreshadowing.get_reminders(chapter_num)
        if reminders:
            prompt_parts.append(self._foreshadowing_reminders(reminders))
        
        # 4. 前文摘要
        summary = self.memory.get_summary(chapter_num - 1)
        if summary:
            prompt_parts.append(self._previous_summary(summary))
        
        # 5. 章节模板（如有）
        if context and "template" in context:
            prompt_parts.append(self._apply_template(context["template"]))
        
        return "\n\n".join(prompt_parts)
    
    def _base_instructions(self) -> str:
        return """## 写作规范
1. 严格使用中文，不要出现英文（游戏术语如HP、MP、BUG等除外）
2. 保持与前文的一致性，角色数值、性格、关系不能矛盾
3. 章节字数：2500-4000字
4. 注意埋设和强化伏笔"""
```

---

## 3. 数据流设计

### 3.1 写作流程数据流

```
用户请求写作第N章
       ↓
┌──────────────────┐
│ 1. 解析请求       │
│    获取章节号N    │
└──────────────────┘
       ↓
┌──────────────────┐
│ 2. 收集上下文     │
│    ├─ 角色数值    │ ← StatsSystem
│    ├─ 活跃伏笔    │ ← ForeshadowingSystem
│    ├─ 前文摘要    │ ← MemorySystem
│    └─ 世界设定    │ ← WorldRepository
└──────────────────┘
       ↓
┌──────────────────┐
│ 3. 生成提示词     │
│    PromptGenerator│
└──────────────────┘
       ↓
┌──────────────────┐
│ 4. AI生成内容     │
│    (外部AI模型)   │
└──────────────────┘
       ↓
┌──────────────────┐
│ 5. 质量检查       │
│    ├─ 语言检查    │ ← LanguageLinter
│    └─ 数值验证    │ ← StatsSystem
└──────────────────┘
       ↓
┌──────────────────┐
│ 6. 保存章节       │
│    更新各系统     │
└──────────────────┘
       ↓
┌──────────────────┐
│ 7. 后台自动化     │
│    ├─ 字数统计    │
│    └─ Git提交     │
└──────────────────┘
```

### 3.2 更新流程

```
新章节保存后：
       ↓
┌──────────────────┐
│ 更新记忆系统     │
│ ├─ 生成摘要      │
│ ├─ 更新知识图谱  │
│ └─ 存入档案      │
└──────────────────┘
       ↓
┌──────────────────┐
│ 更新数值快照     │
│ (如有数值变化)   │
└──────────────────┘
       ↓
┌──────────────────┐
│ 更新伏笔状态     │
│ (如有伏笔操作)   │
└──────────────────┘
       ↓
┌──────────────────┐
│ 触发自动化       │
│ ├─ 字数统计      │
│ └─ Git提交       │
└──────────────────┘
```

---

## 4. 接口定义

### 4.1 核心模块接口

```python
# 所有核心模块的基类
class BaseModule:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
    
    def load(self) -> None:
        """加载数据"""
        raise NotImplementedError
    
    def save(self) -> None:
        """保存数据"""
        raise NotImplementedError
    
    def validate(self) -> List[str]:
        """验证数据，返回错误列表"""
        raise NotImplementedError
```

### 4.2 工具脚本接口

所有工具脚本应支持以下标准：

```bash
# 帮助信息
python tools/<tool_name>.py --help

# 指定项目路径（可选，默认当前目录）
python tools/<tool_name>.py --project /path/to/project

# 输出格式（可选）
python tools/<tool_name>.py --format json|yaml|text

# 静默模式（可选）
python tools/<tool_name>.py --quiet
```

### 4.3 配置文件接口

```yaml
# .novel/config.yaml - 主配置文件

# 小说信息
novel:
  title: "小说标题"
  author: "作者"
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
  whitelist: ".novel/whitelist.txt"

# 自动化
automation:
  auto_commit: true
  commit_delay: 5
  auto_count: true

# 数值系统
stats:
  snapshot_interval: 10

# 伏笔系统
foreshadowing:
  reminder_threshold: 20
```

---

## 5. 扩展性设计

### 5.1 插件系统

```python
# 插件基类
class NovelPlugin:
    """插件基类"""
    
    name: str = ""
    version: str = "1.0"
    
    def on_chapter_save(self, chapter_num: int, content: str):
        """章节保存时触发"""
        pass
    
    def on_stats_update(self, character_id: str, stats: dict):
        """数值更新时触发"""
        pass
    
    def on_foreshadowing_plant(self, fs_id: str, data: dict):
        """埋下伏笔时触发"""
        pass

# 插件管理器
class PluginManager:
    def __init__(self):
        self.plugins: List[NovelPlugin] = []
    
    def register(self, plugin: NovelPlugin):
        self.plugins.append(plugin)
    
    def trigger(self, event: str, *args, **kwargs):
        for plugin in self.plugins:
            method = getattr(plugin, f"on_{event}", None)
            if method:
                method(*args, **kwargs)
```

### 5.2 可选模块

以下模块为可选增强功能：

| 模块 | 用途 | 依赖 |
|------|------|------|
| **知识图谱** | 复杂关系可视化 | Neo4j |
| **向量检索** | 语义相似度搜索 | Chroma/FAISS |
| **Web界面** | 可视化管理 | Flask/FastAPI |
| **导出工具** | 多格式导出 | Pandoc |

---

## 6. 与现有项目集成

### 6.1 fanqie-novel-uploader 集成

```
ai-novel-framework/
├── ... 框架核心文件
└── integrations/
    └── fanqie/
        ├── uploader.py      # 番茄小说上传器
        └── config.yaml      # 番茄小说配置
```

**集成接口：**

```python
# integrations/fanqie/uploader.py
class FanqieUploader:
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
    
    def upload_chapter(self, chapter_path: str) -> dict:
        """上传章节到番茄小说"""
        # 读取章节
        # 转换格式
        # 调用番茄API
        # 返回结果
        pass
```

---

## 7. 性能考虑

### 7.1 缓存策略

- 章节摘要：内存缓存最近10章
- 数值快照：内存缓存最新快照
- 白名单：启动时加载到内存

### 7.2 文件组织

- 按卷分目录，避免单目录文件过多
- 数值快照每10章一个文件
- 定期归档历史数据

### 7.3 性能指标

| 操作 | 目标时间 |
|------|---------|
| 字数统计 | <1秒/百万字 |
| 数值查询 | <100ms |
| 伏笔检索 | <200ms |
| Git提交 | <5秒 |
| 语言检查 | <5秒/章 |

---

**文档状态：** ✅ 完成  
**下一步：** 数据结构设计 (DATA_DESIGN.md)
