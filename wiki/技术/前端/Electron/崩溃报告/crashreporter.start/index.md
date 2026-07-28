---
title: "crashReporter.start()"
description: "启动 Crashpad 收集崩溃；可仅本地落盘或上传到远程服务器。"
category: "技术/前端/Electron/崩溃报告"
api: "crashReporter.start"
tags: ["Electron", "crashReporter", "Crashpad"]
created: "2026-07-28"
updated: "2026-07-28"
---
## API 定位

`crashReporter.start(options)` 是 Electron 主进程 API，用于启动 Crashpad 收集崩溃。启动后会监控随后创建的进程；一旦启动不可关闭。官方建议尽可能早调用，最好在 `app` 的 `ready` 之前；若 Renderer 创建时尚未启动，则该 Renderer 不会被监控。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `options: object` | `void` | 启动崩溃报告；须先于其他 `crashReporter` API。 |
| `options.uploadToServer?: boolean` | — | 是否上传到服务器，默认 `true`。为 `false` 时仅本地落盘到 crashes 目录。 |
| `options.submitURL?: string` | — | 以 POST 提交崩溃的 URL；当 `uploadToServer` 为 `false` 时可省略。 |
| `options.productName?: string` | — | 产品名，默认 `app.name`。 |
| `options.compress?: boolean` | — | 是否 gzip 压缩上传，默认 `true`。 |
| `options.rateLimit?: boolean` | — | macOS/Windows：限制上传频率约 1 次/小时，默认 `false`。 |
| `options.ignoreSystemCrashHandler?: boolean` | — | 主进程崩溃是否仍转发给系统 crash handler，默认 `false`。 |
| `options.extra?` / `options.globalExtra?` | — | 附加字符串注解；key ≤ 39 字节；值有长度限制；`globalExtra` 启动后不可改。 |

崩溃目录默认在 `userData` 下的 `Crashpad`；可在启动前用 `app.setPath('crashDumps', path)` 覆盖。

## 会话提炼场景

桌面诊断链路需要本地保留 minidump，但不上传远程服务器：自定义 `crashDumps` 路径后以 `uploadToServer: false` 启动，随后导出调试 zip 时一并打包该目录。

```ts
import { app, crashReporter } from "electron"
import { mkdirSync } from "node:fs"
import { join } from "node:path"

const dir = join(app.getPath("userData"), "Crashpad")
mkdirSync(dir, { recursive: true })
app.setPath("crashDumps", dir)

crashReporter.start({
  uploadToServer: false,
  compress: true,
})

// 可用 process.crash() 在受控环境验证收集是否生效
```

应用层可将 `crashDumps` 与 `electron-log` 目录、`netLog` 文件一并打进调试导出包；这不属于 `crashReporter.start` 的契约。

## 常见应用场景

- 生产环境提交到自建或第三方崩溃收集服务。
- 仅本地保留 dumps，供支持人员离线分析。
- 在启动极早期初始化，覆盖后续创建的 Renderer / child 进程。
- 用 `globalExtra` 标注构建渠道、实验开关等稳定元数据。

## 边界与注意事项

- 主进程启动后会自动监控子进程，一般不要在子进程重复 `start`。
- Renderer 中调用已弃用；隔离环境下应经 preload/`contextBridge` 暴露受控能力。
- `uploadToServer: false` 时 dumps 留在本地，需自行做保留与导出策略。
- `extra` / `globalExtra` 键值长度受限；超长 key 会被忽略，超长 value 会被截断。

## 官方文档

- [crashReporter | Electron](https://www.electronjs.org/docs/latest/api/crash-reporter)：verified 2026-07-28.
