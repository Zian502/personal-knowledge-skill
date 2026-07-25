import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const skillRoot = fileURLToPath(new URL("..", import.meta.url));
const wikiIndex = fileURLToPath(new URL("../wiki/index.md", import.meta.url));

function wikiNavigationFromIndex() {
  const root = [];
  let category = [];
  for (const line of readFileSync(wikiIndex, "utf8").split("\n")) {
    const categoryMatch = line.match(/^###\s+(.+)$/);
    if (categoryMatch) {
      category = categoryMatch[1].split("/").map((part) => part.trim()).filter(Boolean);
      continue;
    }
    const articleMatch = line.match(/^- \[(.+)]\((\/wiki\/[^)]+)\):/);
    if (!articleMatch || !category.length) continue;

    let level = root;
    for (const label of category) {
      let group = level.find((item) => item.label === label && item.items);
      if (!group) {
        group = { label, items: [] };
        level.push(group);
      }
      level = group.items;
    }
    level.push({ label: articleMatch[1], link: articleMatch[2] });
  }
  return root;
}

function refreshSidebarWhenIndexChanges() {
  return {
    name: "pks-refresh-sidebar-from-wiki-index",
    configureServer(server) {
      server.watcher.add(wikiIndex);
      server.watcher.on("change", async (file) => {
        if (file === wikiIndex) await server.restart();
      });
    },
  };
}

export default defineConfig({
  vite: {
    plugins: [refreshSidebarWhenIndexChanges()],
    server: {
      fs: { allow: [skillRoot] },
    },
  },
  integrations: [
    starlight({
      title: "个人知识库",
      description: "从 LLM 会话沉淀的本地分类 Wiki",
      defaultLocale: "root",
      locales: {
        root: {
          label: "简体中文",
          lang: "zh-CN",
        },
      },
      social: [],
      customCss: ["@fontsource-variable/geist", "./src/styles/custom.css"],
      components: {
        Header: "./src/components/Header.astro",
        PageTitle: "./src/components/PageTitle.astro",
      },
      sidebar: [
        { label: "首页", link: "/" },
        {
          label: "Wiki",
          items: [{ label: "总览", link: "/wiki/" }, ...wikiNavigationFromIndex()],
        },
      ],
    }),
  ],
});
