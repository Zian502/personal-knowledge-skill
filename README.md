# Personal Knowledge Skill (PKS)

[中文](README.zh-CN.md) | English

Turn reusable knowledge from the active LLM conversation into a local Markdown Wiki, then browse and search it with an Astro + Starlight documentation site.

Documentation: <https://zian502.github.io/personal-knowledge-skill/>

## Highlights

- Uses the complete active conversation between the user and the agent as source material.
- Classifies knowledge under `技术`, `管理`, `产品`, `运营`, `测试`, and `其他`, including paths such as `技术/架构`.
- Stores technical knowledge as atomic API articles: module directory → API directory → `index.md`.
- Requires official documentation, parameter/return tables, practical scenarios, and boundaries for technical articles.
- Generates `wiki/index.md` and `wiki/llms.txt`; the documentation sidebar is generated exclusively from `wiki/index.md`.
- Validates metadata, taxonomy paths, and technical API directory conventions.

## Repository layout

```text
personal-knowledge-skill/
├── SKILL.md                         # Agent workflow and constraints
├── wiki/                             # The only source of Wiki Markdown
├── scripts/kb.py                     # Add, index, validate, and list articles
├── scripts/conversation_source.py    # Active-conversation export adapter
├── references/                       # Taxonomy and article contracts
└── docs-site/                        # Astro/Starlight documentation site
```

`docs-site/src/content/docs/wiki` is a symbolic link to the root `wiki/` directory. Maintain articles only in `wiki/`.

## Use the skill

In an agent that supports skills, enter:

```text
/pks archive the current conversation
```

Or use the canonical skill name:

```text
$personal-knowledge-skill archive the current conversation
```

`/pks` is the project’s shorthand intent; native skill selection depends on the host agent.

### Conversation source

The skill works from the full active conversation, not only the latest message. When the host agent offers a native export capability, configure a trusted exporter:

```bash
export PKS_CODEX_CONVERSATION_EXPORT_CMD='<codex active-conversation export command>'
python3 scripts/conversation_source.py --agent codex --output /tmp/pks-current-session.md
```

For Cursor, use `PKS_CURSOR_CONVERSATION_EXPORT_CMD`, or pass an existing export file:

```bash
python3 scripts/conversation_source.py --agent cursor \
  --input /tmp/cursor-current-session.json \
  --output /tmp/pks-current-session.md
```

The adapter only uses an explicitly configured native exporter or an explicit input file. It never scrapes chat databases, browser storage, or other conversation histories. Delete raw temporary exports after the archival run and never commit them.

## Technical article layout

The final technical category level is the module. Each API has one directory and one article:

```text
wiki/技术/后端/Node.js/文件系统/
└── fspromises.open/
    └── index.md
```

Adding a technical article requires the official API name:

```bash
python3 scripts/kb.py add \
  --title "fsPromises.open(): create a controlled file handle" \
  --category "技术/后端/Node.js/文件系统" \
  --api "fsPromises.open" \
  --summary "Creates a controlled FileHandle for authorized file reads." \
  --tags "Node.js,file system" \
  --source-file /tmp/article.md
```

The directory name is a stable lowercase API slug. The `api` frontmatter field preserves the official spelling for validation and navigation.

## Manage and validate the Wiki

```bash
# List archived articles
python3 scripts/kb.py list

# Generate and verify indexes
python3 scripts/kb.py index
python3 scripts/kb.py index --check

# Validate metadata, categories, and technical API paths
python3 scripts/kb.py check
```

After adding, merging, moving, or deleting an article, update and verify the index. `wiki/index.md` is the sole source of truth for the Wiki sidebar; do not maintain article menus in site configuration.

## Run the documentation site locally

```bash
cd docs-site
npm install
npm run dev -- --host 127.0.0.1
```

Open <http://127.0.0.1:4321>. The development server watches `wiki/index.md` and restarts when the index changes; refresh the browser to see the updated sidebar.

Before publishing:

```bash
npm run build
```

GitHub Actions builds and deploys GitHub Pages after a push to `main`. For the first deployment, set **Settings → Pages → Source** to **GitHub Actions**.

## Global installation

Use symbolic links to expose this repository globally to Codex and Cursor. Changes apply immediately when the links point to this repository:

```text
~/.codex/skills/personal-knowledge-skill
~/.cursor/skills/personal-knowledge-skill
```
