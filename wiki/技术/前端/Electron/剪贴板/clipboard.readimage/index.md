---
title: "clipboard.readImage()"
description: "从系统剪贴板读取 NativeImage，供主进程转发给渲染进程作附件。"
category: "技术/前端/Electron/剪贴板"
api: "clipboard.readImage"
tags: ["Electron", "clipboard", "NativeImage"]
created: "2026-07-25"
updated: "2026-07-27"
---
## API 定位

`clipboard.readImage([type])` 从系统剪贴板读取图像内容，返回 `NativeImage`。适合主进程代读剪贴板截图/图片后传给渲染进程。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `type?: "clipboard" \| "selection"` | `NativeImage` | 默认 `"clipboard"`；`"selection"` 仅 Linux。 |

## 会话提炼场景

主进程 IPC `read-clipboard-image` 调用 `clipboard.readImage()`；若图像非空，再转 PNG buffer 与宽高返回渲染进程作附件。**推断**：空剪贴板检测与 PNG 编码属于 `NativeImage` 侧后续步骤，不是 `readImage` 本身返回值字段。

```ts
ipcMain.handle("read-clipboard-image", () => {
  const image = clipboard.readImage()
  if (image.isEmpty()) return null
  return { png: image.toPNG(), size: image.getSize() }
})
```

## 常见应用场景

- 粘贴截图到聊天/编辑器附件。
- 从剪贴板导入位图资源。
- 主进程统一读写剪贴板，避免沙箱 renderer 直连。

## 边界与注意事项

- 自 Electron 40 起，在 renderer 直接使用 clipboard API 已弃用；应放在 preload/主进程经 `contextBridge` 暴露。
- Linux 另有 `selection` 剪贴板，需显式传 `type`。
- 是否“有图”需结合 `NativeImage` 实例方法判断（应用层）。

## 关联 API

- [ipcMain.handle()](/wiki/技术/前端/electron/ipc/ipcmainhandle/)

## 官方文档

- [Electron clipboard](https://www.electronjs.org/docs/latest/api/clipboard)：已于 2026-07-25 查阅。
