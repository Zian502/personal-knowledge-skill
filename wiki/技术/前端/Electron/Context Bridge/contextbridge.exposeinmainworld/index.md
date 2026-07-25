---
title: "contextBridge.exposeInMainWorld()：构建受限 Renderer API"
description: "在 context isolation 下从 preload 向 Renderer 暴露可审计、最小化的原生能力。"
category: "技术/前端/Electron/Context Bridge"
api: "contextBridge.exposeInMainWorld"
tags: ["Electron", "contextBridge", "contextIsolation", "preload", "安全"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`contextBridge.exposeInMainWorld(apiKey, api)` 由 preload 脚本调用，将一个受限 API 注入 Renderer 的主世界 `window[apiKey]`。当 `contextIsolation` 开启时，preload 与页面脚本处在不同 JavaScript context；该 API 是两者之间的显式桥梁。

## 常用参数与返回

| API | 参数 / 返回 | 说明 |
| --- | --- | --- |
| `contextBridge.exposeInMainWorld()` | `apiKey: string` | 注入到 Renderer `window` 对象上的名称。 |
| `contextBridge.exposeInMainWorld()` | `api: object` | 可暴露函数及受支持的可复制值；非函数值会被复制并冻结。 |
| 桥接函数 | 参数、返回值、错误 | 跨 context 传递时为复制语义；自定义原型和 `Symbol` 不应作为边界数据。 |
| `contextBridge.exposeInIsolatedWorld()` | `worldId: number` | 向指定 isolated world 暴露 API；自定义 world 应使用 1000 以上 ID。 |

## 会话提炼场景

OpenCode Desktop 在 BrowserWindow 中开启 `contextIsolation: true`、关闭 `nodeIntegration` 并启用 sandbox。preload 使用 `contextBridge.exposeInMainWorld("api", api)` 提供文件选择、更新、窗口控制和初始化等明确方法；Renderer 只能调用 `window.api`，不能直接取得 Node.js 或完整 `ipcRenderer`。

这使附件读取可以被设计为“选择文件后获取 token，再按 token 读取一次已选路径”，而不是向网页暴露任意路径读文件能力。token 校验和 IPC handler 授权是应用层责任；context bridge 仅提供跨 context 的能力边界。

```ts
contextBridge.exposeInMainWorld("api", {
  attachments: { read: (token: string) => ipcRenderer.invoke("attachments:read", token) },
})
```

## 常见应用场景

- 在安全 Renderer 中公开 `preferences.load()`、`dialog.selectFiles()` 一类细粒度原生能力。
- 为 IPC request-response 或订阅事件提供窄包装函数。
- 在 TypeScript 中配合 `Window` 全局声明，让 Renderer 获得受限 API 的静态类型。

## 边界与注意事项

- `contextIsolation` 不会自动保证安全。不要暴露 `ipcRenderer.send`、完整 `ipcRenderer` 或 Node 模块；官方建议每个允许的 IPC channel 对应一个包装方法。
- Main process 仍需验证 IPC 参数、调用来源和授权。桥接 API 的命名并不是访问控制。
- 函数被代理、数据被复制，不能依赖跨 bridge 的对象身份、可变共享状态或自定义类原型。
- 将 `nodeIntegration` 保持关闭且通过最小 bridge 暴露能力，是本会话所述 Electron desktop 架构的实现建议，不是该 API 自动施加的保证。

## 关联 API

- [ipcMain.handle()](/wiki/技术/前端/electron/ipc/ipcmainhandle/)
- [new BrowserWindow()](/wiki/技术/前端/electron/窗口/browserwindow/)

## 官方文档

- [Electron contextBridge](https://www.electronjs.org/docs/latest/api/context-bridge)：已于 2026-07-25 查阅。
- [Electron Context Isolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation)：已于 2026-07-25 查阅。
