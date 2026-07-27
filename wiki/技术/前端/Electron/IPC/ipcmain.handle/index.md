---
title: "ipcMain.handle()"
description: "为 ipcRenderer.invoke() 注册异步处理器，并以 channel、调用来源和返回值建立受控主进程能力。"
category: "技术/前端/Electron/IPC"
api: "ipcMain.handle"
tags: ["Electron", "ipcMain", "IPC", "安全", "主进程"]
created: "2026-07-25"
updated: "2026-07-27"
---

## API 定位

`ipcMain.handle(channel, listener)` 在主进程注册一个可由 `ipcRenderer.invoke(channel, ...args)` 调用的请求—响应处理器。处理器的普通返回值或 Promise 最终值会回复给调用方。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `channel: string` | `void` | 注册可调用通道；用 `attachments:read` 一类业务命名空间提高可读性。 |
| `listener: (event, ...args) => any \| Promise<any>` | `void` | `event.sender` 表示发起调用的 `WebContents`；listener 的值或 Promise 最终值会回复给调用方。 |

## 会话提炼场景

附件读取接口可以通过 `ipcMain.handle('attachments:read', listener)` 暴露。处理器用 `event.sender.id` 将 token 绑定到请求窗口，再验证允许路径和剩余额度；这套授权表是应用层逻辑，`ipcMain.handle()` 只提供调用边界。

```ts
ipcMain.handle("attachments:read", async (event, token: string) => {
  const grant = grants.get(token)
  if (!grant || grant.webContentsId !== event.sender.id) throw new Error("未授权")
  return readGrantedFile(grant.path, grant.remainingBytes)
})
```

## 常见应用场景

- 从渲染进程请求原生文件选择、文件读写或系统信息。
- 将菜单、窗口或本地服务状态封装为少量受控命令。
- 用统一的请求—响应形式替代大量临时事件监听器。

## 边界与注意事项

- 主进程抛出的错误跨 IPC 时并不透明，渲染进程通常只能得到原始错误的 `message`。
- 不要向渲染进程直接暴露完整 `ipcRenderer`；官方 IPC 指南建议经 preload 和 `contextBridge` 暴露最小能力。
- 通道名称不是权限控制；每个 handler 都必须验证输入和调用来源。

## 关联 API

- [dialog.showOpenDialog()](/wiki/技术/前端/electron/对话框/dialogshowopendialog/)
- [fsPromises.open()](/wiki/技术/后端/nodejs/文件系统/fspromisesopen/)
- [shell.openExternal()](/wiki/技术/前端/electron/shell/shellopenexternal/)
- [clipboard.readImage()](/wiki/技术/前端/electron/剪贴板/clipboardreadimage/)
- [Notification](/wiki/技术/前端/electron/通知/notification/)

## 官方文档

- [Electron ipcMain](https://www.electronjs.org/docs/latest/api/ipc-main)：已于 2026-07-25 查阅。
- [Electron IPC guide](https://www.electronjs.org/docs/latest/tutorial/ipc)：已于 2026-07-25 查阅。
