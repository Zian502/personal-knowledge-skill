---
title: "三方库"
description: "基于当前会话缓存整理与 Electron 生态关联的三方库。"
category: "技术/前端/Electron"
kind: "ecosystem-libraries"
tags: ["Electron", "三方库", "生态"]
created: "2026-07-25"
updated: "2026-07-25"
---

## 三方库列表

| 库名 | 为何使用 | 如何使用 |
| --- | --- | --- |
| `electron-window-state` | 将主窗口的尺寸和位置持久化，并在下次启动时恢复；适合与 `BrowserWindow` 一起改善桌面应用的连续使用体验。 | `npm install electron-window-state`；在主进程创建窗口前调用 `windowStateKeeper()`，将其 `x`、`y`、`width`、`height` 传给 `BrowserWindow`，再调用 `manage(window)`。 |
| `effect` | 为 Electron 主进程中的 sidecar 启动、健康检查与就绪信号提供副作用编排、结构化并发和错误处理原语。 | `npm install effect`；导入 `Effect`、`Deferred`、`Fiber` 等 API。其原子 API 文档位于本目录的 `Effect` 子菜单。 |

## 来源说明

本清单根据当前会话中关于 OpenCode Desktop、Electron Sidecar、主进程边界及窗口状态持久化的素材提炼；“三方库”仅记录与 Electron 搭配的外部包，不记录 `electron` 框架本体。
