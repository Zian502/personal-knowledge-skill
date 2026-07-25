---
title: "url.fileURLToPath()：将 file URL 转为绝对路径"
description: "把 import.meta.url 等 file: URL 转为跨平台绝对路径，用于定位旁路脚本。"
category: "技术/后端/Node.js/URL"
api: "url.fileURLToPath"
tags: ["Node.js", "URL", "ESM", "路径"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`url.fileURLToPath(url[, options])` 将 `file:` URL 转为跨平台有效的绝对路径字符串，正确处理百分号解码与 Windows/POSIX 路径差异。

## 常用参数与返回

| API | 参数 / 返回 | 说明 |
| --- | --- | --- |
| `url.fileURLToPath()` | `url` | `file:` URL 字符串或 URL 对象。 |
| `url.fileURLToPath()` | `options.windows?` | `true` 强制 Windows 路径，`false` 强制 POSIX，`undefined` 用系统默认。 |
| `url.fileURLToPath()` | → `string` | 绝对路径字符串。 |

## 会话提炼场景

Electron 主进程用 `dirname(fileURLToPath(import.meta.url))` 定位与当前模块同目录的 `sidecar.js`，再交给 `utilityProcess.fork`。**推断**：相对 `process.cwd()` 在打包后不可靠，故以当前模块 URL 为锚点。

```ts
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

const sidecarPath = join(dirname(fileURLToPath(import.meta.url)), "sidecar.js")
```

## 常见应用场景

- ESM 下由 `import.meta.url` 得到 `__filename` / 资源旁路路径。
- 修正 `URL.pathname` 在 Windows/`file://` UNC 上的错误切分。
- 为子进程入口、preload、静态资源计算绝对路径。

## 边界与注意事项

- 会解码百分号编码（含 `%2e` / `%2e%2e`）并规范化路径；**不能单独依赖它防目录穿越**，使用前需显式校验路径边界。
- 编码斜杠（`%2F` / `%5C`）会被正确拒绝，但编码的点段仍按真实路径段处理。

## 关联 API

- [utilityProcess.fork()](/wiki/技术/前端/electron/utility-process/utilityprocessfork/)

## 官方文档

- [Node.js url.fileURLToPath](https://nodejs.org/api/url.html#urlfileurltopathurl)：已于 2026-07-25 查阅。
