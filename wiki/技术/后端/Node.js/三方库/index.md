---
title: "三方库"
description: "基于当前会话缓存整理与 Node.js 生态关联的三方库状态。"
category: "技术/后端/Node.js"
kind: "ecosystem-libraries"
tags: ["Node.js", "三方库", "生态"]
created: "2026-07-25"
updated: "2026-07-25"
---

## 三方库列表

| 库名 | 为何使用 | 如何使用 |
| --- | --- | --- |
| 暂未识别关联三方库 | 当前会话中的 `fsPromises.open()`、`FileHandle.read()`、`tls.getCACertificates()`、`tls.setDefaultCACertificates()` 与 `url.fileURLToPath()` 都来自 Node.js 内置 `node:*` 模块，未出现与 Node.js 搭配的外部包。 | 在后续会话或项目资料中确认具体生态包后再补充；不要将 Node.js 或 `node:*` 内置模块作为条目。 |

## 来源说明

本清单仅根据本地当前会话缓存中关于 Node.js 文件系统、TLS 与 URL API 的讨论提炼；“三方库”仅记录与 Node.js 关联的外部包，不记录 Node.js 或其内置模块。
