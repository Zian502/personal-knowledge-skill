---
title: "child_process.spawn()"
description: "异步创建子进程并建立 stdio 管道，适合从 Electron 主进程启动 wsl 等外部命令。"
category: "技术/后端/Node.js/子进程"
api: "child_process.spawn"
tags: ["Node.js", "child_process", "子进程"]
created: "2026-08-07"
updated: "2026-08-07"
---
## API 定位

`child_process.spawn(command[, args][, options])` 是 Node.js 异步创建子进程的主入口。它不阻塞事件循环，默认在父进程与子进程之间建立 stdin/stdout/stderr 管道，并返回 `ChildProcess`（EventEmitter）。Electron 主进程可直接使用该 API 启动系统命令（例如 Windows 上的 `wsl.exe`）。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `command: string` | `ChildProcess` | 要执行的命令（可执行文件名或路径）。 |
| `args?: readonly string[]` | — | 命令行参数列表；省略时默认为空数组。 |
| `options.cwd?` | — | 子进程工作目录；省略则继承当前目录；路径不存在会触发 `ENOENT`。 |
| `options.env?` | — | 子进程环境变量，默认 `process.env`；`undefined` 值会被忽略。 |
| `options.stdio?` | — | stdio 配置；默认对 0/1/2 建管道。可用 `'pipe'` / `'ignore'` / `'inherit'` 等。 |
| `options.shell?` | — | 默认 `false`；为 `true` 时经 shell 执行。开启时勿传入未消毒的用户输入。 |
| `options.windowsHide?` | — | Windows 上是否隐藏子进程控制台窗口，默认 `false`。 |
| `options.signal?` | — | 用 `AbortSignal` 中止子进程。 |
| `options.timeout?` | — | 最长运行毫秒数，默认 `undefined`。 |
| — | `ChildProcess` 事件 | 常见：`error`、`exit`/`close`；以及 `stdout`/`stderr` 的 `data`。 |

## 会话提炼场景

Electron Desktop 在 Windows 主进程里用 `spawn("wsl", ["-d", distro, "--", "bash", "-se"], { stdio: ["pipe", "pipe", "pipe"], windowsHide: true })`，把启动脚本写入 stdin，再监听 stdout/stderr 与 `exit`，与健康检查竞态，失败时 `child.kill()`。

```ts
import { spawn } from "node:child_process"

export function startWslBash(distro: string, script: string) {
  const child = spawn("wsl", ["-d", distro, "--", "bash", "-se"], {
    stdio: ["pipe", "pipe", "pipe"],
    windowsHide: true,
  })
  child.stdin?.end(script)

  child.once("error", (error) => {
    console.error("spawn failed", error)
  })
  child.once("exit", (code, signal) => {
    console.error("exited early", { code, signal })
  })

  return {
    stop: () => child.kill(),
    stdout: child.stdout,
    stderr: child.stderr,
  }
}
```

健康检查超时、密码与 `opencode serve` 参数属于应用层策略，不是 `spawn` 的契约。

## 常见应用场景

- 启动外部 CLI / sidecar，并流式读取日志。
- 在 Windows 上隐藏控制台窗口运行后台工具。
- 用管道向子进程喂入脚本（stdin），避免过长命令行。
- 与 `AbortSignal` / 超时组合，防止卡住的子进程拖死启动流程。

## 边界与注意事项

- 子进程超量写 stdout 且父进程未消费时可能堵死管道；不需要输出时用 `stdio: 'ignore'`。
- `shell: true` 存在命令注入风险；官方要求勿传入未消毒输入。
- 命令或 `cwd` 不存在时会 `ENOENT`。
- Windows 上 `.bat`/`.cmd` 通常不能直接当无执行文件 spawn；应经 `cmd.exe` 或 `exec`（见官方说明）。

## 关联 API

- [`server.listen()`](/wiki/技术/后端/nodejs/网络/server.listen/)（分配临时端口后再 spawn 监听进程）
- [`wsl --distribution`](/wiki/技术/前端/electron/wsl/wsl.--distribution/)（本场景中的 `command`）

## 官方文档

- [child_process.spawn() | Node.js](https://nodejs.org/api/child_process.html#child_processspawncommand-args-options)：verified 2026-08-07.
