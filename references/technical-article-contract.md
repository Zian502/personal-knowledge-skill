# Technical article contract

## Atomicity

- One page explains one primary API unit: module API, class, method, option, or lifecycle event.
- The title is only the official API display name. Preserve useful call or
  constructor syntax, such as `fsPromises.open()` or `new BrowserWindow()`, but
  do not append a Chinese/ASCII colon, purpose text, dash subtitle, or any other
  explanatory suffix. Put the purpose in `description` and `API 定位`.
- Split orchestration patterns into the API pages they use; retain an overview only as a short link hub.

## Directory and navigation model

Technical categories end at the framework/module directory. Each atomic API is a
direct child directory of that module and contains exactly one `index.md` article.
The API directory becomes one clickable menu item in the documentation site.

```text
wiki/技术/后端/Node.js/文件系统/
├── fspromises.open/
│   └── index.md       # frontmatter: api: "fsPromises.open"
└── filehandle.read/
    └── index.md       # frontmatter: api: "FileHandle.read"
```

- Use the official API spelling in frontmatter `api`, for example `fsPromises.open`.
- Use the API display form as the full frontmatter `title`, for example
  `fsPromises.open()`. `contextBridge.exposeInMainWorld()：构建受限 Renderer API`
  is invalid; use `contextBridge.exposeInMainWorld()` instead.
- The parent category identifies the module, for example `技术/后端/Node.js/文件系统`.
- Do not put a technical article directly under its module directory or combine two APIs in one article.
- Each framework/runtime third-level directory has one reserved non-API exception: `三方库/index.md`. Its frontmatter sets `kind: "ecosystem-libraries"`, its title is exactly `三方库`, and its `category` is the third-level framework/runtime path. Place it last in that framework's sidebar menu.
- "三方库" means an external package associated with or used alongside the parent framework; never list the parent framework/runtime package itself. Build this page from the latest `resources/sessions/` cache. Its `三方库列表` table must have `库名｜为何使用｜如何使用` columns. Render each actual package name as a Markdown link to its canonical GitHub repository. When no package is evidenced, leave the table body empty; do not add a placeholder row.
- When an associated library has API pages, place them beneath the list directory: `技术/<领域>/<框架>/三方库/<库名>/<模块>/<api-slug>/index.md`. The article category ends at `<模块>` and may contain up to six levels. For example, Effect APIs used to orchestrate Electron belong under `技术/前端/Electron/三方库/Effect/...`, not in a standalone frontend Effect category.
- Classify by role before choosing a path: the host framework/runtime owns startup, lifecycle, or primary application structure; a library/runtime primitive is imported to add a focused capability without owning the application. When source evidence ties the library to a host, nest it under that host's `三方库`; create a standalone library category only for explicitly requested, host-neutral knowledge.

## Evidence order

1. Current first-party API reference.
2. Current first-party guide when it explains lifecycle, security, or recommended usage.
3. The current conversation for the user-specific application context.

Do not use secondary articles as the source of an API contract. State the source URL and the date checked.

## Required body sections

1. `API 定位`
2. `常用参数与返回`
3. `会话提炼场景`
4. `常见应用场景`
5. `边界与注意事项`
6. `官方文档`

Technical frontmatter must include `api` in addition to the standard fields.

Write `常用参数与返回` as a Markdown table with these columns. Do not repeat the API name here: the page title, frontmatter `api`, and `API 定位` already identify the single atomic API.

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `option: Type` | `Promise<Result>` | Verified purpose, default, or constraint. |

Keep each row to one API call, option, event, or return contract. Put inputs and outputs in their own columns and use `—` when a column does not apply. Do not place scenarios or inferred architecture guidance in this table.

## Third-party dependencies

Do not add an `依赖库` section to any API article. Maintain all package names, GitHub links, reasons, installation, and usage guidance only in the parent framework's `三方库` overview.

## Conversation scenario code example

Every technical article's `会话提炼场景` must contain a focused Markdown code block.

- Make the example executable or directly adaptable, with the exact primary API visible.
- Show the smallest useful flow from the conversation; avoid unrelated framework setup.
- Include cleanup, rejection handling, or an explicit boundary when the API requires it.
- Keep application authorization, limits, and architecture decisions outside the API contract and label inferences clearly.

Use `关联 API` only for related atomic pages. Clearly label architecture advice as an inference rather than an API guarantee.
