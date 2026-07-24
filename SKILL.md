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
- Wiki root: `docs-site/src/content/docs/wiki`
- Site root: `docs-site`

Never write conversation knowledge outside the Wiki root unless the user explicitly requests another location.

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
2. If the conversation contains several independently useful topics, create one article per topic. Do not force unrelated topics into one article.
3. Read `references/taxonomy.md`. Choose exactly one primary path with 2–4 levels. The first level must be one of `技术`, `管理`, `产品`, `运营`, `测试`, or `其他`.
4. Search existing articles before writing:

   ```bash
   python3 scripts/kb.py list
   rg -n -i "<key terms>" docs-site/src/content/docs/wiki
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
7. For a merge, edit only the matching Wiki article. Preserve useful existing content and frontmatter, update `updated`, and integrate rather than append duplicate sections.
8. Run `python3 scripts/kb.py check`. Report the saved or updated article paths and their classification.

Do not claim that raw conversation text was preserved. The default output is a distilled Wiki article, not a transcript.

## List and view knowledge

Use the script for a compact inventory:

```bash
python3 scripts/kb.py list
python3 scripts/kb.py list --category "技术/前端"
```

Use `rg` for full-text lookup:

```bash
rg -n -i "<query>" docs-site/src/content/docs/wiki
```

For a visual site, run:

```bash
cd docs-site
npm install
npm run dev
```

Return the local URL printed by Astro. Do not leave a development server running unless the user asked to keep it running.

## Validate the site

After changing site configuration, dependencies, components, or styles, run:

```bash
cd docs-site
npm install
npm run build
```

Article-only changes require `kb.py check`; run the full site build when risk or user intent warrants it.
