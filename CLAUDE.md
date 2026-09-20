# deepthink 项目级指令(Claude Code 自动加载)

## 关键规则:Cloudflare 部署保护

**永久禁止**部署到以下项目(出过一次事故,绝不再犯):

- `wxhou` —— 用户主账户的个人 Pages 项目,已恢复,**任何情况下不得用此名 deploy**

### 部署地址

deepthink 宣传页部署目标:

- 项目名:`deepthink`(URL: `https://deepthink.wxhou.workers.dev`)
- 命令: `./scripts/deploy-site.sh`(已 hardcode `--project-name=deepthink`,内置 wxhou 黑名单阻断)

## 通用部署守则

部署到任何命名空间(Cloudflare Pages、npm、Vercel、Docker Hub 等)前:

1. `pages project list`(或对应 list 命令) → 若目标名**已存在**,**停下来问用户**:复用还是新建?
2. 用户若说复用某个已存在项目,**二次确认**"会覆盖现有部署,确认吗?"
3. **禁止**:看到任何已存在项目名就默认复用 —— 这是 wxhou 事故的根源
4. deploy 命令始终显式带 `--project-name`/`--name`,不依赖默认

## 仓库结构

- `core/` —— 权威协议源(平台无关)
- `references/` —— Claude Code 向后兼容
- `site/` —— 宣传页(单文件 index.html)
- `scripts/run_evals.py` —— 评测
- `evals/evals.json` —— 12 条 evals + trigger 配置

发布:`npx skills add wxhou/deepthink`(发布到 skills.sh)