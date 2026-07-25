---
title: "fsPromises.open()：创建受控文件句柄"
description: "用 Node.js 的异步文件系统 API 创建受控 FileHandle，作为后续授权文件读取的起点。"
category: "技术/后端/Node.js/文件系统"
api: "fsPromises.open"
tags: ["Node.js", "node:fs/promises", "FileHandle", "文件读取", "安全"]
created: "2026-07-25"
updated: "2026-07-25"
---

## API 定位

`fsPromises.open(path, flags[, mode])` 在 `node:fs/promises` 中异步打开文件并返回 `FileHandle`。该句柄是后续受控读取、检查元数据和关闭文件的起点。

## 常用参数与返回

| API | 参数 | 返回 | 说明 |
| --- | --- | --- | --- |
| `fsPromises.open()` | `path`、`flags`、`mode?` | `Promise<FileHandle>` | 用路径与文件系统标志异步打开文件；附件读取通常使用只读标志 `r`。 |

## 会话提炼场景

桌面端附件选择后，主进程只对本次授权的路径调用 `fsPromises.open(path, 'r')`。随后由应用层通过 FileHandle 检查大小、读取允许长度，并在 `finally` 中关闭。路径授权与额度扣减是应用层策略，不是该 API 自带能力。

```ts
const handle = await fsPromises.open(grant.path, "r")
try {
  const { size } = await handle.stat()
  return await readWithinLimit(handle, Math.min(size, grant.remainingBytes))
} finally {
  await handle.close()
}
```

## 常见应用场景

- 上传前读取并校验本地附件。
- 读取受控配置、证书或离线资源。
- 为后续 `FileHandle.read()`、`stat()` 与 `close()` 获得显式句柄。

## 边界与注意事项

- 打开成功不等于文件内容在后续读取前不会变化；预算检查仍需由后续操作实施。
- Promise 文件系统操作使用线程池，针对同一文件的并发修改并不自动同步。
- 不要把任意渲染进程传来的路径直接交给该 API；先在应用层确认授权主体和允许路径。

## 关联 API

- [FileHandle.read()](/wiki/技术/后端/nodejs/文件系统/filehandleread/)
- [dialog.showOpenDialog()](/wiki/技术/前端/electron/对话框/dialogshowopendialog/)
- [ipcMain.handle()](/wiki/技术/前端/electron/ipc/ipcmainhandle/)

## 官方文档

- [Node.js File system / FileHandle](https://nodejs.org/api/fs.html)：已于 2026-07-25 查阅。
