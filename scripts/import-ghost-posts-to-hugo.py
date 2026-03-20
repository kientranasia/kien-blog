#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path

from markdownify import markdownify as md


def ghost_dt_to_iso_utc(s: str) -> str:
    """
    Ghost export uses: 'YYYY-MM-DD HH:MM:SS'
    We'll treat it as UTC and append 'Z'.
    """
    if not s:
        return ""
    s = str(s).strip()
    if not s:
        return ""
    if "T" in s:
        # already ISO-like
        if s.endswith("Z"):
            return s
        # normalize milliseconds if present
        return s
    # '2022-12-21 13:55:09' -> '2022-12-21T13:55:09Z'
    return s.replace(" ", "T") + "Z"


def yaml_quote(s: str) -> str:
    s = "" if s is None else str(s)
    # Use double quotes; escape quotes + newlines
    s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\r", " ").replace("\n", " ")
    return f"\"{s}\""


def yaml_list_of_strings(items) -> str:
    if not items:
        return "[]"
    out = []
    for it in items:
        out.append(f"- {yaml_quote(it)}")
    return "\n".join(out)


def plain_excerpt(text: str, limit_chars: int = 160) -> str:
    if not text:
        return ""
    t = re.sub(r"\s+", " ", str(text)).strip()
    if len(t) <= limit_chars:
        return t
    return t[: limit_chars - 1].rstrip() + "…"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ghost-json", required=True, help="Ghost export JSON file")
    ap.add_argument("--out-dir", required=True, help="Hugo posts folder (e.g. content/posts)")
    ap.add_argument("--type", default="post", help="Ghost type to import (default: post)")
    ap.add_argument("--limit", type=int, default=0, help="Import first N posts (0 = all)")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite if file exists")
    args = ap.parse_args()

    ghost_json = Path(args.ghost_json).expanduser()
    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(ghost_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    db = data.get("db", [])
    if not db:
        raise RuntimeError("Ghost export missing 'db' root")
    d = db[0].get("data", {})

    posts = d.get("posts", [])
    tags = d.get("tags", [])
    posts_tags = d.get("posts_tags", [])

    tag_by_id = {t["id"]: t for t in tags}

    post_id_to_tag_names = {}
    for pt in posts_tags:
        pid = pt.get("post_id")
        tid = pt.get("tag_id")
        if not pid or not tid:
            continue
        t = tag_by_id.get(tid)
        if not t:
            continue
        post_id_to_tag_names.setdefault(pid, []).append(t.get("name"))

    imported = 0
    skipped = 0

    for post in posts:
        if post.get("type") != args.type:
            continue

        slug = post.get("slug") or ""
        if not slug:
            continue

        out_path = out_dir / f"{slug}.md"
        if out_path.exists() and not args.overwrite:
            skipped += 1
            continue

        title = post.get("title") or slug
        status = post.get("status") or ""
        draft = status.lower() != "published"

        published_at = post.get("published_at") or ""
        created_at = post.get("created_at") or ""
        date_src = published_at if published_at else created_at
        date_iso = ghost_dt_to_iso_utc(date_src)

        plaintext = post.get("plaintext") or ""
        description = plain_excerpt(plaintext, 170)

        # Convert HTML -> Markdown
        html = post.get("html") or ""
        content_md = md(html)
        content_md = content_md.strip()

        post_id = post.get("id")
        tag_names = post_id_to_tag_names.get(post_id, [])
        # Keep stable ordering and remove empties
        tag_names = [t for t in tag_names if t]

        fm_lines = [
            "---",
            f"title: {yaml_quote(title)}",
            f"date: {yaml_quote(date_iso)}",
            f"draft: {'true' if draft else 'false'}",
            f"description: {yaml_quote(description)}",
            f"slug: {yaml_quote(slug)}",
        ]
        if tag_names:
            fm_lines.append("tags:")
            fm_lines.extend([f"- {yaml_quote(t)}" for t in tag_names])

        fm_lines.append("---")

        md_text = "\n".join(fm_lines) + "\n\n" + content_md + "\n"
        out_path.write_text(md_text, encoding="utf-8")

        imported += 1
        if args.limit and imported >= args.limit:
            break

    print(f"Imported: {imported}, skipped(existing): {skipped}")


if __name__ == "__main__":
    main()

