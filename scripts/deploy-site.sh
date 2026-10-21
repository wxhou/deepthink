#!/usr/bin/env bash
# deepthink 宣传页部署脚本 —— 锁定目标,防误覆盖
#
# 用法: ./scripts/deploy-site.sh [--dry-run]
#
# 部署形态:Cloudflare Workers 静态资源(assets),由仓库根 wrangler.toml 的
# [assets] 指向 site/。不是 Cloudflare Pages。
#
# 历史事故:曾用 --project-name=wxhou 误覆盖用户 wxhou.pages.dev。
# wxhou 永久禁止作为部署目标。

set -euo pipefail

cd "$(dirname "$0")/.."   # 保证能读到仓库根的 wrangler.toml

TARGET_NAME="deepthink"    # ⚠️ 不要改 —— URL 是 deepthink.wxhou.workers.dev
SOURCE_DIR="site"          # 静态资源目录(wrangler.toml 的 [assets] 也指向这里)
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

echo "▶ Deploying $SOURCE_DIR/ → Workers script '$TARGET_NAME'"
echo "  Target URL: https://${TARGET_NAME}.wxhou.workers.dev"
echo ""

if [ "${1:-}" = "--dry-run" ]; then
  echo "✅ Dry run: would run:"
  echo "   npx --yes wrangler@${WRANGLER_VERSION} deploy"
  exit 0
fi

# 主命令:读 wrangler.toml 的 name 与 [assets],不需要也不接受 --project-name
exec npx --yes wrangler@${WRANGLER_VERSION} deploy
