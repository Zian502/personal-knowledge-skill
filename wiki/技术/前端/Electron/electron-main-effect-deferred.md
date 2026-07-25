---
title: "用 Effect Deferred 协调 Electron 主进程启动"
description: "用 Effect 编排启动流，用 Deferred 作为 sidecar 凭证就绪闸门，用 Fiber 等待后台 loading 任务。"
category: "技术/前端/Electron"
tags: ["Effect", "Deferred", "Fiber", "Electron", "异步"]
created: "2026-07-25"
updated: "2026-07-25"
---
## 背景与适用场景

Electron 主进程启动常有多段异步：等 `app.whenReady`、清理、spawn 本地服务、健康检查、再开窗口。同时 UI 侧又希望尽早 `awaitInitialization` 拿到服务凭证。用裸 Promise 容易嵌套深、失败分支散乱；需要「一次性闸门」和「可等待的后台任务」。

## 核心结论

- **`Effect`**：可组合的异步工作流（`gen` / `promise` / `catch` / `timeout` / `forkChild` / `runFork`），适合编排主进程启动。
- **`Deferred`**：一次性将来值；多处 `await`，一处 `succeed`/`fail`。适合「server 凭证已就绪」「回调式 listen 拿到端口」这类同步点。
- **`Fiber`**：Effect 的后台任务句柄；`forkChild` 后可用 `Fiber.await` 等待结果，而不把所有逻辑写成一条阻塞链。

典型模式：sidecar spawn 成功后立刻 `Deferred.succeed(serverReady, credentials)`，渲染进程 IPC 侧 `Deferred.await(serverReady)`；健康检查可在子 Fiber 里继续跑，主流程再决定是否等它结束再恢复窗口。

## 实现要点（模式）

```ts
const serverReady = Deferred.makeUnsafe<Credentials, unknown>()

// IPC：UI 等待凭证
awaitInitialization: () => Effect.runPromise(
  Effect.gen(function* () {
    return yield* Deferred.await(serverReady)
  }),
)

// spawn 成功后尽早放行 UI
yield* Deferred.succeed(serverReady, { url, username, password })

const loadingTask = yield* Effect.gen(function* () {
  // spawn + health...
}).pipe(Effect.forkChild)

yield* Fiber.await(loadingTask)
```

回调式 API（如 `server.listen(0, cb)`）也可先 `Deferred.make`，在回调里 `succeed`/`fail`，外层 `yield* Deferred.await`。

## 常见问题与注意事项

- Deferred 是一次性的：成功或失败后不要重复 settle；初始化失败应有明确 fail/转发路径。
- `forkChild` 的失败不会自动变成「父 Effect 的未捕获异常」除非你 `Fiber.await` 或显式转发；产品代码常把初始化失败写回同一个 Deferred。
- 不必为整个 Electron 应用全面 Effect 化；在「启动编排 + 跨 IPC 就绪信号」边界收益最大。
