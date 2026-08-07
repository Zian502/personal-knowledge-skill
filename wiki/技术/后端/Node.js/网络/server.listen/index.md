---
title: "server.listen()"
description: "让 net.Server 监听 TCP；port 为 0 时由操作系统分配临时端口。"
category: "技术/后端/Node.js/网络"
api: "server.listen"
tags: ["Node.js", "net", "端口"]
created: "2026-08-07"
updated: "2026-08-07"
---
## API 定位

`server.listen([port[, host[, backlog]]][, callback])` 是 `net.Server` 的 TCP 监听入口。当 `port` 省略或为 `0` 时，操作系统会分配一个当前未占用的临时端口；可在 `'listening'` 之后通过 `server.address().port` 读取。常与 `net.createServer()` 组合使用。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `port?: number` | `net.Server`（链式） | 监听端口；`0` 或省略表示由 OS 分配临时端口。 |
| `host?: string` | — | 绑定地址；省略时在可用时监听 `::`，否则 `0.0.0.0`。 |
| `backlog?: number` | — | 等待连接队列长度（各 `listen` 重载共用的常见参数）。 |
| `callback?: () => void` | — | 作为 `'listening'` 监听器追加。 |
| — | `'listening'` 事件 | 开始接受连接后触发。 |
| — | `server.address()` | 监听成功后返回地址信息；TCP 场景含 `port`、`address`、`family`。 |
| — | `server.close([callback])` | 停止接受新连接；已有连接需另行关闭。 |

## 会话提炼场景

为即将在 WSL 内启动的 `opencode serve` 挑选本机空闲端口：在 Windows 侧 `listen(0, "127.0.0.1")`，读取 `address.port` 后立刻 `close`，再把该端口传给 Linux 侧进程，避免硬编码冲突。

```ts
import { createServer } from "node:net"

export function allocatePort() {
  return new Promise<number>((resolve, reject) => {
    const server = createServer()
    server.on("error", reject)
    server.listen(0, "127.0.0.1", () => {
      const address = server.address()
      if (typeof address !== "object" || !address) {
        server.close()
        reject(new Error("Failed to get port"))
        return
      }
      server.close(() => resolve(address.port))
    })
  })
}
```

应用层推断：关闭探测 socket 与真正服务绑定之间存在极短竞态窗口；高并发下仍可能撞车，需要重试或由服务端自行绑定 `0` 再回传端口。这不是 `listen(0)` 的保证。

## 常见应用场景

- 集成测试中为临时 HTTP/TCP 服务申请空闲端口。
- 桌面应用启动本地 sidecar 前探测可用端口。
- 仅绑定 `127.0.0.1`，避免对外网卡暴露探测/服务端口。

## 边界与注意事项

- 必须在 `'listening'`（或 listen 回调）之后再读 `server.address().port`。
- 省略 `host` 时可能同时涉及 IPv6 `::` 与 IPv4 行为，跨平台需验证。
- `listen` 是异步的；错误通过 `'error'` 事件传递。
- 仅探测端口时记得 `close`，否则会一直占用该端口。

## 关联 API

- [`child_process.spawn()`](/wiki/技术/后端/nodejs/子进程/child_process.spawn/)

## 官方文档

- [server.listen(port) | Node.js net](https://nodejs.org/api/net.html#serverlistenport-host-backlog-callback)：verified 2026-08-07.
