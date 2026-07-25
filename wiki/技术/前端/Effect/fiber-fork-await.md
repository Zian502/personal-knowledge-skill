---
title: "Effect.fork 与 Fiber.await：观察后台任务"
description: "将 Effect 作为 Fiber 在后台执行，并在需要时等待其退出结果而不把启动流程写成一条阻塞链。"
category: "技术/前端/Effect"
tags: ["Effect", "Fiber", "并发", "后台任务"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

Fiber 是 Effect 的轻量并发执行单元。`Effect.fork`（或具备作用域语义的 `Effect.forkChild`）启动后台 Effect，`Fiber.await` 等待该 Fiber 的退出结果。

## 常用参数与返回

- `Effect.fork(effect)`：返回启动目标 Effect 的 Effect，成功值是 `Fiber` 句柄。
- `Effect.forkChild(effect)`：在父作用域下启动子 Fiber，适合需要随父任务管理生命周期的后台工作。
- `Fiber.await(fiber)`：等待 Fiber 完成并返回其 `Exit`；需要结果值时再按 Exit 的成功/失败分支处理。
- `Fiber.interrupt(fiber)`：请求中断后台工作，用于取消或关闭流程。

## 会话提炼场景

主进程可以 fork Sidecar 的 spawn 与健康检查任务，同时通过 Deferred 先发布“可连接”的凭证；在窗口展示或退出阶段，再 `Fiber.await` 或中断该后台任务。何时把“已 spawn”视为“可用”仍需要应用层健康检查定义。

## 常见应用场景

- 并行预热缓存、加载配置或启动本地服务。
- 对长任务保留取消、等待和错误观测能力。
- 将后台工作与父作用域的生命周期绑定。

## 边界与注意事项

- fork 并不自动说明任务成功；必须处理 `Exit` 或错误传播。
- 后台任务应有取消与退出策略，避免应用关闭后的孤儿工作。
- 不要为了并发而 fork 所有工作；有顺序依赖的任务仍应明确等待。

## 关联 API

- [Deferred.make() / await() / succeed()](/wiki/技术/前端/effect/deferred/)

## 官方文档

- [Effect Fibers](https://www.effect.website/docs/v3/concurrency/fibers)：已于 2026-07-25 查阅。
