---
title: Wiki
description: 按领域分类的个人知识文章。
sidebar:
  order: 0
---

这里收录从 LLM 会话中提炼出的可复用知识。每篇文章都包含独立的背景、结论、步骤与边界；可从下方索引或顶部搜索进入。

## 知识索引

### 技术/前端/Effect

- [Deferred.make() / await() / succeed()：一次性就绪信号](/wiki/技术/前端/effect/deferred/): 用 Effect Deferred 表示只能完成一次的异步结果，并让等待方以不阻塞线程的方式等待。
- [Effect.fork 与 Fiber.await：观察后台任务](/wiki/技术/前端/effect/fiber-fork-await/): 将 Effect 作为 Fiber 在后台执行，并在需要时等待其退出结果而不把启动流程写成一条阻塞链。

### 技术/前端/Electron

- [new BrowserWindow()：创建并显示主窗口](/wiki/技术/前端/electron/browser-window/): 使用 BrowserWindow 构造选项、webPreferences 与 ready-to-show 事件建立安全且避免闪烁的窗口生命周期。
- [dialog.showOpenDialog()：选择本地文件](/wiki/技术/前端/electron/dialog-show-open-dialog/): 在 Electron 主进程调用原生打开对话框，并以取消状态和文件路径列表处理结果。
- [ipcMain.handle()：实现请求—响应式 IPC](/wiki/技术/前端/electron/ipcmain-handle/): 为 ipcRenderer.invoke() 注册异步处理器，并以 channel、调用来源和返回值建立受控主进程能力。
- [utilityProcess.fork()：隔离桌面端 Sidecar](/wiki/技术/前端/electron/utility-process-fork/): 从 Electron 主进程启动具备 Node.js 环境的 Utility Process，并通过生命周期与消息通道管理本地服务。

### 技术/后端/Node.js

- [fsPromises.open() 与 FileHandle.read()：受控读取文件](/wiki/技术/后端/nodejs/fspromises-filehandle-read/): 用 Node.js 的异步文件句柄 API 在明确的大小上限与关闭边界内读取授权文件。

## 一级分类

- 技术
- 管理
- 产品
- 运营
- 测试
- 其他
