#!/usr/bin/env python3
"""
Compile a WeChat article into MyAIWiki artifacts.

This script writes draft-level `raw`, `digest`, and `wiki` entries, then
updates the category index, master index, and log idempotently.

Usage:
  python3 scripts/compile_wechat_to_wiki.py <url>
  python3 scripts/compile_wechat_to_wiki.py <url> --category 02-ai-coding
  python3 scripts/compile_wechat_to_wiki.py <url> --output-root /tmp/MyAIWiki
  python3 scripts/compile_wechat_to_wiki.py <url> --force
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from build_wechat_raw import build_raw_markdown, fetch_article, slugify
from wiki_ingest_state import IngestStateStore


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = SCRIPT_DIR.parent
CATEGORY_LABELS = {
    "01-ai-agents": "AI Agents",
    "02-ai-coding": "AI Coding",
    "03-productivity": "Productivity",
    "04-app-dev": "App Dev",
    "05-content-creation": "Content Creation",
    "06-ai-tech": "AI Tech",
    "07-rag-systems": "RAG Systems",
}
CATEGORY_TAGS = {
    "01-ai-agents": "#主题/AI-Agent #场景/公众号长文",
    "02-ai-coding": "#主题/AI-Coding #场景/公众号长文",
    "03-productivity": "#主题/效率 #场景/公众号长文",
    "04-app-dev": "#主题/APP研发 #场景/公众号长文",
    "05-content-creation": "#主题/内容创作 #场景/公众号长文",
    "06-ai-tech": "#主题/AI科技 #场景/公众号长文",
    "07-rag-systems": "#主题/RAG #场景/公众号长文",
}


@dataclass
class Paths:
    root: Path
    raw: Path
    digest: Path
    wiki: Path
    category_index: Path
    master_index: Path
    log: Path
    state: Path


def normalize_paragraphs(text: str) -> list[str]:
    paragraphs = []
    for line in text.splitlines():
        cleaned = re.sub(r"\s+", " ", line).strip()
        if not cleaned:
            continue
        if cleaned.startswith(("作者：", "原文：", "•", "-", "标签：")):
            continue
        if len(cleaned) < 12:
            continue
        paragraphs.append(cleaned)
    return paragraphs


def summarize_line(text: str, limit: int = 64) -> str:
    sentence = re.split(r"[。！？.!?]", text, maxsplit=1)[0].strip()
    sentence = sentence or text.strip()
    if len(sentence) <= limit:
        return sentence
    return sentence[: limit - 1].rstrip() + "…"


def derive_core_points(paragraphs: list[str], count: int = 5) -> list[str]:
    points = []
    seen = set()
    for paragraph in paragraphs:
        summary = summarize_line(paragraph, limit=72)
        if summary in seen:
            continue
        seen.add(summary)
        points.append(summary)
        if len(points) >= count:
            break
    return points or ["待补充：自动抽取未拿到稳定段落，请人工补全核心观点。"]


def derive_analysis_angles(core_points: list[str]) -> list[tuple[str, str]]:
    templates = [
        ("这篇文章主要回答了什么问题", "文章把重点放在：{point}"),
        ("为什么这个判断值得关注", "它反复强调：{point}"),
        ("对个人工作方式的直接启发", "可直接落地的一点是：{point}"),
        ("对团队协作的启发", "放到团队场景里，可以理解为：{point}"),
        ("它反对的低效做法是什么", "反过来看，它也在提醒不要忽视：{point}"),
        ("最值得沉淀进知识库的内容", "适合长期保留的结论是：{point}"),
        ("下一步可以怎么继续深入", "继续延展时，可围绕这一点展开：{point}"),
    ]
    angles = []
    for index, (heading, template) in enumerate(templates):
        point = core_points[min(index, len(core_points) - 1)]
        angles.append((heading, template.format(point=point)))
    return angles


def derive_hooks(core_points: list[str]) -> list[str]:
    templates = [
        "如果你只把这篇文章当作常规经验帖，那最关键的一层你还没抓到：{point}",
        "真正值得记下来的，不是表面案例，而是它指向了：{point}",
        "这篇内容最有价值的地方，在于它把一个常被忽略的问题说透了：{point}",
        "很多人会直接跳到结论，但更该看到的是：{point}",
        "把它放到日常工作里看，最先该调整的是：{point}",
        "真正能复用到后续任务里的，其实是这一点：{point}",
        "如果要把全文压成一句执行提醒，我会保留：{point}",
    ]
    hooks = []
    for index, template in enumerate(templates):
        point = core_points[min(index, len(core_points) - 1)]
        hooks.append(f"{index + 1}. {template.format(point=point)}")
    return hooks


def build_digest_markdown(article: dict, tags: str) -> str:
    title = article.get("title", "").strip() or "未命名微信文章"
    author = article.get("author", "").strip() or "未知作者"
    url = article.get("url", "").strip()
    paragraphs = normalize_paragraphs(
        article.get("content_text", "").strip() or article.get("body_text", "").strip()
    )
    core_points = derive_core_points(paragraphs)
    analysis_angles = derive_analysis_angles(core_points)
    hooks = derive_hooks(core_points)

    lines = [
        f"# {title} — 拆解",
        "",
        f"**来源：** {url}",
        f"**作者：** {author}",
        f"**标签：** {tags}",
        "",
        "> 自动编译草稿，建议人工补齐核心观点与钩子质量。",
        "",
        "---",
        "",
        "## 核心观点",
        "",
    ]

    for index, point in enumerate(core_points, start=1):
        lines.append(f"{index}. **{point}**")

    lines.extend(["", "---", "", "## 7个分析角度", ""])
    for heading, body in analysis_angles:
        lines.extend([f"### {heading}", f"- {body}", ""])

    lines.extend(["---", "", "## 开头钩子", ""])
    lines.extend(hooks)
    lines.extend(["", "---", "", "## 相关链接", "", "- 待补充：人工补齐相关页面", ""])
    return "\n".join(lines).rstrip() + "\n"


def build_wiki_markdown(article: dict, tags: str, category: str) -> str:
    title = article.get("title", "").strip() or "未命名微信文章"
    url = article.get("url", "").strip()
    paragraphs = normalize_paragraphs(
        article.get("content_text", "").strip() or article.get("body_text", "").strip()
    )
    core_points = derive_core_points(paragraphs, count=7)
    one_line = core_points[0]

    tag_values = [tag.lstrip("#") for tag in tags.split()]
    nodes = [summarize_line(point, 24) for point in core_points[:5]]
    while len(nodes) < 5:
        nodes.append(f"待提炼节点{len(nodes) + 1}")
    lines = [
        "---",
        f"title: {title}",
        f"category: {category}",
        "tags:",
        *[f"  - {tag}" for tag in tag_values],
        f"nodes: [{', '.join(nodes)}]",
        "links: []",
        f"date: {date.today()}",
        f"source: 微信公众号 / {article.get('author', '').strip() or '未知作者'}",
        "status: draft",
        "---",
        "",
        f"# {title}",
        "",
        "## 核心结论（一句话）",
        "",
        one_line,
        "",
        "## 分类提炼",
        "",
        f"- 场景：{CATEGORY_LABELS.get(category, category)} / 公众号长文",
        f"- 标签： {tags}",
        "- 类型：自动编译草稿 / 待人工复核",
        "",
        "## 知识节点",
        "",
    ]

    for index, point in enumerate(core_points, start=1):
        lines.append(f"{index}. {point}")

    lines.extend(
        [
            "",
            "## 关联图谱",
            "",
            "### 上游（基于 / 来自）",
            "- 待发布：补充已验证的已有页面链接。",
            "",
            "### 下游（应用于 / 验证于）",
            "- 待发布：补充应用或验证关系。",
            "",
            "### 同级（横向 / 并列）",
            "- 待发布：补充同主题的已有页面链接。",
            "",
            "## 标签",
            "",
            tags,
            "",
            "## 相关链接",
            "",
            f"- 原文链接：{url}",
            "- 待补充：人工补齐相关页面",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def resolve_paths(root: Path, category: str, slug: str, state: Path) -> Paths:
    return Paths(
        root=root,
        raw=root / "raw" / f"{slug}.md",
        digest=root / "raw" / f"{slug}-digest.md",
        wiki=root / "wiki" / category / f"{slug}.md",
        category_index=root / "wiki" / category / "index.md",
        master_index=root / "wiki" / "master-index.md",
        log=root / "log.md",
        state=state,
    )


def write_if_needed(path: Path, content: str, force: bool) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return "skipped"
    path.write_text(content, encoding="utf-8")
    return "written"


def validate_published_wiki(markdown: str, root: Path | None = None) -> None:
    if not markdown.startswith("---\n"):
        raise ValueError("Published wiki must start with YAML frontmatter.")
    end = markdown.find("\n---", 3)
    if end < 0:
        raise ValueError("Published wiki frontmatter is not closed.")
    frontmatter = markdown[3:end]
    for field in ("title", "category", "tags", "nodes", "links", "date", "source"):
        if not re.search(rf"^{field}:", frontmatter, flags=re.MULTILINE):
            raise ValueError(f"Published wiki missing frontmatter field: {field}")
    if not re.search(r"^status:\s*published\s*$", frontmatter, flags=re.MULTILINE):
        raise ValueError("Published wiki must declare status: published.")
    links = re.search(r"^links:\s*(.+)$", frontmatter, flags=re.MULTILINE)
    if not links or "[[" not in links.group(1):
        raise ValueError("Published wiki requires at least one wiki link.")
    if root:
        targets = {
            path.relative_to(root / "wiki").with_suffix("").as_posix()
            for path in (root / "wiki").rglob("*.md")
        }
        for target in re.findall(r"\[\[([^\]|#]+)", links.group(1)):
            normalized = target.strip()
            if normalized not in targets and not any(Path(candidate).name == normalized for candidate in targets):
                raise ValueError(f"Published wiki links to a missing page: {normalized}")
    nodes = re.search(r"^nodes:\s*\[(.*)\]$", frontmatter, flags=re.MULTILINE)
    if not nodes or len([item for item in nodes.group(1).split(",") if item.strip()]) < 5:
        raise ValueError("Published wiki requires at least five nodes.")
    for heading in ("## 关联图谱", "### 上游（基于 / 来自）", "### 下游（应用于 / 验证于）", "### 同级（横向 / 并列）"):
        if heading not in markdown:
            raise ValueError(f"Published wiki missing graph heading: {heading}")


def publish_article(root: Path, category: str, slug: str) -> dict[str, str]:
    wiki_path = root / "wiki" / category / f"{slug}.md"
    raw_path = root / "raw" / f"{slug}.md"
    if not raw_path.exists():
        raise ValueError(f"Cannot publish without raw source: {raw_path}")
    markdown = wiki_path.read_text(encoding="utf-8")
    validate_published_wiki(markdown, root)
    title_match = re.search(r"^title:\s*(.+)$", markdown, flags=re.MULTILINE)
    title = title_match.group(1).strip().strip("'\"") if title_match else slug
    store = IngestStateStore(root)
    record = store.find_by_artifact(str(wiki_path.relative_to(root)))
    if not record:
        raise ValueError("Cannot publish without an ingest state record.")
    if record["status"] == "drafted":
        store.transition(record["id"], "polished")
    if store.read(record["id"])["status"] == "polished":
        store.transition(record["id"], "validated")
    paths = resolve_paths(root, category, slug, store.path_for(record["id"]))
    today = str(date.today())
    statuses = {
        "category_index": update_category_index(paths.category_index, slug, title, summarize_line(title, 40)),
        "master_index": update_master_index(paths.master_index, category, slug, title, today),
        "log": update_log(paths.log, title, slug, category, record["url"], "#场景/公众号长文", today),
    }
    store.transition(record["id"], "published")
    statuses["state"] = "published"
    return statuses


def insert_after_heading(text: str, heading: str, block: str) -> str:
    if block.strip() in text:
        return text
    marker = f"{heading}\n"
    if marker not in text:
        return text.rstrip() + "\n\n" + heading + "\n" + block
    return text.replace(marker, marker + block, 1)


def update_category_index(path: Path, slug: str, title: str, summary: str) -> str:
    entry = f"- [[{slug}]] - 自动编译草稿：{summary}\n"
    if path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = f"# {CATEGORY_LABELS.get(path.parent.name, path.parent.name)}\n"
    if f"[[{slug}]]" in text:
        return "skipped"
    updated = insert_after_heading(text, "### 实战案例", entry)
    if updated == text:
        updated = text.rstrip() + "\n\n### 实战案例\n" + entry
    path.write_text(updated, encoding="utf-8")
    return "written"


def update_master_index(path: Path, category: str, slug: str, title: str, today: str) -> str:
    recent_entry = f"- [{title}](./{category}/{slug}.md) — {today}\n"
    category_label = CATEGORY_LABELS.get(category, category)
    category_entry = f"- [{title}](./{category}/{slug}.md)\n"

    text = path.read_text(encoding="utf-8") if path.exists() else "# AI 知识库索引\n"
    changed = False

    if f"./{category}/{slug}.md" not in text.split("## 分类", 1)[0]:
        text = insert_after_heading(text, "## 最近更新", recent_entry)
        changed = True

    category_heading = f"### {category_label}"
    if category_entry.strip() not in text:
        updated = insert_after_heading(text, category_heading, category_entry)
        if updated == text:
            updated = text.rstrip() + "\n\n" + category_heading + "\n" + category_entry
        text = updated
        changed = True

    if changed:
        path.write_text(text, encoding="utf-8")
        return "written"
    return "skipped"


def ensure_date_heading(text: str, today: str) -> str:
    heading = f"## {today}"
    if heading in text:
        return text
    if text.startswith("# AI Wiki Log"):
        marker = "---\n"
        if marker in text:
            return text.replace(marker, marker + "\n" + heading + "\n\n", 1)
    return text.rstrip() + "\n\n" + heading + "\n"


def update_log(path: Path, title: str, slug: str, category: str, url: str, tags: str, today: str) -> str:
    if path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = "# AI Wiki Log\n\n---\n"

    if f"### ingest | {title}" in text:
        return "skipped"

    text = ensure_date_heading(text, today)
    entry = "\n".join(
        [
            f"### ingest | {title}",
            f"- 来源：{url}",
            f"- 原文：raw/{slug}.md",
            f"- 拆解：raw/{slug}-digest.md",
            f"- wiki：wiki/{category}/{slug}.md",
            f"- 标签： {tags}",
            "- 说明：自动编译草稿，建议人工复核 digest 与 wiki 提炼质量",
            "",
        ]
    )
    heading = f"## {today}"
    updated = insert_after_heading(text, heading, entry)
    path.write_text(updated, encoding="utf-8")
    return "written"


def compile_article(
    url: str,
    root: Path,
    category: str,
    slug: str | None,
    tags: str | None,
    force: bool,
) -> tuple[Paths, dict[str, str]]:
    store = IngestStateStore(root)
    record = store.start(url)
    if record["status"] == "published" and not force:
        raise ValueError("Article is already published; use --force only for a deliberate rebuild.")
    if record["status"] == "published":
        record = store.transition(record["id"], "fetched")
    try:
        article = fetch_article(url)
        title = article.get("title", "").strip() or "wechat-article"
        article_slug = slug or slugify(title)
        article_tags = tags or CATEGORY_TAGS.get(category, "#场景/公众号长文")
        paths = resolve_paths(root, category, article_slug, store.path_for(record["id"]))
        raw_markdown = build_raw_markdown(article)
        content = article.get("content_text", "").strip() or article.get("body_text", "").strip()
        content_hash = __import__("hashlib").sha256(content.encode("utf-8")).hexdigest()
        statuses = {
            "raw": write_if_needed(paths.raw, raw_markdown, force),
            "digest": write_if_needed(paths.digest, build_digest_markdown(article, article_tags), force),
            "wiki": write_if_needed(paths.wiki, build_wiki_markdown(article, article_tags, category), force),
            "category_index": "pending_publish",
            "master_index": "pending_publish",
            "log": "pending_publish",
        }
        store.transition(record["id"], "drafted", artifacts={"raw": str(paths.raw.relative_to(root)), "digest": str(paths.digest.relative_to(root)), "wiki": str(paths.wiki.relative_to(root))}, content_sha256=content_hash)
        statuses["state"] = "drafted"
        return paths, statuses
    except Exception as error:
        store.transition(record["id"], "failed", error=str(error))
        raise


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compile a WeChat article into MyAIWiki draft artifacts."
    )
    parser.add_argument("url", help="WeChat article URL")
    parser.add_argument(
        "--category",
        default="02-ai-coding",
        help="Wiki category directory, default: 02-ai-coding",
    )
    parser.add_argument("--slug", help="Optional output slug")
    parser.add_argument("--tags", help="Optional tag string")
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_ROOT),
        help="Root directory of the target MyAIWiki, default: current repo root",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing raw/digest/wiki files",
    )
    args = parser.parse_args()

    root = Path(args.output_root).expanduser().resolve()
    paths, statuses = compile_article(
        url=args.url,
        root=root,
        category=args.category,
        slug=args.slug,
        tags=args.tags,
        force=args.force,
    )

    for name in ("raw", "digest", "wiki", "category_index", "master_index", "log", "state"):
        print(f"{name}: {statuses[name]} -> {getattr(paths, name)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
