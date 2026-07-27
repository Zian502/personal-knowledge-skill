---
title: "tls.getCACertificates()：读取 CA 证书来源"
description: "按 default/system/bundled/extra 返回 PEM CA 数组，用于检查或组装信任链。"
category: "技术/后端/Node.js/TLS"
api: "tls.getCACertificates"
tags: ["Node.js", "TLS", "证书", "CA"]
created: "2026-07-25"
updated: "2026-07-25"
---
## API 定位

`tls.getCACertificates([type])` 按来源类型返回 PEM 编码 CA 证书数组，用于检查或组装当前运行时可信任的根证书集合。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `type?: "default" \| "system" \| "bundled" \| "extra"` | `string[]` | 默认 `"default"`，返回 PEM 编码证书。 |
| `type: "default"` | `string[]` | 当前 TLS 客户端默认会使用的 CA（可能含 bundled / system / `NODE_EXTRA_CA_CERTS`，取决于启动选项）。 |
| `type: "system"` | `string[]` | 操作系统信任库中的证书。 |
| `type: "bundled"` / `"extra"` | `string[]` | Mozilla 捆绑包，或 `NODE_EXTRA_CA_CERTS` 额外文件；未设置 extra 时为空数组。 |

## 会话提炼场景

Sidecar 通过 `getCACertificates("default")` 与 `getCACertificates("system")` 取证书，去重后交给 `setDefaultCACertificates`，以覆盖企业 MITM/自签根证书场景。

```ts
const certificates = [...new Set([
  ...tls.getCACertificates("default"),
  ...tls.getCACertificates("system"),
])]
tls.setDefaultCACertificates(certificates)
```

## 常见应用场景

- 诊断当前进程实际信任哪些 CA。
- 在替换默认列表前读取现有证书并追加自定义 PEM。
- 明确区分 bundled 与 system 来源，避免误以为 Node 默认等于系统钥匙串。

## 边界与注意事项

- Added in: v23.10.0 / v22.15.0。
- `"default"` 的具体组成依赖 `--use-bundled-ca` / `--use-system-ca` / `NODE_EXTRA_CA_CERTS`。
- 返回值可能重复；若再写入 `setDefaultCACertificates`，后者会去重。

## 关联 API

- [tls.setDefaultCACertificates()](/wiki/技术/后端/nodejs/tls/tlssetdefaultcacertificates/)

## 官方文档

- [Node.js tls.getCACertificates](https://nodejs.org/api/tls.html#tlsgetcacertificatestype)：已于 2026-07-25 查阅。
