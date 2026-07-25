---
title: "Effect：第三方依赖库"
description: "基于当前会话缓存整理 Effect API 页面使用的第三方依赖。"
category: "技术/前端/Effect"
kind: "dependency-list"
tags: ["Effect", "第三方依赖", "依赖清单"]
created: "2026-07-25"
updated: "2026-07-25"
---

## 依赖库列表

| 库名 | 为何使用 | 如何使用 |
| --- | --- | --- |
| `effect` | 当前会话中的 `Deferred`、`Effect.fork()` 与 `Fiber.await()` 依赖 Effect 提供的类型化 Effect 运行时和结构化并发原语。 | `npm install effect`；按所需 API 导入，例如 `import { Deferred, Effect, Fiber } from "effect"`。 |

## 来源说明

本清单仅根据本地当前会话缓存中关于 Effect、Deferred 和 Fiber 的讨论提炼；新增依赖前应再次核对会话证据与官方文档。
