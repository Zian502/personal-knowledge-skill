---
title: "Notification：创建并展示系统通知"
description: "主进程创建 OS 通知对象，调用 show() 后展示；适合经 IPC 转发的桌面提示。"
category: "技术/前端/Electron/通知"
api: "Notification"
tags: ["Electron", "Notification", "系统通知"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`new Notification([options])` 创建操作系统桌面通知对象。实例化不会自动展示，必须调用 `notification.show()`。

## 常用参数与返回

| API | 参数 | 返回 | 说明 |
| --- | --- | --- | --- |
| `new Notification()` | `title?` / `body?` | `Notification` 实例 | 通知标题与正文。 |
| `new Notification()` | `subtitle?` (macOS) | — | 标题下的副标题。 |
| `new Notification()` | `silent?` | — | 是否抑制系统提示音。 |
| `notification.show()` | — | 实例方法 | 立即向用户展示；再次 `show` 会关掉旧的并以相同属性新建。 |
| `Notification.isSupported()` | — | `boolean` | 当前系统是否支持桌面通知。 |

## 会话提炼场景

渲染进程经 IPC `show-notification` 把 `title`/`body` 交给主进程，主进程执行 `new Notification({ title, body }).show()`。

```ts
ipcMain.handle("show-notification", (_event, title: string, body: string) => {
  new Notification({ title, body }).show()
})
```

## 常见应用场景

- 后台任务完成、消息到达等系统级提示。
- 主进程统一发通知，渲染进程只发意图。
- macOS/Windows 上扩展回复、动作按钮等高级交互（需额外选项与事件）。

## 边界与注意事项

- 渲染进程若要发通知，官方更推荐 Web Notifications API；主进程用该类。
- macOS 基于 UNNotification，**需要代码签名**才会真正出现；未签名二进制可能触发 `failed`。
- Electron 内置类不可在用户代码中子类化。

## 关联 API

- [ipcMain.handle()](/wiki/技术/前端/electron/ipc/ipcmainhandle/)

## 官方文档

- [Electron Notification](https://www.electronjs.org/docs/latest/api/notification)：已于 2026-07-25 查阅。
