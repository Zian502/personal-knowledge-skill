---
title: Wiki
description: 按领域分类的个人知识文章。
sidebar:
  order: 0
---

这里收录从 LLM 会话中提炼出的可复用知识。每篇文章都包含独立的背景、结论、步骤与边界；可从下方索引或顶部搜索进入。

## 知识索引

### 技术/前端/Effect/Deferred

- [Deferred.make()：创建一次性就绪信号](/wiki/技术/前端/effect/deferred/deferredmake/): 用 Effect Deferred 创建只能完成一次的异步结果，以便等待方共享同一个就绪信号。

### 技术/前端/Effect/Fiber

- [Effect.fork()：启动后台 Fiber](/wiki/技术/前端/effect/fiber/effectfork/): 将 Effect 作为 Fiber 在后台启动，并保留后续等待、取消和观测的能力。

### 技术/前端/Electron/IPC

- [ipcMain.handle()：实现请求—响应式 IPC](/wiki/技术/前端/electron/ipc/ipcmainhandle/): 为 ipcRenderer.invoke() 注册异步处理器，并以 channel、调用来源和返回值建立受控主进程能力。

### 技术/前端/Electron/Utility Process

- [utilityProcess.fork()：隔离桌面端 Sidecar](/wiki/技术/前端/electron/utilityprocess/utilityprocessfork/): 从 Electron 主进程启动具备 Node.js 环境的 Utility Process，并通过生命周期与消息通道管理本地服务。

### 技术/前端/Electron/对话框

- [dialog.showOpenDialog()：选择本地文件](/wiki/技术/前端/electron/对话框/dialogshowopendialog/): 在 Electron 主进程调用原生打开对话框，并以取消状态和文件路径列表处理结果。

### 技术/前端/Electron/窗口

- [new BrowserWindow()：创建并显示主窗口](/wiki/技术/前端/electron/窗口/browserwindow/): 使用 BrowserWindow 构造选项、webPreferences 与 ready-to-show 事件建立安全且避免闪烁的窗口生命周期。

### 技术/后端/Node.js/文件系统

- [fsPromises.open()：创建受控文件句柄](/wiki/技术/后端/nodejs/文件系统/fspromisesopen/): 用 Node.js 的异步文件系统 API 创建受控 FileHandle，作为后续授权文件读取的起点。

## 一级分类

- 技术
- 管理
- 产品
- 运营
- 测试
- 其他
