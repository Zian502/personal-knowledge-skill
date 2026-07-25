# Personal Knowledge Skill（PKS）

[English](README.md) | 中文

将当前 LLM 会话中的可复用内容提炼为本地 Markdown Wiki，并通过 Astro + Starlight 文档站点浏览、检索与长期维护。

在线文档：<https://zian502.github.io/personal-knowledge-skill/>

## 核心能力

- 以当前会话的完整用户与助手消息为知识源，由当前 Agent 分析、总结并形成可独立阅读的 Wiki。
- 按 `技术`、`管理`、`产品`、`运营`、`测试`、`其他` 分类；支持 `技术/架构` 等分类路径。
- 技术知识按原子 API 归档：模块目录 → API 目录 → `index.md`。
- 技术文章包含官方文档依据、常用参数与返回表格、会话场景、通用场景与边界说明。
- 自动生成 `wiki/index.md` 与 `wiki/llms.txt`；文档站点左侧 Wiki 菜单只从 `wiki/index.md` 生成。
- 校验元数据、分类路径及技术 API 目录规范，避免不一致的条目。

## 项目结构

```text
personal-knowledge-skill/
├── SKILL.md                         # Agent 工作流与约束
├── wiki/                             # 唯一的 Wiki Markdown 源
├── scripts/kb.py                     # 新增、索引、检查与列表工具
├── scripts/conversation_source.py    # 当前会话导出适配器
├── references/                       # 分类法与文章契约
└── docs-site/                        # Astro/Starlight 文档站点
```

`docs-site/src/content/docs/wiki` 是指向根目录 `wiki/` 的软链接；不要通过站点目录重复维护文章。

## 使用 Skill

在支持 Skill 的 Agent 中输入：

```text
/pks 录入当前会话
```

或使用原始 Skill 名称：

```text
$personal-knowledge-skill 录入当前会话
```

`/pks` 是约定的快捷意图；原生 Skill 选择以 Agent 支持的方式为准。

### 会话源

Skill 使用当前会话的完整上下文，不只取最后一条消息。若 Agent 提供原生会话导出能力，可配置可信的导出命令：

```bash
export PKS_CODEX_CONVERSATION_EXPORT_CMD='<codex 当前会话导出命令>'
python3 scripts/conversation_source.py --agent codex --output /tmp/pks-current-session.md
```

Cursor 可使用 `PKS_CURSOR_CONVERSATION_EXPORT_CMD`，也可传入已有导出文件：

```bash
python3 scripts/conversation_source.py --agent cursor \
  --input /tmp/cursor-current-session.json \
  --output /tmp/pks-current-session.md
```

适配器只接受明确配置的原生导出器或显式文件；不会扫描聊天数据库、浏览器存储或其他历史会话。临时原始会话文件仅供本次提炼使用，完成后应删除，不能提交到仓库。

## 技术文章目录规范

技术分类的最后一级是模块。一个 API 对应一个目录和一篇文章：

```text
wiki/技术/后端/Node.js/文件系统/
└── fspromises.open/
    └── index.md
```

录入时必须提供 API 原名：

```bash
python3 scripts/kb.py add \
  --title "fsPromises.open()：创建受控文件句柄" \
  --category "技术/后端/Node.js/文件系统" \
  --api "fsPromises.open" \
  --summary "创建受控 FileHandle，作为授权文件读取的起点。" \
  --tags "Node.js,文件系统" \
  --source-file /tmp/article.md
```

目录名使用稳定的小写 API slug；frontmatter 中的 `api` 保留官方 API 拼写，并作为菜单识别依据。

## 管理与校验 Wiki

```bash
# 列出文章
python3 scripts/kb.py list

# 生成并检查索引
python3 scripts/kb.py index
python3 scripts/kb.py index --check

# 校验分类、元数据与技术 API 路径
python3 scripts/kb.py check
```

每次新增、合并、移动或删除文章后，都应先更新并检查索引。`wiki/index.md` 是文档站点左侧 Wiki 菜单的唯一数据源，不能在站点配置中手动维护文章菜单。

## 本地文档站点

```bash
cd docs-site
npm install
npm run dev -- --host 127.0.0.1
```

访问 <http://127.0.0.1:4321>。开发服务会监听 `wiki/index.md`，索引更新后自动重启；刷新浏览器即可看到新的左侧菜单。

发布前执行：

```bash
npm run build
```

推送到 `main` 后，GitHub Actions 会构建并部署 GitHub Pages。首次启用时，请在仓库 **Settings → Pages** 将发布来源设为 **GitHub Actions**。

## 全局安装

本项目可通过软链接供 Codex 与 Cursor 全局发现。软链接指向本仓库时，源码更新会立即生效：

```text
~/.codex/skills/personal-knowledge-skill
~/.cursor/skills/personal-knowledge-skill
```
