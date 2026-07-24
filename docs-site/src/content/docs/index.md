---
title: 个人知识库
description: 从对话中提炼、分类并长期保存的本地 Wiki。
template: splash
hero:
  title: 个人知识库
  tagline: 把一次对话，变成以后还能找到、看懂和复用的知识。
  actions:
    - text: 浏览 Wiki
      link: /wiki/
      icon: right-arrow
      variant: primary
---

import { Card, CardGrid } from '@astrojs/starlight/components';

<CardGrid>
  <Card title="技术" icon="seti:config">
    前端、后端、架构、DevOps、AI、数据与安全。
  </Card>
  <Card title="管理" icon="seti:info">
    项目、团队、流程、协作与研发效能。
  </Card>
  <Card title="产品" icon="seti:map">
    需求、设计、路线图、研究与产品数据。
  </Card>
  <Card title="运营" icon="seti:document">
    内容、用户、活动、增长与商业化。
  </Card>
  <Card title="测试" icon="seti:check">
    测试策略、自动化、性能与质量保障。
  </Card>
</CardGrid>

## 如何录入

在包含目标内容的 Codex 会话中输入：

```text
$personal-knowledge-skill 录入当前会话
```

Skill 会提炼可复用知识、匹配分类，并把 Markdown 文章写入本站内容目录。

也可以在支持把普通 `/` 文本传给 Agent 的环境中使用简写：

```text
/pks 录入当前会话
```
