---
name: personal-knowledge-skill
description: Build and maintain a private local Markdown knowledge base from the current LLM conversation. Use when the user enters “/pks”, says “录入知识库”, “保存到 Wiki”, “沉淀当前会话”, “总结并归档”, asks to classify reusable knowledge under 技术/管理/产品/运营 or their subcategories, wants to browse/search the local Wiki, or wants to start/build the bundled docs site.
---

# Personal Knowledge Skill

Turn useful content in the current conversation into durable, self-contained Wiki articles. Store articles in the bundled Astro Starlight site so they are immediately browsable.

## Paths

Resolve all paths relative to this `SKILL.md`:

- Writer: `scripts/kb.py`
- Taxonomy rules: `references/taxonomy.md`
- Article contract: `references/article-format.md`
- Session cache: `resources/sessions/` (local-only; never commit or publish)
- Wiki root: `wiki`
- Site root: `docs-site`

Write all distilled knowledge under `wiki/`. `docs-site/src/content/docs/wiki` is a symbolic link to that directory; never write articles through the site path.

## Interpret commands

Treat these as equivalent recording commands:

- `/pks`
- `/pks 录入当前会话`
- `$personal-knowledge-skill 录入`
- `$personal-knowledge-skill 录入当前会话`
- `把上面的内容保存到个人知识库`
- `总结并归档到 Wiki`

Treat `/pks` as the short natural-language trigger when it reaches the agent. The Codex skill specification does not define an alias field; use `$personal-knowledge-skill` or `/skills` for guaranteed native skill selection.

Treat “查看知识库” as a request to list articles or start the documentation site, based on context.

## Acquire the current conversation as source data

When recording, use the **entire active conversation** as the source, not only the latest user message. The current Agent must obtain the conversation through its host-native conversation/context API first, then hand the resulting transcript back to itself as the source material for this Skill.

1. Identify the current host Agent (`codex`, `cursor`, or another supported host).
2. Ask the host to export or read the active conversation's user and assistant messages, including earlier turns in this same conversation. Do not collect hidden system prompts, tool secrets, other chats, or application-wide history.
3. Normalize and cache a host export with the bundled adapter. Configure a trusted host-native exporter through `PKS_CONVERSATION_EXPORT_CMD`, `PKS_CODEX_CONVERSATION_EXPORT_CMD`, or `PKS_CURSOR_CONVERSATION_EXPORT_CMD`; alternatively pass the host-provided export file explicitly. Use the current host's thread/session ID as `--session-id` when available:

   ```bash
   python3 scripts/conversation_source.py --agent codex \
     --cache-dir resources/sessions --session-id "<current-thread-id>"
   # or
   python3 scripts/conversation_source.py --agent cursor \
     --input /tmp/cursor-current-session.json \
     --cache-dir resources/sessions --session-id "<current-thread-id>"
   ```

4. Read the cached source completely and treat it as the sole conversation evidence for this archival run. The current Agent performs the analysis and writes the Wiki; the script only acquires and normalizes source data.
5. Keep the cache local for traceability. Never commit, publish, render in the docs site, or use it as a Wiki article. Cache only the current conversation's visible user and assistant messages; exclude system prompts, tool calls/output, other chats, and credentials. If the host cannot export the entire active conversation, ask the user to export it rather than creating a partial cache.

The adapter must not scrape Codex/Cursor local databases, browser storage, or filesystem histories. If the current host exposes no conversation-export capability, use the conversation context already supplied to the Agent; if that is incomplete, ask the user to export or paste the current chat rather than silently archiving a partial conversation.

## Record the current conversation

1. Read the acquired full current-conversation source and select only durable, reusable knowledge. Exclude greetings, negotiation about the task, transient tool output, credentials, tokens, personal secrets, and unsupported claims.
2. If the conversation contains several independently useful topics, create one article per topic. Do not force unrelated topics into one article. For `技术` content, split a broad design into atomic API knowledge pages as described below. For every technology third-level framework/runtime directory involved in the conversation (for example `技术/前端/Electron` or `技术/后端/Node.js`), also create or refresh `三方库/index.md` from the latest local session cache. It is an ecosystem-library page, not an API page. When a listed library has reusable API knowledge, place its articles beneath that framework's `三方库/<库名>/` subtree rather than creating a parallel top-level framework category.
3. Read `references/taxonomy.md` and inspect existing directories below `wiki/`. Choose exactly one primary path with 2–6 levels. The first level must be one of `技术`, `管理`, `产品`, `运营`, or `其他`. If no existing second-level category accurately fits the knowledge, create a concise, reusable second-level directory under the correct first-level category and add its recommended path to `references/taxonomy.md`. Do not force a poor fit or create a synonym of an existing category.
4. Search existing articles before writing:

   ```bash
   python3 scripts/kb.py list
   rg -n -i "<key terms>" wiki
   ```

5. Read `references/article-format.md`. Draft a self-contained Markdown body in a temporary file. Improve or merge an existing article when the new knowledge materially overlaps; create a new article otherwise.
6. For a new article, write it with:

   ```bash
   python3 scripts/kb.py add \
     --title "<clear title>" \
     --category "<一级/二级/三级>" \
     --summary "<one-sentence summary>" \
     --tags "<tag1,tag2>" \
     --source-file "<temporary Markdown body>"
   ```

   Pass `--slug` only when a stable English slug is valuable. The command refuses to overwrite an existing file.
   It also refreshes `wiki/index.md` and the LLM-readable `wiki/llms.txt` inventory.
7. For a merge, edit only the matching Wiki article. Preserve useful existing content and frontmatter, update `updated`, and integrate rather than append duplicate sections.
8. Run `python3 scripts/kb.py check`. Report the saved or updated article paths and their classification.

## Wiki index and sidebar consistency

Treat `wiki/index.md` as the sole source of truth for the documentation site's left Wiki menu. Do not manually add, remove, or reorder Wiki entries in the site configuration. Generate its article links only with `scripts/kb.py index`, which follows Astro's directory-route normalization; do not derive URLs by hand. Render every generated category group and the outer `Wiki` group collapsed by default; Starlight may expand the path to the current article for orientation.

After every Wiki addition, merge, deletion, or category move:

1. Run `python3 scripts/kb.py index`, then `python3 scripts/kb.py index --check`.
2. Confirm the article appears under the intended category in `wiki/index.md`.
3. Keep the local docs server running. It recursively watches `wiki/` and automatically restarts after an article, index, or category is added, updated, moved, or deleted; refresh the browser after the restart. The restart reloads both article content and the sidebar generated from `wiki/index.md`.
4. Before publishing the online site, run the documentation build only after the index check passes. The published sidebar is generated from that same index snapshot.

When a `三方库` overview also has nested library API articles, render one `三方库` sidebar group: put its overview page inside as `总览`, put library directories (such as `Effect`) beside it, and never render duplicate sibling items with the same `三方库` label. Keep that group as the final item under its parent framework.

The local cache preserves the visible source conversation for traceability; the default Wiki output remains a distilled article, not a transcript.

## Technical article standard: atomic API knowledge

For every article whose first-level category is `技术`, read `references/technical-article-contract.md` before drafting.

Technical knowledge uses a fixed **framework/module/API article** layout. The final category level is the module; each API has its own direct child directory and an `index.md` article, for example `技术/后端/Node.js/文件系统/fspromises.open/index.md` (the directory uses a lowercase-safe API slug, while `api` keeps the official spelling). This API directory is one clickable item in the documentation sidebar. Do not place technical pages directly under a module or combine multiple APIs in one page.

Each technology third-level framework/runtime directory also has one reserved `三方库/index.md` ecosystem-library page. Its frontmatter uses `kind: "ecosystem-libraries"`, its title is exactly `三方库`, and its category has three levels, for example `技术/前端/Electron`; it is the only non-API exception to the module/API layout and must be the final item in that framework's sidebar menu. "三方库" means external packages associated with, or commonly used alongside, the parent framework (for example `electron-window-state` or `effect` for Electron). Do not list the parent framework/runtime package itself (such as `electron` or `node:*`) as a three-party library. When an associated library has API pages, store them under `技术/<领域>/<框架>/三方库/<库名>/<模块>/<api-slug>/index.md`, with a category that ends at `<模块>`; Effect therefore belongs at `技术/前端/Electron/三方库/Effect/...`, not as a parallel `技术/前端/Effect` category. Derive the list from the latest `resources/sessions/` cache: state every evidenced package's name, why it is used with the framework, and how to install/import or minimally use it. Render every actual package name as a Markdown link to its canonical GitHub repository. If no associated package is evidenced, keep the `三方库列表` table empty (header and separator only); do not add a placeholder row or invent a dependency.

Classify a technology before choosing its path: a framework or host runtime owns application startup, lifecycle, or primary structure (for example Electron); a library or runtime primitive is imported into that host to provide a focused capability without owning the application (for example Effect). If the conversation ties a library to a host framework, nest it beneath that host's `三方库` directory. Create an independent library category only when the source establishes genuinely host-neutral, cross-framework knowledge and the user requests that independent classification.

1. Define one primary unit: a framework/module API, class, method, option, or lifecycle event. Use the API name in the title and record its official spelling in frontmatter `api`. Do not combine unrelated APIs into a solution overview.
2. Reconstruct the user-relevant technical point from the current conversation, then identify the primary API behind it. Split into separate pages when the conversation depends on several APIs.
3. Search the latest official documentation before writing. Prefer the framework or runtime's first-party docs; record the direct URL and the verification date. Never infer parameter defaults, return values, lifecycle guarantees, or security behavior from memory.
4. Identify whether the API requires a third-party library or runtime package. When it does, add a `依赖库` section immediately after `API 定位`, with the library name, why this API needs it, and an install/import or minimal-use example. Do not list a third-party dependency for standard-library or runtime-built-in APIs that need none.
5. Explain only the common parameters, return values, lifecycle/events, and failure or security boundaries relevant to the API. Render `常用参数与返回` as a Markdown table with API、参数、返回、说明 columns. Put inputs and outputs in separate columns; use `—` for a field that does not apply. Mark implementation guidance as an inference when it goes beyond the official contract.
6. Include two scenario sections: `会话提炼场景` (grounded in the current conversation) and `常见应用场景` (established industry use). Keep them clearly separate from the API contract. `会话提炼场景` must include one focused Markdown code block that demonstrates the discussed API in context. Use executable or directly adaptable code, keep it to the smallest useful flow, and include error handling or resource cleanup when the API needs it. Clearly label application-layer policy or inference in surrounding prose; never present it as an API guarantee.
7. Put links to companion API pages under `关联 API`; use a separate overview page only when it links to atomic pages rather than duplicating their API details.

When adding a technical page, supply `--api` so the writer creates the required API directory automatically:

```bash
python3 scripts/kb.py add \
  --title "fsPromises.open()：创建受控文件句柄" \
  --category "技术/后端/Node.js/文件系统" \
  --api "fsPromises.open" \
  --summary "..." --tags "Node.js,文件系统" --source-file /tmp/article.md
```

Create the associated ecosystem-library list for a technology third-level directory with:

```bash
python3 scripts/kb.py add \
  --title "三方库" \
  --category "技术/前端/Electron" \
  --summary "..." --tags "Electron,三方库" \
  --ecosystem-libraries --source-file /tmp/dependencies.md
```

Run `python3 scripts/kb.py check` and `python3 scripts/kb.py index --check` after recording. If the current conversation lacks a trustworthy official source, ask the user or leave the article unsaved rather than inventing an API contract.

## List and view knowledge

Use the script for a compact inventory:

```bash
python3 scripts/kb.py list
python3 scripts/kb.py list --category "技术/前端"
python3 scripts/kb.py index --check
```

Use `rg` for full-text lookup:

```bash
rg -n -i "<query>" wiki
```

For a visual site, run:

```bash
cd docs-site
npm install
npm run build
npm run preview -- --host 127.0.0.1
```

The preview server renders the current `wiki/` source through the site link. Return the local URL printed by Astro. Do not leave a server running unless the user asked to keep it running.

## Validate the site

After changing site configuration, dependencies, components, or styles, run:

```bash
cd docs-site
npm install
npm run build
```

Article-only changes require `kb.py check`; run the full site build when risk or user intent warrants it.
