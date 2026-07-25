---
title: "ipcMain.handle()：实现请求—响应式 IPC"
description: "为 ipcRenderer.invoke() 注册异步处理器，并以 channel、调用来源和返回值建立受控主进程能力。"
category: "技术/前端/Electron"
tags: ["Electron", "ipcMain", "IPC", "安全", "主进程"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`ipcMain.handle(channel, listener)` 在主进程注册一个可由 `ipcRenderer.invoke(channel, ...args)` 调用的请求—响应处理器。处理器的普通返回值或 Promise 最终值会回复给调用方。

## 常用参数与返回

- `channel`：开发者定义的字符串通道；用业务命名空间（如 `attachments:read`）提高可读性。
- `listener(event, ...args)`：可返回值或 Promise；`event.sender` 表示发起调用的 `WebContents`。
- `ipcRenderer.invoke()`：渲染进程获得一个 Promise 结果。
- `ipcMain.removeHandler(channel)`：在退出、重载或测试清理时移除处理器。

## 会话提炼场景

附件读取接口可以通过 `ipcMain.handle('attachments:read', listener)` 暴露。处理器用 `event.sender.id` 将 token 绑定到请求窗口，再验证允许路径和剩余额度；这套授权表是应用层逻辑，`ipcMain.handle()` 只提供调用边界。

## 常见应用场景

- 从渲染进程请求原生文件选择、文件读写或系统信息。
- 将菜单、窗口或本地服务状态封装为少量受控命令。
- 用统一的请求—响应形式替代大量临时事件监听器。

## 边界与注意事项

- 主进程抛出的错误跨 IPC 时并不透明，渲染进程通常只能得到原始错误的 `message`。
- 不要向渲染进程直接暴露完整 `ipcRenderer`；官方 IPC 指南建议经 preload 和 `contextBridge` 暴露最小能力。
- 通道名称不是权限控制；每个 handler 都必须验证输入和调用来源。

## 关联 API

- [dialog.showOpenDialog()](/wiki/技术/前端/electron/dialog-show-open-dialog/)
- [fsPromises.open() 与 FileHandle.read()](/wiki/技术/后端/node.js/fspromises-filehandle-read/)

## 官方文档

- [Electron ipcMain](https://www.electronjs.org/docs/latest/api/ipc-main)：已于 2026-07-25 查阅。
- [Electron IPC guide](https://www.electronjs.org/docs/latest/tutorial/ipc)：已于 2026-07-25 查阅。
