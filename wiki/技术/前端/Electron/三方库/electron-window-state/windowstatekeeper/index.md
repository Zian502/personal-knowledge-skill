---
title: "windowStateKeeper()"
description: "读取、恢复并持续保存 Electron BrowserWindow 的尺寸、位置与窗口模式。"
category: "技术/前端/Electron/三方库/electron-window-state"
api: "windowStateKeeper"
tags: ["Electron", "electron-window-state", "窗口状态"]
created: "2026-07-27"
updated: "2026-07-27"
---
## API 定位

`windowStateKeeper(options)` 是 `electron-window-state` 的 CommonJS 主入口。它在 Electron 主进程中读取窗口状态文件，返回可用于创建 `BrowserWindow` 的尺寸、位置和窗口模式，并通过返回对象的 `manage(window)` 监听窗口移动、缩放与关闭事件。

该库的 README 明确要求在 Electron `ready` 事件之后调用；现代 Electron 应用可以在 `app.whenReady()` 完成后调用。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `options: Options` | `State` | 配置状态文件、默认窗口尺寸以及最大化、全屏恢复行为；TypeScript 声明将该参数标记为必填。 |
| `options.defaultWidth?: number` | — | 尚无有效状态文件时使用的宽度，默认 `800`。 |
| `options.defaultHeight?: number` | — | 尚无有效状态文件时使用的高度，默认 `600`。 |
| `options.path?: string` | — | 状态文件目录，默认 `app.getPath("userData")`。 |
| `options.file?: string` | — | 状态文件名，默认 `window-state.json`；多窗口可使用不同文件名。 |
| `options.maximize?: boolean` | — | 是否恢复上次关闭时的最大化状态，默认 `true`。 |
| `options.fullScreen?: boolean` | — | 是否恢复上次关闭时的全屏状态，默认 `true`。 |
| — | `State.x`、`State.y` | 已保存的窗口坐标；尚未保存时可能为 `undefined`。 |
| — | `State.width`、`State.height` | 已保存的窗口尺寸；没有有效状态时使用默认尺寸。 |
| — | `State.manage(window): void` | 注册窗口尺寸、位置和关闭事件监听，并恢复最大化或全屏状态。 |
| — | `State.unmanage(): void` | 移除当前受管窗口的监听器。 |
| — | `State.saveState(window): void` | 立即保存指定窗口的当前状态；官方说明多数场景优先使用 `manage()`。 |

## 会话提炼场景

Electron 的“三方库”总览已经列出 `electron-window-state`，但此前没有对应库目录。将窗口状态恢复逻辑沉淀为独立 API 页面后，文档菜单可以从库名直接进入 `windowStateKeeper()`，并与 Electron 自身的 `BrowserWindow` API 页面分开。

```js
const { app, BrowserWindow } = require("electron");
const windowStateKeeper = require("electron-window-state");

app.whenReady().then(() => {
  const state = windowStateKeeper({
    defaultWidth: 1000,
    defaultHeight: 720,
    file: "main-window-state.json",
  });

  const window = new BrowserWindow({
    x: state.x,
    y: state.y,
    width: state.width,
    height: state.height,
  });

  state.manage(window);
  window.loadFile("index.html");
});
```

这是应用层组合示例：窗口内容、安全配置和多窗口命名策略仍由应用负责，`windowStateKeeper()` 只管理窗口状态。

## 常见应用场景

- 恢复主窗口上次关闭时的尺寸和屏幕位置。
- 使用不同 `file` 值分别保存多个窗口的状态。
- 恢复最大化或全屏模式，减少桌面应用重复调整窗口的操作。
- 在显示器布局发生变化后，将不可见窗口回退到主显示器的安全默认位置。

## 边界与注意事项

- 必须在 Electron `ready` 之后调用，因为默认路径和显示器信息依赖 Electron 的 `app`、`screen` API。
- 官方 README 提醒创建 `BrowserWindow` 时不要启用 `useContentSize: true`，否则窗口尺寸计算方式会改变。
- `manage(window)` 会负责监听与关闭时保存；只有需要提前解除管理时才调用 `unmanage()`。
- 该库同步读写 JSON 状态文件，并在源码中吞掉读写异常；应用若需要可观测的持久化错误，应在更高层增加诊断策略。最后一点是根据实现源码作出的应用层建议，不是库的错误回调契约。
- 官方仓库当前发布版本为 `5.0.3`，发布时间较早；升级 Electron 时应在目标平台验证多显示器、全屏和窗口关闭行为。

## 关联 API

- [`new BrowserWindow()`](/wiki/技术/前端/electron/窗口/browserwindow/)

## 官方文档

- [electron-window-state README](https://github.com/mawie81/electron-window-state#readme)：API、参数、返回状态与使用示例，核验于 2026-07-27。
- [TypeScript declarations](https://github.com/mawie81/electron-window-state/blob/master/index.d.ts)：`Options` 与 `State` 类型，核验于 2026-07-27。
- [Implementation source](https://github.com/mawie81/electron-window-state/blob/master/index.js)：状态验证、显示器边界和保存行为，核验于 2026-07-27。
