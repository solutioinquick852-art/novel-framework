# AI网文小说写作框架

一个专为AI辅助网文创作设计的框架系统，支持长篇小说的连贯性管理。

## ✨ 核心功能

- 📚 **长篇连贯性** - 混合记忆架构，支持数百万字
- 🔢 **数值系统** - 角色属性、技能伤害自动追踪
- 🎯 **伏笔管理** - 生命周期追踪，自动提醒
- 🌐 **语言规范** - 中文输出，自动检查
- 📊 **字数统计** - 自动统计，不消耗AI token
- 🔄 **自动发布** - 审核通过后自动推送到GitHub

## 🚀 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/solutioinquick852-art/novel-framework/main/remote-install.sh | bash
```

安装完成后：
```bash
# 添加到 PATH（如果需要）
export PATH="$HOME/.local/bin:$PATH"

# 创建新小说项目
novel init --name "我的小说"
```

## 📖 使用方法

### 初始化项目

```bash
# 创建新小说
novel init --name "天道至尊" --author "作者名"

# 带更多选项
novel init --name "修仙模拟器" \
    --author "作者" \
    --genre "玄幻" \
    --target-words 3000000
```

### 工作流程

```
Writer 写作 → planning-review/ → Reviewer 审核
                                      ↓
                            ┌─────────┴─────────┐
                            ↓                   ↓
                        通过 ✓              不通过 ✗
                            ↓                   ↓
                   ready-to-publish/      revisions/
                            ↓                   ↓
                      自动发布 ←←←←← 修改后重新提交
```

### 审核命令

```bash
# 查看状态
./tools/review.sh status

# 审核通过
./tools/review.sh approve ch_001.md

# 需要修改
./tools/review.sh revise ch_001.md

# 重新提交
./tools/review.sh resubmit ch_001.md
```

### 自动发布

```bash
# 启动监控（后台运行）
./tools/auto_publish.sh start

# 查看状态
./tools/auto_publish.sh status

# 停止监控
./tools/auto_publish.sh stop

# 查看日志
./tools/auto_publish.sh log
```

## 📁 项目结构

```
novel-project/
├── workflow/
│   ├── planning-review/      # 待审核
│   ├── revisions/            # 修改中
│   └── ready-to-publish/     # 待发布
├── content/
│   ├── volumes/              # 正式内容
│   └── outlines/             # 大纲
├── data/
│   ├── characters/           # 角色设定
│   ├── stats/                # 数值快照
│   ├── foreshadowing/        # 伏笔管理
│   └── world/                # 世界观
├── reports/                  # 统计报告
└── tools/                    # 自动化脚本
```

## 🛠 更多选项

```bash
# 指定安装路径
curl -fsSL URL | bash -s -- --dir /opt/novel

# 全局安装（需要 sudo）
curl -fsSL URL | bash -s -- --global

# 查看帮助
curl -fsSL URL | bash -s -- --help
```

## 📄 License

MIT
