---
title: Wiki
description: 按领域分类的个人知识文章。
tags: ["知识库", "索引"]
sidebar:
  order: 0
---

这里收录从 LLM 会话中提炼出的可复用知识。每篇文章都包含独立的背景、结论、步骤与边界；可从下方索引或顶部搜索进入。

## 知识索引

<div class="pks-knowledge-index-marker" aria-hidden="true"></div>

| 创建时间 | 知识 | 分类 | 摘要 |
| --- | --- | --- | --- |
| 2026-08-07 | [child_process.spawn()](/wiki/技术/后端/nodejs/子进程/child_processspawn/) | 技术/后端/Node.js/子进程 | 异步创建子进程并建立 stdio 管道，适合从 Electron 主进程启动 wsl 等外部命令。 |
| 2026-08-07 | [server.listen()](/wiki/技术/后端/nodejs/网络/serverlisten/) | 技术/后端/Node.js/网络 | 让 net.Server 监听 TCP；port 为 0 时由操作系统分配临时端口。 |
| 2026-08-07 | [wsl --distribution](/wiki/技术/前端/electron/wsl/wsl--distribution/) | 技术/前端/Electron/WSL | 在指定 WSL Linux 发行版中运行命令，供 Windows 主机自动化启动 Linux 侧服务。 |
| 2026-07-28 | [crashReporter.start()](/wiki/技术/前端/electron/崩溃报告/crashreporterstart/) | 技术/前端/Electron/崩溃报告 | 启动 Crashpad 收集崩溃；可仅本地落盘或上传到远程服务器。 |
| 2026-07-28 | [log.initialize()](/wiki/技术/前端/electron/三方库/electron-log/loginitialize/) | 技术/前端/Electron/三方库/electron-log | 在 Electron 主进程初始化 electron-log，打通 Renderer 日志通道并配置文件输出。 |
| 2026-07-28 | [netLog.startLogging()](/wiki/技术/前端/electron/网络日志/netlogstartlogging/) | 技术/前端/Electron/网络日志 | 在 app ready 后将网络事件写入文件，供排查与调试导出。 |
| 2026-07-28 | [new Store()](/wiki/技术/前端/electron/三方库/electron-store/store/) | 技术/前端/Electron/三方库/electron-store | 创建 Electron 应用的小型 JSON KV 持久化实例，可指定文件名与 userData 目录。 |
| 2026-07-27 | [windowStateKeeper()](/wiki/技术/前端/electron/三方库/electron-window-state/windowstatekeeper/) | 技术/前端/Electron/三方库/electron-window-state | 读取、恢复并持续保存 Electron BrowserWindow 的尺寸、位置与窗口模式。 |
| 2026-07-25 | [clipboard.readImage()](/wiki/技术/前端/electron/剪贴板/clipboardreadimage/) | 技术/前端/Electron/剪贴板 | 从系统剪贴板读取 NativeImage，供主进程转发给渲染进程作附件。 |
| 2026-07-25 | [contextBridge.exposeInMainWorld()](/wiki/技术/前端/electron/context-bridge/contextbridgeexposeinmainworld/) | 技术/前端/Electron/Context Bridge | 在 context isolation 下从 preload 向 Renderer 暴露可审计、最小化的原生能力。 |
| 2026-07-25 | [Deferred.await()](/wiki/技术/前端/electron/三方库/effect/deferred/deferredawait/) | 技术/前端/Electron/三方库/Effect/Deferred | 挂起直到 Deferred 完成，多个等待方可共享同一就绪信号。 |
| 2026-07-25 | [Deferred.make()](/wiki/技术/前端/electron/三方库/effect/deferred/deferredmake/) | 技术/前端/Electron/三方库/Effect/Deferred | 用 Effect Deferred 创建只能完成一次的异步结果，以便等待方共享同一个就绪信号。 |
| 2026-07-25 | [Deferred.succeed()](/wiki/技术/前端/electron/三方库/effect/deferred/deferredsucceed/) | 技术/前端/Electron/三方库/Effect/Deferred | 以成功值完成 Deferred 并唤醒等待方，返回是否首次完成。 |
| 2026-07-25 | [dialog.showOpenDialog()](/wiki/技术/前端/electron/对话框/dialogshowopendialog/) | 技术/前端/Electron/对话框 | 在 Electron 主进程调用原生打开对话框，并以取消状态和文件路径列表处理结果。 |
| 2026-07-25 | [Effect.fork()](/wiki/技术/前端/electron/三方库/effect/fiber/effectfork/) | 技术/前端/Electron/三方库/Effect/Fiber | 将 Effect 作为 Fiber 在后台启动，并保留后续等待、取消和观测的能力。 |
| 2026-07-25 | [Fiber.await()](/wiki/技术/前端/electron/三方库/effect/fiber/fiberawait/) | 技术/前端/Electron/三方库/Effect/Fiber | 挂起直到目标 Fiber 结束，返回 Exit 而不自动传播失败。 |
| 2026-07-25 | [FileHandle.read()](/wiki/技术/后端/nodejs/文件系统/filehandleread/) | 技术/后端/Node.js/文件系统 | 从 FileHandle 读取数据到 buffer，并返回 bytesRead，适合受控分段读附件。 |
| 2026-07-25 | [fsPromises.open()](/wiki/技术/后端/nodejs/文件系统/fspromisesopen/) | 技术/后端/Node.js/文件系统 | 用 Node.js 的异步文件系统 API 创建受控 FileHandle，作为后续授权文件读取的起点。 |
| 2026-07-25 | [ipcMain.handle()](/wiki/技术/前端/electron/ipc/ipcmainhandle/) | 技术/前端/Electron/IPC | 为 ipcRenderer.invoke() 注册异步处理器，并以 channel、调用来源和返回值建立受控主进程能力。 |
| 2026-07-25 | [new BrowserWindow()](/wiki/技术/前端/electron/窗口/browserwindow/) | 技术/前端/Electron/窗口 | 使用 BrowserWindow 构造选项、webPreferences 与 ready-to-show 事件建立安全且避免闪烁的窗口生命周期。 |
| 2026-07-25 | [Notification](/wiki/技术/前端/electron/通知/notification/) | 技术/前端/Electron/通知 | 主进程创建 OS 通知对象，调用 show() 后展示；适合经 IPC 转发的桌面提示。 |
| 2026-07-25 | [shell.openExternal()](/wiki/技术/前端/electron/shell/shellopenexternal/) | 技术/前端/Electron/Shell | 在主进程打开外部协议 URL，例如默认浏览器中的 https 链接。 |
| 2026-07-25 | [tls.getCACertificates()](/wiki/技术/后端/nodejs/tls/tlsgetcacertificates/) | 技术/后端/Node.js/TLS | 按 default/system/bundled/extra 返回 PEM CA 数组，用于检查或组装信任链。 |
| 2026-07-25 | [tls.setDefaultCACertificates()](/wiki/技术/后端/nodejs/tls/tlssetdefaultcacertificates/) | 技术/后端/Node.js/TLS | 替换当前 Node 线程 TLS 客户端默认 CA 列表，常与系统证书合并使用。 |
| 2026-07-25 | [url.fileURLToPath()](/wiki/技术/后端/nodejs/url/urlfileurltopath/) | 技术/后端/Node.js/URL | 把 import.meta.url 等 file: URL 转为跨平台绝对路径，用于定位旁路脚本。 |
| 2026-07-25 | [utilityProcess.fork()](/wiki/技术/前端/electron/utility-process/utilityprocessfork/) | 技术/前端/Electron/Utility Process | 从 Electron 主进程启动具备 Node.js 环境的 Utility Process，并通过生命周期与消息通道管理本地服务。 |
| 2026-07-25 | [三方库](/wiki/技术/前端/electron/三方库/) | 技术/前端/Electron | 基于当前会话缓存整理与 Electron 生态关联的三方库。 |
| 2026-07-25 | [三方库](/wiki/技术/后端/nodejs/三方库/) | 技术/后端/Node.js | 基于当前会话缓存整理与 Node.js 生态关联的三方库状态。 |

<script type="application/json" id="pks-sidebar-source" data-pagefind-ignore>
[
  {
    "category": "技术/前端/Electron/Context Bridge",
    "title": "contextBridge.exposeInMainWorld()",
    "link": "/wiki/技术/前端/electron/context-bridge/contextbridgeexposeinmainworld/"
  },
  {
    "category": "技术/前端/Electron/IPC",
    "title": "ipcMain.handle()",
    "link": "/wiki/技术/前端/electron/ipc/ipcmainhandle/"
  },
  {
    "category": "技术/前端/Electron/Shell",
    "title": "shell.openExternal()",
    "link": "/wiki/技术/前端/electron/shell/shellopenexternal/"
  },
  {
    "category": "技术/前端/Electron/Utility Process",
    "title": "utilityProcess.fork()",
    "link": "/wiki/技术/前端/electron/utility-process/utilityprocessfork/"
  },
  {
    "category": "技术/前端/Electron/WSL",
    "title": "wsl --distribution",
    "link": "/wiki/技术/前端/electron/wsl/wsl--distribution/"
  },
  {
    "category": "技术/前端/Electron/三方库/Effect/Deferred",
    "title": "Deferred.await()",
    "link": "/wiki/技术/前端/electron/三方库/effect/deferred/deferredawait/"
  },
  {
    "category": "技术/前端/Electron/三方库/Effect/Deferred",
    "title": "Deferred.make()",
    "link": "/wiki/技术/前端/electron/三方库/effect/deferred/deferredmake/"
  },
  {
    "category": "技术/前端/Electron/三方库/Effect/Deferred",
    "title": "Deferred.succeed()",
    "link": "/wiki/技术/前端/electron/三方库/effect/deferred/deferredsucceed/"
  },
  {
    "category": "技术/前端/Electron/三方库/Effect/Fiber",
    "title": "Effect.fork()",
    "link": "/wiki/技术/前端/electron/三方库/effect/fiber/effectfork/"
  },
  {
    "category": "技术/前端/Electron/三方库/Effect/Fiber",
    "title": "Fiber.await()",
    "link": "/wiki/技术/前端/electron/三方库/effect/fiber/fiberawait/"
  },
  {
    "category": "技术/前端/Electron/三方库/electron-log",
    "title": "log.initialize()",
    "link": "/wiki/技术/前端/electron/三方库/electron-log/loginitialize/"
  },
  {
    "category": "技术/前端/Electron/三方库/electron-store",
    "title": "new Store()",
    "link": "/wiki/技术/前端/electron/三方库/electron-store/store/"
  },
  {
    "category": "技术/前端/Electron/三方库/electron-window-state",
    "title": "windowStateKeeper()",
    "link": "/wiki/技术/前端/electron/三方库/electron-window-state/windowstatekeeper/"
  },
  {
    "category": "技术/前端/Electron/剪贴板",
    "title": "clipboard.readImage()",
    "link": "/wiki/技术/前端/electron/剪贴板/clipboardreadimage/"
  },
  {
    "category": "技术/前端/Electron/对话框",
    "title": "dialog.showOpenDialog()",
    "link": "/wiki/技术/前端/electron/对话框/dialogshowopendialog/"
  },
  {
    "category": "技术/前端/Electron/崩溃报告",
    "title": "crashReporter.start()",
    "link": "/wiki/技术/前端/electron/崩溃报告/crashreporterstart/"
  },
  {
    "category": "技术/前端/Electron/窗口",
    "title": "new BrowserWindow()",
    "link": "/wiki/技术/前端/electron/窗口/browserwindow/"
  },
  {
    "category": "技术/前端/Electron/网络日志",
    "title": "netLog.startLogging()",
    "link": "/wiki/技术/前端/electron/网络日志/netlogstartlogging/"
  },
  {
    "category": "技术/前端/Electron/通知",
    "title": "Notification",
    "link": "/wiki/技术/前端/electron/通知/notification/"
  },
  {
    "category": "技术/前端/Electron",
    "title": "三方库",
    "link": "/wiki/技术/前端/electron/三方库/"
  },
  {
    "category": "技术/后端/Node.js/TLS",
    "title": "tls.getCACertificates()",
    "link": "/wiki/技术/后端/nodejs/tls/tlsgetcacertificates/"
  },
  {
    "category": "技术/后端/Node.js/TLS",
    "title": "tls.setDefaultCACertificates()",
    "link": "/wiki/技术/后端/nodejs/tls/tlssetdefaultcacertificates/"
  },
  {
    "category": "技术/后端/Node.js/URL",
    "title": "url.fileURLToPath()",
    "link": "/wiki/技术/后端/nodejs/url/urlfileurltopath/"
  },
  {
    "category": "技术/后端/Node.js/子进程",
    "title": "child_process.spawn()",
    "link": "/wiki/技术/后端/nodejs/子进程/child_processspawn/"
  },
  {
    "category": "技术/后端/Node.js/文件系统",
    "title": "FileHandle.read()",
    "link": "/wiki/技术/后端/nodejs/文件系统/filehandleread/"
  },
  {
    "category": "技术/后端/Node.js/文件系统",
    "title": "fsPromises.open()",
    "link": "/wiki/技术/后端/nodejs/文件系统/fspromisesopen/"
  },
  {
    "category": "技术/后端/Node.js/网络",
    "title": "server.listen()",
    "link": "/wiki/技术/后端/nodejs/网络/serverlisten/"
  },
  {
    "category": "技术/后端/Node.js",
    "title": "三方库",
    "link": "/wiki/技术/后端/nodejs/三方库/"
  }
]
</script>