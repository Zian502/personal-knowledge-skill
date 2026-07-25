---
title: "Deferred.await()：等待一次性结果"
description: "挂起直到 Deferred 完成，多个等待方可共享同一就绪信号。"
category: "技术/前端/Effect/Deferred"
api: "Deferred.await"
tags: ["Effect", "Deferred", "并发"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`Deferred.await(deferred)` 读取 Deferred 的值；若尚未完成，则挂起当前 fiber，直到该 Deferred 被完成一次。

## 常用参数与返回

| API | 参数 | 返回 | 说明 |
| --- | --- | --- | --- |
| `Deferred.await()` | `self: Deferred<A, E>` | — | 要等待的 Deferred。 |
| `Deferred.await()` | — | `Effect<A, E>` | 成功时得到 `A`；若 Deferred 以错误完成则失败为 `E`。 |

## 会话提炼场景

多个 `awaitInitialization` IPC 调用都 `Deferred.await(serverReady)`，共享同一 sidecar 凭证闸门；生产者稍后 `Deferred.succeed` 一次即可唤醒全部等待方。

```ts
const awaitInitialization = Deferred.await(serverReady).pipe(
  Effect.map((credentials) => ({ url: credentials.url })),
)
```

## 常见应用场景

- 多消费者等待同一初始化结果。
- 把“服务已就绪”建模为一次性同步点。
- 与超时组合（应用层对 await 的 Effect 加 timeout）。

## 边界与注意事项

- Deferred 只能完成一次；重复完成不会再次改变已等待方已取得的结果语义（完成 API 返回 boolean 表示是否首次完成）。
- 谁负责 succeed/fail、超时与取消策略需应用层明确。

## 关联 API

- [Deferred.make()](/wiki/技术/前端/effect/deferred/deferredmake/)
- [Deferred.succeed()](/wiki/技术/前端/effect/deferred/deferredsucceed/)

## 官方文档

- [Effect Deferred.await API](https://effect-ts.github.io/effect/effect/Deferred.ts.html#await)：已于 2026-07-25 查阅。
