---
title: "wsl --distribution"
description: "在指定 WSL Linux 发行版中运行命令，供 Windows 主机自动化启动 Linux 侧服务。"
category: "技术/前端/Electron/WSL"
api: "wsl.--distribution"
tags: ["Electron", "WSL", "Windows"]
created: "2026-08-07"
updated: "2026-08-07"
---
## API 定位

`wsl --distribution <Distribution Name>`（短选项 `-d`）是 Windows Subsystem for Linux 的命令行入口之一，用于在指定已安装的 Linux 发行版中运行命令或进入该发行版。WSL 本身是 Windows 功能：可在无需单独双系统或传统完整虚拟机工作流的情况下，在 Windows 上运行 Linux 环境与发行版。

可与 `--user <User Name>` 组合指定发行版内用户。未指定发行版时，WSL 使用默认发行版。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `--distribution` / `-d` `<name>` | 进程退出码（经 shell/`CreateProcess`） | 指定要运行的已安装发行版名称（如 `Debian`、`Ubuntu`）。 |
| `--user` / `-u` `<username>` | — | 以该发行版内已存在的用户运行；用户不存在会报错。 |
| `--` 后的命令参数 | — | 在发行版内执行的命令与参数（例如 `bash -se`）。 |
| `wsl --list --verbose` | 文本列表 | 查看已安装发行版、运行状态与 WSL 1/2 版本。 |
| `wsl --status` | 文本状态 | 默认发行版、内核等信息。 |

完整选项以 `wsl --help` 与 Microsoft 基本命令文档为准。

## 会话提炼场景

Electron 主进程在 Windows 上通过 `child_process.spawn("wsl", ["-d", distro, "--", "bash", "-se"], …)`，向指定 distro 注入脚本并启动 Linux 内的 `opencode serve`，再从 Windows 用 `http://127.0.0.1:<port>` 连接。`--distribution` 保证多发行版机器上不会误用默认 distro。

```ts
import { spawn } from "node:child_process"

const distro = "Debian"
const child = spawn(
  "wsl",
  ["--distribution", distro, "--", "bash", "-lc", "echo hello-from-wsl"],
  { stdio: ["ignore", "pipe", "pipe"], windowsHide: true },
)

child.stdout?.setEncoding("utf8")
child.stdout?.on("data", (chunk) => process.stdout.write(chunk))
child.on("exit", (code) => {
  if (code !== 0) throw new Error(`wsl exited with ${code}`)
})
```

网络互通、localhost 转发与健康检查属于应用与 WSL 网络行为组合，不是 `--distribution` 开关本身的契约。

## 常见应用场景

- 在多发行版环境中固定目标 distro 跑构建、测试或服务。
- 从 PowerShell/CMD/Node 自动化调用 Linux 工具链。
- 配合 `--user` 以非默认用户执行需要特定权限的命令。
- 运维脚本先 `wsl --list --verbose` 再选择可运行的发行版。

## 边界与注意事项

- 发行版必须已安装；可用 `wsl --list --online` / `--install` 管理（见官方基本命令文档）。
- 从 Bash 内部调用时文档建议使用 `wsl.exe` 形式。
- WSL 2 默认以轻量 VM 运行 Linux 内核；与 WSL 1 的系统调用/文件系统特性不同。
- 终止可用 `wsl --terminate <name>` 或 `wsl --shutdown`（影响范围不同，按文档选用）。

## 关联 API

- [`child_process.spawn()`](/wiki/技术/后端/nodejs/子进程/child_process.spawn/)
- [`server.listen()`](/wiki/技术/后端/nodejs/网络/server.listen/)

## 官方文档

- [What is WSL | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/about)：verified 2026-08-07.
- [Basic commands for WSL | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)：verified 2026-08-07.
