#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI网文小说写作框架 - CLI入口
支持自动创建GitHub仓库和Git自动化
"""

import sys
import argparse
import subprocess
import re
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


def get_pinyin(text):
    """将中文转换为拼音"""
    try:
        from pypinyin import pinyin, Style
        # 转换为拼音列表
        py_list = pinyin(text, style=Style.NORMAL)
        # 拼接并转小写
        result = ''.join([p[0] for p in py_list])
        # 只保留字母和数字
        result = re.sub(r'[^a-z0-9]', '', result.lower())
        return result or 'novel'
    except ImportError:
        # 如果没有pypinyin，使用内置简单拼音映射
        simple_map = {
            '修': 'xiu', '仙': 'xian', '模': 'mo', '拟': 'ni', '器': 'qi',
            '天': 'tian', '道': 'dao', '至': 'zhi', '尊': 'zun',
            '我': 'wo', '的': 'de', '小': 'xiao', '说': 'shuo',
            '神': 'shen', '魔': 'mo', '幻': 'huan', '世': 'shi', '界': 'jie',
            '传': 'chuan', '奇': 'qi', '武': 'wu', '侠': 'xia',
            '都': 'du', '市': 'shi', '异': 'yi', '能': 'neng',
            '科': 'ke', '技': 'ji', '末': 'mo', '日': 'ri',
            '历': 'li', '史': 'shi', '军': 'jun', '事': 'shi',
        }
        result = ''
        for char in text:
            if char in simple_map:
                result += simple_map[char]
            elif '\u4e00' <= char <= '\u9fff':
                result += 'x'  # 未知中文字符
            else:
                result += char.lower()
        # 只保留字母和数字
        result = re.sub(r'[^a-z0-9]', '', result)
        return result or 'novel'


def create_github_repo(repo_name, description, private=True):
    """创建GitHub仓库"""
    try:
        # 检查gh命令是否可用
        result = subprocess.run(['gh', '--version'], capture_output=True)
        if result.returncode != 0:
            return False, "gh CLI 未安装"
        
        # 创建仓库
        cmd = ['gh', 'repo', 'create', repo_name]
        if private:
            cmd.append('--private')
        cmd.extend(['--description', description])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)


def cmd_init(args):
    """初始化项目 - 创建文件夹、配置自动化、创建GitHub仓库"""
    import yaml
    
    novel_name = args.name or "我的小说"
    author = args.author or "作者"
    
    # 生成仓库名：novel + 拼音
    pinyin_name = get_pinyin(novel_name)
    repo_name = f"novel-{pinyin_name}"
    
    # 确定项目路径
    if args.path:
        project_path = Path(args.path)
    else:
        project_path = Path.cwd() / repo_name
    
    print(f"\n{'='*50}")
    print(f"🚀 初始化小说项目")
    print(f"{'='*50}")
    print(f"小说名称: {novel_name}")
    print(f"仓库名称: {repo_name}")
    print(f"项目路径: {project_path}")
    print(f"{'='*50}\n")
    
    # ===== 1. 创建目录结构 =====
    print("📁 创建目录结构...")
    project_path.mkdir(parents=True, exist_ok=True)
    
    dirs = [
        ".novel",
        "data/characters/main",
        "data/characters/support",
        "data/stats/snapshots",
        "data/foreshadowing/archive",
        "data/world",
        "data/memory/summaries",
        "content/volumes/vol_01",
        "content/outlines",
        "workflow/planning-review",      # 待审核
        "workflow/revisions",             # 修改中
        "workflow/ready-to-publish",      # 审核通过，待发布
        "reports/stats",
        "reports/quality",
        "tools",
    ]
    
    for d in dirs:
        (project_path / d).mkdir(parents=True, exist_ok=True)
    print("   ✓ 目录结构创建完成")
    
    # ===== 2. 创建配置文件 =====
    print("⚙️  创建配置文件...")
    
    config = {
        "novel": {
            "title": novel_name,
            "author": author,
            "genre": args.genre or "玄幻",
            "target_words": args.target_words or 3000000,
            "status": "ongoing",
            "repo_name": repo_name,
            "created": datetime.now().strftime("%Y-%m-%d")
        },
        "language": {
            "primary": "zh-CN",
            "allow_english": False,
            "whitelist": ".novel/whitelist.txt"
        },
        "automation": {
            "auto_commit": {
                "enabled": True,
                "delay": 5,
                "branch": "main"
            },
            "auto_count": {"enabled": True},
            "auto_sync": {"enabled": True}
        },
        "stats": {"snapshot_interval": 10},
        "foreshadowing": {"reminder_threshold": 20}
    }
    
    config_path = project_path / ".novel" / "config.yaml"
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    print("   ✓ 配置文件创建完成")
    
    # 创建白名单
    whitelist = ["HP", "MP", "EXP", "LV", "BUG", "GG", "ID", "NPC", "BOSS",
                 "AOE", "DOT", "CD", "PVP", "PVE", "AFK", "OP", "UP", "UID"]
    whitelist_path = project_path / ".novel" / "whitelist.txt"
    with open(whitelist_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(whitelist))
    
    # 创建示例数值快照
    snapshot = {
        "range": {"start": 1, "end": 10},
        "characters": {}
    }
    snapshot_path = project_path / "data/stats/snapshots/ch_001-010.yaml"
    with open(snapshot_path, 'w', encoding='utf-8') as f:
        yaml.dump(snapshot, f, allow_unicode=True, default_flow_style=False)
    
    # 创建伏笔文件
    fs_active = {"foreshadowing": []}
    fs_path = project_path / "data/foreshadowing/active.yaml"
    with open(fs_path, 'w', encoding='utf-8') as f:
        yaml.dump(fs_active, f, allow_unicode=True, default_flow_style=False)
    print("   ✓ 数据模板创建完成")
    
    # ===== 3. 创建.gitignore =====
    print("🔧 配置Git...")
    gitignore = """# 临时文件
*.pyc
__pycache__/
.DS_Store
*.swp
*.swo

# 编辑器
.vscode/
.idea/
*.sublime-*

# 备份
backups/
*.bak

# 日志
*.log

# 环境
.env
venv/
.envrc
"""
    with open(project_path / ".gitignore", 'w') as f:
        f.write(gitignore)
    
    # ===== 4. Git初始化 =====
    try:
        subprocess.run(['git', 'init'], cwd=project_path, capture_output=True)
        subprocess.run(['git', 'add', '.'], cwd=project_path, capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'初始化项目: {novel_name}'], 
                      cwd=project_path, capture_output=True)
        print("   ✓ Git仓库初始化完成")
    except Exception as e:
        print(f"   ⚠️ Git初始化失败: {e}")
    
    # ===== 5. 创建GitHub仓库 =====
    if not args.no_github:
        print("\n📤 创建GitHub仓库...")
        success, message = create_github_repo(
            repo_name,
            f"小说《{novel_name}》- AI辅助创作项目",
            private=not args.public
        )
        
        if success:
            print(f"   ✓ GitHub仓库创建成功")
            print(f"   📎 {message}")
            
            # 关联远程仓库并推送
            try:
                github_user = subprocess.check_output(
                    ['gh', 'api', 'user', '-q', '.login'],
                    text=True
                ).strip()
                remote_url = f"git@github.com:{github_user}/{repo_name}.git"
                
                subprocess.run(['git', 'remote', 'add', 'origin', remote_url],
                             cwd=project_path, capture_output=True)
                subprocess.run(['git', 'branch', '-M', 'main'],
                             cwd=project_path, capture_output=True)
                subprocess.run(['git', 'push', '-u', 'origin', 'main'],
                             cwd=project_path, capture_output=True)
                print("   ✓ 代码已推送到GitHub")
            except Exception as e:
                print(f"   ⚠️ 推送失败: {e}")
        else:
            print(f"   ⚠️ GitHub仓库创建失败: {message}")
            print("   提示: 请确保已安装 gh CLI 并已登录 (gh auth login)")
    
    # ===== 6. 创建自动提交脚本 =====
    print("\n🤖 创建自动化脚本...")
    
    # 自动发布脚本 - 监控 ready-to-publish 文件夹
    auto_publish = f'''#!/bin/bash
# 自动监控发布脚本 - {novel_name}
# 监控 workflow/ready-to-publish/ 文件夹，自动发布到 GitHub

PROJECT_DIR="{project_path}"
READY_DIR="$PROJECT_DIR/workflow/ready-to-publish"
CONTENT_DIR="$PROJECT_DIR/content/volumes/vol_01"
LOG_FILE="$PROJECT_DIR/reports/publish.log"
INTERVAL=10  # 检查间隔（秒）

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

log() {{
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}}

publish_files() {{
    cd "$PROJECT_DIR"
    
    # 查找待发布文件
    FILES=$(find "$READY_DIR" -name "*.md" -type f 2>/dev/null)
    
    if [ -z "$FILES" ]; then
        return 0
    fi
    
    log "📤 发现待发布章节..."
    
    # 处理每个文件
    for FILE in $FILES; do
        FILENAME=$(basename "$FILE")
        
        # 移动到正式内容目录
        mv "$FILE" "$CONTENT_DIR/$FILENAME"
        log "   ✓ 发布: $FILENAME"
    done
    
    # 获取最新章节号
    LATEST=$(find "$CONTENT_DIR" -name "ch_*.md" -type f 2>/dev/null | sort | tail -1)
    if [ -n "$LATEST" ]; then
        CHAPTER=$(basename "$LATEST" .md | sed 's/ch_//')
        MSG="发布第${{CHAPTER}}章"
    else
        MSG="发布更新 | $(date '+%Y-%m-%d %H:%M')"
    fi
    
    # Git 提交
    git add -A
    git commit -m "$MSG" 2>/dev/null
    git push 2>/dev/null
    
    log "✅ $MSG"
}}

# PID 文件
PID_FILE="/tmp/novel-$(echo '{novel_name}' | md5sum | cut -c1-8).pid"

case "$1" in
    start)
        # 检查是否已有监控进程
        if [ -f "$PID_FILE" ]; then
            OLD_PID=$(cat "$PID_FILE")
            if ps -p "$OLD_PID" > /dev/null 2>&1; then
                echo "⚠️ 监控已在运行 (PID: $OLD_PID)"
                echo "使用 '$0 stop' 停止监控"
                exit 1
            fi
        fi
        
        echo "🚀 启动自动发布监控..."
        echo "   小说: {novel_name}"
        echo "   监控: $READY_DIR"
        echo "   间隔: ${{INTERVAL}}秒"
        echo "   日志: $LOG_FILE"
        echo ""
        echo "按 Ctrl+C 停止"
        echo ""
        
        echo $$ > "$PID_FILE"
        
        while true; do
            publish_files
            sleep "$INTERVAL"
        done
        ;;
    
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            kill "$PID" 2>/dev/null
            rm "$PID_FILE"
            echo "⏹️ 监控已停止"
        else
            echo "⚠️ 没有运行中的监控"
        fi
        ;;
    
    status)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "✅ 监控运行中 (PID: $PID)"
            else
                echo "⚠️ 监控进程已退出"
                rm -f "$PID_FILE"
            fi
        else
            echo "⏹️ 监控未运行"
        fi
        
        echo ""
        echo "📋 待发布文件:"
        FILES=$(find "$READY_DIR" -name "*.md" -type f 2>/dev/null)
        if [ -n "$FILES" ]; then
            for FILE in $FILES; do
                echo "   $(basename "$FILE")"
            done
        else
            echo "   (空)"
        fi
        ;;
    
    once)
        publish_files
        ;;
    
    log)
        if [ -f "$LOG_FILE" ]; then
            tail -20 "$LOG_FILE"
        else
            echo "暂无日志"
        fi
        ;;
    
    *)
        echo "用法: $0 {{start|stop|status|once|log}}"
        echo ""
        echo "命令:"
        echo "  start   启动持续监控"
        echo "  stop    停止监控"
        echo "  status  查看状态"
        echo "  once    执行一次发布"
        echo "  log     查看发布日志"
        ;;
esac
'''
    
    publish_script = project_path / "tools" / "auto_publish.sh"
    with open(publish_script, 'w') as f:
        f.write(auto_publish)
    subprocess.run(['chmod', '+x', publish_script])
    print("   ✓ 自动监控发布脚本创建完成")
    
    # 审核工具脚本
    review_tool = f'''#!/bin/bash
# 审核工具 - {novel_name}
# 用于移动章节到不同状态目录

PROJECT_DIR="{project_path}"
PLANNING_DIR="$PROJECT_DIR/workflow/planning-review"
REVISIONS_DIR="$PROJECT_DIR/workflow/revisions"
READY_DIR="$PROJECT_DIR/workflow/ready-to-publish"

case "$1" in
    approve)
        # 审核通过：移动到 ready-to-publish
        if [ -z "$2" ]; then
            echo "用法: $0 approve <章节文件>"
            exit 1
        fi
        mv "$PLANNING_DIR/$2" "$READY_DIR/$2"
        echo "✅ 审核通过: $2 → ready-to-publish"
        ;;
    revise)
        # 需要修改：移动到 revisions
        if [ -z "$2" ]; then
            echo "用法: $0 revise <章节文件>"
            exit 1
        fi
        mv "$PLANNING_DIR/$2" "$REVISIONS_DIR/$2"
        echo "📝 需要修改: $2 → revisions"
        ;;
    resubmit)
        # 修改完成：重新提交审核
        if [ -z "$2" ]; then
            echo "用法: $0 resubmit <章节文件>"
            exit 1
        fi
        mv "$REVISIONS_DIR/$2" "$PLANNING_DIR/$2"
        echo "🔄 重新提交: $2 → planning-review"
        ;;
    status)
        # 查看状态
        echo "📊 章节状态"
        echo "==========="
        echo "待审核 (planning-review):"
        ls -1 "$PLANNING_DIR"/*.md 2>/dev/null | xargs -I{{}} basename {{}} || echo "  (空)"
        echo ""
        echo "修改中 (revisions):"
        ls -1 "$REVISIONS_DIR"/*.md 2>/dev/null | xargs -I{{}} basename {{}} || echo "  (空)"
        echo ""
        echo "待发布 (ready-to-publish):"
        ls -1 "$READY_DIR"/*.md 2>/dev/null | xargs -I{{}} basename {{}} || echo "  (空)"
        ;;
    *)
        echo "用法: $0 {{approve|revise|resubmit|status}} <章节文件>"
        ;;
esac
'''
    
    review_script = project_path / "tools" / "review.sh"
    with open(review_script, 'w') as f:
        f.write(review_tool)
    subprocess.run(['chmod', '+x', review_script])
    print("   ✓ 审核工具脚本创建完成")
    
    # ===== 7. 创建README =====
    readme = f'''# {novel_name}

> 作者: {author}  
> 创建时间: {datetime.now().strftime("%Y-%m-%d")}  
> 目标字数: {args.target_words or 3000000:,}

## 工作流程

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

## 目录结构

```
├── workflow/
│   ├── planning-review/      # 待审核
│   ├── revisions/            # 修改中
│   └── ready-to-publish/     # 待发布
├── content/volumes/          # 正式内容
├── data/                     # 设定数据
├── reports/                  # 统计报告
└── tools/                    # 工具脚本
```

## 常用命令

```bash
# Writer: 写完章节放入待审核
cp ch_001.md workflow/planning-review/

# Reviewer: 查看状态
./tools/review.sh status

# Reviewer: 审核通过
./tools/review.sh approve ch_001.md

# Reviewer: 需要修改
./tools/review.sh revise ch_001.md

# 启动自动发布监控（后台运行）
./tools/auto_publish.sh start

# 查看监控状态
./tools/auto_publish.sh status

# 停止监控
./tools/auto_publish.sh stop

# 手动发布一次
./tools/auto_publish.sh once
```
'''
    
    with open(project_path / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme)
    print("   ✓ README创建完成")
    
    # ===== 完成 =====
    print(f"\n{'='*50}")
    print("✅ 项目初始化完成！")
    print(f"{'='*50}")
    print(f"📂 项目路径: {project_path}")
    print(f"🔗 GitHub: novel-{pinyin_name}")
    print(f"\n下一步:")
    print(f"  1. 编辑 .novel/config.yaml 配置小说信息")
    print(f"  2. 在 content/outlines/ 创建大纲")
    print(f"  3. 在 content/volumes/vol_01/ 开始写作")
    print(f"  4. 运行 ./tools/auto_commit.sh 自动提交")
    print(f"{'='*50}\n")


def cmd_stats(args):
    """数值系统管理"""
    from stats.manager import StatsManager
    
    project_root = args.project or Path.cwd()
    manager = StatsManager(project_root)
    
    if args.action == "get":
        char_id = args.character
        chapter = args.chapter or 1
        
        if char_id:
            stats = manager.get_character_snapshot(char_id, chapter)
            if stats:
                print(f"角色: {char_id}")
                print(f"章节: {chapter}")
                print(f"\n数值:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
            else:
                print(f"未找到角色 {char_id} 在第 {chapter} 章的数值")
        else:
            chars = manager.get_all_characters()
            print(f"所有角色: {', '.join(chars) if chars else '无'}")
    
    elif args.action == "validate":
        issues = manager.validate_consistency(args.character)
        if issues:
            print("一致性问题:")
            for issue in issues:
                print(f"  ⚠️ {issue['character']}: {issue['message']}")
        else:
            print("✓ 数值一致性检查通过")


def cmd_fs(args):
    """伏笔管理"""
    from foreshadowing.manager import ForeshadowingManager
    
    project_root = args.project or Path.cwd()
    manager = ForeshadowingManager(project_root)
    
    if args.action == "list":
        fs_list = manager.list_all(
            status=args.status,
            fs_type=args.type,
            importance=args.importance
        )
        
        if fs_list:
            print(f"活跃伏笔 (共{len(fs_list)}个)\n")
            print(f"{'ID':<10} | {'类型':<6} | {'标题':<20} | {'状态':<8}")
            print("-" * 60)
            for fs in fs_list:
                print(f"{fs['id']:<10} | {fs['type']:<6} | {fs['title']:<20} | {fs['status']:<8}")
        else:
            print("无活跃伏笔")
    
    elif args.action == "remind":
        reminders = manager.get_reminders(args.chapter)
        if reminders:
            print("伏笔提醒:\n")
            for r in reminders:
                print(f"  [{r['urgency']}] {r['fs_id']}: {r['title']}")
        else:
            print("暂无需要关注的伏笔")


def cmd_count(args):
    """字数统计"""
    import subprocess
    
    project_root = Path(args.project or Path.cwd())
    count_script = PROJECT_ROOT / "tools" / "count_words.py"
    
    if count_script.exists():
        cmd = [sys.executable, str(count_script), "--project", str(project_root)]
        subprocess.run(cmd)
    else:
        print("字数统计工具未找到")


def cmd_check(args):
    """质量检查"""
    import subprocess
    
    project_root = Path(args.project or Path.cwd())
    check_script = PROJECT_ROOT / "tools" / "check_language.py"
    
    if check_script.exists():
        cmd = [sys.executable, str(check_script), "--project", str(project_root)]
        subprocess.run(cmd)
    else:
        print("语言检查工具未找到")


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="AI网文小说写作框架",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-p", "--project", help="项目路径")
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # init 命令
    init_parser = subparsers.add_parser("init", help="初始化新小说项目")
    init_parser.add_argument("-n", "--name", required=True, help="小说名称")
    init_parser.add_argument("-a", "--author", help="作者")
    init_parser.add_argument("-g", "--genre", help="类型(玄幻/都市/仙侠等)")
    init_parser.add_argument("-w", "--target-words", type=int, help="目标字数")
    init_parser.add_argument("--path", help="项目路径(默认=仓库名)")
    init_parser.add_argument("--no-github", action="store_true", help="不创建GitHub仓库")
    init_parser.add_argument("--public", action="store_true", help="创建公开仓库(默认私有)")
    init_parser.set_defaults(func=cmd_init)
    
    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="数值系统管理")
    stats_parser.add_argument("action", choices=["get", "validate"], help="操作")
    stats_parser.add_argument("-c", "--character", help="角色ID")
    stats_parser.add_argument("--chapter", type=int, help="章节号")
    stats_parser.set_defaults(func=cmd_stats)
    
    # fs 命令 (伏笔)
    fs_parser = subparsers.add_parser("fs", help="伏笔管理")
    fs_parser.add_argument("action", choices=["list", "remind"], help="操作")
    fs_parser.add_argument("--type", help="伏笔类型")
    fs_parser.add_argument("--status", help="状态筛选")
    fs_parser.add_argument("--importance", help="重要性筛选")
    fs_parser.add_argument("--chapter", type=int, help="当前章节")
    fs_parser.set_defaults(func=cmd_fs)
    
    # count 命令
    count_parser = subparsers.add_parser("count", help="字数统计")
    count_parser.set_defaults(func=cmd_count)
    
    # check 命令
    check_parser = subparsers.add_parser("check", help="质量检查")
    check_parser.set_defaults(func=cmd_check)
    
    args = parser.parse_args()
    
    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
