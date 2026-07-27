---
title: "Effect.fork()"
description: "将 Effect 作为 Fiber 在后台启动，并保留后续等待、取消和观测的能力。"
category: "技术/前端/Electron/三方库/Effect/Fiber"
api: "Effect.fork"
tags: ["Effect", "Fiber", "并发", "后台任务"]
created: "2026-07-25"
updated: "2026-07-27"
---

## API 定位

`Effect.fork()` 将目标 Effect 作为轻量 Fiber 在后台启动，并返回该 Fiber 的句柄；后续可等待、取消或观测其退出状态。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `self: Effect<A, E, R>` | `Effect<Fiber.RuntimeFiber<A, E>>` | 在后台启动目标 Effect，并产生 Fiber 句柄。 |

## 会话提炼场景

主进程可以 fork Sidecar 的 spawn 与健康检查任务，同时通过 Deferred 先发布“可连接”的凭证；在窗口展示或退出阶段，再 `Fiber.await` 或中断该后台任务。何时把“已 spawn”视为“可用”仍需要应用层健康检查定义。

```ts
const healthFiber = yield* Effect.fork(
  waitForSidecarHealth(url).pipe(Effect.timeout("10 seconds")),
)
// 退出时由应用生命周期中断该 Fiber。
```

## 常见应用场景

- 并行预热缓存、加载配置或启动本地服务。
- 对长任务保留取消、等待和错误观测能力。
- 将后台工作与父作用域的生命周期绑定。

## 边界与注意事项

- fork 并不自动说明任务成功；必须处理 `Exit` 或错误传播。
- 后台任务应有取消与退出策略，避免应用关闭后的孤儿工作。
- 不要为了并发而 fork 所有工作；有顺序依赖的任务仍应明确等待。

## 关联 API

- [Fiber.await()](/wiki/技术/前端/electron/三方库/effect/fiber/fiberawait/)
- [Deferred.make()](/wiki/技术/前端/electron/三方库/effect/deferred/deferredmake/)
- [Deferred.succeed()](/wiki/技术/前端/electron/三方库/effect/deferred/deferredsucceed/)

## 官方文档

- [Effect Fiber API](https://effect-ts.github.io/effect/effect/Fiber.ts.html)：已于 2026-07-25 查阅。
