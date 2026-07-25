---
title: "Deferred.succeed()：成功完成 Deferred"
description: "以成功值完成 Deferred 并唤醒等待方，返回是否首次完成。"
category: "技术/前端/Effect/Deferred"
api: "Deferred.succeed"
tags: ["Effect", "Deferred", "并发"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`Deferred.succeed(deferred, value)`（或柯里化形式）用成功值完成 Deferred，并唤醒所有正在 `Deferred.await` 的 fiber。

## 常用参数与返回

| API | 参数 / 返回 | 说明 |
| --- | --- | --- |
| `Deferred.succeed()` | `self: Deferred<A, E>`、`value: A` | 以成功值完成。 |
| `Deferred.succeed()` | → `Effect<boolean>` | `true` 表示本次完成生效；若早已完成则为 `false`。 |

## 会话提炼场景

sidecar `utilityProcess.fork` 成功并拿到本地 URL/账号后，主进程 `Deferred.succeed(serverReady, credentials)`，让 UI 侧初始化不再阻塞。健康检查可以仍在后台 Fiber 继续。

```ts
const publishCredentials = (credentials: SidecarCredentials) =>
  Deferred.succeed(serverReady, credentials).pipe(
    Effect.catchTag("DeferredAlreadyDoneException", () => Effect.void),
  )
```

## 常见应用场景

- 发布一次性配置、端口、令牌或连接句柄。
- 将回调完成转换为 Effect 同步点。
- 与 `Deferred.fail` / `done` 对称表达失败路径。

## 边界与注意事项

- 只应有明确的生产者完成 Deferred；多处竞态 succeed 时只有第一次返回 `true`。
- 成功完成不等于业务永久可用；后续失效需另建信号，不要把 Deferred 当可变状态容器。

## 关联 API

- [Deferred.make()](/wiki/技术/前端/effect/deferred/deferredmake/)
- [Deferred.await()](/wiki/技术/前端/effect/deferred/deferredawait/)
- [utilityProcess.fork()](/wiki/技术/前端/electron/utility-process/utilityprocessfork/)

## 官方文档

- [Effect Deferred.succeed API](https://effect-ts.github.io/effect/effect/Deferred.ts.html#succeed)：已于 2026-07-25 查阅。
