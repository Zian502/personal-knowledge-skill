---
title: "Node.js：第三方依赖库"
description: "基于当前会话缓存整理 Node.js API 页面涉及的第三方依赖状态。"
category: "技术/后端/Node.js"
kind: "dependency-list"
tags: ["Node.js", "第三方依赖", "依赖清单"]
created: "2026-07-25"
updated: "2026-07-25"
---

## 依赖库列表

| 库名 | 为何使用 | 如何使用 |
| --- | --- | --- |
| 无第三方依赖 | 当前会话中的 `fsPromises.open()`、`FileHandle.read()`、`tls.getCACertificates()`、`tls.setDefaultCACertificates()` 与 `url.fileURLToPath()` 都来自 Node.js 内置 `node:*` 模块。 | 无需通过 npm 安装；按需导入，例如 `import { open } from "node:fs/promises"` 或 `import { fileURLToPath } from "node:url"`。 |

## 来源说明

本清单仅根据本地当前会话缓存中关于 Node.js 文件系统、TLS 与 URL API 的讨论提炼；当前缓存没有识别到这些 API 的额外第三方包。
