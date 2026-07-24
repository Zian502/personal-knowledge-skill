# Personal Knowledge Skill（PKS）

将 LLM 当前会话中的可复用内容沉淀为结构化 Markdown Wiki，并通过本地文档站点浏览与检索。

## 能力

- 分析、提炼当前会话，生成可独立阅读的知识文档。
- 自动归类到 `技术`、`管理`、`产品`、`运营`、`测试` 等目录；技术类可继续细分为前端、Electron、Node.js、React、Vue 等。
- 在写入前校验文档元数据、目录与文件名，避免重复或不规范的条目。
- 使用 Astro + Starlight 渲染 `wiki/` 中的 Markdown，提供本地知识库站点。

## 项目结构

```text
personal-knowledge-skill/
├── SKILL.md                 # Skill 使用说明与工作流
├── wiki/                    # 知识库 Markdown 源文件
├── scripts/kb.py            # 录入、检查与列表工具
├── references/              # 分类法和文章模板
└── docs-site/               # Astro/Starlight 文档站点
```

`docs-site/src/content/docs/wiki` 是指向仓库根目录 `wiki/` 的软链接，因此 Wiki 只维护一份源文件。

## 使用 Skill

在支持 Codex Skill 的 Agent 中直接调用：

```text
$personal-knowledge-skill 录入当前会话
```

也可以用 `/pks` 作为意图别名，例如：`/pks 总结并归档当前会话`。Skill 会先确认要沉淀的范围，再生成、分类并校验 Markdown。

## 启动本地知识库站点

```bash
cd docs-site
npm install
npm run build
npm run preview -- --host 127.0.0.1
```

然后访问 `http://127.0.0.1:4321`。由于 Wiki 来自仓库根目录的软链接，推荐使用 `build + preview` 来确保本地预览与生产构建一致。

## 管理 Wiki

```bash
# 列出已归档文章
python3 scripts/kb.py list

# 校验全部 Wiki 文档
python3 scripts/kb.py check
```

文章以 YAML frontmatter 记录标题、分类、标签、摘要与创建时间。详细格式见 `references/article-format.md`，分类规则见 `references/taxonomy.md`。

## 全局安装

本项目可通过软链接被 Codex 与 Cursor 全局发现；软链接指向该仓库时，更新源码会立即生效：

```text
~/.codex/skills/personal-knowledge-skill
~/.cursor/skills/personal-knowledge-skill
```

## 开发

```bash
cd docs-site
npm run build
```

构建完成后，站点会将 `wiki/` 中的文章作为文档内容渲染。
