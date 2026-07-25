---
title: "tls.setDefaultCACertificates()：设置进程默认 CA"
description: "替换当前 Node 线程 TLS 客户端默认 CA 列表，常与系统证书合并使用。"
category: "技术/后端/Node.js/TLS"
api: "tls.setDefaultCACertificates"
tags: ["Node.js", "TLS", "证书", "CA"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`tls.setDefaultCACertificates(certs)` 设置当前 Node.js 线程上 TLS 客户端默认信任的 CA 证书列表。后续未自行指定 CA 的 TLS 连接会使用该列表；成功解析后也会成为 `tls.getCACertificates()` 的默认返回内容。

## 常用参数与返回

| API | 参数 | 返回 | 说明 |
| --- | --- | --- | --- |
| `tls.setDefaultCACertificates()` | `certs: string[] \| ArrayBufferView[]` | `void` | PEM 格式 CA 数组；设置前会去重。 |
| `tls.setDefaultCACertificates()` | — | 副作用范围 | 仅影响当前 Node.js 线程；不会改写已缓存 HTTPS Agent 会话。 |

## 会话提炼场景

Electron Utility Process（Sidecar）启动 OpenCode Server 前，会把 default CA 与 system CA 合并后再调用该 API。**推断**：主进程里设置的默认 CA 不会自动传到 utility process，因此必须在子进程入口再次配置，否则企业代理/系统钥匙串根证书可能导致出站 HTTPS 失败。

```ts
// sidecar 的入口文件中执行，而不是只在 Electron 主进程中设置。
const ca = [...new Set([...getCACertificates("default"), ...getCACertificates("system")])]
setDefaultCACertificates(ca)
```

## 常见应用场景

- 桌面或服务器进程需要信任系统安装的企业根证书。
- 在建立可缓存的 TLS 连接之前，统一进程默认信任链。
- 与 `tls.getCACertificates('default'|'system')` 组合实现“默认 + 系统”合并。

## 边界与注意事项

- 官方要求在产生不想要的可缓存 TLS 连接之前调用。
- 该调用**完全替换**默认列表；若要追加，必须先 `getCACertificates` 再拼接传入。
- Added in: v24.5.0 / v22.19.0；旧运行时可能没有该 API，应用层常包 `try/catch`（这是应用策略，不是 API 保证）。

## 关联 API

- [tls.getCACertificates()](/wiki/技术/后端/nodejs/tls/tlsgetcacertificates/)
- [utilityProcess.fork()](/wiki/技术/前端/electron/utility-process/utilityprocessfork/)

## 官方文档

- [Node.js tls.setDefaultCACertificates](https://nodejs.org/api/tls.html#tlssetdefaultcacertificatescerts)：已于 2026-07-25 查阅。
