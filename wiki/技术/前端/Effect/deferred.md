---
title: "Deferred.make() / await() / succeed()：一次性就绪信号"
description: "用 Effect Deferred 表示只能完成一次的异步结果，并让等待方以不阻塞线程的方式等待。"
category: "技术/前端/Effect"
tags: ["Effect", "Deferred", "并发", "同步"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`Deferred` 是 Effect 的一次性同步原语。`Deferred.make()` 创建空值，随后仅能由 `succeed`、`fail`、`done` 等方式完成一次；`Deferred.await()` 读取结果。

## 常用参数与返回

| API | 参数 / 返回 | 说明 |
| --- | --- | --- |
| `Deferred.make<Success, Error>()` | → `Effect<Deferred<Success, Error>>` | 创建一次性 Deferred 的 Effect。 |
| `Deferred.await()` | `deferred` → `Effect<Success, Error>` | 等待成功值或错误；等待 Fiber 语义性暂停，不阻塞线程。 |
| `Deferred.succeed()` | `deferred`、`value` → `Effect<boolean>` | 以成功值完成；重复完成不会替换既有结果。 |
| `Deferred.fail()` | `deferred`、`error` → `Effect<boolean>` | 以预期错误完成。 |

## 会话提炼场景

Electron Sidecar 启动后可用 `Deferred.succeed(serverReady, credentials)` 发布连接凭证；多个 `awaitInitialization` 调用都等待同一个 `serverReady`。这比散落的 Promise resolver 更适合表达“只发布一次”的启动闸门。

## 常见应用场景

- 等待服务端口、连接、配置或一次性初始化完成。
- 将回调式事件转换为可组合的 Effect 等待点。
- 多个消费者等待同一结果，而不重复启动底层任务。

## 边界与注意事项

- `Deferred` 适合一次性结果；可重复状态更新应使用 `Ref`、Queue 或 PubSub 等原语。
- 谁负责完成 Deferred、何时超时或失败是应用设计，需要显式定义。
- 不要将敏感凭证无限期保存在全局 Deferred 中；按生命周期释放或替换。

## 关联 API

- [Fiber.fork 与 Fiber.await](/wiki/技术/前端/effect/fiber-fork-await/)

## 官方文档

- [Effect Deferred](https://effect.website/docs/concurrency/deferred/)：已于 2026-07-25 查阅。
