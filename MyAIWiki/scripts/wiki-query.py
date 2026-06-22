#!/usr/bin/env python3
"""
wiki-query.py - MyAIWiki 轻量查询工具

设计哲学（参考 LLM-Wiki Skill）：
  - 用 ripgrep 命令式查询，绕开 LLM 意图识别
  - token 消耗极低，响应极快
  - 支持多种查询模式：node / tag / text / backlink / category / date / orphan

使用示例：
  python3 scripts/wiki-query.py node "LLM-Wiki"
  python3 scripts/wiki-query.py tag "#主题/AI-Coding"
  python3 scripts/wiki-query.py text "知识库"
  python3 scripts/wiki-query.py backlink "Codex"
  python3 scripts/wiki-query.py category "02-ai-coding"
  python3 scripts/wiki-query.py date "2026-06"
  python3 scripts/wiki-query.py orphan
  python3 scripts/wiki-query.py frontmatter-missing
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# 路径
WIKI_PATH = os.path.expanduser("~/ouyangrong1313/MyAIWiki")
WIKI_DIR = os.path.join(WIKI_PATH, "wiki")
MASTER_INDEX = os.path.join(WIKI_DIR, "master-index.md")
LOG_PATH = os.path.join(WIKI_PATH, "log.md")

CATEGORIES = [
    "01-ai-agents",
    "02-ai-coding",
    "03-productivity",
    "04-app-dev",
    "05-content-creation",
    "06-ai-tech",
    "07-rag-systems",
]


def has_ripgrep() -> bool:
    """检查 ripgrep 是否可用"""
    try:
        subprocess.run(["rg", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_all_wiki_files() -> List[Path]:
    """获取所有 wiki 文件（不含 index.md）"""
    files = []
    for category in CATEGORIES:
        cat_dir = Path(WIKI_DIR) / category
        if cat_dir.exists():
            files.extend(cat_dir.rglob("*.md"))
    return [f for f in files if f.name != "index.md" and f.name != "master-index.md"]


def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """解析 YAML frontmatter（用 regex 简化实现，不依赖 PyYAML）

    支持的格式：
    - key: value
    - key: [a, b, c]  # 内联列表
    - key:             # 多行列表
        - a
        - b
    """
    fm = {}
    if not content.startswith("---"):
        return fm, content

    end = content.find("\n---", 3)
    if end == -1:
        return fm, content

    fm_text = content[3:end].strip()
    body = content[end + 4:].strip()

    def clean_value(v: str) -> str:
        return v.strip().strip('"').strip("'").strip()

    def parse_inline_list(v: str) -> List[str]:
        """解析 [a, b, c] 格式的内联列表"""
        v = v.strip()
        if not (v.startswith("[") and v.endswith("]")):
            return []
        inner = v[1:-1]
        # 按 , 分割（但不能切到 [[...]] 内的内容）
        # 先把 [[...]] 临时占位
        protected = re.sub(r"\[\[([^\]]+)\]\]", lambda m: "[[" + m.group(1).replace(",", "〈,〉") + "]]", inner)
        items = [clean_value(x).replace("〈,〉", ",") for x in protected.split(",")]
        return [x for x in items if x]

    current_list_key = None
    for line in fm_text.split("\n"):
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue

        # 多行列表项
        if re.match(r"^\s+[-*]\s+", line):
            if current_list_key:
                value = re.sub(r"^\s+[-*]\s+", "", line).strip()
                fm[current_list_key].append(clean_value(value))
            continue

        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if not value:
                # 列表开始（下一行会是 - xxx）
                fm[key] = []
                current_list_key = key
            elif value.startswith("[") and value.endswith("]"):
                # 内联列表
                fm[key] = parse_inline_list(value)
                current_list_key = None
            else:
                fm[key] = clean_value(value)
                current_list_key = None

    return fm, body


def format_path(path: Path) -> str:
    """格式化路径为相对路径"""
    try:
        return str(path.relative_to(WIKI_PATH))
    except ValueError:
        return str(path)


def extract_title(path: Path, content: str) -> str:
    """从 frontmatter 或 H1 提取标题"""
    fm, _ = parse_frontmatter(content)
    if "title" in fm:
        return fm["title"]
    # 从 H1 提取
    for line in content.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


# ==================== 查询实现 ====================

def query_node(node_name: str) -> List[Dict]:
    """查询包含某知识节点的文章"""
    results = []
    for path in get_all_wiki_files():
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        fm, _ = parse_frontmatter(content)
        nodes = fm.get("nodes", [])
        if isinstance(nodes, list) and any(node_name in str(n) for n in nodes):
            results.append({
                "path": path,
                "title": extract_title(path, content),
                "category": fm.get("category", ""),
                "nodes": nodes,
            })
    return results


def query_tag(tag: str) -> List[Dict]:
    """查询带某标签的文章"""
    # 标签可能带 # 前缀
    tag = tag.lstrip("#")
    results = []
    for path in get_all_wiki_files():
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        fm, _ = parse_frontmatter(content)
        tags = fm.get("tags", [])
        if isinstance(tags, list) and any(tag in str(t).lstrip("#") for t in tags):
            results.append({
                "path": path,
                "title": extract_title(path, content),
                "category": fm.get("category", ""),
                "tags": tags,
            })
    return results


def query_text(text: str) -> List[Dict]:
    """基于 ripgrep 的全文查询"""
    if not has_ripgrep():
        print("❌ ripgrep 未安装，请先安装：brew install ripgrep", file=sys.stderr)
        return []

    try:
        result = subprocess.run(
            ["rg", "-l", "--no-heading", text, WIKI_DIR],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            paths = [Path(p) for p in result.stdout.strip().split("\n") if p]
        else:
            return []
    except subprocess.TimeoutExpired:
        print("❌ ripgrep 查询超时", file=sys.stderr)
        return []

    results = []
    for path in paths:
        if path.name in ("index.md", "master-index.md"):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        results.append({
            "path": path,
            "title": extract_title(path, content),
        })
    return results


def query_backlink(target: str) -> List[Dict]:
    """查询引用了某文章/节点的文章（基于双向链接 [[...]]）

    三级匹配策略：
    1. 精确（10 分）：[[Codex配置原则总览]] 查 "Codex配置原则总览"
    2. 前缀（5 分）：[[Codex配置原则总览]] 查 "Codex"
    3. 包含（1 分）：模糊匹配（兜底）
    """
    results = []
    # 标准化 target（去掉可能的 [[...]] 包装）
    target_clean = target.strip("[]")

    for path in get_all_wiki_files():
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        # 找到所有 [[...]] 链接
        all_links = re.findall(r"\[\[([^\]]+)\]\]", content)
        matched = []
        for link in all_links:
            # 去掉 |alias 部分
            link_target = link.split("|")[0].strip()
            # 三级匹配
            if link_target == target_clean:
                matched.append((link_target, 10))
            elif link_target.startswith(target_clean):
                matched.append((link_target, 5))
            elif target_clean in link_target:
                matched.append((link_target, 1))

        if matched:
            # 按匹配分数排序，取 top 5
            matched.sort(key=lambda x: x[1], reverse=True)
            total_score = sum(s for _, s in matched)
            results.append({
                "path": path,
                "title": extract_title(path, content),
                "match_count": len(matched),
                "match_score": total_score,
                "matched_links": [m[0] for m in matched[:5]],
            })

    # 先按匹配分数、再按次数排序
    results.sort(key=lambda x: (x["match_score"], x["match_count"]), reverse=True)
    return results


def query_category(category: str) -> List[Dict]:
    """查询某分类下的所有文章"""
    cat_dir = Path(WIKI_DIR) / category
    if not cat_dir.exists():
        print(f"❌ 分类目录不存在：{category}", file=sys.stderr)
        return []

    results = []
    for path in cat_dir.rglob("*.md"):
        if path.name == "index.md":
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        results.append({
            "path": path,
            "title": extract_title(path, content),
        })
    return results


def query_date(date_pattern: str) -> List[Dict]:
    """查询某日期范围的 frontmatter.date 文章"""
    results = []
    for path in get_all_wiki_files():
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        fm, _ = parse_frontmatter(content)
        date = fm.get("date", "")
        if date and date_pattern in str(date):
            results.append({
                "path": path,
                "title": extract_title(path, content),
                "date": date,
                "category": fm.get("category", ""),
            })
    # 按日期降序
    results.sort(key=lambda x: x.get("date", ""), reverse=True)
    return results


def query_orphan() -> List[Dict]:
    """查询孤立节点（在 frontmatter.nodes 中声明但没有任何 inbound 链接）"""
    # 先收集所有节点
    all_nodes = {}  # node_name -> [(file, title)]
    for path in get_all_wiki_files():
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        fm, _ = parse_frontmatter(content)
        nodes = fm.get("nodes", [])
        for node in nodes:
            if isinstance(node, str):
                all_nodes.setdefault(node, []).append((path, extract_title(path, content)))

    # 收集所有双向链接的目标
    all_links = set()
    for path in get_all_wiki_files():
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for match in re.findall(r"\[\[([^\]]+)\]\]", content):
            # 去掉可能的 |alias
            target = match.split("|")[0].strip()
            all_links.add(target)

    # 找孤立节点（在 nodes 中但没在任何 [[...]] 中作为目标出现）
    orphan_results = []
    for node, sources in all_nodes.items():
        if node not in all_links:
            orphan_results.append({
                "node": node,
                "sources": sources,
            })

    return orphan_results


def query_frontmatter_missing() -> List[Dict]:
    """查询缺少 frontmatter 的 wiki 文章"""
    results = []
    for path in get_all_wiki_files():
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if not content.startswith("---"):
            results.append({
                "path": path,
                "title": extract_title(path, content),
            })
    return results


# ==================== 输出格式化 ====================

def print_results(results: List[Dict], query_type: str, query_value: str) -> None:
    """统一格式化输出"""
    if not results:
        print(f"\n🔍 {query_type}={query_value}：无结果\n")
        return

    print(f"\n🔍 {query_type}={query_value}：共 {len(results)} 条结果\n")
    print("=" * 80)
    for i, r in enumerate(results, 1):
        if query_type == "node":
            print(f"{i}. 📌 {r['title']}")
            print(f"   分类：{r.get('category', '-')}")
            print(f"   路径：{format_path(r['path'])}")
            if r.get("nodes"):
                print(f"   节点：{', '.join(r['nodes'][:5])}{'...' if len(r['nodes']) > 5 else ''}")
            print()
        elif query_type == "tag":
            print(f"{i}. 🏷️  {r['title']}")
            print(f"   分类：{r.get('category', '-')}")
            print(f"   路径：{format_path(r['path'])}")
            print()
        elif query_type == "text":
            print(f"{i}. 📄 {r['title']}")
            print(f"   路径：{format_path(r['path'])}")
            print()
        elif query_type == "backlink":
            print(f"{i}. 🔗 {r['title']}（引用 {r['match_count']} 次）")
            print(f"   路径：{format_path(r['path'])}")
            if r.get("matched_links"):
                print(f"   匹配链接：{', '.join(r['matched_links'])}")
            print()
        elif query_type == "category":
            print(f"{i}. 📁 {r['title']}")
            print(f"   路径：{format_path(r['path'])}")
            print()
        elif query_type == "date":
            print(f"{i}. 📅 [{r.get('date', '-')}] {r['title']}")
            print(f"   分类：{r.get('category', '-')}")
            print(f"   路径：{format_path(r['path'])}")
            print()
        elif query_type == "orphan":
            print(f"{i}. 🏝️ 孤立节点：{r['node']}")
            for src_path, src_title in r["sources"]:
                print(f"   声明于：{format_path(src_path)}")
            print()
        elif query_type == "frontmatter-missing":
            print(f"{i}. ⚠️  {r['title']}")
            print(f"   路径：{format_path(r['path'])}")
            print()
    print("=" * 80)
    print()


# ==================== 主入口 ====================

def main():
    parser = argparse.ArgumentParser(
        description="MyAIWiki 轻量查询工具（ripgrep 驱动，零 LLM 依赖）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s node "LLM-Wiki"
  %(prog)s tag "#主题/AI-Coding"
  %(prog)s text "知识库"
  %(prog)s backlink "Codex"
  %(prog)s category "02-ai-coding"
  %(prog)s date "2026-06"
  %(prog)s orphan          # 找孤立节点
  %(prog)s frontmatter-missing  # 找缺 frontmatter 的文章
        """,
    )

    parser.add_argument(
        "query_type",
        choices=["node", "tag", "text", "backlink", "category", "date", "orphan", "frontmatter-missing"],
        help="查询类型",
    )
    parser.add_argument(
        "value",
        nargs="?",
        help="查询值（frontmatter-missing / orphan 不需要）",
    )
    parser.add_argument(
        "--path",
        default=None,
        help="自定义 wiki 根路径",
    )

    args = parser.parse_args()

    # 不需要 value 的查询类型
    if args.query_type not in ("orphan", "frontmatter-missing") and not args.value:
        parser.error(f"{args.query_type} 需要提供 value 参数")

    # 执行查询
    if args.query_type == "node":
        results = query_node(args.value)
    elif args.query_type == "tag":
        results = query_tag(args.value)
    elif args.query_type == "text":
        results = query_text(args.value)
    elif args.query_type == "backlink":
        results = query_backlink(args.value)
    elif args.query_type == "category":
        results = query_category(args.value)
    elif args.query_type == "date":
        results = query_date(args.value)
    elif args.query_type == "orphan":
        results = query_orphan()
        print_results(results, "orphan", "孤立节点")
        return
    elif args.query_type == "frontmatter-missing":
        results = query_frontmatter_missing()
        print_results(results, "frontmatter-missing", "缺 frontmatter 的文章")
        return

    print_results(results, args.query_type, args.value or "")


if __name__ == "__main__":
    main()
