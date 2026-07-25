import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const skillRoot = fileURLToPath(new URL("..", import.meta.url));
const wikiRoot = join(skillRoot, "wiki");

function titleFromMarkdown(path) {
  const source = readFileSync(path, "utf8").slice(0, 2048);
  const match = source.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  return match ? match[1] : path.replace(/\.md$/, "");
}

function apiFromMarkdown(path) {
  const source = readFileSync(path, "utf8").slice(0, 2048);
  const match = source.match(/^api:\s*["']?(.+?)["']?\s*$/m);
  return match ? match[1] : titleFromMarkdown(path);
}

function wikiRoute(parts) {
  const sourceParts = parts
    .map((part) => part.replace(/\.md$/, "").toLowerCase().replace(/[^\w\u4e00-\u9fff-]/g, ""))
    .filter((part, index, all) => !(index === all.length - 1 && part === "index"));
  const route = sourceParts.join("/");
  return `/wiki/${route}/`;
}

function wikiNavigation(directory = wikiRoot, parts = []) {
  const entries = readdirSync(directory, { withFileTypes: true })
    .filter((entry) => entry.name !== "index.md" && entry.name !== "llms.txt")
    .sort((left, right) => left.name.localeCompare(right.name, "zh-CN"));

  const directories = entries.filter((entry) => entry.isDirectory());
  const articles = entries.filter((entry) => entry.isFile() && entry.name.endsWith(".md"));

  return [
    ...directories.map((entry) => {
      const childDirectory = join(directory, entry.name);
      const articlePath = join(childDirectory, "index.md");
      if (existsSync(articlePath)) {
        return {
          label: apiFromMarkdown(articlePath),
          link: wikiRoute([...parts, entry.name, "index.md"]),
        };
      }
      return {
        label: entry.name,
        items: wikiNavigation(childDirectory, [...parts, entry.name]),
      };
    }),
    ...articles.map((entry) => ({
      label: titleFromMarkdown(join(directory, entry.name)),
      link: wikiRoute([...parts, entry.name]),
    })),
  ];
}

export default defineConfig({
  vite: {
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
          items: [{ label: "总览", link: "/wiki/" }, ...wikiNavigation()],
        },
      ],
    }),
  ],
});
