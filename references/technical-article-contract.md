# Technical article contract

## Atomicity

- One page explains one primary API unit: module API, class, method, option, or lifecycle event.
- The title begins with the API name or makes it unmistakable.
- Split orchestration patterns into the API pages they use; retain an overview only as a short link hub.

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

Write `常用参数与返回` as a Markdown table with these columns:

| API | 参数 / 返回 | 说明 |
| --- | --- | --- |
| `module.method()` | `option: Type` | Verified purpose, default, or constraint. |

Keep each row to one API call, option, event, or return contract. Do not place scenarios or inferred architecture guidance in this table.

Use `关联 API` only for related atomic pages. Clearly label architecture advice as an inference rather than an API guarantee.
