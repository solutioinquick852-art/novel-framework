#!/bin/bash
# AI网文小说写作框架 - 安装脚本
# 支持全局安装和本地安装

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 框架信息
FRAMEWORK_NAME="AI网文小说写作框架"
FRAMEWORK_VERSION="1.0.0"

# 默认安装路径
DEFAULT_INSTALL_DIR="/usr/local/lib/novel-framework"
DEFAULT_BIN_DIR="/usr/local/bin"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "=================================================="
echo "🚀 $FRAMEWORK_NAME 安装程序"
echo "   版本: $FRAMEWORK_VERSION"
echo "=================================================="
echo ""

# 检查 Python
check_python() {
    echo -e "${BLUE}检查 Python...${NC}"
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}❌ 未找到 Python，请先安装 Python 3.8+${NC}"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"
}

# 检查依赖
check_dependencies() {
    echo -e "${BLUE}检查依赖...${NC}"
    
    # 检查 pip（可选）
    if $PYTHON_CMD -m pip --version &> /dev/null; then
        # 安装 Python 依赖（可选）
        echo -e "${BLUE}安装 Python 依赖...${NC}"
        $PYTHON_CMD -m pip install pyyaml pypinyin --quiet --break-system-packages 2>/dev/null || {
            echo -e "${YELLOW}⚠️ 部分依赖安装失败，使用内置功能${NC}"
        }
    else
        echo -e "${YELLOW}⚠️ pip 未安装，将使用内置功能${NC}"
    fi
    
    echo -e "${GREEN}✓ 依赖检查完成${NC}"
}

# 本地安装（当前用户）
install_local() {
    INSTALL_DIR="$HOME/.local/lib/novel-framework"
    BIN_DIR="$HOME/.local/bin"
    
    echo -e "${BLUE}安装模式: 本地安装（当前用户）${NC}"
    echo -e "   安装路径: $INSTALL_DIR"
    echo -e "   命令路径: $BIN_DIR/novel"
    echo ""
    
    # 创建目录
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR"
    
    # 复制框架文件
    echo -e "${BLUE}复制框架文件...${NC}"
    cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/"
    
    # 创建启动脚本
    cat > "$BIN_DIR/novel" << EOF
#!/bin/bash
$PYTHON_CMD "$INSTALL_DIR/src/cli/main.py" "\$@"
EOF
    chmod +x "$BIN_DIR/novel"
    
    # 检查 PATH
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo ""
        echo -e "${YELLOW}⚠️ $BIN_DIR 不在 PATH 中${NC}"
        echo -e "${YELLOW}请运行以下命令添加到 PATH：${NC}"
        echo ""
        echo "    echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
        echo "    source ~/.bashrc"
        echo ""
    fi
    
    echo -e "${GREEN}✓ 本地安装完成${NC}"
}

# 全局安装（需要 sudo）
install_global() {
    INSTALL_DIR="$DEFAULT_INSTALL_DIR"
    BIN_DIR="$DEFAULT_BIN_DIR"
    
    echo -e "${BLUE}安装模式: 全局安装（所有用户）${NC}"
    echo -e "   安装路径: $INSTALL_DIR"
    echo -e "   命令路径: $BIN_DIR/novel"
    echo ""
    
    # 检查 sudo 权限
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}需要 sudo 权限进行全局安装${NC}"
        exec sudo "$0" --global
        exit $?
    fi
    
    # 创建目录
    mkdir -p "$INSTALL_DIR"
    
    # 复制框架文件
    echo -e "${BLUE}复制框架文件...${NC}"
    cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/"
    
    # 创建启动脚本
    cat > "$BIN_DIR/novel" << EOF
#!/bin/bash
$PYTHON_CMD "$INSTALL_DIR/src/cli/main.py" "\$@"
EOF
    chmod +x "$BIN_DIR/novel"
    
    echo -e "${GREEN}✓ 全局安装完成${NC}"
}

# 便携安装（指定目录）
install_portable() {
    INSTALL_DIR="$1"
    
    if [ -z "$INSTALL_DIR" ]; then
        echo -e "${RED}❌ 请指定安装路径${NC}"
        echo "用法: $0 --portable /path/to/install"
        exit 1
    fi
    
    # 转换为绝对路径
    INSTALL_DIR="$(cd "$(dirname "$INSTALL_DIR")" 2>/dev/null && pwd)/$(basename "$INSTALL_DIR")" 2>/dev/null || INSTALL_DIR="$INSTALL_DIR"
    
    echo -e "${BLUE}安装模式: 便携安装${NC}"
    echo -e "   安装路径: $INSTALL_DIR"
    echo ""
    
    # 创建目录
    mkdir -p "$INSTALL_DIR"
    
    # 复制框架文件
    echo -e "${BLUE}复制框架文件...${NC}"
    cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/"
    
    # 创建启动脚本
    cat > "$INSTALL_DIR/novel" << EOF
#!/bin/bash
$PYTHON_CMD "$INSTALL_DIR/src/cli/main.py" "\$@"
EOF
    chmod +x "$INSTALL_DIR/novel"
    
    echo ""
    echo -e "${GREEN}✓ 便携安装完成${NC}"
    echo ""
    echo "使用方法:"
    echo "    $INSTALL_DIR/novel init --name \"你的小说\""
    echo ""
    echo "或添加到 PATH:"
    echo "    export PATH=\"$INSTALL_DIR:\$PATH\""
    echo "    novel init --name \"你的小说\""
}

# 卸载
uninstall() {
    echo -e "${BLUE}卸载框架...${NC}"
    
    # 检查本地安装
    if [ -d "$HOME/.local/lib/novel-framework" ]; then
        rm -rf "$HOME/.local/lib/novel-framework"
        rm -f "$HOME/.local/bin/novel"
        echo -e "${GREEN}✓ 已卸载本地安装${NC}"
    fi
    
    # 检查全局安装
    if [ -d "/usr/local/lib/novel-framework" ]; then
        if [ "$EUID" -ne 0 ]; then
            exec sudo "$0" --uninstall
        fi
        rm -rf "/usr/local/lib/novel-framework"
        rm -f "/usr/local/bin/novel"
        echo -e "${GREEN}✓ 已卸载全局安装${NC}"
    fi
    
    echo -e "${GREEN}✓ 卸载完成${NC}"
}

# 显示帮助
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --local      本地安装（仅当前用户，默认）"
    echo "  --global     全局安装（所有用户，需要 sudo）"
    echo "  --portable   便携安装（指定目录）"
    echo "  --uninstall  卸载框架"
    echo "  --help       显示帮助"
    echo ""
    echo "示例:"
    echo "  $0                      # 本地安装"
    echo "  $0 --local              # 本地安装"
    echo "  $0 --global             # 全局安装（需要 sudo）"
    echo "  $0 --portable ~/tools   # 安装到 ~/tools"
    echo "  $0 --uninstall          # 卸载"
    echo ""
    echo "安装后使用:"
    echo "  novel init --name \"我的小说\""
}

# 主程序
main() {
    case "${1:-}" in
        --global)
            check_python
            check_dependencies
            install_global
            ;;
        --portable)
            check_python
            check_dependencies
            install_portable "$2"
            ;;
        --uninstall)
            uninstall
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        --local|"")
            check_python
            check_dependencies
            install_local
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            show_help
            exit 1
            ;;
    esac
    
    # 安装成功后的提示
    if [ "${1:-}" != "--uninstall" ] && [ "${1:-}" != "--help" ] && [ "${1:-}" != "-h" ]; then
        echo ""
        echo "=================================================="
        echo -e "${GREEN}✅ 安装成功！${NC}"
        echo "=================================================="
        echo ""
        echo "快速开始:"
        echo "    novel init --name \"我的小说\""
        echo ""
        echo "查看帮助:"
        echo "    novel --help"
        echo ""
        echo "=================================================="
    fi
}

main "$@"
