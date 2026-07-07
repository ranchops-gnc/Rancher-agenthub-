#!/bin/bash
# AgentHub 一键安装脚本
# 用法:
#   curl -fsSL https://raw.githubusercontent.com/xuanyuanluoxue/AgentHub/main/misc/install.sh | bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "  ${BLUE}>${NC} $1"; }
log_ok() { echo -e "  ${GREEN}✓${NC} $1"; }
log_warn() { echo -e "  ${YELLOW}!${NC} $1"; }
log_err() { echo -e "  ${RED}✗${NC} $1"; }

print_banner() {
    echo ""
    echo -e "  ${CYAN}    _                    _   _   _       _     ${NC}"
    echo -e "  ${CYAN}   / \   __ _  ___ _ __ | |_| | | |_   _| |__  ${NC}"
    echo -e "  ${CYAN}  / _ \ / _\` |/ _ \ '_ \| __| |_| | | | | '_ \ ${NC}"
    echo -e "  ${CYAN} / ___ \ (_| |  __/ | | | |_|  _  | |_| | |_) |${NC}"
    echo -e "  ${CYAN}/_/   \_\__, |\___|_| |_|\__|_| |_|\__,_|_.__/ ${NC}"
    echo -e "  ${CYAN}        |___/                               ${NC}"
    echo ""
    echo -e "  ${CYAN}统一 AI 工具四大共享生态${NC}"
    echo -e "  ${CYAN}Skill · Agent · 画像 · 记忆${NC}"
    echo ""
}

detect_os() {
    case "$(uname -s)" in
        Linux*)
            if grep -qiE "(microsoft|wsl)" /proc/version 2>/dev/null; then
                echo "wsl"
            else
                echo "linux"
            fi
            ;;
        Darwin*)
            echo "macos"
            ;;
        CYGWIN*|MINGW*|MSYS*)
            echo "windows"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

is_installed() {
    [ -d "${HOME}/.agenthub" ] && [ -f "${HOME}/.agenthub/pyproject.toml" ]
}

show_menu() {
    echo "  请选择操作:"
    echo ""
    echo -e "    ${GREEN}[1]${NC} 安装 AgentHub"
    echo -e "    ${GREEN}[2]${NC} 更新 AgentHub"
    echo -e "    ${GREEN}[3]${NC} 重新安装"
    echo -e "    ${YELLOW}[4]${NC} 卸载 AgentHub"
    echo -e "    ${CYAN}[5]${NC} 打开配置目录"
    echo -e "    ${DIM}[6]${NC} 退出"
    echo ""
}

print_usage() {
    echo ""
    echo -e "  ${CYAN}AgentHub 安装脚本${NC}"
    echo ""
    echo "  用法:"
    echo "    curl -fsSL https://.../install.sh | bash"
    echo ""
    echo "  选项:"
    echo "    1 - 安装"
    echo "    2 - 更新"
    echo "    3 - 重新安装"
    echo "    4 - 卸载"
    echo "    5 - 打开配置目录"
    echo "    6 - 退出"
    echo ""
    echo -e "  ${YELLOW}提示: 管道模式下无法交互，请用以下方式:${NC}"
    echo "    curl -fsSL https://.../install.sh -o /tmp/install.sh && bash /tmp/install.sh"
    echo ""
}

do_install() {
    log_info "开始安装 AgentHub..."
    echo ""

    if [ ! -d "${HOME}/.agenthub" ]; then
        log_info "正在克隆 AgentHub 仓库..."
        git clone https://github.com/xuanyuanluoxue/AgentHub.git "${HOME}/.agenthub"
        echo ""
    fi

    case "$os_type" in
        linux|wsl)
            if command -v pip &> /dev/null; then
                cd "${HOME}/.agenthub" && pip install -e . --user
                log_ok "Python 包安装成功"
            else
                log_err "未找到 pip，请先安装 Python"
                exit 1
            fi
            ;;
        macos)
            if command -v pip3 &> /dev/null; then
                cd "${HOME}/.agenthub" && pip3 install -e . --user
                log_ok "Python 包安装成功"
            else
                log_err "未找到 pip3，请先安装 Python"
                exit 1
            fi
            ;;
        windows)
            if command -v pip &> /dev/null; then
                cd "${USERPROFILE}\.agenthub" && pip install -e . --user
                log_ok "Python 包安装成功"
            else
                log_err "未找到 pip，请先安装 Python"
                exit 1
            fi
            ;;
    esac

    log_ok "安装完成！"
    echo ""
    log_info "运行 ${CYAN}agenthub --help${NC} 查看帮助"
}

do_uninstall() {
    log_info "开始卸载 AgentHub..."
    echo ""

    if [ -d "${HOME}/.agenthub" ]; then
        log_warn "配置目录: ${HOME}/.agenthub"
        echo ""
        echo -n "  是否删除配置目录? [y/N]: "
        read -r REPLY
        echo ""

        if [[ "$REPLY" =~ ^[Yy]$ ]]; then
            rm -rf "${HOME}/.agenthub"
            log_ok "配置目录已删除"
        else
            log_info "保留配置目录"
        fi
    fi

    case "$os_type" in
        linux|wsl|macos)
            pip uninstall -y agenthub 2>/dev/null || true
            ;;
        windows)
            pip uninstall -y agenthub 2>/dev/null || true
            ;;
    esac

    log_ok "卸载完成"
}

do_update() {
    if ! is_installed; then
        log_err "AgentHub 未安装，无法更新"
        exit 1
    fi

    log_info "正在更新 AgentHub..."
    echo ""

    cd "${HOME}/.agenthub" && git pull 2>/dev/null || {
        log_err "Git 更新失败，请手动更新"
        exit 1
    }

    pip install -e . --quiet 2>/dev/null || pip install -e . --user --quiet

    log_ok "更新完成"
}

do_reinstall() {
    log_warn "强制重新安装"
    echo ""
    do_uninstall
    do_install
}

do_open() {
    if [ -d "${HOME}/.agenthub" ]; then
        log_info "正在打开配置目录..."
        case "$os_type" in
            linux|wsl)
                xdg-open "${HOME}/.agenthub" 2>/dev/null || echo "请手动打开: ${HOME}/.agenthub"
                ;;
            macos)
                open "${HOME}/.agenthub" 2>/dev/null || echo "请手动打开: ${HOME}/.agenthub"
                ;;
            windows)
                explorer.exe "${USERPROFILE}\.agenthub"
                ;;
        esac
    else
        log_err "AgentHub 未安装"
        exit 1
    fi
}

main() {
    local choice=""
    os_type=$(detect_os)

    print_banner
    log_info "检测到操作系统: ${CYAN}${os_type}${NC}"
    echo ""

    if [ -t 0 ]; then
        show_menu
        echo -n "  请输入选项 [1-6]: "
        read -r choice
        echo ""
    else
        print_usage
        exit 1
    fi

    case "$choice" in
        1) do_install ;;
        2) do_update ;;
        3) do_reinstall ;;
        4) do_uninstall ;;
        5) do_open ;;
        6|*) log_info "退出"; exit 0 ;;
    esac
}

main "$@"