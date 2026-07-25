---
title: "fsPromises.open() 与 FileHandle.read()：受控读取文件"
description: "用 Node.js 的异步文件句柄 API 在明确的大小上限与关闭边界内读取授权文件。"
category: "技术/后端/Node.js"
tags: ["Node.js", "node:fs/promises", "FileHandle", "文件读取", "安全"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`fsPromises.open(path, flags[, mode])` 创建 `FileHandle`；`FileHandle.read()` 从该句柄读入 Buffer；`FileHandle.close()` 释放文件描述符。它们属于 `node:fs/promises` 的异步文件系统 API。

## 常用参数与返回

- `open(path, 'r')`：以只读标志打开文件，返回 `Promise<FileHandle>`。
- `filehandle.stat()`：返回文件状态；附件场景用其中的 `size` 在分配 Buffer 前实施上限。
- `filehandle.read(buffer, { offset, length, position })`：将数据读到给定 Buffer，返回包含 `bytesRead` 与 `buffer` 的结果。`position: 0` 表示从开头读取。
- `filehandle.close()`：等待该句柄的待处理操作完成后关闭；官方文档要求显式关闭，不能依赖垃圾回收。

## 会话提炼场景

桌面端附件选择后，主进程只对本次授权的路径调用 `open(..., 'r')`。先用 `stat().size` 与单文件/总预算比较，再按允许的长度读取；无论成功、拒绝或异常都在 `finally` 中 `close()`。路径授权与额度扣减是应用层策略，不是 Node.js API 自带能力。

## 常见应用场景

- 上传前读取并校验本地附件。
- 读取受控配置、证书或离线资源。
- 分段读取大文件，避免一次性无上限地占用内存。

## 边界与注意事项

- `stat()` 与实际读取之间文件可能变化；预算检查是防护层，不是不可变快照。
- Promise 文件系统操作使用线程池，针对同一文件的并发修改并不自动同步。
- 不要把任意渲染进程传来的路径直接交给该 API；先在应用层确认授权主体和允许路径。

## 关联 API

- [dialog.showOpenDialog()](/wiki/技术/前端/electron/dialog-show-open-dialog/)
- [ipcMain.handle()](/wiki/技术/前端/electron/ipcmain-handle/)

## 官方文档

- [Node.js File system / FileHandle](https://nodejs.org/api/fs.html)：已于 2026-07-25 查阅。
