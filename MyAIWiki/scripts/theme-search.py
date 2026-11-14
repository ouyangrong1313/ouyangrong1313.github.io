#!/usr/bin/env python3
"""
theme-search.py - MyAIWiki 主题多轮筛选工具

设计哲学（参考 LLM-Wiki Skill）：
  - 输入主题 → 意图识别（拆 5-10 个关键词） → 多轮 ripgrep 收窄 → 列出相关文章
  - 用 grep 命令式查询绕开 LLM 意图识别，整体 token 消耗极低
  - 不需要 LLM 介入就能完成"主题 → 文章列表"的检索

使用示例：
  python3 scripts/theme-search.py "知识工作者编排 Agent"
  python3 scripts/theme-search.py "Codex 知识库 优化"
  python3 scripts/theme-search.py "Harness 实践" --rounds 3
  python3 scripts/theme-search.py "RAG 检索" --per-round 3 --limit 10
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple

# 路径
WIKI_PATH = os.path.expanduser("~/ouyangrong1313/MyAIWiki")
WIKI_DIR = os.path.join(WIKI_PATH, "wiki")

CATEGORIES = [
    "01-ai-agents",
    "02-ai-coding",
    "03-productivity",
    "04-app-dev",
    "05-content-creation",
    "06-ai-tech",
    "07-rag-systems",
]

# 停用词（中文 + 英文），提取关键词时跳过
STOP_WORDS = {
    # 中文
    "的", "是", "在", "和", "与", "或", "一个", "一些", "这", "那", "了", "着", "过",
    "什么", "怎么", "如何", "为什么", "可以", "应该", "需要", "可能", "通过", "进行",
    "我们", "你", "我", "他", "她", "它", "他们", "文章", "内容", "方面", "部分",
    # 英文
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "in", "on", "at", "to", "for", "of", "with", "by", "from", "as", "into",
    "and", "or", "but", "if", "then", "so", "than", "that", "this", "these", "those",
    "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her", "its", "our", "their",
}


def has_ripgrep() -> bool:
    try:
        subprocess.run(["rg", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def extract_keywords(theme: str) -> List[str]:
    """从主题中提取关键词（轻量意图识别，不调用 LLM）

    策略：
    1. 按空格和标点分词
    2. 过滤停用词
    3. 保留 2-6 字中文 / 2 词以上英文
    4. 按出现频率排序
    """
    # 移除标点，保留中英文和数字
    text = re.sub(r"[，。！？、；：\"\"''（）()【】\[\]《》<>「」『』.,!?;:\(\)\[\]\{\}]", " ", theme)
    # 分词
    raw_tokens = re.split(r"\s+", text.strip())

    # 过滤
    keywords = []
    for token in raw_tokens:
        token = token.strip()
        if not token:
            continue
        if token.lower() in STOP_WORDS:
            continue
        # 中文 2-6 字 / 英文 2+ 字符
        if re.match(r"^[\u4e00-\u9fa5]+$", token):
            if 2 <= len(token) <= 6:
                keywords.append(token)
        elif re.match(r"^[A-Za-z][A-Za-z0-9\-_]*$", token):
            if len(token) >= 2:
                keywords.append(token)

    # 去重保持顺序
    seen = set()
    unique = []
    for k in keywords:
        if k.lower() not in seen:
            seen.add(k.lower())
            unique.append(k)

    # 限制在 5-10 个关键词
    return unique[:10]


def ripgrep_search(keyword: str, limit: int = 50) -> List[Path]:
    """用 ripgrep 搜索包含关键词的文件"""
    try:
        result = subprocess.run(
            ["rg", "-l", "--no-heading", keyword, WIKI_DIR],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            paths = [Path(p) for p in result.stdout.strip().split("\n") if p]
            # 过滤掉 index.md / master-index.md
            paths = [p for p in paths if p.name not in ("index.md", "master-index.md")]
            return paths[:limit]
        return []
    except subprocess.TimeoutExpired:
        return []


def extract_title(path: Path) -> str:
    """从 H1 提取标题"""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.startswith("# "):
                    return line[2:].strip()
    except Exception:
        pass
    return path.stem


def format_path(path: Path) -> str:
    try:
        return str(path.relative_to(WIKI_PATH))
    except ValueError:
        return str(path)


def parse_frontmatter(content: str) -> Dict:
    """简化的 frontmatter 解析"""
    fm = {}
    if not content.startswith("---"):
        return fm
    end = content.find("\n---", 3)
    if end == -1:
        return fm
    fm_text = content[3:end].strip()

    def clean_value(v: str) -> str:
        return v.strip().strip('"').strip("'").strip()

    def parse_inline_list(v: str) -> List[str]:
        v = v.strip()
        if not (v.startswith("[") and v.endswith("]")):
            return []
        inner = v[1:-1]
        protected = re.sub(r"\[\[([^\]]+)\]\]", lambda m: "[[" + m.group(1).replace(",", "〈,〉") + "]]", inner)
        items = [clean_value(x).replace("〈,〉", ",") for x in protected.split(",")]
        return [x for x in items if x]

    current_list_key = None
    for line in fm_text.split("\n"):
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
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
                fm[key] = []
                current_list_key = key
            elif value.startswith("[") and value.endswith("]"):
                fm[key] = parse_inline_list(value)
                current_list_key = None
            else:
                fm[key] = clean_value(value)
                current_list_key = None
    return fm


def get_category(path: Path) -> str:
    """从路径获取分类"""
    parts = path.parts
    for cat in CATEGORIES:
        if cat in parts:
            return cat
    return ""


def theme_search(theme: str, rounds: int = 3, per_round: int = 5, limit: int = 15) -> Dict:
    """主题多轮筛选主流程

    流程：
    1. 从主题提取关键词（意图识别）
    2. 第 1 轮：用 top-N 关键词做 ripgrep，收集候选文件
    3. 第 2 轮：用剩余关键词 + frontmatter 节点再次筛选
    4. 第 3 轮：交叉验证（多关键词命中加权）
    5. 输出排序后的 top-K 结果

    Args:
        theme: 输入主题
        rounds: 筛选轮数
        per_round: 每轮用的关键词数
        limit: 最终返回结果数

    Returns:
        {
            "theme": 原始主题,
            "keywords": [关键词列表],
            "rounds": [每轮信息],
            "results": [最终结果],
        }
    """
    if not has_ripgrep():
        print("❌ ripgrep 未安装，请先安装：brew install ripgrep", file=sys.stderr)
        sys.exit(1)

    # Step 1: 提取关键词
    keywords = extract_keywords(theme)
    if not keywords:
        print(f"⚠️  未能从主题中提取到关键词：{theme}", file=sys.stderr)
        return {"theme": theme, "keywords": [], "rounds": [], "results": []}

    # Step 2: 多轮筛选
    candidates: Dict[str, Set[str]] = {}  # path_str -> set of matched keywords
    round_info = []

    for round_idx in range(min(rounds, len(keywords))):
        # 每轮用 per_round 个关键词
        start = round_idx * per_round
        end = start + per_round
        round_keywords = keywords[start:end]

        if not round_keywords:
            break

        round_files = []
        for kw in round_keywords:
            files = ripgrep_search(kw, limit=100)
            for f in files:
                path_str = str(f)
                if path_str not in candidates:
                    candidates[path_str] = set()
                candidates[path_str].add(kw)
                round_files.append(path_str)

        round_info.append({
            "round": round_idx + 1,
            "keywords": round_keywords,
            "hits": len(round_files),
            "cumulative": len(candidates),
        })

    # Step 3: 排序（命中关键词数 × 分类权重）
    # 优先级：多关键词命中 > 单一关键词命中
    scored = []
    for path_str, matched_kws in candidates.items():
        path = Path(path_str)
        # 读取 frontmatter 拿 category
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            fm = parse_frontmatter(content)
            category = fm.get("category", get_category(path))
            # 检查 frontmatter.nodes 中是否也命中了关键词
            nodes = fm.get("nodes", [])
            node_hits = sum(1 for kw in keywords if any(kw in str(n) for n in nodes))
            tags = fm.get("tags", [])
            tag_hits = sum(1 for kw in keywords if any(kw in str(t) for t in tags))
        except Exception:
            category = get_category(path)
            node_hits = 0
            tag_hits = 0

        # 评分：关键词命中数 × 5 + 节点命中数 × 3 + 标签命中数 × 2
        score = len(matched_kws) * 5 + node_hits * 3 + tag_hits * 2
        scored.append({
            "path": path,
            "title": extract_title(path),
            "category": category,
            "matched_keywords": list(matched_kws),
            "node_hits": node_hits,
            "score": score,
        })

    # 按分数降序
    scored.sort(key=lambda x: x["score"], reverse=True)
    top_results = scored[:limit]

    return {
        "theme": theme,
        "keywords": keywords,
        "rounds": round_info,
        "results": top_results,
    }


def print_result(data: Dict) -> None:
    """格式化输出"""
    print(f"\n🔍 主题搜索：{data['theme']}")
    print(f"📋 提取关键词：{', '.join(data['keywords'])}")

    if not data["keywords"]:
        return

    print(f"\n📊 筛选过程（共 {len(data['rounds'])} 轮）")
    print("-" * 80)
    for r in data["rounds"]:
        print(f"  第 {r['round']} 轮：关键词 {r['keywords']} → 命中 {r['hits']} 文件，累计 {r['cumulative']} 候选")

    print(f"\n📑 最终结果：top {len(data['results'])} 条")
    print("=" * 80)
    for i, r in enumerate(data["results"], 1):
        print(f"\n{i}. 📄 {r['title']}")
        print(f"   分类：{r.get('category', '-')}")
        print(f"   路径：{format_path(r['path'])}")
        print(f"   匹配关键词：{', '.join(r['matched_keywords'])} (×{len(r['matched_keywords'])})")
        if r.get("node_hits", 0) > 0:
            print(f"   节点命中：{r['node_hits']} 个")
        print(f"   评分：{r['score']}")
    print("\n" + "=" * 80)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="MyAIWiki 主题多轮筛选（ripgrep 驱动，零 LLM 依赖）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s "知识工作者编排 Agent"
  %(prog)s "Codex 知识库 优化" --rounds 2
  %(prog)s "Harness 实践" --per-round 3 --limit 10
        """,
    )
    parser.add_argument("theme", help="搜索主题")
    parser.add_argument("--rounds", type=int, default=3, help="筛选轮数（默认 3）")
    parser.add_argument("--per-round", type=int, default=5, help="每轮用的关键词数（默认 5）")
    parser.add_argument("--limit", type=int, default=15, help="最终返回结果数（默认 15）")
    parser.add_argument("--path", default=None, help="自定义 wiki 根路径")

    args = parser.parse_args()

    data = theme_search(args.theme, args.rounds, args.per_round, args.limit)
    print_result(data)


if __name__ == "__main__":
    main()
