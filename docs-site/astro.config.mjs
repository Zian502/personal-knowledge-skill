import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import { readFileSync } from "node:fs";
import { relative } from "node:path";
import { fileURLToPath } from "node:url";

const skillRoot = fileURLToPath(new URL("..", import.meta.url));
const wikiRoot = fileURLToPath(new URL("../wiki", import.meta.url));
const wikiIndex = fileURLToPath(new URL("../wiki/index.md", import.meta.url));
const site = process.env.GITHUB_ACTIONS === "true"
  ? "https://zian502.github.io"
  : undefined;

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
        group = { label, collapsed: true, items: [] };
        const existingLink = level.find((item) => item.label === label && item.link);
        if (existingLink) {
          group.items.push({ label: "总览", link: existingLink.link });
          level.splice(level.indexOf(existingLink), 1, group);
        } else {
          level.push(group);
        }
      }
      level = group.items;
    }
    const existingGroup = level.find(
      (item) => item.label === articleMatch[1] && item.items,
    );
    if (existingGroup) {
      existingGroup.items.unshift({ label: "总览", link: articleMatch[2] });
    } else {
      level.push({ label: articleMatch[1], link: articleMatch[2] });
    }
  }
  const placeEcosystemLibrariesLast = (items) => {
    items.sort((left, right) => {
      const leftIsEcosystemLibraries = left.label === "三方库";
      const rightIsEcosystemLibraries = right.label === "三方库";
      if (leftIsEcosystemLibraries === rightIsEcosystemLibraries) return 0;
      return leftIsEcosystemLibraries ? 1 : -1;
    });
    for (const item of items) {
      if (item.items) placeEcosystemLibrariesLast(item.items);
    }
  };
  placeEcosystemLibrariesLast(root);
  return root;
}

function refreshWikiWhenSourceChanges() {
  return {
    name: "pks-refresh-local-wiki",
    configureServer(server) {
      server.watcher.add(wikiRoot);

      let restartTimer;
      const isWikiSource = (file) => {
        const path = relative(wikiRoot, file);
        return path && !path.startsWith("..") && !path.includes("../");
      };
      const scheduleRestart = (file) => {
        if (!isWikiSource(file)) return;
        clearTimeout(restartTimer);
        restartTimer = setTimeout(() => server.restart(), 120);
      };

      server.watcher.on("add", scheduleRestart);
      server.watcher.on("change", scheduleRestart);
      server.watcher.on("unlink", scheduleRestart);
      server.watcher.on("addDir", scheduleRestart);
      server.watcher.on("unlinkDir", scheduleRestart);

      return () => {
        clearTimeout(restartTimer);
      };
    },
  };
}

export default defineConfig({
  site,
  vite: {
    plugins: [refreshWikiWhenSourceChanges()],
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
          collapsed: true,
          items: [{ label: "总览", link: "/wiki/" }, ...wikiNavigationFromIndex()],
        },
      ],
    }),
  ],
});
