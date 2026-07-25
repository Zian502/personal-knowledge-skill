---
title: "OpenCode Desktop Sidecar 架构"
description: "用 Utility Process 跑与 CLI 同一套 OpenCode Server，实现桌面壳与后端隔离、本机鉴权与自定义协议 CORS。"
category: "技术/前端/Electron"
tags: ["Electron", "sidecar", "utilityProcess", "OpenCode", "TLS"]
created: "2026-07-25"
updated: "2026-07-25"
---
## 背景与适用场景

Electron 桌面应用若把完整业务后端（HTTP API、工具执行、模型调用）直接塞进主进程，会带来两类问题：后端崩溃或卡死会拖垮窗口/IPC；后端体积大，与桌面壳的生命周期纠缠在一起。OpenCode Desktop 用 **Utility Process 形态的 Sidecar** 跑与 CLI 同一套 OpenCode Server，渲染进程只通过本机 HTTP 使用它。

## 核心结论

- **职责分离**：Main 管窗口/IPC/系统能力；Sidecar 管 Server；Renderer 只拿 `{ url, username, password }` 后发 HTTP。
- **复用 CLI Server**：Sidecar 动态 `import("virtual:opencode-server")`，构建时解析到 `packages/opencode/dist/node/node.js`，避免桌面端重写后端。
- **进程隔离**：`utilityProcess.fork(sidecar.js)`；Server 崩溃不影响 Electron 壳。
- **凭证与端口由主进程预分配**：先选空闲端口、生成随机 password，再 `postMessage({ type: "start", ... })`，便于尽早把就绪信号交给 UI。
- **安全边界**：监听 `127.0.0.1` + Basic Auth；CORS 仅放行自定义协议来源（如 `oc://renderer`）。
- **Sidecar 是独立进程**：主进程里设的 TLS/代理不会自动继承，Sidecar 启动前需自行配置系统 CA、`NO_PROXY`、环境代理等。

## 实现要点

### 启动时序（主进程）

1. 解析或探测空闲端口，hostname 固定本机 loopback。
2. 生成随机 password。
3. `spawnLocalServer` → fork `sidecar.js`（路径用当前模块目录拼接，避免打包后 cwd 漂移）。
4. `postMessage({ type: "start", hostname, port, password, userDataPath })`。
5. 等待 sidecar 的 `ready`；再做 `/api/health`（或兼容路径）健康检查。
6. 用 `Deferred.succeed` 一类闸门把凭证交给 `awaitInitialization` IPC，供 Renderer 使用。
7. 退出/重启时先发 `stop`，超时再 `kill`。

### Sidecar 内启动 Server

```ts
const { Server } = await import("virtual:opencode-server")
listener = await Server.listen({
  port,
  hostname,
  username: "opencode",
  password,
  cors: ["oc://renderer"],
})
parentPort.postMessage({ type: "ready" })
```

动态 import 的原因：Server 很重；且需在环境变量、证书、代理准备完成后再加载。

### 系统证书

Sidecar 内合并 Node default CA 与 OS system CA，再 `setDefaultCACertificates`，以支持企业代理/自签根证书；失败只 warn，不阻断启动。主进程若也有同类逻辑，仍须在 Sidecar 再做一遍。

### 与 WSL Sidecar 的关系

Windows 上可在 WSL 内再起一套 server（WSL sidecar）。概念相同：**桌面壳 + 独立 server 进程**，运行环境不同。

## 常见问题与注意事项

- 不要假设 Utility Process 继承主进程的 TLS 默认值或 Electron session 配置。
- 路径定位优先 `dirname(fileURLToPath(import.meta.url))`，不要写死相对 cwd。
- CORS 必须与渲染页实际 origin 一致（自定义协议页不是 `http://localhost`）。
- Health check 与 `ready` 消息分工：`ready` 表示已 listen；health 表示 HTTP 栈真正可服务。
