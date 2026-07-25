---
title: "FileHandle.read()：向缓冲区读取文件字节"
description: "从 FileHandle 读取数据到 buffer，并返回 bytesRead，适合受控分段读附件。"
category: "技术/后端/Node.js/文件系统"
api: "FileHandle.read"
tags: ["Node.js", "文件系统", "FileHandle", "附件"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`filehandle.read(...)` 从已打开的 `FileHandle` 读取数据写入给定 buffer，并返回实际读取字节数。它是受控附件读取循环的核心原语。

## 常用参数与返回

| API | 参数 | 返回 | 说明 |
| --- | --- | --- | --- |
| `filehandle.read(buffer, offset, length, position)` | 四参数形式 | `{ bytesRead, buffer }` | 向 `buffer` 的 `offset` 起写入最多 `length` 字节；`position` 为文件偏移。 |
| `filehandle.read([options])` / `read(buffer[, options])` | `offset` 默认 `0`；`length` 默认 `buffer.byteLength - offset`；`position` 默认 `null` | `{ bytesRead, buffer }` | `position` 为 `null`/`-1` 时从当前文件位置读并推进；非负整数时不改当前文件位置。 |

## 会话提炼场景

桌面端附件在 `fsPromises.open(path, "r")` 后，先 `stat` 做字节上限检查，再循环调用 `filehandle.read`，直到读满或 `bytesRead === 0`。路径是否允许、总预算多少属于应用层授权，不是该 API 自带能力。

```ts
const buffer = Buffer.alloc(Math.min(allowedBytes, size))
let offset = 0
while (offset < buffer.length) {
  const { bytesRead } = await handle.read(buffer, offset, buffer.length - offset, offset)
  if (bytesRead === 0) break
  offset += bytesRead
}
```

## 常见应用场景

- 分段读取大文件或流式填充预分配缓冲区。
- 在明确长度约束下读取配置/附件，避免一次 `readFile` 失控。
- 与 `filehandle.stat()` / `close()` 组成显式生命周期。

## 边界与注意事项

- 文件未被并发修改时，读到 `bytesRead === 0` 表示 EOF。
- 若先多次 `read` 再 `readFile`，后者从**当前文件位置**读到末尾，不一定从文件头开始。
- `position` 自 v21 起可接受 `bigint`。

## 关联 API

- [fsPromises.open()](/wiki/技术/后端/nodejs/文件系统/fspromisesopen/)
- [dialog.showOpenDialog()](/wiki/技术/前端/electron/对话框/dialogshowopendialog/)

## 官方文档

- [Node.js FileHandle.read](https://nodejs.org/api/fs.html#filehandlereadoptions)：已于 2026-07-25 查阅。
