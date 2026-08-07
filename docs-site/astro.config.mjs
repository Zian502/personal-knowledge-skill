import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import { watch } from "chokidar";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const skillRoot = fileURLToPath(new URL("..", import.meta.url));
const wikiRoot = fileURLToPath(new URL("../wiki", import.meta.url));
const wikiIndex = fileURLToPath(new URL("../wiki/index.md", import.meta.url));
const site = process.env.GITHUB_ACTIONS === "true"
  ? "https://zian502.github.io"
  : undefined;
const wikiWatcherKey = Symbol.for("personal-knowledge-skill.wiki-watcher");

function wikiNavigationFromIndex() {
  const source = readFileSync(wikiIndex, "utf8");
  const dataMatch = source.match(
    /<script type="application\/json" id="pks-sidebar-source"[^>]*>\s*([\s\S]*?)\s*<\/script>/,
  );
  if (!dataMatch) {
    throw new Error("Wiki index is missing the generated pks-sidebar-source data block");
  }
  const entries = JSON.parse(dataMatch[1]);
  const root = [];
  for (const entry of entries) {
    const category = entry.category
      .split("/")
      .map((part) => part.trim())
      .filter(Boolean);
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
      (item) => item.label === entry.title && item.items,
    );
    if (existingGroup) {
      existingGroup.items.unshift({ label: "总览", link: entry.link });
    } else {
      level.push({ label: entry.title, link: entry.link });
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
      const previousWatcher = globalThis[wikiWatcherKey];
      if (previousWatcher) void previousWatcher.close();

      const wikiWatcher = watch(wikiRoot, {
        ignoreInitial: true,
        awaitWriteFinish: {
          stabilityThreshold: 100,
          pollInterval: 20,
        },
      });
      globalThis[wikiWatcherKey] = wikiWatcher;

      let restartTimer;
      const scheduleRestart = (event, file) => {
        clearTimeout(restartTimer);
        restartTimer = setTimeout(async () => {
          server.config.logger.info(
            `[pks] Wiki ${event}: ${file}. Restarting local docs...`,
          );
          try {
            await server.restart();
          } catch (error) {
            server.config.logger.error(
              `[pks] Failed to restart after Wiki update: ${error}`,
            );
          }
        }, 150);
      };

      wikiWatcher.on("all", scheduleRestart);
      const closeWatcher = () => {
        clearTimeout(restartTimer);
        void wikiWatcher.close();
        if (globalThis[wikiWatcherKey] === wikiWatcher) {
          delete globalThis[wikiWatcherKey];
        }
      };
      server.httpServer?.once("close", closeWatcher);
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
