---
title: "utilityProcess.fork()：隔离桌面端 Sidecar"
description: "从 Electron 主进程启动具备 Node.js 环境的 Utility Process，并通过生命周期与消息通道管理本地服务。"
category: "技术/前端/Electron/Utility Process"
api: "utilityProcess.fork"
tags: ["Electron", "utilityProcess", "Sidecar", "进程隔离"]
created: "2026-07-25"
updated: "2026-07-25"
---

## API 定位

`utilityProcess.fork(modulePath[, args][, options])` 从 Electron 主进程创建一个具有 Node.js 和 MessagePort 能力的 Utility Process。它是 Electron 为主进程派生子进程提供的 API。

## 依赖库

| 库 | 为何使用 | 如何使用 |
| --- | --- | --- |
| `electron` | 提供 `utilityProcess`，用于从主进程启动隔离的 Node.js Sidecar。 | `npm install --save-dev electron`；`import { utilityProcess } from "electron"`。 |

## 常用参数与返回

| API | 参数 | 返回 | 说明 |
| --- | --- | --- | --- |
| `utilityProcess.fork()` | `modulePath: string` | — | 子进程入口脚本路径。 |
| `fork()` | `args?: string[]` | — | 子进程通过 `process.argv` 获取的可选字符串参数。 |
| `fork()` | `options?: { env, cwd, stdio, session, serviceName }` | — | 常用进程与网络选项；只有 `stdio: 'pipe'` 才能读取 stdout/stderr。 |
| `fork()` | — | `UtilityProcess` | 监听 `spawn` 确认创建、`exit` 处理退出；可用 `postMessage()` 通信及 `kill()` 终止。 |

## 会话提炼场景

本地 OpenCode 服务可作为 Sidecar 由该 API 启动：主进程预分配端口和短期凭证，`fork()` 后通过消息发送启动配置，收到就绪信号后再向 UI 提供连接信息。端口、Basic Auth、健康检查和 CORS 白名单属于服务设计，而不是 `utilityProcess` 的默认安全配置。

```ts
const child = utilityProcess.fork(sidecarPath, [], { stdio: "pipe" })
child.once("message", (message) => publishSidecarCredentials(message))
child.once("exit", (code) => logger.info({ code }, "sidecar exited"))
```

## 常见应用场景

- 将易崩溃、CPU 密集或不受信任的逻辑从主进程隔离出去。
- 运行本地 HTTP 服务、转码器或命令包装器。
- 需要与渲染进程建立 MessagePort 通信的后台任务。

## 边界与注意事项

- 官方要求在 `app` 发出 `ready` 后再调用 `fork()`。
- `pid` 在成功 `spawn` 前和退出事件后都是 `undefined`；不要把它当成启动成功的唯一信号。
- 为子进程单独设置代理、系统 CA 或环境变量；主进程的运行时设置不会自动成为服务自身的应用配置。

## 关联 API

- [url.fileURLToPath()](/wiki/技术/后端/nodejs/url/urlfileurltopath/)
- [tls.setDefaultCACertificates()](/wiki/技术/后端/nodejs/tls/tlssetdefaultcacertificates/)
- [tls.getCACertificates()](/wiki/技术/后端/nodejs/tls/tlsgetcacertificates/)
- [Deferred.succeed()](/wiki/技术/前端/electron/三方库/effect/deferred/deferredsucceed/)

## 官方文档

- [Electron utilityProcess](https://www.electronjs.org/docs/latest/api/utility-process)：已于 2026-07-25 查阅。
- [Electron process model](https://www.electronjs.org/docs/latest/tutorial/process-model)：已于 2026-07-25 查阅。
