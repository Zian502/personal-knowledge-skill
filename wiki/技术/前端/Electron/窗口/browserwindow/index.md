---
title: "new BrowserWindow()：创建并显示主窗口"
description: "使用 BrowserWindow 构造选项、webPreferences 与 ready-to-show 事件建立安全且避免闪烁的窗口生命周期。"
category: "技术/前端/Electron/窗口"
api: "BrowserWindow"
tags: ["Electron", "BrowserWindow", "窗口", "安全"]
created: "2026-07-25"
updated: "2026-07-25"
---

## API 定位

`new BrowserWindow([options])` 在 Electron 主进程创建和控制原生浏览器窗口。`BrowserWindow` 是 `EventEmitter`，可监听 `ready-to-show` 等窗口事件。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `options?: BrowserWindowConstructorOptions` | `BrowserWindow` | 可先设置 `show: false` 创建隐藏窗口，待内容可显示时再调用 `show()`。 |
| `options.webPreferences.preload?: string` | `BrowserWindow` | 绝对脚本路径；即使关闭 Node integration 仍可访问 Node API，应只暴露最小能力。 |
| `options.webPreferences.contextIsolation?: boolean` | `BrowserWindow` | 默认 `true`；将 preload 与网站代码置于不同 JavaScript context，应通过 `contextBridge` 显式共享 API。 |
| `options.webPreferences.nodeIntegration?: boolean` | `BrowserWindow` | 默认 `false`；控制渲染进程 Node integration。 |
| `options.webPreferences.sandbox?: boolean` | `BrowserWindow` | Electron 20 起默认 `true`；设置 `nodeIntegration: true` 会自动关闭该沙箱。 |

## 会话提炼场景

多窗口恢复可由应用层 Registry 保存窗口 ID，而每个 ID 对应的几何状态由窗口状态库保存。每次恢复时用 `BrowserWindow` 创建隐藏窗口、接入受限 preload API，再在 `ready-to-show` 显示。Registry 的保留/清理策略并非 `BrowserWindow` API 的自动行为。

```ts
const window = new BrowserWindow({
  show: false,
  webPreferences: {
    preload,
    contextIsolation: true,
    nodeIntegration: false,
    sandbox: true,
  },
})
window.once("ready-to-show", () => window.show())
window.on("closed", () => windowRegistry.delete(window.id))
```

## 常见应用场景

- 主窗口、编辑器窗口或预览窗口的创建与恢复。
- 通过 preload 暴露受限原生能力。
- 以 `show: false` 和 `ready-to-show` 降低白屏或闪烁。

## 边界与注意事项

- 不要为了方便开启 `nodeIntegration`；它会改变渲染进程的安全边界。
- `contextIsolation: true` 只隔离全局对象；preload 仍应以 `contextBridge` 暴露最小 API，并由 Main process 校验每个 IPC 调用。
- Linux Wayland 对创建后的移动、聚焦和调整大小存在限制。
- 对复杂应用，官方指出 `ready-to-show` 可能让首屏显得较慢；应结合背景色和体验目标决定策略。

## 官方文档

- [Electron BrowserWindow](https://www.electronjs.org/docs/latest/api/browser-window)：已于 2026-07-25 查阅。
