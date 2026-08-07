#!/usr/bin/env python3
"""Deterministic storage and validation for the personal knowledge Wiki."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import unicodedata
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
WIKI_ROOT = SKILL_ROOT / "wiki"
ALLOWED_ROOTS = {"技术", "管理", "产品", "运营", "其他"}
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def fail(message: str) -> "NoReturn":
    print(f"错误：{message}", file=sys.stderr)
    raise SystemExit(2)


def quote_yaml(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def normalize_category(raw: str) -> list[str]:
    parts = [part.strip() for part in re.split(r"[/／>＞]+", raw) if part.strip()]
    if not 2 <= len(parts) <= 6:
        fail("分类必须包含 2–6 层，例如：技术/前端/Electron/三方库/Effect/Deferred")
    if parts[0] not in ALLOWED_ROOTS:
        fail(f"一级分类必须是：{', '.join(sorted(ALLOWED_ROOTS))}")
    for part in parts:
        if part in {".", ".."} or "/" in part or "\\" in part:
            fail(f"非法分类名称：{part}")
    return parts


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).strip().lower()
    value = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", value, flags=re.UNICODE)
    value = re.sub(r"[-_.]{2,}", "-", value).strip("-_.")
    if not value or value in {".", ".."}:
        fail("无法生成有效文件名，请使用 --slug 指定")
    return value


def api_directory(value: str) -> str:
    """Create a stable, filesystem-safe directory for an API name."""
    value = unicodedata.normalize("NFKC", value).strip().lower()
    if not re.fullmatch(r"[A-Za-z0-9_$.-]+", value) or value in {".", ".."}:
        fail("API 名称只能包含字母、数字、_、$、. 或 -")
    return value


def has_api_title_suffix(value: str) -> bool:
    """Reject explanatory subtitles while allowing namespace colons such as node:fs."""
    return "：" in value or bool(re.search(r":\s+", value))


def parse_tags(raw: str) -> list[str]:
    seen: set[str] = set()
    tags: list[str] = []
    for item in re.split(r"[,，]", raw):
        tag = item.strip()
        if tag and tag.casefold() not in seen:
            tags.append(tag)
            seen.add(tag.casefold())
    return tags


def cmd_add(args: argparse.Namespace) -> None:
    category = normalize_category(args.category)
    source = Path(args.source_file).expanduser().resolve()
    if not source.is_file():
        fail(f"正文文件不存在：{source}")
    body = source.read_text(encoding="utf-8").strip()
    if not body:
        fail("正文不能为空")
    if body.startswith("---"):
        fail("正文文件不要包含 frontmatter；元数据由 kb.py 生成")

    target_dir = WIKI_ROOT.joinpath(*category)
    api = args.api.strip() if args.api else ""
    is_ecosystem_libraries = args.ecosystem_libraries
    if is_ecosystem_libraries:
        if category[0] != "技术" or len(category) != 3:
            fail("三方库清单必须位于技术三级目录，例如：技术/前端/Electron")
        if api or args.slug:
            fail("三方库清单不接受 --api 或 --slug")
        if args.title.strip() != "三方库":
            fail("三方库清单的标题必须为“三方库”")
        target = target_dir / "三方库" / "index.md"
    elif category[0] == "技术":
        if not api:
            fail("技术文章必须指定 --api，并按“模块/API/index.md”存放")
        if has_api_title_suffix(args.title.strip()):
            fail("API 标题只能保留官方 API 名称，不得追加冒号及用途说明")
        if args.slug:
            fail("技术文章的 API 目录由 --api 自动生成，请不要使用 --slug")
        if "三方库" in category and (
            len(category) not in {5, 6} or category[3] != "三方库"
        ):
            fail(
                "三方库 API 分类必须为“技术/<领域>/<框架>/三方库/<库名>[/<模块>]”"
            )
        target = target_dir / api_directory(api) / "index.md"
    else:
        target = target_dir / f"{slugify(args.slug or args.title)}.md"
    if target.exists():
        fail(f"文章已存在，拒绝覆盖：{target}")

    today = dt.date.today().isoformat()
    tags = parse_tags(args.tags)
    frontmatter = [
        "---",
        f"title: {quote_yaml(args.title.strip())}",
        f"description: {quote_yaml(args.summary.strip())}",
        f"category: {quote_yaml('/'.join(category))}",
        *([f"kind: {quote_yaml('ecosystem-libraries')}"] if is_ecosystem_libraries else []),
        *([f"api: {quote_yaml(api)}"] if api else []),
        f"tags: {json.dumps(tags, ensure_ascii=False)}",
        f"created: {quote_yaml(today)}",
        f"updated: {quote_yaml(today)}",
        "---",
        "",
    ]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(frontmatter) + body + "\n", encoding="utf-8")
    cmd_index(argparse.Namespace(check=False))
    print(target)


def article_meta(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            result[key.strip()] = value.strip().strip('"')
    return result


def markdown_files() -> list[Path]:
    if not WIKI_ROOT.exists():
        return []
    return sorted(path for path in WIKI_ROOT.rglob("*.md") if path != WIKI_ROOT / "index.md")


def article_rows() -> list[dict[str, str | Path]]:
    rows: list[dict[str, str | Path]] = []
    for path in markdown_files():
        meta = article_meta(path)
        rows.append(
            {
                "path": path,
                "relative": path.relative_to(WIKI_ROOT),
                "title": meta.get("title", path.stem),
                "description": meta.get("description", ""),
                "category": meta.get("category", "未分类"),
                "created": meta.get("created", ""),
                "kind": meta.get("kind", ""),
            }
        )
    return rows


def sorted_categories(groups: dict[str, list[dict[str, str | Path]]]) -> list[tuple[str, list[dict[str, str | Path]]]]:
    """Keep an ecosystem-library page after the framework's API categories."""
    def key(item: tuple[str, list[dict[str, str | Path]]]) -> tuple[str, ...]:
        category, entries = item
        parts = tuple(category.split("/"))
        if all(entry["kind"] == "ecosystem-libraries" for entry in entries):
            return (*parts, "\U0010ffff")
        return parts

    return sorted(groups.items(), key=key)


def site_path(relative: Path) -> str:
    """Map a Wiki source path to Starlight's directory-style route."""
    source_parts = list(relative.with_suffix("").parts)
    if source_parts and source_parts[-1] == "index":
        source_parts.pop()
    def route_part(part: str) -> str:
        # Match Astro's file-based route normalization: whitespace becomes a
        # separator, while punctuation such as the dot in "Node.js" is removed.
        normalized = re.sub(r"\s+", "-", part.lower())
        return re.sub(r"[^\w\u4e00-\u9fff-]+", "", normalized)

    route_parts = [route_part(part) for part in source_parts]
    return "/wiki/" + "/".join(route_parts) + "/"


def chronological_rows(rows: list[dict[str, str | Path]]) -> list[dict[str, str | Path]]:
    """Sort newest creation dates first and titles alphabetically within a date."""
    by_title = sorted(rows, key=lambda row: str(row["title"]).casefold())
    return sorted(by_title, key=lambda row: str(row["created"]), reverse=True)


def markdown_table_cell(value: str | Path) -> str:
    """Escape values inserted into the generated Markdown index table."""
    return str(value).replace("|", "\\|").replace("\n", " ")


def wiki_index_content(rows: list[dict[str, str | Path]]) -> str:
    groups: dict[str, list[dict[str, str | Path]]] = {}
    for row in rows:
        groups.setdefault(str(row["category"]), []).append(row)

    lines = [
        "---",
        "title: Wiki",
        "description: 按领域分类的个人知识文章。",
        'tags: ["知识库", "索引"]',
        "sidebar:",
        "  order: 0",
        "---",
        "",
        "这里收录从 LLM 会话中提炼出的可复用知识。每篇文章都包含独立的背景、结论、步骤与边界；可从下方索引或顶部搜索进入。",
        "",
        "## 知识索引",
        "",
    ]
    if not rows:
        lines.append("暂未归档文章。使用 `/pks 录入当前会话` 创建第一篇知识条目。")
    else:
        lines.extend([
            '<div class="pks-knowledge-index-marker" aria-hidden="true"></div>',
            "",
            "| 创建时间 | 知识 | 分类 | 摘要 |",
            "| --- | --- | --- | --- |",
        ])
        for row in chronological_rows(rows):
            lines.append(
                "| "
                f"{markdown_table_cell(row['created'])} | "
                f"[{markdown_table_cell(row['title'])}]({site_path(row['relative'])}) | "
                f"{markdown_table_cell(row['category'])} | "
                f"{markdown_table_cell(row['description'])} |"
            )
        sidebar_entries = [
            {
                "category": category,
                "title": str(row["title"]),
                "link": site_path(row["relative"]),
            }
            for category, entries in sorted_categories(groups)
            for row in entries
        ]
        sidebar_json = json.dumps(sidebar_entries, ensure_ascii=False, indent=2).replace(
            "</", "<\\/"
        )
        lines.extend([
            "",
            '<script type="application/json" id="pks-sidebar-source" data-pagefind-ignore>',
            sidebar_json,
            "</script>",
        ])
    return "\n".join(lines)


def llms_index_content(rows: list[dict[str, str | Path]]) -> str:
    """Return an llms.txt-compatible, concise inventory of the Wiki."""
    groups: dict[str, list[dict[str, str | Path]]] = {}
    for row in rows:
        groups.setdefault(str(row["category"]), []).append(row)

    lines = [
        "# 个人知识库",
        "",
        "> 一个从 LLM 会话中提炼的本地 Markdown Wiki，按领域归档可复用的技术、管理、产品与运营知识。",
        "",
        "优先阅读与问题最匹配的分类；每篇文章均可脱离原会话独立理解。",
        "",
    ]
    for category, entries in sorted_categories(groups):
        lines.extend([f"## {category}", ""])
        for row in entries:
            lines.append(f"- [{row['title']}](./{row['relative']}): {row['description']}")
        lines.append("")
    return "\n".join(lines)


def cmd_index(args: argparse.Namespace) -> None:
    rows = article_rows()
    targets = {
        WIKI_ROOT / "index.md": wiki_index_content(rows),
        WIKI_ROOT / "llms.txt": llms_index_content(rows),
    }
    outdated = [path for path, content in targets.items() if not path.exists() or path.read_text(encoding="utf-8") != content]
    if args.check:
        if outdated:
            fail("Wiki 索引已过期，请运行 `python3 scripts/kb.py index`")
        print(f"索引已同步：{len(rows)} 篇文章")
        return
    for path, content in targets.items():
        path.write_text(content, encoding="utf-8")
    print(f"已更新 Wiki 索引：{len(rows)} 篇文章")


def cmd_list(args: argparse.Namespace) -> None:
    prefix = args.category.strip().replace("／", "/") if args.category else ""
    rows = []
    for path in markdown_files():
        meta = article_meta(path)
        category = meta.get("category", "")
        if prefix and not category.startswith(prefix):
            continue
        rows.append(
            {
                "title": meta.get("title", path.stem),
                "category": category or "未分类",
                "updated": meta.get("updated", ""),
                "path": str(path),
            }
        )
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if not rows:
        print("知识库暂无匹配文章。")
        return
    for row in rows:
        print(f"[{row['category']}] {row['title']} ({row['updated']})\n  {row['path']}")


def cmd_check(_: argparse.Namespace) -> None:
    errors: list[str] = []
    for path in markdown_files():
        meta = article_meta(path)
        relative = path.relative_to(WIKI_ROOT)
        for field in ("title", "description", "category", "tags", "created", "updated"):
            if not meta.get(field):
                errors.append(f"{relative}: 缺少 frontmatter 字段 {field}")
        if meta.get("tags", "").strip() in {"[]", "[ ]"}:
            errors.append(f"{relative}: tags 不能为空")
        category = meta.get("category", "")
        try:
            parts = normalize_category(category)
        except SystemExit:
            errors.append(f"{relative}: 分类无效：{category}")
            continue
        expected_parent = Path(*parts)
        if meta.get("kind") == "ecosystem-libraries":
            if parts[0] != "技术" or len(parts) != 3:
                errors.append(f"{relative}: 三方库清单必须使用技术三级 category")
                continue
            if meta.get("title") != "三方库":
                errors.append(f"{relative}: 三方库清单的标题必须为“三方库”")
            expected_path = expected_parent / "三方库" / "index.md"
            if relative != expected_path:
                errors.append(
                    f"{relative}: 三方库清单应位于 {expected_path}"
                )
        elif parts[0] == "技术":
            api = meta.get("api", "")
            if not api:
                errors.append(f"{relative}: 技术文章缺少 frontmatter 字段 api")
                continue
            if has_api_title_suffix(meta.get("title", "")):
                errors.append(
                    f"{relative}: API 标题只能保留官方 API 名称，不得追加冒号及用途说明"
                )
            if "三方库" in parts and (
                len(parts) not in {5, 6} or parts[3] != "三方库"
            ):
                errors.append(
                    f"{relative}: 三方库 API 分类必须为 技术/<领域>/<框架>/三方库/<库名>[/<模块>]"
                )
                continue
            expected_path = expected_parent / api_directory(api) / "index.md"
            if relative != expected_path:
                errors.append(
                    f"{relative}: 技术文章应位于 {expected_path}（模块/API/index.md）"
                )
        elif relative.parent != expected_parent:
            errors.append(
                f"{relative}: 目录与 category 不一致，应位于 {expected_parent}"
            )
    if errors:
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"检查通过：{len(markdown_files())} 篇文章，Wiki 根目录 {WIKI_ROOT}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="个人知识库 Markdown 管理工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="新增 Wiki 文章（拒绝覆盖）")
    add.add_argument("--title", required=True)
    add.add_argument("--category", required=True)
    add.add_argument("--summary", required=True)
    add.add_argument("--tags", default="")
    add.add_argument("--slug")
    add.add_argument("--api", help="技术文章的唯一 API 名称；生成 API/index.md 目录")
    add.add_argument(
        "--ecosystem-libraries",
        "--dependency-list",
        dest="ecosystem_libraries",
        action="store_true",
        help="创建技术三级目录下与框架关联的三方库清单",
    )
    add.add_argument("--source-file", required=True)
    add.set_defaults(func=cmd_add)

    list_cmd = subparsers.add_parser("list", help="列出 Wiki 文章")
    list_cmd.add_argument("--category")
    list_cmd.add_argument("--json", action="store_true")
    list_cmd.set_defaults(func=cmd_list)

    check = subparsers.add_parser("check", help="校验 Wiki 元数据和目录")
    check.set_defaults(func=cmd_check)

    index = subparsers.add_parser("index", help="生成面向人类和 LLM 的 Wiki 索引")
    index.add_argument("--check", action="store_true", help="仅检查索引是否与文章同步")
    index.set_defaults(func=cmd_index)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
