---
title: "Deferred.make()：创建一次性就绪信号"
description: "用 Effect Deferred 创建只能完成一次的异步结果，以便等待方共享同一个就绪信号。"
category: "技术/前端/Electron/三方库/Effect/Deferred"
api: "Deferred.make"
tags: ["Effect", "Deferred", "并发", "同步"]
created: "2026-07-25"
updated: "2026-07-25"
---

## API 定位

`Deferred.make()` 创建一个空的 Effect Deferred。Deferred 是一次性同步原语，后续可由 `succeed`、`fail`、`done` 等方式完成一次。

## 依赖库

| 库 | 为何使用 | 如何使用 |
| --- | --- | --- |
| `effect` | 提供 `Deferred.make()` 与 Effect 的资源/错误模型，用于创建共享的就绪信号。 | `npm install effect`；`import { Deferred } from "effect"`。 |

## 常用参数与返回

| API | 参数 | 返回 | 说明 |
| --- | --- | --- | --- |
| `Deferred.make<Success, Error>()` | — | `Effect<Deferred<Success, Error>>` | 创建一次性 Deferred 的 Effect。 |

## 会话提炼场景

Electron Sidecar 启动后可用 `Deferred.succeed(serverReady, credentials)` 发布连接凭证；多个 `awaitInitialization` 调用都等待同一个 `serverReady`。这比散落的 Promise resolver 更适合表达“只发布一次”的启动闸门。

```ts
const serverReady = yield* Deferred.make<SidecarCredentials>()

yield* Deferred.succeed(serverReady, { url: localUrl, token })
```

## 常见应用场景

- 等待服务端口、连接、配置或一次性初始化完成。
- 将回调式事件转换为可组合的 Effect 等待点。
- 多个消费者等待同一结果，而不重复启动底层任务。

## 边界与注意事项

- `Deferred` 适合一次性结果；可重复状态更新应使用 `Ref`、Queue 或 PubSub 等原语。
- 谁负责完成 Deferred、何时超时或失败是应用设计，需要显式定义。
- 不要将敏感凭证无限期保存在全局 Deferred 中；按生命周期释放或替换。

## 关联 API

- [Deferred.await()](/wiki/技术/前端/electron/三方库/effect/deferred/deferredawait/)
- [Deferred.succeed()](/wiki/技术/前端/electron/三方库/effect/deferred/deferredsucceed/)
- [Effect.fork()](/wiki/技术/前端/electron/三方库/effect/fiber/effectfork/)
- [Fiber.await()](/wiki/技术/前端/electron/三方库/effect/fiber/fiberawait/)

## 官方文档

- [Effect Deferred API](https://effect-ts.github.io/effect/effect/Deferred.ts.html)：已于 2026-07-25 查阅。
