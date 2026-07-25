# Technical article contract

## Atomicity

- One page explains one primary API unit: module API, class, method, option, or lifecycle event.
- The title begins with the API name or makes it unmistakable.
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
- The parent category identifies the module, for example `技术/后端/Node.js/文件系统`.
- Do not put a technical article directly under its module directory or combine two APIs in one article.

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

Write `常用参数与返回` as a Markdown table with these columns:

| API | 参数 | 返回 | 说明 |
| --- | --- | --- | --- |
| `module.method()` | `option: Type` | `Promise<Result>` | Verified purpose, default, or constraint. |

Keep each row to one API call, option, event, or return contract. Put inputs and outputs in their own columns and use `—` when a column does not apply. Do not place scenarios or inferred architecture guidance in this table.

## Conversation scenario code example

Every technical article's `会话提炼场景` must contain a focused Markdown code block.

- Make the example executable or directly adaptable, with the exact primary API visible.
- Show the smallest useful flow from the conversation; avoid unrelated framework setup.
- Include cleanup, rejection handling, or an explicit boundary when the API requires it.
- Keep application authorization, limits, and architecture decisions outside the API contract and label inferences clearly.

Use `关联 API` only for related atomic pages. Clearly label architecture advice as an inference rather than an API guarantee.
