---
name: personal-knowledge-skill
description: Build and maintain a private local Markdown knowledge base from the current LLM conversation. Use when the user enters “/pks”, says “录入知识库”, “保存到 Wiki”, “沉淀当前会话”, “总结并归档”, asks to classify reusable knowledge under 技术/管理/产品/运营/测试 or their subcategories, wants to browse/search the local Wiki, or wants to start/build the bundled docs site.
---

# Personal Knowledge Skill

Turn useful content in the current conversation into durable, self-contained Wiki articles. Store articles in the bundled Astro Starlight site so they are immediately browsable.

## Paths

Resolve all paths relative to this `SKILL.md`:

- Writer: `scripts/kb.py`
- Taxonomy rules: `references/taxonomy.md`
- Article contract: `references/article-format.md`
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

## Record the current conversation

1. Read the current conversation and select only durable, reusable knowledge. Exclude greetings, negotiation about the task, transient tool output, credentials, tokens, personal secrets, and unsupported claims.
2. If the conversation contains several independently useful topics, create one article per topic. Do not force unrelated topics into one article. For `技术` content, split a broad design into atomic API knowledge pages as described below.
3. Read `references/taxonomy.md`. Choose exactly one primary path with 2–4 levels. The first level must be one of `技术`, `管理`, `产品`, `运营`, `测试`, or `其他`.
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

Do not claim that raw conversation text was preserved. The default output is a distilled Wiki article, not a transcript.

## Technical article standard: atomic API knowledge

For every article whose first-level category is `技术`, read `references/technical-article-contract.md` before drafting.

1. Define one primary unit: a framework/module API, class, method, option, or lifecycle event. Use the API name in the title. Do not combine unrelated APIs into a solution overview.
2. Reconstruct the user-relevant technical point from the current conversation, then identify the primary API behind it. Split into separate pages when the conversation depends on several APIs.
3. Search the latest official documentation before writing. Prefer the framework or runtime's first-party docs; record the direct URL and the verification date. Never infer parameter defaults, return values, lifecycle guarantees, or security behavior from memory.
4. Explain only the common parameters, return values, lifecycle/events, and failure or security boundaries relevant to the API. Render `常用参数与返回` as a Markdown table with API、参数/返回、说明 columns. Mark implementation guidance as an inference when it goes beyond the official contract.
5. Include two scenario sections: `会话提炼场景` (grounded in the current conversation) and `常见应用场景` (established industry use). Keep them clearly separate from the API contract.
6. Put links to companion API pages under `关联 API`; use a separate overview page only when it links to atomic pages rather than duplicating their API details.

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
