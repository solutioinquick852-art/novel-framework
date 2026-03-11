#!/bin/bash
# AI网文小说写作框架 - 远程安装脚本
# 使用方法: curl -fsSL https://raw.githubusercontent.com/USER/REPO/main/remote-install.sh | bash

set -e

# 配置
REPO_USER="solutioinquick852-art"
REPO_NAME="novel-framework"
INSTALL_VERSION="latest"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 默认安装路径
INSTALL_DIR="${1:-$HOME/.local/lib/novel-framework}"
BIN_DIR="$HOME/.local/bin"

echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   AI网文小说写作框架 - 远程安装程序            ║${NC}"
echo -e "${CYAN}║   Version: 1.0.0                               ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════╝${NC}"
echo ""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --dir|-d)
            INSTALL_DIR="$2"
            shift 2
            ;;
        --local)
            INSTALL_DIR="$HOME/.local/lib/novel-framework"
            shift
            ;;
        --global)
            INSTALL_DIR="/usr/local/lib/novel-framework"
            BIN_DIR="/usr/local/bin"
            shift
            ;;
        --help|-h)
            echo "用法: curl -fsSL URL | bash -s -- [选项]"
            echo ""
            echo "选项:"
            echo "  --dir, -d PATH    指定安装路径"
            echo "  --local           安装到当前用户 (默认)"
            echo "  --global          安装到所有用户 (需要 sudo)"
            echo "  --help, -h        显示帮助"
            echo ""
            echo "示例:"
            echo "  # 默认安装到 ~/.local/lib/novel-framework"
            echo "  curl -fsSL URL | bash"
            echo ""
            echo "  # 安装到指定目录"
            echo "  curl -fsSL URL | bash -s -- --dir /opt/novel"
            echo ""
            echo "  # 全局安装"
            echo "  curl -fsSL URL | bash -s -- --global"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

# 检查 Python
echo -e "${BLUE}▸ 检查 Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}✗ 未找到 Python，请先安装 Python 3.8+${NC}"
    exit 1
fi
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}  ✓ Python $PYTHON_VERSION${NC}"

# 检查 curl 或 wget
echo -e "${BLUE}▸ 检查下载工具...${NC}"
if command -v curl &> /dev/null; then
    DOWNLOADER="curl"
    echo -e "${GREEN}  ✓ curl 可用${NC}"
elif command -v wget &> /dev/null; then
    DOWNLOADER="wget"
    echo -e "${GREEN}  ✓ wget 可用${NC}"
else
    echo -e "${RED}✗ 需要 curl 或 wget${NC}"
    exit 1
fi

# 下载框架
echo -e "${BLUE}▸ 下载框架...${NC}"
TEMP_DIR=$(mktemp -d)
ARCHIVE_URL="https://github.com/${REPO_USER}/${REPO_NAME}/archive/refs/heads/main.tar.gz"

if [ "$DOWNLOADER" = "curl" ]; then
    curl -fsSL "$ARCHIVE_URL" -o "$TEMP_DIR/framework.tar.gz"
else
    wget -q "$ARCHIVE_URL" -O "$TEMP_DIR/framework.tar.gz"
fi

if [ ! -f "$TEMP_DIR/framework.tar.gz" ]; then
    echo -e "${RED}✗ 下载失败${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi
echo -e "${GREEN}  ✓ 下载完成${NC}"

# 解压
echo -e "${BLUE}▸ 解压文件...${NC}"
tar -xzf "$TEMP_DIR/framework.tar.gz" -C "$TEMP_DIR"
SOURCE_DIR="$TEMP_DIR/${REPO_NAME}-main"

if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}✗ 解压失败${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi
echo -e "${GREEN}  ✓ 解压完成${NC}"

# 全局安装需要 sudo
if [[ "$INSTALL_DIR" == /usr/* ]] || [[ "$INSTALL_DIR" == /opt/* ]]; then
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}▸ 全局安装需要 sudo 权限...${NC}"
        exec sudo "$0" "$@"
    fi
fi

# 安装
echo -e "${BLUE}▸ 安装到 $INSTALL_DIR...${NC}"
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
cp -r "$SOURCE_DIR"/* "$INSTALL_DIR/"
echo -e "${GREEN}  ✓ 文件复制完成${NC}"

# 创建命令
echo -e "${BLUE}▸ 创建 novel 命令...${NC}"
cat > "$BIN_DIR/novel" << EOF
#!/bin/bash
$PYTHON_CMD "$INSTALL_DIR/src/cli/main.py" "\$@"
EOF
chmod +x "$BIN_DIR/novel"
echo -e "${GREEN}  ✓ 命令创建完成${NC}"

# 清理
rm -rf "$TEMP_DIR"

# 检查 PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo -e "${YELLOW}⚠️  $BIN_DIR 不在 PATH 中${NC}"
    echo -e "${YELLOW}请运行以下命令添加到 PATH：${NC}"
    echo ""
    if [ -f "$HOME/.zshrc" ]; then
        echo -e "    ${CYAN}echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc${NC}"
        echo -e "    ${CYAN}source ~/.zshrc${NC}"
    else
        echo -e "    ${CYAN}echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc${NC}"
        echo -e "    ${CYAN}source ~/.bashrc${NC}"
    fi
    echo ""
fi

# 完成
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║            ✅ 安装成功！                       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "安装路径: ${CYAN}$INSTALL_DIR${NC}"
echo -e "命令路径: ${CYAN}$BIN_DIR/novel${NC}"
echo ""
echo -e "${CYAN}快速开始:${NC}"
echo "    novel init --name \"我的小说\""
echo ""
echo -e "${CYAN}查看帮助:${NC}"
echo "    novel --help"
echo ""
