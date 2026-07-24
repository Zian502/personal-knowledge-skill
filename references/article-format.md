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

## Quality bar

- Make the article understandable without the original conversation.
- Prefer conclusions and rationale over a chronological transcript.
- Preserve useful code, commands, decisions, constraints, and failure modes.
- Distinguish verified facts from inference or opinion.
- Never store secrets, access tokens, passwords, private keys, or needless personal data.
- Avoid phrases such as “as discussed above” or “the user said”.
- Use concise Chinese by default; preserve necessary English technical terms.
- Add external links only when known and relevant. Do not invent citations.
