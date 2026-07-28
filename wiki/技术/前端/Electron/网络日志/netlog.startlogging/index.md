---
title: "netLog.startLogging()"
description: "在 app ready 后将网络事件写入文件，供排查与调试导出。"
category: "技术/前端/Electron/网络日志"
api: "netLog.startLogging"
tags: ["Electron", "netLog", "网络诊断"]
created: "2026-07-28"
updated: "2026-07-28"
---
## API 定位

`netLog.startLogging(path[, options])` 是 Electron 主进程 API，用于把当前 session 的网络事件写入指定文件。须在 `app` 的 `ready` 之后调用。可用 `netLog.stopLogging()` 刷盘结束；未手动停止时会在应用退出时结束。只读属性 `netLog.currentlyLogging` 表示是否正在记录。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `path: string` | `Promise<void>` | 网络日志输出文件路径；Promise 在开始记录后 resolve。 |
| `options?: object` | — | 捕获范围与文件大小上限。 |
| `options.captureMode?: 'default' \| 'includeSensitive' \| 'everything'` | — | 默认仅请求元数据；`includeSensitive` 含 cookie/认证；`everything` 含 socket 全部字节。 |
| `options.maxFileSize?: number` | — | 超过该字节数后自动停止；默认不限制。 |
| — | `netLog.stopLogging(): Promise<string>` | 停止并刷盘；resolve 为日志路径。 |
| — | `netLog.currentlyLogging: boolean` | 是否正在记录（只读）。 |

## 会话提炼场景

调试导出需要把最近网络活动打进 zip：导出前若正在记录则先 `stopLogging`，写完 zip 后再按原路径重启，避免文件占用；启动时用 `maxFileSize` 限制体积。

```ts
import { app, netLog } from "electron"
import { join } from "node:path"

const netLogPath = join(app.getPath("userData"), "logs", "current", "network.netlog")

export async function startNetLog() {
  if (netLog.currentlyLogging) return
  await netLog.startLogging(netLogPath, {
    captureMode: "default",
    maxFileSize: 20 * 1024 * 1024,
  })
}

export async function exportWithNetLog(writeZip: () => Promise<void>) {
  const restart = netLog.currentlyLogging
  if (restart) {
    await netLog.stopLogging().catch(() => undefined)
  }
  try {
    await writeZip()
  } finally {
    if (restart) await startNetLog().catch(() => undefined)
  }
}

app.whenReady().then(() => startNetLog())
```

`captureMode: "default"` 适合常规排障；需要 cookie/正文时再提高级别，并注意隐私与体积。

## 常见应用场景

- 排查桌面客户端连不上本地/远程 API 的网络层问题。
- 支持工单：导出 netlog 与应用日志一并分析。
- 用 `maxFileSize` 防止长时间运行撑满磁盘。
- 与命令行 `--log-net-log` 互补：API 适合运行中按需启停。

## 边界与注意事项

- `ready` 之前调用无效（文档约束）。
- `includeSensitive` / `everything` 可能包含凭证与载荷，导出与分享前需评估隐私。
- 正在写入的 netlog 文件可能被占用；导出前应停止记录。
- `currentlyLogging` 可用于幂等启动与导出时的停/启编排。

## 官方文档

- [netLog | Electron](https://www.electronjs.org/docs/latest/api/net-log)：verified 2026-07-28.
