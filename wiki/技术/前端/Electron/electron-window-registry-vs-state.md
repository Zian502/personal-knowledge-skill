---
title: "Electron 多窗口：Registry 与 window-state"
description: "Window Registry 持久化窗口 ID 列表，electron-window-state 持久化单窗几何，二者用同一 id 协作且关闭策略不同。"
category: "技术/前端/Electron"
tags: ["Electron", "BrowserWindow", "window-state", "多窗口"]
created: "2026-07-25"
updated: "2026-07-25"
---
## 背景与适用场景

Electron 多窗口应用需要同时回答两个问题：「下次启动恢复哪些窗口？」以及「每个窗口上次在哪、多大？」。二者容易混在一个 store 里，或误以为 `electron-window-state` 能管窗口列表。

## 核心结论

| 组件 | 管什么 | 持久化 |
|------|--------|--------|
| **Window Registry** | 窗口 ID 列表 + 运行时 `Map` + 最后聚焦 | 如 store 的 `windowIds` |
| **electron-window-state** | 单个窗口的 x/y/width/height | 如 `window-state-<id>.json` |

- Registry 回答「有哪些窗」；window-state 回答「每个窗几何」。
- 二者用同一窗口 `id` 关联；从 Registry 删除某个 id 时应 `cleanup` 对应的 state/业务数据文件。
- **故意关闭某个窗口**（应用仍在跑）应从持久化 ID 列表移除并清理文件；**退出应用导致关窗**应保留 ID，以便下次恢复多窗布局。

## 实现要点

### Registry 行为摘要

- `register(id, win)`：写入内存 Map，并把 id 追加到持久化列表。
- `closed(id)`：若正在 quitting 或已是最后一个窗口，不删持久化 id；否则从列表移除并调用 `cleanup(id)`。
- `focused` / `lastFocused`：深链、菜单命令等需要「当前窗」时使用。
- 启动时 `restoreMainWindows()`：读持久化 ids，无则新建一个 UUID，再逐个 `createMainWindow(id)`。

### createMainWindow 关键顺序

1. 用 `windowState({ file: window-state-<id>.json, defaultWidth/Height })` 恢复几何。
2. 创建 `BrowserWindow`：`show: false`，平台相关无边框/标题栏；`webPreferences` 使用 `contextIsolation`、关 `nodeIntegration`、`sandbox`，经 preload 暴露 API。
3. 接线权限白名单、无响应/加载失败恢复对话框、session 请求头改写。
4. `state.manage(win)` 持续落盘几何；`registerWindow`；加载页面（开发用 `ELECTRON_RENDERER_URL`，生产用自定义协议如 `oc://renderer/...`）。
5. `ready-to-show` 后再 `show()`，减少白屏闪烁。

## 常见问题与注意事项

- 关闭最后一个窗口时，`closed` 往往早于 `before-quit`；若此时删掉 id，下次就无法恢复——Registry 通常把「最后一个窗关闭」视同退出并保留 id。
- Windows 关机/注销可能不走完整 `before-quit`，可用窗口 `session-end` 提前标记 quitting。
- 每窗业务状态（如 tabs）应另文件按 id 存储，与几何 state 分开，但在同一 `cleanup` 路径删除。
