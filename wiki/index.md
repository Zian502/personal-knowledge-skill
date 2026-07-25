---
title: Wiki
description: 按领域分类的个人知识文章。
sidebar:
  order: 0
---

这里收录从 LLM 会话中提炼出的可复用知识。每篇文章都包含独立的背景、结论、步骤与边界；可从下方索引或顶部搜索进入。

## 知识索引

### 技术/前端/Electron/Context Bridge

- [contextBridge.exposeInMainWorld()：构建受限 Renderer API](/wiki/技术/前端/electron/context-bridge/contextbridgeexposeinmainworld/): 在 context isolation 下从 preload 向 Renderer 暴露可审计、最小化的原生能力。

### 技术/前端/Electron/IPC

- [ipcMain.handle()：实现请求—响应式 IPC](/wiki/技术/前端/electron/ipc/ipcmainhandle/): 为 ipcRenderer.invoke() 注册异步处理器，并以 channel、调用来源和返回值建立受控主进程能力。

### 技术/前端/Electron/Shell

- [shell.openExternal()：用系统默认方式打开外部 URL](/wiki/技术/前端/electron/shell/shellopenexternal/): 在主进程打开外部协议 URL，例如默认浏览器中的 https 链接。

### 技术/前端/Electron/Utility Process

- [utilityProcess.fork()：隔离桌面端 Sidecar](/wiki/技术/前端/electron/utility-process/utilityprocessfork/): 从 Electron 主进程启动具备 Node.js 环境的 Utility Process，并通过生命周期与消息通道管理本地服务。

### 技术/前端/Electron/三方库/Effect/Deferred

- [Deferred.await()：等待一次性结果](/wiki/技术/前端/electron/三方库/effect/deferred/deferredawait/): 挂起直到 Deferred 完成，多个等待方可共享同一就绪信号。
- [Deferred.make()：创建一次性就绪信号](/wiki/技术/前端/electron/三方库/effect/deferred/deferredmake/): 用 Effect Deferred 创建只能完成一次的异步结果，以便等待方共享同一个就绪信号。
- [Deferred.succeed()：成功完成 Deferred](/wiki/技术/前端/electron/三方库/effect/deferred/deferredsucceed/): 以成功值完成 Deferred 并唤醒等待方，返回是否首次完成。

### 技术/前端/Electron/三方库/Effect/Fiber

- [Effect.fork()：启动后台 Fiber](/wiki/技术/前端/electron/三方库/effect/fiber/effectfork/): 将 Effect 作为 Fiber 在后台启动，并保留后续等待、取消和观测的能力。
- [Fiber.await()：等待 Fiber 并取得 Exit](/wiki/技术/前端/electron/三方库/effect/fiber/fiberawait/): 挂起直到目标 Fiber 结束，返回 Exit 而不自动传播失败。

### 技术/前端/Electron/剪贴板

- [clipboard.readImage()：读取剪贴板图像](/wiki/技术/前端/electron/剪贴板/clipboardreadimage/): 从系统剪贴板读取 NativeImage，供主进程转发给渲染进程作附件。

### 技术/前端/Electron/对话框

- [dialog.showOpenDialog()：选择本地文件](/wiki/技术/前端/electron/对话框/dialogshowopendialog/): 在 Electron 主进程调用原生打开对话框，并以取消状态和文件路径列表处理结果。

### 技术/前端/Electron/窗口

- [new BrowserWindow()：创建并显示主窗口](/wiki/技术/前端/electron/窗口/browserwindow/): 使用 BrowserWindow 构造选项、webPreferences 与 ready-to-show 事件建立安全且避免闪烁的窗口生命周期。

### 技术/前端/Electron/通知

- [Notification：创建并展示系统通知](/wiki/技术/前端/electron/通知/notification/): 主进程创建 OS 通知对象，调用 show() 后展示；适合经 IPC 转发的桌面提示。

### 技术/前端/Electron

- [三方库](/wiki/技术/前端/electron/三方库/): 基于当前会话缓存整理与 Electron 生态关联的三方库。

### 技术/后端/Node.js/TLS

- [tls.getCACertificates()：读取 CA 证书来源](/wiki/技术/后端/nodejs/tls/tlsgetcacertificates/): 按 default/system/bundled/extra 返回 PEM CA 数组，用于检查或组装信任链。
- [tls.setDefaultCACertificates()：设置进程默认 CA](/wiki/技术/后端/nodejs/tls/tlssetdefaultcacertificates/): 替换当前 Node 线程 TLS 客户端默认 CA 列表，常与系统证书合并使用。

### 技术/后端/Node.js/URL

- [url.fileURLToPath()：将 file URL 转为绝对路径](/wiki/技术/后端/nodejs/url/urlfileurltopath/): 把 import.meta.url 等 file: URL 转为跨平台绝对路径，用于定位旁路脚本。

### 技术/后端/Node.js/文件系统

- [FileHandle.read()：向缓冲区读取文件字节](/wiki/技术/后端/nodejs/文件系统/filehandleread/): 从 FileHandle 读取数据到 buffer，并返回 bytesRead，适合受控分段读附件。
- [fsPromises.open()：创建受控文件句柄](/wiki/技术/后端/nodejs/文件系统/fspromisesopen/): 用 Node.js 的异步文件系统 API 创建受控 FileHandle，作为后续授权文件读取的起点。

### 技术/后端/Node.js

- [三方库](/wiki/技术/后端/nodejs/三方库/): 基于当前会话缓存整理与 Node.js 生态关联的三方库状态。
