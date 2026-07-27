---
title: "shell.openExternal()"
description: "在主进程打开外部协议 URL，例如默认浏览器中的 https 链接。"
category: "技术/前端/Electron/Shell"
api: "shell.openExternal"
tags: ["Electron", "shell", "桌面集成"]
created: "2026-07-25"
updated: "2026-07-27"
---
## API 定位

`shell.openExternal(url[, options])` 用系统默认方式打开外部协议 URL（例如用默认浏览器打开 `https:`，或用邮件客户端打开 `mailto:`）。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `url: string` | `Promise<void>` | 要打开的外部协议 URL。 |
| `options.activate?: boolean`（macOS） | `Promise<void>` | 是否把打开的应用置于前台；默认 `true`。 |
| `options.workingDirectory?: string`（Windows） | `Promise<void>` | 工作目录。 |
| `options.logUsage?: boolean`（Windows） | `Promise<void>` | 是否按用户发起启动记入常用程序跟踪；默认 `false`。 |

## 会话提炼场景

渲染进程通过 IPC（如 `open-link`）把 URL 交给主进程，主进程调用 `shell.openExternal`。沙箱渲染进程不应直接依赖 `shell`。

```ts
ipcMain.handle("open-link", async (_event, rawUrl: string) => {
  const url = new URL(rawUrl)
  if (url.protocol !== "https:") throw new Error("仅允许 HTTPS 链接")
  await shell.openExternal(url.toString())
})
```

## 常见应用场景

- 应用内链接跳转到系统浏览器。
- 打开帮助文档、账单或第三方 OAuth 页面。
- 处理自定义协议以外的外部 URI。

## 边界与注意事项

- `shell` 可在主进程使用；在沙箱渲染进程中不可用。官方建议不在 renderer 直接调用。
- 打开任意用户可控 URL 前应做协议/域名校验（应用层策略）。
- 同模块还有 `openPath`、`showItemInFolder` 等桌面集成方法，用途不同，应分 API 使用。

## 关联 API

- [ipcMain.handle()](/wiki/技术/前端/electron/ipc/ipcmainhandle/)

## 官方文档

- [Electron shell](https://www.electronjs.org/docs/latest/api/shell)：已于 2026-07-25 查阅。
