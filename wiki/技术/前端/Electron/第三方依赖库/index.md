---
title: "Electron：第三方依赖库"
description: "基于当前会话缓存整理 Electron 主进程与 preload API 使用的第三方依赖。"
category: "技术/前端/Electron"
kind: "dependency-list"
tags: ["Electron", "第三方依赖", "依赖清单"]
created: "2026-07-25"
updated: "2026-07-25"
---

## 依赖库列表

| 库名 | 为何使用 | 如何使用 |
| --- | --- | --- |
| `electron` | 当前会话中的 `BrowserWindow`、`ipcMain`、`contextBridge`、`utilityProcess`、`dialog`、`clipboard`、`Notification` 与 `shell` 都由 Electron 的主进程或 preload 运行时提供。 | `npm install --save-dev electron`；在对应进程导入所需能力，例如 `import { app, BrowserWindow, ipcMain } from "electron"`。 |

## 来源说明

本清单仅根据本地当前会话缓存中关于 OpenCode Desktop、Electron Sidecar 和主进程边界的讨论提炼；新增依赖前应再次核对会话证据与官方文档。
