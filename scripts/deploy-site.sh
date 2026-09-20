#!/usr/bin/env bash
# deepthink 宣传页部署脚本 —— 锁定目标项目,防误覆盖
#
# 用法: ./scripts/deploy-site.sh [--dry-run]
#
# 设计:把 `wrangler pages deploy` 的所有可变参数 hardcode 死,只暴露一个开关。
# 防止任何未来修改(包括我自己)误覆盖其他 Pages 项目。
#
# 历史事故:曾用 --project-name=wxhou 误覆盖用户 wxhou.pages.dev。
# 这里的 --project-name=deepthink 是唯一允许的目标。

set -euo pipefail

PROJECT_NAME="deepthink"   # ⚠️ 不要改 —— URL 是 deepthink.wxhou.workers.dev
SOURCE_DIR="site"          # 静态资源目录

# 校验:阻断 wxhou —— 这是 CLAUDE.md 中唯一永久禁止的项目名(出过覆盖事故)
# 其他现有项目(如 openspec-playwright / wechat-markdown 等)不在此拦截,
# 因为它们可能用于其它 deploy 用途;如需 deploy 到那些项目,用户须明确指示。
BLOCKED_NAMES=("wxhou")
for blocked in "${BLOCKED_NAMES[@]}"; do
  if [ "$PROJECT_NAME" = "$blocked" ]; then
    echo "❌ REFUSED: project name '$PROJECT_NAME' is permanently blocked (see CLAUDE.md)" >&2
    echo "   Edit PROJECT_NAME in this script only after user explicitly approves." >&2
    exit 1
  fi
done

# 校验:源目录必须存在
if [ ! -d "$SOURCE_DIR" ]; then
  echo "❌ Source directory not found: $SOURCE_DIR/" >&2
  exit 1
fi

echo "▶ Deploying $SOURCE_DIR/ → Cloudflare Pages project '$PROJECT_NAME'"
echo "  Target URL: https://${PROJECT_NAME}.wxhou.workers.dev"
echo ""

if [ "${1:-}" = "--dry-run" ]; then
  echo "✅ Dry run: would run:"
  echo "   npx --yes wrangler@latest pages deploy $SOURCE_DIR/ --project-name=$PROJECT_NAME --commit-dirty=true"
  exit 0
fi

# 主命令
exec npx --yes wrangler@latest pages deploy "$SOURCE_DIR/" \
  --project-name="$PROJECT_NAME" \
  --commit-dirty=true