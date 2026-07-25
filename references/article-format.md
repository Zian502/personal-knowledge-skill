# Wiki article contract

The writer script creates Starlight-compatible frontmatter. The temporary source file must contain only the article body.

## Body structure

Use this structure when relevant:

```markdown
## 背景与适用场景

Explain the problem and boundaries.

## 核心结论

State the reusable conclusions.

## 实现或操作步骤

Give a reproducible procedure, examples, or code.

## 常见问题与注意事项

Record pitfalls, trade-offs, and exceptions.

## 延伸阅读

Link only sources actually used or mentioned.
```

Adapt headings to the topic. Do not create empty sections.

## Technical article structure

For articles under `技术`, use one primary API and this structure instead of a broad solution narrative:

```markdown
## API 定位

Name the module, API, runtime/process boundary, and the exact responsibility.

## 依赖库

Only when a third-party library or runtime package is required: state its name, why the API needs it, and a minimal install/import or usage example. Omit this section for built-in APIs with no third-party dependency.

## 常用参数与返回

Use a four-column Markdown table: `API｜参数｜返回｜说明`. List only parameters, return values, events, or lifecycle rules verified in current official documentation. Keep parameters and returns separate; use `—` when either is not applicable.

## 会话提炼场景

Apply the API to the user-relevant situation distilled from this conversation.
Include one focused, executable or directly adaptable Markdown code block using the primary API. Keep policy decisions distinct from the API contract.

## 常见应用场景

List established uses that are distinct from the conversation-specific case.

## 边界与注意事项

Separate official constraints from implementation inferences.

## 官方文档

- [API reference](https://example.com): verified YYYY-MM-DD.
```

Use `关联 API` for companion APIs. Split the article if it needs more than one primary API to explain its contract.
Its frontmatter must include the exact primary API as `api`, and its path must be
`技术/<领域>/<框架>/<模块>/<api-slug>/index.md` (within the 2–4 category levels,
the final category is the module).

## Ecosystem-library structure

For a third-level technology framework/runtime, use the non-API path
`技术/<领域>/<框架>/三方库/index.md` with frontmatter `kind: ecosystem-libraries`
and `category: 技术/<领域>/<框架>`, and set its title to exactly `三方库`. This is the final item in the framework's sidebar menu. It lists external packages associated with or used alongside the framework, not the framework/runtime package itself. Base its content on the latest local session cache:

```markdown
## 三方库列表

| 库名 | 为何使用 | 如何使用 |
| --- | --- | --- |
| `package-name` | Why this conversation needs it. | Install/import or minimum usage. |
```

When no associated external package is evidenced, include one row stating `暂未识别关联三方库`; do not turn the framework/runtime package into a list entry.

## Quality bar

- Make the article understandable without the original conversation.
- Prefer conclusions and rationale over a chronological transcript.
- Preserve useful code, commands, decisions, constraints, and failure modes.
- Distinguish verified facts from inference or opinion.
- Never store secrets, access tokens, passwords, private keys, or needless personal data.
- Avoid phrases such as “as discussed above” or “the user said”.
- Use concise Chinese by default; preserve necessary English technical terms.
- Add external links only when known and relevant. Do not invent citations.
- For `技术` articles, use the latest first-party API reference and state the verification date.
