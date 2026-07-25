---
title: "Electron 附件选择：Token 授权与字节预算"
description: "主进程对话框选文件后签发 token，渲染进程仅能读取本次授权路径，并受总附件字节上限约束。"
category: "技术/前端/Electron"
tags: ["Electron", "安全", "附件", "IPC", "沙箱"]
created: "2026-07-25"
updated: "2026-07-25"
---
## 背景与适用场景

桌面端选文件附件时，若渲染进程拿到任意绝对路径后自行读盘，等于绕过沙箱。更稳妥的做法是：主进程对话框选文件 → 发临时 token → 渲染进程只能凭 token 读「本次选中」的路径，并有总字节预算。

## 核心结论

- **授权表**：`token → { senderId, allowedPaths, remainingBytes }`。
- **读文件**：校验 `sender` 与 token 匹配，且 path 在允许集合内；读成功后从集合删除该 path，额度扣减；集合空则删 token。
- **先 stat 再读**：超过 `maxBytes`（默认如 20MB，或剩余额度）直接抛错，避免大文件进内存。
- **选择阶段也可预检**：对所选文件 `size` 求和，超总预算则拒收，不必等到逐个读取。

## 实现要点

### 读盘实现注意点

- `fs.promises.open` + 循环 `file.read` 填满预分配 Buffer，最后 `close`。
- 返回 `ArrayBuffer`（对 Buffer 做 `slice`）便于 IPC 传到渲染进程。
- `allocUnsafe` 可接受，因为随后会覆盖全部有效字节；只返回实际读到的长度切片。

### 与 IPC 的配合

1. `dialog.showOpenDialog` 得到路径列表。
2. `assertAttachmentBudget` 检查总大小。
3. `authorizations.add(webContentsId, paths)` 返回 token。
4. Renderer `read-picked-file(token, path)` / `release-picked-files(token)`。

## 常见问题与注意事项

- Token 必须绑定 `event.sender.id`，防止其他窗口冒用。
- 剩余额度应按**实际读出的 byteLength**扣减，而不是仅信初始 stat（文件可能被并发改写；仍以 stat 上限为第一道门）。
- 用完或取消选择要 `release`，避免 Map 泄漏。
