#!/usr/bin/env python3
"""
Morning Digest - AI Wiki 晨间简报
升级目标：
1. 不只看 raw，当 wiki 新页面更新时也能识别新增
2. 同时检视 OpenClaw 最近的记忆 / skill / 决策演化
3. 晨报输出更像“主编 + 系统观察者”，主动提炼进步、判断、机会与风险
"""

import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple

WIKI_PATH = os.path.expanduser("~/ouyangrong1313/MyAIWiki")
LOG_PATH = os.path.join(WIKI_PATH, "log.md")
RAW_PATH = os.path.join(WIKI_PATH, "raw")
WIKI_DIR = os.path.join(WIKI_PATH, "wiki")
OPENCLAW_PATH = os.path.expanduser("~/.openclaw/workspace")
MEMORY_PATH = os.path.join(OPENCLAW_PATH, "MEMORY.md")
DAILY_MEMORY_DIR = os.path.join(OPENCLAW_PATH, "memory")
DECISIONS_PATH = os.path.join(OPENCLAW_PATH, "memory/decisions/decisions.md")
SKILLS_DIR = os.path.join(OPENCLAW_PATH, "skills")

FALLBACK_TOPICS = [
    {
        "title": "把知识库从“资料堆”升级为“可执行系统”",
        "keywords": ["wiki", "知识库", "schema", "ingest", "lint", "query", "第二大脑", "second brain"],
        "thinking": [
            "如果知识库只能存文章摘要，它更像归档系统；只有当它能持续更新索引、修正旧结论、沉淀可复用方法时，才开始接近第二大脑。",
            "对你来说，最有价值的不是“又收了几篇文章”，而是这些文章有没有进入你日常的编译、检索、复盘和决策链路。",
        ],
        "work_help": [
            "把高频任务（例如 /compile、/lint、晨间简报）继续流程化，减少每次从零开始。",
            "让“好的回答回写知识库”成为默认动作，这样分析结论不会只停留在聊天记录里。",
        ],
    },
    {
        "title": "Agent 系统真正的复利点在 Skill，而不在单次回答",
        "keywords": ["agent", "skill", "workflow", "harness", "memory", "上下文", "评估"],
        "thinking": [
            "单次回答再聪明，也会消失；只有流程、规则和经验沉淀成 Skill，系统能力才会复利。",
            "最近你已经在把 OpenClaw、知识库、Seetong 分析串起来，这本质上就是从“问答工具”往“工作流系统”迁移。",
        ],
        "work_help": [
            "优先把重复任务 Skill 化：知识库编译、需求澄清、反馈分析、预合并检查。",
            "每次发现重复错误，不只是修一次，而是补到 Skill / 检查表 / 记忆文件里。",
        ],
    },
    {
        "title": "APP 产品开发正在进入“需求、埋点、分析、回写”的闭环时代",
        "keywords": ["产品", "app", "研发", "埋点", "反馈", "版本", "需求", "tapd", "sensors", "umeng"],
        "thinking": [
            "产品开发不再只是“提需求—做功能—上线”，而是“需求定义—埋点设计—版本观察—用户反馈—回写迭代”的连续闭环。",
            "如果知识库和 Agent 系统能承接这个闭环，研发团队会越来越像一个会自我校正的系统。",
        ],
        "work_help": [
            "把用户反馈、神策、友盟、TAPD 的分析结论沉淀成可复用页面，减少版本复盘时重新翻资料。",
            "让 AI Agent 不只服务知识管理，也服务需求澄清、质量复盘、版本决策。",
        ],
    },
]


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""



def get_recent_log_entries():
    """从 log.md 读取最近 7 天的 ingest 记录"""
    entries = []
    try:
        with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.split("\n")
            week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            in_section = False
            current_date = None
            for line in lines:
                if line.startswith("## [") and line[4:14] >= week_ago:
                    current_date = line
                    in_section = True
                elif line.startswith("## [") and current_date:
                    in_section = False
                elif in_section and "### ingest" in line:
                    entries.append(current_date + " " + line)
    except FileNotFoundError:
        pass
    return entries



def get_recent_files(base_path: str, days: int = 1, suffix: str = ".md") -> List[str]:
    results = []
    cutoff = datetime.now() - timedelta(days=days)
    root = Path(base_path)
    if not root.exists():
        return results

    for path in root.rglob(f"*{suffix}"):
        try:
            if datetime.fromtimestamp(path.stat().st_mtime) > cutoff:
                results.append(str(path.relative_to(root)))
        except Exception:
            continue
    return sorted(results)



def get_new_raw_files():
    """查找 24 小时内新增的 raw 文件"""
    new_files = []
    yesterday = datetime.now() - timedelta(days=1)
    try:
        for root, dirs, files in os.walk(RAW_PATH):
            if "articles" in root:
                continue
            for f in files:
                if f.endswith(".md") and not f.endswith("-digest.md"):
                    path = os.path.join(root, f)
                    mtime = datetime.fromtimestamp(os.path.getmtime(path))
                    if mtime > yesterday:
                        rel = os.path.relpath(path, RAW_PATH)
                        new_files.append(rel)
    except Exception:
        pass
    return sorted(new_files)



def get_new_wiki_files():
    """查找 48 小时内新增或更新的 wiki 页面，避免错过昨天晚上补的内容"""
    return get_recent_files(WIKI_DIR, days=2, suffix=".md")



def extract_section(text: str, heading: str):
    lines = text.splitlines()
    result = []
    capture = False
    target = heading.strip()
    for line in lines:
        if line.strip() == target:
            capture = True
            continue
        if capture and re.match(r"^##\s+", line):
            break
        if capture:
            result.append(line)
    return "\n".join(result).strip()



def extract_bullets(text: str, max_items: int = 4):
    bullets = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(("- ", "* ")):
            item = s[2:].strip()
            if item and 10 <= len(item) <= 140 and "链接：" not in item:
                bullets.append(item)
        if len(bullets) >= max_items:
            break
    return bullets



def summarize_article(path: Path, rel_path: str, base_label: str):
    text = safe_read(path)
    if not text:
        return None

    title = rel_path
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip()
            break

    joined = text.lower()
    core = extract_section(text, "## 核心观点")
    summary = extract_section(text, "## 内容摘要")

    bullets = []
    core_lines = [l.strip("- *\t") for l in core.splitlines() if l.strip()]
    summary_lines = [l.strip("- *\t") for l in summary.splitlines() if l.strip()]
    for line in core_lines[:3] + summary_lines[:3]:
        clean = re.sub(r"\s+", " ", line).strip()
        if 16 <= len(clean) <= 140 and clean not in bullets:
            bullets.append(clean)
        if len(bullets) >= 4:
            break

    if not bullets:
        bullets = extract_bullets(text, 4)

    tags = []
    work_help = []
    think_more = []
    judgment = "这篇内容值得看的点，不在信息量，而在它能否推动你现有系统往前走一步。"
    action = "把这篇内容补成一页可执行方法或检查清单，而不是只保留摘要。"

    if any(k in joined for k in ["multi-agent", "多智能体", "subagent", "fan-out", "router", "worker"]):
        tags.append("AI Agent")
        work_help.append("能直接反哺 OpenClaw / Codex / Claude Code 的多 agent 分工设计，不再只停留在“多开几个 agent”层面。")
        work_help.append("适合你拿来校准：什么时候该并行，什么时候该单 agent，什么时候该用 gateway routing。")
        think_more.append("哪些任务真的值得 fan-out，哪些只是“看起来复杂”但其实更适合单线程闭环？")
        think_more.append("你现有 OpenClaw 的价值，更多来自 routing 还是来自 subagent 协作？")
        judgment = "这类内容最有价值的，不是概念新，而是它能帮你更清楚地区分“并行炫技”和“运行时设计”。"
        action = "把多 agent 分工原则写成一页内部方法：触发条件、拓扑选择、上下文隔离、merge 责任。"

    if any(k in joined for k in ["wiki", "schema", "第二大脑", "second brain", "ingest", "lint", "query"]):
        if "知识库" not in tags:
            tags.append("知识库")
        work_help.append("能直接帮助 MyAIWiki 继续从“文章仓库”升级成“持续维护的知识系统”。")
        think_more.append("哪些页面应该从“摘抄”升级成“决策依据 / 方法手册 / 操作规约”？")
        if "多 agent" not in judgment:
            judgment = "这类内容更适合拿来校准你的知识系统分层，而不是只做阅读摘录。"

    if any(k in joined for k in ["app", "产品", "埋点", "反馈", "版本", "tapd", "umeng", "sensors"]):
        tags.append("APP研发")
        work_help.append("适合把需求、埋点、反馈、复盘串成持续更新的产品知识链，服务 Seetong 实际研发。")
        think_more.append("能不能把“需求—埋点—反馈—复盘”沉淀成固定分析框架，而不是每次临场拼装？")

    if not work_help:
        work_help.append("先别把它当“读过一篇文章”，而是判断它能否转成你每天会复用的方法。")
    if not think_more:
        think_more.append("今天最值得做的，不是收藏这篇内容，而是挑一条真正进入你的工作流。")

    return {
        "title": title,
        "path": rel_path,
        "source": base_label,
        "tags": tags[:3],
        "bullets": bullets[:4],
        "work_help": work_help[:3],
        "think_more": think_more[:2],
        "judgment": judgment,
        "action": action,
    }



def scan_wiki_corpus(limit_files: int = 120):
    corpus = []
    wiki_root = Path(WIKI_DIR)
    if not wiki_root.exists():
        return ""
    count = 0
    for path in sorted(wiki_root.rglob("*.md")):
        corpus.append(safe_read(path)[:2000])
        count += 1
        if count >= limit_files:
            break
    return "\n".join(corpus)



def pick_fallback_topic():
    corpus = scan_wiki_corpus()
    corpus_lower = corpus.lower()
    best = None
    best_score = -1
    for topic in FALLBACK_TOPICS:
        score = sum(corpus_lower.count(k.lower()) for k in topic["keywords"])
        if score > best_score:
            best = topic
            best_score = score
    return best or FALLBACK_TOPICS[0]



def get_openclaw_changes() -> Dict[str, List[str]]:
    changes = {
        "skills": [],
        "memory": [],
        "decisions": [],
        "insights": [],
    }

    skills_root = Path(SKILLS_DIR)
    if skills_root.exists():
        cutoff = datetime.now() - timedelta(days=3)
        for path in skills_root.glob("*/SKILL.md"):
            try:
                if datetime.fromtimestamp(path.stat().st_mtime) > cutoff:
                    changes["skills"].append(path.parent.name)
            except Exception:
                continue

    for rel in ["memory/2026-05-20.md", "memory/2026-05-19.md", "memory/consolidated-candidates.md", "MEMORY.md"]:
        p = Path(OPENCLAW_PATH) / rel
        if p.exists():
            changes["memory"].append(rel)

    decisions_text = safe_read(Path(DECISIONS_PATH))
    if decisions_text:
        for line in decisions_text.splitlines():
            if line.startswith("## 2026-05"):
                changes["decisions"].append(line.replace("## ", "").strip())

    if "待验证" in decisions_text and "降级策略" in decisions_text:
        changes["insights"].append("每周经验沉淀已经开始显式记录“会话层取数异常时的降级策略”，这说明 OpenClaw 的流程开始更像一个可维护系统。")
    if "Pattern 检测" in decisions_text:
        changes["insights"].append("最近的进步不只是新增 skill，而是开始关注 pattern 检测、失败捕获、验证闭环这些系统能力。")
    if changes["skills"]:
        changes["insights"].append("最近多批 skill 在集中整理，说明你正在把零散经验往“可复用流程层”迁移。")

    return changes



def summarize_openclaw_progress(changes: Dict[str, List[str]]) -> Tuple[List[str], List[str], str, str]:
    progress = []
    opportunities = []

    if changes["skills"]:
        skill_names = "、".join(changes["skills"][:6])
        progress.append(f"最近改动较活跃的 skill 有：{skill_names}，说明你在持续把工作方法从临场发挥迁移到技能层。")
        opportunities.append("把最近反复修改的 skill 再抽象一层：补触发条件、边界、失败案例和验证标准。")

    if changes["memory"]:
        progress.append("memory 自动化链路在持续产出 daily memory 与 consolidated candidates，但当前仍混入不少流程元规则，说明“自动沉淀”已经启动，“候选质量治理”还在路上。")
        opportunities.append("下一步最值钱的不是再多记，而是提高“什么该进 MEMORY、什么只留候选区”的筛选质量。")

    if changes["decisions"]:
        progress.append("决策日志已经开始记录：简报失败复盘、每周经验沉淀、skill 失败自动捕获、pattern 检测增强等，这比只改文件更进一步。")

    progress.extend(changes["insights"][:2])

    if not progress:
        progress.append("OpenClaw 最近没有明显结构性更新，今天更适合回看旧配置里哪些规则已经失效。")

    judgment = "你这套系统最近最真实的进步，不是多了几个文件，而是开始出现“决策日志、降级策略、候选治理、模式识别”这些系统自我维护能力。"
    action = "今天最值得补的一刀，是把 AI Wiki 晨报和 OpenClaw 近期演化真正串起来：不仅报新增文章，也要报系统最近学会了什么。"
    return progress[:4], opportunities[:3], judgment, action



def get_editor_view(info_list, openclaw_changes):
    joined = "\n".join(
        " ".join(item.get("tags", []) + item.get("bullets", []) + item.get("work_help", []))
        for item in info_list
    ).lower()

    if info_list and any(k in joined for k in ["multi-agent", "subagent", "worker", "router", "ai agent"]):
        return {
            "theme": "今天新增内容的重心，已经从“AI 能做什么”往“AI 系统该怎么分工、怎么运行、怎么收口”迁移。",
            "priority": "优先级判断：值得把新内容直接反哺到 OpenClaw / Skill / 多 agent 方法论，而不是只做知识摘录。",
        }
    if any(k in joined for k in ["知识库", "wiki", "第二大脑", "ingest", "schema"]):
        return {
            "theme": "今天新增内容的共同主题，是把知识从“收集”推进到“系统化维护”。",
            "priority": "优先级判断：更适合投入到 MyAIWiki / OpenClaw / Skill 的衔接，而不是继续找更多新工具。",
        }
    if openclaw_changes.get("skills") or openclaw_changes.get("decisions"):
        return {
            "theme": "今天更值得看的，不只是知识库新增，而是你的 OpenClaw 系统本身也在发生结构性进步。",
            "priority": "优先级判断：把“新文章启发”与“系统真实演化”放在一起看，晨报才会越来越有用。",
        }
    return {
        "theme": "今天新增内容更偏方法论输入，关键在于挑一条接进你当前的工作流。",
        "priority": "优先级判断：少看一点、多落一点，会比继续囤资料更有复利。",
    }



def get_personal_focus_hint(info_list, openclaw_changes):
    joined = "\n".join(
        " ".join(item.get("tags", []) + item.get("bullets", []) + item.get("work_help", []))
        for item in info_list
    ).lower()

    if any(k in joined for k in ["multi-agent", "subagent", "worker", "router", "ai agent"]):
        return "你今天最值得推进的，不是再看一篇 agent 文章，而是把‘何时并行 / 何时单 agent / 谁负责 merge’写成你自己的运行规则。"
    if openclaw_changes.get("skills"):
        return "你今天最值得推进的，是把最近集中修改的 skill 再补一层：触发条件、失败案例、验证标准。"
    if any(k in joined for k in ["知识库", "wiki", "第二大脑"]):
        return "你今天最值得推进的，不是再读一篇，而是让一条知识真正进入 MyAIWiki → OpenClaw → Skill 的协作链。"
    return "你今天最值得推进的，是让旧知识进入工作流，而不是继续停留在阅读层。"



def get_opportunity_and_risk(info_list, has_new_files: bool, openclaw_changes: Dict[str, List[str]]):
    joined = "\n".join(
        " ".join(item.get("tags", []) + item.get("bullets", []) + item.get("work_help", []) + item.get("think_more", []))
        for item in info_list
    ).lower()

    opportunity = "今天最好的机会，是把一条新知识转成可复用的方法，而不是停留在阅读层。"
    risk = "今天最大的风险，是看完觉得有启发，但没有真正接进知识库、流程或研发工作。"

    if any(k in joined for k in ["multi-agent", "subagent", "worker", "router", "ai agent"]):
        opportunity = "今天最好的机会，是把多 agent 的讨论从“概念热闹”落成你自己的运行时规则：触发、拓扑、上下文、merge。"
        risk = "今天最大的风险，是继续把多智能体理解成“多开几个模型实例”，忽略真正决定成败的运行时设计。"
    elif any(k in joined for k in ["知识库", "wiki", "第二大脑", "schema", "ingest"]):
        opportunity = "今天最好的机会，是把知识库再往前推一步：从“整理内容”升级成“维护系统”。"
        risk = "今天最大的风险，是继续把 wiki 当文章仓库，而不是把它变成能支持决策和执行的工作系统。"
    elif openclaw_changes.get("skills") or openclaw_changes.get("decisions"):
        opportunity = "今天最好的机会，是顺着 OpenClaw 最近的演化，把‘决策日志、模式识别、候选治理’继续往前打磨。"
        risk = "今天最大的风险，是文件越来越多，但“真正进入工作流的进步”没有被晨报识别和强化。"

    if not has_new_files and not (openclaw_changes.get("skills") or openclaw_changes.get("decisions")):
        risk = "今天最大的风险，不是没有新增内容，而是旧知识和旧经验一直没有真正进入你的工作流。"

    return opportunity, risk



def get_workflow_priority(info_list, has_new_files: bool, openclaw_changes: Dict[str, List[str]]):
    joined = "\n".join(
        " ".join(item.get("tags", []) + item.get("bullets", []) + item.get("work_help", []))
        for item in info_list
    ).lower()

    if any(k in joined for k in ["multi-agent", "subagent", "worker", "router", "ai agent"]):
        return "如果今天要只推进一件事，优先把“多 agent 分工原则”补成一页内部方法：何时拆、怎么拆、谁收口。"
    if openclaw_changes.get("skills"):
        return "如果今天要只推进一件事，优先挑一个最近常改的 skill，补齐触发条件、边界和失败案例。"
    if any(k in joined for k in ["知识库", "wiki", "第二大脑"]):
        return "如果今天要只推进一件事，优先补齐一页能连接 MyAIWiki、OpenClaw、Skill、Memory 的工作分层说明。"
    if has_new_files:
        return "如果今天要只推进一件事，优先让今天新增内容真正进入系统，而不是只停留在阅读层。"
    return "如果今天要只推进一件事，优先从旧知识里抽一条能直接指导今天工作的结论。"



def get_anti_hype_warning(info_list, openclaw_changes: Dict[str, List[str]]):
    joined = "\n".join(
        " ".join(item.get("tags", []) + item.get("bullets", []) + item.get("work_help", []) + item.get("think_more", []))
        for item in info_list
    ).lower()

    if any(k in joined for k in ["multi-agent", "subagent", "worker", "router", "ai agent"]):
        return (
            "今天不该做什么：不要一上来就把复杂任务默认拆成多 agent，更不要把“并行”当成先进性的代名词。",
            "最容易自嗨的点：看完多智能体材料后，马上想设计一套很炫的拓扑，但没有先写清楚 ownership、上下文边界和 merge 责任。",
        )
    if any(k in joined for k in ["知识库", "wiki", "第二大脑", "ingest", "schema"]):
        return (
            "今天不该做什么：不要继续囤新文章、改目录结构、补标签，却没有把任何一条知识接进真实工作流。",
            "最容易自嗨的点：把知识库维护误当成知识进步，结果页面越来越多，可执行的方法并没有同步增加。",
        )
    if openclaw_changes.get("skills") or openclaw_changes.get("decisions"):
        return (
            "今天不该做什么：不要看到最近 skill、memory、决策都在更新，就误以为系统能力一定已经稳定落地。",
            "最容易自嗨的点：文件层面的变化很多，但真正经受过失败、复盘、重复使用验证的规则还不够多。",
        )
    return (
        "今天不该做什么：不要为了保持忙碌感继续补资料，而回避真正该落地的一步。",
        "最容易自嗨的点：把“看了很多、记了很多”误当成“系统真的更强了”。",
    )



# ==================== 知识节点融合（2026-06 升级）====================

def parse_simple_frontmatter(content: str) -> Dict:
    """简化的 frontmatter 解析（复用 wiki-query.py 的逻辑）"""
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


def get_today_new_nodes() -> List[Dict]:
    """获取最近 48 小时内新增的 wiki 文章中的知识节点

    Returns:
        [{node, source_path, source_title, category, date}]
    """
    yesterday = datetime.now() - timedelta(days=2)
    results = []

    try:
        for root, dirs, files in os.walk(WIKI_DIR):
            # 跳过 index.md 和 master-index.md
            for f in files:
                if not f.endswith(".md"):
                    continue
                if f in ("index.md", "master-index.md"):
                    continue
                path = os.path.join(root, f)
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                if mtime < yesterday:
                    continue
                try:
                    content = safe_read(Path(path))
                    fm = parse_simple_frontmatter(content)
                    nodes = fm.get("nodes", [])
                    if not nodes:
                        continue
                    # 提取标题
                    title = fm.get("title", "")
                    if not title:
                        for line in content.split("\n"):
                            if line.startswith("# "):
                                title = line[2:].strip()
                                break
                    if not title:
                        title = f
                    for node in nodes:
                        if isinstance(node, str) and node.strip():
                            results.append({
                                "node": node.strip(),
                                "source_path": path,
                                "source_title": title,
                                "category": fm.get("category", ""),
                                "date": fm.get("date", ""),
                            })
                except Exception:
                    pass
    except Exception:
        pass
    return results


def find_related_nodes(node: str, limit: int = 5) -> List[Dict]:
    """根据节点名找相关文章（用 wiki-query 思路的命令式查询）

    Returns:
        [{node, source_path, source_title, category, match_type}]
    """
    results = []
    seen_paths = set()

    # 策略 1：精确节点名匹配
    for root, dirs, files in os.walk(WIKI_DIR):
        for f in files:
            if not f.endswith(".md") or f in ("index.md", "master-index.md"):
                continue
            path = os.path.join(root, f)
            try:
                content = safe_read(Path(path))
                fm = parse_simple_frontmatter(content)
                nodes = fm.get("nodes", [])
                for n in nodes:
                    if isinstance(n, str) and n.strip() == node:
                        if path not in seen_paths:
                            seen_paths.add(path)
                            title = fm.get("title", "")
                            if not title:
                                for line in content.split("\n"):
                                    if line.startswith("# "):
                                        title = line[2:].strip()
                                        break
                            if not title:
                                title = f
                            results.append({
                                "node": n.strip(),
                                "source_path": path,
                                "source_title": title,
                                "category": fm.get("category", ""),
                                "match_type": "精确节点匹配",
                            })
            except Exception:
                pass

    # 策略 2：双向链接中包含该节点
    for root, dirs, files in os.walk(WIKI_DIR):
        for f in files:
            if not f.endswith(".md") or f in ("index.md", "master-index.md"):
                continue
            path = os.path.join(root, f)
            if path in seen_paths:
                continue
            try:
                content = safe_read(Path(path))
                # 找 [[node]] 或 [[node|alias]] 或 标题中含 node
                pattern = rf"\[\[[^\]]*{re.escape(node)}[^\]]*\]\]"
                if re.search(pattern, content):
                    fm = parse_simple_frontmatter(content)
                    title = fm.get("title", "")
                    if not title:
                        for line in content.split("\n"):
                            if line.startswith("# "):
                                title = line[2:].strip()
                                break
                    if not title:
                        title = f
                    results.append({
                        "node": node,
                        "source_path": path,
                        "source_title": title,
                        "category": fm.get("category", ""),
                        "match_type": "双向链接",
                    })
                    seen_paths.add(path)
            except Exception:
                pass

    # 策略 3：ripgrep 全文匹配（兌底）
    # 适用于老文章没有 frontmatter 的场景
    try:
        import subprocess
        result = subprocess.run(
            ["rg", "-l", "--no-heading", node, WIKI_DIR],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            rg_files = [Path(p) for p in result.stdout.strip().split("\n") if p]
            # 过滤 index.md / master-index.md
            rg_files = [p for p in rg_files if p.name not in ("index.md", "master-index.md")]
            # 统计每个文件里节点名出现次数
            rg_scored = []
            for f in rg_files:
                if str(f) in seen_paths:
                    continue
                try:
                    content = safe_read(f)
                    count = content.count(node)
                    if count > 0:
                        rg_scored.append((f, count))
                except Exception:
                    pass
            # 按出现次数降序
            rg_scored.sort(key=lambda x: x[1], reverse=True)
            for f, count in rg_scored[:limit]:
                try:
                    content = safe_read(f)
                    fm = parse_simple_frontmatter(content)
                    title = fm.get("title", "")
                    if not title:
                        for line in content.split("\n"):
                            if line.startswith("# "):
                                title = line[2:].strip()
                                break
                    if not title:
                        title = f.name
                    results.append({
                        "node": node,
                        "source_path": str(f),
                        "source_title": title,
                        "category": fm.get("category", ""),
                        "match_type": f"全文匹配（出现{count}次）",
                    })
                    seen_paths.add(str(f))
                except Exception:
                    pass
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # ripgrep 未装或超时，静默跳过
        pass

    return results[:limit]


def get_node_fusion_section() -> List[str]:
    """生成“知识节点融合”章节（发芽报告的核心升级）

    Returns:
        markdown 行列表
    """
    lines = []
    new_nodes = get_today_new_nodes()

    if not new_nodes:
        return lines

    # 按节点去重，保留所有来源
    unique_nodes = {}
    for n in new_nodes:
        key = n["node"]
        if key not in unique_nodes:
            unique_nodes[key] = []
        unique_nodes[key].append(n)

    lines.append("## 🌱 今日新节点（发芽报告升级版）")
    lines.append("")
    lines.append(f"> 本节是 LLM-Wiki 风格升级：除了今天新增的文章，还提炼出今天**新出现的独立知识节点**，并为每个节点找 3-5 个关联节点。")
    lines.append("")

    # 今日新节点列表（按来源文章分组，能看出每篇文章的节点贡献）
    lines.append("### 📌 今日新增知识节点")
    lines.append(f"> 今日共提炼出 **{len(unique_nodes)} 个新节点**（来源：{len(new_nodes)} 条记录）")
    lines.append("")

    # 按来源文章分组
    from collections import defaultdict
    by_source = defaultdict(list)
    for n in new_nodes:
        by_source[n["source_title"]].append(n["node"])

    # 先按文章展示，每篇最多 6 个节点
    for source_title, nodes in by_source.items():
        unique_nodes_in_source = list(dict.fromkeys(nodes))  # 去重保持顺序
        node_strs = [f"**{n}**" for n in unique_nodes_in_source[:8]]
        suffix = f"（共 {len(unique_nodes_in_source)} 个）" if len(unique_nodes_in_source) > 8 else ""
        lines.append(f"- 《{source_title[:40]}{'...' if len(source_title) > 40 else ''}》")
        lines.append(f"  {', '.join(node_strs)} {suffix}")
    lines.append("")

    # 关联节点融合（选有最多关联的 5 个新节点——优先选有 inbound 引用的）
    lines.append("### 🔗 节点关联与碰撞")

    # 先扫一遍所有新节点，找有 inbound 关联的
    nodes_with_links = []
    for node, sources in unique_nodes.items():
        related = find_related_nodes(node, limit=3)
        related = [r for r in related if r["source_path"] not in [s["source_path"] for s in sources]]
        if related:
            nodes_with_links.append((node, sources, related))

    # 按关联数降序
    nodes_with_links.sort(key=lambda x: len(x[2]), reverse=True)
    for node, sources, related in nodes_with_links[:5]:
        lines.append(f"- **{node}** 的关联节点：")
        for r in related[:3]:
            lines.append(f"  - → {r['source_title'][:50]}{'...' if len(r['source_title']) > 50 else ''}（{r['match_type']}）")
        lines.append("")

    lines.append("> 💡 **建议**：阅读以上“今日新节点” + “关联节点”，尝试用一句话讲清两者如何碰撞出新的判断——这是发芽报告的核心动作。")
    lines.append("")
    return lines


def generate_markdown():
    today = datetime.now().strftime("%Y-%m-%d")

    lines = []
    lines.append("# 📚 AI Wiki 晨间简报")
    lines.append(f"日期：{today}")
    lines.append("")

    entries = get_recent_log_entries()
    new_raw_files = get_new_raw_files()
    new_wiki_files = get_new_wiki_files()
    openclaw_changes = get_openclaw_changes()

    has_knowledge_updates = bool(new_raw_files or new_wiki_files)

    # 【2026-06 升级】知识节点融合章节（发芽报告核心）
    node_fusion = get_node_fusion_section()
    if node_fusion:
        lines.extend(node_fusion)

    if entries:
        lines.append("## 📝 最近 7 天新增知识轨迹")
        for e in entries[-5:]:
            parts = e.split("|")
            if len(parts) >= 2:
                date = parts[0].replace("## [", "").replace("]", "").strip()
                title = parts[1].strip()
                lines.append(f"- **{date}**：{title}")
            else:
                lines.append(f"- {e}")
        lines.append("")

    info_list = []

    if new_raw_files:
        lines.append("## 🆕 最近新增 / 更新的原始资料")
        for f in new_raw_files[:5]:
            lines.append(f"- {f}")
            info = summarize_article(Path(RAW_PATH) / f, f, "raw")
            if info:
                info_list.append(info)
        lines.append("")

    if new_wiki_files:
        lines.append("## 📄 最近新增 / 更新的知识页面")
        for f in new_wiki_files[:5]:
            lines.append(f"- {f}")
            if len(info_list) < 3:
                info = summarize_article(Path(WIKI_DIR) / f, f, "wiki")
                if info:
                    info_list.append(info)
        lines.append("")

    progress, opportunities, openclaw_judgment, openclaw_action = summarize_openclaw_progress(openclaw_changes)

    if has_knowledge_updates or progress:
        editor = get_editor_view(info_list, openclaw_changes)
        opportunity, risk = get_opportunity_and_risk(info_list, has_knowledge_updates, openclaw_changes)
        workflow_priority = get_workflow_priority(info_list, has_knowledge_updates, openclaw_changes)

        lines.append("## 🧭 主编视角")
        lines.append(f"- {editor['theme']}")
        lines.append(f"- {editor['priority']}")
        lines.append("")

        lines.append("## 📈 今日机会提醒")
        lines.append(f"- {opportunity}")
        if opportunities:
            lines.append(f"- {opportunities[0]}")
        lines.append("")

        anti_do_not, anti_hype = get_anti_hype_warning(info_list, openclaw_changes)

        lines.append("## ⚠️ 今日风险提醒")
        lines.append(f"- {risk}")
        lines.append("")

        lines.append("## 🚫 今天不该做什么")
        lines.append(f"- {anti_do_not}")
        lines.append("")

        lines.append("## 🪞 最容易自嗨的点")
        lines.append(f"- {anti_hype}")
        lines.append("")

        if info_list:
            lines.append("## 🎯 今天最值得看的内容")
            for info in info_list[:2]:
                lines.append(f"### {info['title']}")
                if info.get("tags"):
                    lines.append(f"**标签**：{' / '.join(info['tags'])}")
                if info.get("source"):
                    lines.append(f"**来源层**：{info['source']}")
                lines.append("")
                lines.append("**核心内容**")
                for b in info["bullets"]:
                    lines.append(f"- {b}")
                lines.append("")
                lines.append("**这对你今天的工作有什么帮助**")
                for hp in info["work_help"]:
                    lines.append(f"- {hp}")
                lines.append("")
                lines.append("**我的判断**")
                lines.append(f"- {info['judgment']}")
                lines.append("")
                lines.append("**值得继续想一层**")
                for t in info["think_more"]:
                    lines.append(f"- {t}")
                lines.append("")
                lines.append("**今天建议动作**")
                lines.append(f"- {info['action']}")
                lines.append("")

        lines.append("## 🔧 这两天 OpenClaw 真正的进步")
        for item in progress[:4]:
            lines.append(f"- {item}")
        lines.append("")
        lines.append("**我的判断**")
        lines.append(f"- {openclaw_judgment}")
        lines.append("")
        lines.append("**今天建议动作**")
        lines.append(f"- {openclaw_action}")
        lines.append("")

        lines.append("## 🎯 结合你当前工作的今日重点")
        lines.append(f"- {get_personal_focus_hint(info_list, openclaw_changes)}")
        lines.append(f"- {workflow_priority}")
        lines.append("")
    else:
        topic = pick_fallback_topic()
        opportunity, risk = get_opportunity_and_risk([], False, openclaw_changes)
        workflow_priority = get_workflow_priority([], False, openclaw_changes)
        lines.append("## 🧠 今日发散思考（近期无明显新增）")
        lines.append(f"### {topic['title']}")
        lines.append("")
        lines.append("## 📈 今日机会提醒")
        lines.append(f"- {opportunity}")
        lines.append("")
        anti_do_not, anti_hype = get_anti_hype_warning([], openclaw_changes)
        lines.append("## ⚠️ 今日风险提醒")
        lines.append(f"- {risk}")
        lines.append("")
        lines.append("## 🚫 今天不该做什么")
        lines.append(f"- {anti_do_not}")
        lines.append("")
        lines.append("## 🪞 最容易自嗨的点")
        lines.append(f"- {anti_hype}")
        lines.append("")
        lines.append("核心启发")
        for t in topic["thinking"]:
            lines.append(f"- {t}")
        lines.append("")
        lines.append("这对你今天的工作有什么帮助")
        for hp in topic["work_help"]:
            lines.append(f"- {hp}")
        lines.append("")
        lines.append("我的判断")
        lines.append("- 这条主题最有价值的地方，在于它能否进入你的日常系统，而不是停留在理念层。")
        lines.append("")
        lines.append("今天建议动作")
        lines.append("- 从现有 wiki 里挑 1 个高频主题，补一条“可执行方法”或“检查清单”，让知识进入工作流。")
        lines.append("")
        lines.append("## 🎯 结合你当前工作的今日重点")
        lines.append(f"- {workflow_priority}")
        lines.append("")

    lines.append("## ☕ 主编一句话")
    if has_knowledge_updates or progress:
        lines.append("- 今天别满足于“我看到了新增”，更重要的是把这些新增和系统进步接进今天的工作。")
        lines.append("- 真正的复利，不在多看一篇，而在让知识、流程、记忆开始彼此增强。")
    else:
        lines.append("- 今天更值得做的是“让旧知识进入工作流”，而不是继续囤新资料。")
        lines.append("- 旧知识一旦被接进产品研发和 Agent 流程，才会真正开始产生价值。")
    lines.append("")
    lines.append("💡 提示：用 /compile 编译新文章，用 /lint 检查知识库健康")
    lines.append("")

    return "\n".join(lines)



def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        import json
        payload = {
            "entries": get_recent_log_entries(),
            "new_raw_files": get_new_raw_files(),
            "new_wiki_files": get_new_wiki_files(),
            "openclaw_changes": get_openclaw_changes(),
            "preview": generate_markdown(),
        }
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(generate_markdown())


if __name__ == "__main__":
    main()
