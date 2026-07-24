import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

export default defineConfig({
  integrations: [
    starlight({
      title: "个人知识库",
      description: "从 LLM 会话沉淀的本地分类 Wiki",
      defaultLocale: "zh-cn",
      locales: {
        "zh-cn": {
          label: "简体中文",
          lang: "zh-CN",
        },
      },
      social: [],
      customCss: ["./src/styles/custom.css"],
      sidebar: [
        { label: "首页", link: "/" },
        {
          label: "Wiki",
          items: [{ autogenerate: { directory: "wiki" } }],
        },
      ],
    }),
  ],
});
