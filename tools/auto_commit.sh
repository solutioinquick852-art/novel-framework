#!/bin/bash
# Git自动提交工具
# 用于自动提交小说更新

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 进入项目目录
cd "$PROJECT_ROOT"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印帮助信息
print_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -m, --message MSG   自定义提交信息"
    echo "  -d, --delay SECONDS 延迟提交（默认5秒）"
    echo "  -n, --dry-run       只显示将要执行的操作，不实际执行"
    echo "  -p, --push          提交后自动推送"
    echo "  -h, --help          显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                    # 自动提交"
    echo "  $0 -m \"添加第51章\"     # 自定义提交信息"
    echo "  $0 -p                 # 提交并推送"
    echo "  $0 -d 10              # 延迟10秒后提交"
}

# 解析参数
MESSAGE=""
DELAY=0
DRY_RUN=false
PUSH=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--message)
            MESSAGE="$2"
            shift 2
            ;;
        -d|--delay)
            DELAY="$2"
            shift 2
            ;;
        -n|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -p|--push)
            PUSH=true
            shift
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            print_help
            exit 1
            ;;
    esac
done

# 检查是否在Git仓库中
if [ ! -d ".git" ]; then
    echo -e "${RED}✗ 当前目录不是Git仓库${NC}"
    exit 1
fi

# 检查是否有更改
if git diff --quiet && git diff --staged --quiet; then
    echo -e "${YELLOW}没有需要提交的更改${NC}"
    exit 0
fi

# 获取最新章节号
get_latest_chapter() {
    local latest=0
    for file in $(find content/volumes -name "ch_*.md" 2>/dev/null); do
        local num=$(basename "$file" | grep -oP 'ch_\K\d+')
        if [ ! -z "$num" ] && [ "$num" -gt "$latest" ]; then
            latest=$num
        fi
    done
    echo $latest
}

# 获取字数统计
get_word_count() {
    if [ -f "tools/count_words.py" ]; then
        python3 tools/count_words.py --quick 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# 生成提交信息
generate_commit_message() {
    if [ ! -z "$MESSAGE" ]; then
        echo "$MESSAGE"
        return
    fi
    
    local latest_ch=$(get_latest_chapter)
    local word_count=$(get_word_count)
    
    if [ "$latest_ch" -gt 0 ]; then
        echo "更新至第${latest_ch}章 | 当前字数：${word_count}"
    else
        echo "更新内容"
    fi
}

# 延迟
if [ "$DELAY" -gt 0 ]; then
    echo -e "${YELLOW}等待 ${DELAY} 秒后提交...${NC}"
    sleep "$DELAY"
fi

# 生成提交信息
COMMIT_MSG=$(generate_commit_message)

# 显示将要执行的操作
echo -e "${GREEN}将要执行的操作：${NC}"
echo "  提交信息: $COMMIT_MSG"
if [ "$PUSH" = true ]; then
    echo "  推送: 是"
fi
echo ""

# 干运行模式
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY-RUN] 不会实际执行${NC}"
    echo "将执行的命令:"
    echo "  git add -A"
    echo "  git commit -m \"$COMMIT_MSG\""
    if [ "$PUSH" = true ]; then
        echo "  git push"
    fi
    exit 0
fi

# 执行提交
echo -e "${GREEN}正在提交...${NC}"
git add -A
git commit -m "$COMMIT_MSG"

if [ "$PUSH" = true ]; then
    echo -e "${GREEN}正在推送...${NC}"
    git push
fi

echo -e "${GREEN}✓ 已提交：$COMMIT_MSG${NC}"
