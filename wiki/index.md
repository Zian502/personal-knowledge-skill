---
title: Wiki
description: 按领域分类的个人知识文章。
sidebar:
  order: 0
---

这里收录从 LLM 会话中提炼出的可复用知识。每篇文章都包含独立的背景、结论、步骤与边界；可从下方索引或顶部搜索进入。

## 知识索引

### 技术/前端/Electron

- [Electron 附件选择：Token 授权与字节预算](/wiki/技术/前端/electron/electron-attachment-token-budget/): 主进程对话框选文件后签发 token，渲染进程仅能读取本次授权路径，并受总附件字节上限约束。
- [用 Effect Deferred 协调 Electron 主进程启动](/wiki/技术/前端/electron/electron-main-effect-deferred/): 用 Effect 编排启动流，用 Deferred 作为 sidecar 凭证就绪闸门，用 Fiber 等待后台 loading 任务。
- [Electron 多窗口：Registry 与 window-state](/wiki/技术/前端/electron/electron-window-registry-vs-state/): Window Registry 持久化窗口 ID 列表，electron-window-state 持久化单窗几何，二者用同一 id 协作且关闭策略不同。
- [OpenCode Desktop Sidecar 架构](/wiki/技术/前端/electron/opencode-desktop-sidecar/): 用 Utility Process 跑与 CLI 同一套 OpenCode Server，实现桌面壳与后端隔离、本机鉴权与自定义协议 CORS。

## 一级分类

- 技术
- 管理
- 产品
- 运营
- 测试
- 其他
