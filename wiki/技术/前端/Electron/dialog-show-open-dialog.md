---
title: "dialog.showOpenDialog()：选择本地文件"
description: "在 Electron 主进程调用原生打开对话框，并以取消状态和文件路径列表处理结果。"
category: "技术/前端/Electron"
tags: ["Electron", "dialog", "文件选择", "主进程"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`dialog.showOpenDialog([window, ]options)` 是 Electron 主进程的异步原生文件/目录选择 API。传入窗口可让对话框成为该窗口的模态对话框。

## 常用参数与返回

- `window`：可选的 `BaseWindow`，用于绑定父窗口。
- `options.properties`：常用 `openFile`、`openDirectory`、`multiSelections`；Windows 与 Linux 上同时设置文件和目录选择会显示目录选择器。
- `options.filters`：文件类型过滤；扩展名不带点或通配前缀，例如 `png`，全部文件使用 `*`。
- 返回 `Promise<{ canceled, filePaths, bookmarks? }>`；取消时 `canceled` 为 `true`，`filePaths` 为空。

## 会话提炼场景

附件流程应在主进程打开对话框、检查所选文件总大小，并只把临时授权标识交给渲染进程。`filePaths` 是 API 返回的数据，但将路径绑定到调用窗口、签发一次性 token、限制总字节数都是应用层安全策略。

## 常见应用场景

- “导入文件”或“添加附件”按钮。
- 选择工作区、导出目录或配置文件。
- 通过过滤器限制可见的媒体、日志或项目文件类型。

## 边界与注意事项

- 异步版本适合 UI 流程；官方特别建议 macOS 使用异步对话框以避免展开/折叠问题。
- macOS MAS 的安全作用域书签需要显式启用相关选项；不要把它假定为跨平台能力。
- 选择文件不等于授权渲染进程可读取任意路径。

## 关联 API

- [ipcMain.handle()](/wiki/技术/前端/electron/ipcmain-handle/)
- [fsPromises.open() 与 FileHandle.read()](/wiki/技术/后端/node.js/fspromises-filehandle-read/)

## 官方文档

- [Electron dialog](https://www.electronjs.org/docs/latest/api/dialog)：已于 2026-07-25 查阅。
