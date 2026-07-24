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
WIKI_ROOT = SKILL_ROOT / "docs-site" / "src" / "content" / "docs" / "wiki"
ALLOWED_ROOTS = {"技术", "管理", "产品", "运营", "测试", "其他"}
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def fail(message: str) -> "NoReturn":
    print(f"错误：{message}", file=sys.stderr)
    raise SystemExit(2)


def quote_yaml(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def normalize_category(raw: str) -> list[str]:
    parts = [part.strip() for part in re.split(r"[/／>＞]+", raw) if part.strip()]
    if not 2 <= len(parts) <= 4:
        fail("分类必须包含 2–4 层，例如：技术/前端/React")
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

    filename = f"{slugify(args.slug or args.title)}.md"
    target_dir = WIKI_ROOT.joinpath(*category)
    target = target_dir / filename
    if target.exists():
        fail(f"文章已存在，拒绝覆盖：{target}")

    today = dt.date.today().isoformat()
    tags = parse_tags(args.tags)
    frontmatter = [
        "---",
        f"title: {quote_yaml(args.title.strip())}",
        f"description: {quote_yaml(args.summary.strip())}",
        f"category: {quote_yaml('/'.join(category))}",
        f"tags: {json.dumps(tags, ensure_ascii=False)}",
        f"created: {quote_yaml(today)}",
        f"updated: {quote_yaml(today)}",
        "---",
        "",
    ]
    target_dir.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(frontmatter) + body + "\n", encoding="utf-8")
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
    return sorted(path for path in WIKI_ROOT.rglob("*.md") if path.name != "index.md")


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
        category = meta.get("category", "")
        try:
            parts = normalize_category(category)
        except SystemExit:
            errors.append(f"{relative}: 分类无效：{category}")
            continue
        expected_parent = Path(*parts)
        if relative.parent != expected_parent:
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
    add.add_argument("--source-file", required=True)
    add.set_defaults(func=cmd_add)

    list_cmd = subparsers.add_parser("list", help="列出 Wiki 文章")
    list_cmd.add_argument("--category")
    list_cmd.add_argument("--json", action="store_true")
    list_cmd.set_defaults(func=cmd_list)

    check = subparsers.add_parser("check", help="校验 Wiki 元数据和目录")
    check.set_defaults(func=cmd_check)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
