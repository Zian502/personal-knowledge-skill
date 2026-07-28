---
title: "三方库"
description: "基于当前会话缓存整理与 Electron 生态关联的三方库。"
category: "技术/前端/Electron"
kind: "ecosystem-libraries"
tags: ["Electron", "三方库", "生态"]
created: "2026-07-25"
updated: "2026-07-28"
---

## 三方库列表

| 库名 | 为何使用 | 如何使用 |
| --- | --- | --- |
| [`electron-store`](https://github.com/sindresorhus/electron-store) | 在 Main 持久化小型 KV（设置、窗口 ID、功能开关）；支持自定义文件名与目录，适配改写后的 `userData`。 | `npm install electron-store`；`import Store from 'electron-store'` 后 `new Store({ name, cwd })`。原子 API 见本目录 `electron-store` 子菜单。 |
| [`electron-log`](https://github.com/megahertz/electron-log) | 统一 Main/Renderer 日志到磁盘，支持按 scope 分文件、自定义路径，以及 Renderer console 侦听，便于诊断导出。 | `npm install electron-log`；主进程 `import log from 'electron-log/main'`，配置 `transports.file` 后调用 `log.initialize(...)`。原子 API 见本目录 `electron-log` 子菜单。 |
| [`electron-window-state`](https://github.com/mawie81/electron-window-state) | 将主窗口的尺寸和位置持久化，并在下次启动时恢复；适合与 `BrowserWindow` 一起改善桌面应用的连续使用体验。 | `npm install electron-window-state`；在主进程创建窗口前调用 `windowStateKeeper()`，将其 `x`、`y`、`width`、`height` 传给 `BrowserWindow`，再调用 `manage(window)`。其原子 API 文档位于本目录的 `electron-window-state` 子菜单。 |
| [`effect`](https://github.com/Effect-TS/effect) | 为 Electron 主进程中的 sidecar 启动、健康检查与就绪信号提供副作用编排、结构化并发和错误处理原语。 | `npm install effect`；导入 `Effect`、`Deferred`、`Fiber` 等 API。其原子 API 文档位于本目录的 `Effect` 子菜单。 |

## 来源说明

本清单根据当前会话中关于 OpenCode Desktop 的 `electron-store` 延迟持久化、`electron-log` 诊断日志，以及既有窗口状态与 Effect sidecar 素材提炼；“三方库”仅记录与 Electron 搭配的外部包，不记录 `electron` 框架本体。