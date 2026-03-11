# AI网文小说写作框架 - 使用指南

> 本指南帮助 AI 快速上手使用框架进行网文小说创作

---

## 🚀 快速开始

### 一、 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/solutioinquick852-art/novel-framework/master/remote-install.sh | bash
```

### 2. 安装完成后
```bash
# 添加到 PATH（如果需要）
export PATH="$HOME/.local/bin:$PATH"

# 创建新小说项目
novel init --name "我的小说"
```

---

## 📖 详细使用方法

### 创建新项目
```bash
# 基础用法
novel init --name "小说名"

# 完整选项
novel init --name "天道至尊" \
    --author "作者名" \
    --genre "玄幻" \
    --target-words 3000000
```

### 安装选项
| 选项 | 说明 |
|------|------|
| `--name, -n` | 小说名称 |
| `--socket, -s` | 指定安装路径（默认=仓库名） |
| `--author, -a` | 作者 |
| `--genre, -g` | 类型（玄幻/都市/仙侠/科幻) |
| `--target-words, -w` | 目标字数 |
| `--no-github` | 不创建 GitHub 仓库 |
| `--public` | 创建公开仓库（默认私有） |

---

## 📁 项目结构

```
novel-project/
├── .novel/
│   └── config.yaml       # 配置文件
├── workflow/
│   ├── planning-review/   # 待审核（Writer 放这里）
│   ├── revisions/        # 修改中（审核不通过）
│   └── ready-to-publish/  # 待发布（审核通过）
├── content/
│   ├── volumes/vol_01/   # 正式内容
│   └── outlines/         # 大纲
├── data/
│   ├── characters/        # 角色设定
│   ├── stats/             # 数值快照
│   ├── foreshadowing/     # 伏笔管理
│   └── world/              # 世界观
├── reports/               # 统计报告
└── tools/                # 工具脚本
```

---

## 🔄 工作流程

```
┌─────────────┐
│  Writer 写作  │
└──────┬──────┘
       ↓
┌──────────────────┐
│ planning-review/ │  ← Writer 放这里
└──────┬───────────┘
       ↓
┌──────────────┐
│ Reviewer 审核 │
└──┬───────┬───┘
       ↓
    ┌─────────┴─────────────┐
    │ 通过 ✓            │ 不通过 ✗ │
    ↓                 ↓
    ┌───────────────┐  ┌───────────────┐
    │ ready-to-publish/│  │ revisions/     │
    └───────┬──────┘  └───────┬──────┘
       ↓                  ↓
    ┌─────────────────┐
    │ 自动发布监控    │  │ Writer 修改后重新提交 │
    └───────┬───────────┘  └─────────────────┘
       ↓                  ↓
    ┌───────────────┐
    │ 发布到 GitHub     │  │ 重新审核      │
    └─────────────────┘  └───────────────┘
```

---

## 🛠 寽令速查

### Writer 命令

```bash
# 写完章节，cp ch_001.md workflow/planning-review/

# 查看所有待审核章节
./tools/review.sh status
```

### Reviewer 命令

```bash
# 查看状态
./tools/review.sh status

# 审核通过
./tools/review.sh approve ch_001.md

# 需要修改
./tools/review.sh revise ch_002.md

# 修改完成后重新提交
./tools/review.sh resubmit ch_002.md
```

### 自动发布命令
```bash
# 启动监控（后台运行）
./tools/auto_publish.sh start

# 查看监控状态
./tools/auto_publish.sh status

# 手动发布一次
./tools/auto_publish.sh once

# 查看发布日志
./tools/auto_publish.sh log

# 停止监控
./tools/auto_publish.sh stop
```

---

## 📊 数据管理命令

### 数值系统
```bash
# 查看角色数值
novel stats get ye_fan --chapter 1

# 验证数值一致性
novel stats validate

# 查看所有角色
novel stats get
```

### 伏笔管理
```bash
# 列出所有伏笔
novel fs list

# 获取伏笔提醒
novel fs remind

# 查看特定状态的伏笔
novel fs list --status active
```

---

## 💡 写作提示词示例

当您需要让 AI 写新章节时，可以使用以下提示词模板：

```
请使用 AI网文小说写作框架为我创建/续写第N章。

## 框架位置
/home/worker/.openclaw/workspace/ai-novel-framework

## 当前状态
- 最新章节：第X章
- 当前字数：XXX 字
- 主角数值：
  - 等级： X
  - 境界： XXX
  - 生命值： XXX
  - 攻击力： XXX

## 需要参考的数据

### 角色数值
请查看 `data/stats/snapshots/` 获取当前数值

### 活跃伏笔
请查看 `data/foreshadowing/active.yaml`

### 世界观设定
请查看 `data/world/` 目录

## 章节要求
- 字数： 2500-4000字
- 纯中文（游戏术语如HP、MP等除外）
- 保持与前文一致

## 输出
1. 保存章节到 `workflow/planning-review/`
2. 更新相关数据文件（如有变化）
```

---

## 🔧 高级配置

### 修改检查间隔
编辑 `tools/auto_publish.sh` 中的 `INTERVAL` 变量

### 修改仓库名格式
编辑 `src/cli/main.py` 中的 `get_pinyin()` 函数

### 添加新的语言白名单
编辑 `.novel/whitelist.txt`

---

## 📞 常见问题

**Q: 监控不工作？**
A: 检查是否有进程在运行： `./tools/auto_publish.sh status`

**Q: 忘记添加到 PATH？**
A: 运行 `export PATH="$HOME/.local/bin:$PATH"`

**Q: 如何更新框架？**
A: 重新运行安装脚本即可

---

## 🌟 最佳实践

1. **定期备份** - 定期提交到 Git
2. **审核及时** - 避免章节堆积
3. **保持数值更新** - 每次有变化时更新数值快照
4. **管理伏笔** - 定期查看伏笔提醒

---

**祝创作顺利！** 🎉
