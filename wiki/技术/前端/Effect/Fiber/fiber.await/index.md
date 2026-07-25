---
title: "Fiber.await()：等待 Fiber 并取得 Exit"
description: "挂起直到目标 Fiber 结束，返回 Exit 而不自动传播失败。"
category: "技术/前端/Effect/Fiber"
api: "Fiber.await"
tags: ["Effect", "Fiber", "并发"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`Fiber.await(fiber)` 挂起当前 fiber，直到目标 fiber 结束，并返回描述结果的 `Exit`（成功、失败、中断等），而不会把失败自动传播到当前 Effect。

## 常用参数与返回

| API | 参数 / 返回 | 说明 |
| --- | --- | --- |
| `Fiber.await()` | `self: Fiber<A, E>` | 要等待的 fiber。 |
| `Fiber.await()` | → `Effect<Exit<A, E>>` | 始终成功得到 `Exit`；需自行解读成败。 |

## 会话提炼场景

主进程用 `Effect.forkChild` 启动 sidecar spawn/健康检查任务后，以 `Fiber.await(loadingTask)` 等待后台任务结束，再恢复窗口。若需要失败直接让当前流程失败，应改用 `Fiber.join`（官方区分：`await` 检视 Exit，`join` 传播错误）。

```ts
const loadingTask = yield* Effect.forkChild(startSidecarAndCheckHealth)
const exit = yield* Fiber.await(loadingTask)

if (Exit.isFailure(exit)) yield* Effect.logWarning("sidecar 未就绪")
```

## 常见应用场景

- 等待后台预热/初始化并检查 Exit。
- 在取消、失败、成功分支上做不同收尾。
- 与 fork 类 API 组成“启动 + 可观测等待”。

## 边界与注意事项

- `Fiber.await` **不会**把 fiber 失败扁平化为当前 Effect 的失败；要传播错误用 `Fiber.join`。
- 仅等待不等于已定义业务“就绪”；业务健康检查仍是应用层概念。

## 关联 API

- [Effect.fork()](/wiki/技术/前端/effect/fiber/effectfork/)
- [Deferred.await()](/wiki/技术/前端/effect/deferred/deferredawait/)

## 官方文档

- [Effect Fiber.await API](https://effect-ts.github.io/effect/effect/Fiber.ts.html#await)：已于 2026-07-25 查阅。
