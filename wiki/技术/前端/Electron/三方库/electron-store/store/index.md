---
title: "new Store()"
description: "创建 Electron 应用的小型 JSON KV 持久化实例，可指定文件名与 userData 目录。"
category: "技术/前端/Electron/三方库/electron-store"
api: "Store"
tags: ["Electron", "electron-store", "持久化"]
created: "2026-07-28"
updated: "2026-07-28"
---
## API 定位

`new Store(options?)` 是 [`electron-store`](https://github.com/sindresorhus/electron-store) 的构造入口。它在 Electron 主进程（也可经官方约定在 Renderer）创建基于 JSON 文件的小型 KV 持久化实例，默认落在 `app.getPath('userData')`。适合用户设置、窗口 ID、开关类小数据，不是数据库。

## 常用参数与返回

| 参数 | 返回 | 说明 |
| --- | --- | --- |
| `options?: Options` | `Store` 实例 | 创建新的存储实例；不传则使用默认文件名 `config` 与默认 `userData` 目录。 |
| `options.name?: string` | — | 存储文件名（不含扩展名），默认 `'config'`；多文件或可复用模块应使用自定义名。 |
| `options.cwd?: string` | — | 存储目录，默认 `app.getPath('userData')`；官方警告除非绝对必要否则不要改。相对路径相对于默认 cwd。 |
| `options.fileExtension?: string` | — | 文件扩展名，默认 `'json'`。 |
| `options.accessPropertiesByDotNotation?: boolean` | — | 是否用点号访问嵌套属性，默认 `true`；设为 `false` 时整段字符串作为单一 key。 |
| `options.defaults?: object` | — | 缺省值。 |
| `options.schema?: object` | — | JSON Schema（draft-2020-12）校验。 |
| — | `.get(key, defaultValue?)` | 读取；不存在时返回 `defaultValue`。 |
| — | `.set(key, value)` / `.set(object)` | 写入；值须可 JSON 序列化；崩溃时原子写盘，不损坏已有文件。 |
| — | `.delete(key)` / `.clear()` | 删除单项或清空（已知项可回落到 defaults/schema）。 |
| — | `.path` | 当前存储文件绝对路径。 |

## 会话提炼场景

桌面应用若在启动早期调用 `app.setPath('userData', ...)` 自定义数据目录，则不能在模块顶层立刻 `new Store()`：模块提升会在 `setPath` 之前执行，文件会写到 Electron 默认 `userData`。应延迟到 `setPath` 之后，并显式传入当前 `userData` 作为 `cwd`，再按名缓存实例。

```ts
import Store from "electron-store"
import { app } from "electron"

const cache = new Map<string, Store>()

export function getStore(name = "opencode.settings") {
  const cached = cache.get(name)
  if (cached) return cached

  const next = new Store({
    name,
    cwd: app.getPath("userData"),
    fileExtension: "",
    accessPropertiesByDotNotation: false,
  })
  cache.set(name, next)
  return next
}

// 须在 app.setPath("userData", ...) 之后调用
const settings = getStore()
settings.set("defaultServerUrl", "http://127.0.0.1:4096")
console.log(settings.get("defaultServerUrl"))
```

应用层策略（非库契约）：Main 直接读写；Renderer 经 `ipcMain.handle` 代理 `get/set/delete/clear`，避免在隔离 Renderer 中直接依赖 Node 文件系统。

## 常见应用场景

- 持久化用户偏好、功能开关、默认服务地址。
- 用不同 `name` 拆分设置文件与更新器状态等独立域。
- 关闭点号嵌套后，把带 `.` 的字符串当作完整 key。
- 与 IPC 组合：Main 持有 Store，Renderer 只通过 invoke 访问。

## 边界与注意事项

- 每次变更读写整份 JSON，仅适合小数据；大数据应改用 SQLite 等（官方 FAQ）。
- 官方建议尽量不要自定义 `cwd`；若应用已改写 `userData`，延迟初始化并显式 `cwd` 是应用层必要推断，不是库默认行为。
- 仅在 Renderer 使用且 Main 未创建实例时，需在 Main 调用 `Store.initRenderer()`。
- 加密选项只做混淆，不能当作安全存储方案。

## 官方文档

- [electron-store README](https://github.com/sindresorhus/electron-store/blob/main/readme.md)：verified 2026-07-28.
