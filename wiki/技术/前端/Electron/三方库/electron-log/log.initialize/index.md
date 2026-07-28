---
title: "log.initialize()"
description: "在 Electron 主进程初始化 electron-log，打通 Renderer 日志通道并配置文件输出。"
category: "技术/前端/Electron/三方库/electron-log"
api: "log.initialize"
tags: ["Electron", "electron-log", "日志"]
created: "2026-07-28"
updated: "2026-07-28"
---
## API 定位

`log.initialize(options?)` 是 [`electron-log`](https://github.com/megahertz/electron-log) 主进程入口的初始化方法。v5 起日志逻辑集中在 Main：Renderer 侧只采集并通过 IPC 送到 Main。应在创建首个窗口之前调用，以便注入 preload 或启用 console 侦听。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `options?: object` | `void` | 在 `app` ready 后按选项配置 preload 注入与 Renderer console 侦听。 |
| `options.preload?: boolean \| string` | — | 是否注入内置 preload（默认 `true`）；也可传自定义 preload 路径字符串。设为 `false` 可禁用自动注入。 |
| `options.spyRendererConsole?: boolean` | — | 默认 `false`；为 `true` 时把 Renderer 的 `console` 消息转到 Main 处理（对象会变成 `[Object]` 文本）。 |
| `options.getSessions?: () => Session[]` | — | 返回需要注入 preload 的自定义 `session` 列表。 |
| `options.includeFutureSession?: boolean` | — | 是否对之后新建的 session 继续注入；设为 `false` 可关闭对未来 session 的注入。 |

相关配置（同属主进程 `electron-log/main`，常在 `initialize` 前后使用）：

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `log.transports.file.resolvePathFn` | — | 自定义日志文件路径；可按 scope / processType 分文件。 |
| `log.transports.file.maxSize` | — | 单文件大小上限（字节）。 |
| `log.scope(name)` | 带 scope 的 logger | 输出带 scope 标签；便于按模块拆分文件名。 |

## 会话提炼场景

诊断日志模块在自定义 `userData/logs/<启动时间戳>/` 下按 scope 写文件，并关闭自动 preload（改用自有 preload/IPC），同时打开 `spyRendererConsole` 收集 Renderer console。

```ts
import log from "electron-log/main.js"
import { join } from "node:path"
import { mkdirSync } from "node:fs"
import { app } from "electron"

const run = join(app.getPath("userData"), "logs", new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, ""))
mkdirSync(run, { recursive: true })

log.transports.file.maxSize = 5 * 1024 * 1024
log.transports.file.resolvePathFn = (_vars, message) => {
  const scope = message?.scope ?? (message?.variables?.processType === "renderer" ? "renderer" : "main")
  return join(run, `${scope}.log`)
}

log.initialize({ preload: false, spyRendererConsole: true })

const scoped = log.scope("network")
scoped.info("net log started", { path: join(run, "network.netlog") })
```

导出调试包、Crashpad、netLog 属于应用编排；`log.initialize` 只负责把 Main/Renderer 日志通道接好。

## 常见应用场景

- 打包应用中统一收集 Main 与 Renderer 日志到磁盘。
- 用 `resolvePathFn` 把每次启动写到独立目录，便于按会话导出。
- 用 `scope` 区分 crash、network、updater 等子系统。
- 开发期用 `spyRendererConsole` 把页面 `console` 落到主日志。

## 边界与注意事项

- 必须在 Main 调用；Renderer 应使用 `electron-log/renderer` 或依赖 Main 注入的通道。
- `spyRendererConsole` 无法完整传递对象参数，复杂结构会丢信息。
- 关闭 `preload` 后，需自行保证 Renderer 日志如何到达 Main（自有 preload、IPC 或仅 spy console）。
- 控制台 transport 在 stdout 被关闭时可能抛 `EPIPE`；应用可捕获后禁用 console transport（应用层策略）。

## 官方文档

- [electron-log README](https://github.com/megahertz/electron-log/blob/master/README.md)：verified 2026-07-28.
- [initialize.md](https://github.com/megahertz/electron-log/blob/master/docs/initialize.md)：verified 2026-07-28.
- [initialize 源码（preload / spyRendererConsole 默认值）](https://github.com/megahertz/electron-log/blob/master/src/main/initialize.js)：verified 2026-07-28.
