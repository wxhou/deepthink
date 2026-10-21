#!/usr/bin/env bash
# deepthink 宣传页部署脚本 —— 锁定目标,防误覆盖
#
# 用法: ./scripts/deploy-site.sh [--dry-run]
#
# 部署形态:Cloudflare Pages,项目名 deepthink,静态目录 site/。
# 线上 URL: https://deepthink-boa.pages.dev
#
# 历史事故:曾用 --project-name=wxhou 误覆盖用户 wxhou.pages.dev。
# wxhou 永久禁止作为部署目标。

set -euo pipefail

cd "$(dirname "$0")/.."   # 保证能读到仓库根的 wrangler.toml

TARGET_NAME="deepthink"    # ⚠️ 不要改 —— Pages 项目名
SOURCE_DIR="site"          # 静态资源目录
PAGES_URL="https://deepthink-boa.pages.dev"  # 项目实际域名(裸名已被占用)
WRANGLER_VERSION="4.151.3" # 钉死版本:latest 会随上游发版改变部署行为,部署不可复现

# 校验:阻断 wxhou —— 这是 CLAUDE.md 中唯一永久禁止的目标名(出过覆盖事故)
BLOCKED_NAMES=("wxhou")
for blocked in "${BLOCKED_NAMES[@]}"; do
  if [ "$TARGET_NAME" = "$blocked" ]; then
    echo "❌ REFUSED: target '$TARGET_NAME' is permanently blocked (see CLAUDE.md)" >&2
    echo "   Edit TARGET_NAME in this script only after user explicitly approves." >&2
    exit 1
  fi
done

# 校验:源目录必须存在
if [ ! -d "$SOURCE_DIR" ]; then
  echo "❌ Source directory not found: $SOURCE_DIR/" >&2
  exit 1
fi

# 双重校验:wrangler.toml 的 name 必须与锁定目标一致,防止配置层被改而脚本无感
CONFIG_NAME=$(grep -E '^name[[:space:]]*=' wrangler.toml | head -1 | sed -E 's/.*=[[:space:]]*"([^"]+)".*/\1/')
if [ "$CONFIG_NAME" != "$TARGET_NAME" ]; then
  echo "❌ REFUSED: wrangler.toml name='$CONFIG_NAME' does not match locked target '$TARGET_NAME'" >&2
  exit 1
fi

echo "▶ Deploying $SOURCE_DIR/ → Cloudflare Pages project '$TARGET_NAME'"
echo "  Target URL: ${PAGES_URL}"
echo ""

if [ "${1:-}" = "--dry-run" ]; then
  echo "✅ Dry run: would run:"
  echo "   npx --yes wrangler@${WRANGLER_VERSION} pages deploy $SOURCE_DIR/ --project-name=$TARGET_NAME --commit-dirty=true"
  exit 0
fi

# 主命令:显式带 --project-name,不依赖 wrangler.toml 默认值
exec npx --yes wrangler@${WRANGLER_VERSION} pages deploy "$SOURCE_DIR/" \
  --project-name="$TARGET_NAME" \
  --commit-dirty=true
