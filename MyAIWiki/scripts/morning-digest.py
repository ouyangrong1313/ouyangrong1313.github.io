#!/usr/bin/env python3
"""
Morning Digest - AI Wiki 晨间简报
输出更有洞察的 Markdown：
1. 最近新增的核心内容
2. 对实际工作的帮助
3. 若 24 小时内无新增，则基于既有知识库做发散思考
"""

import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

WIKI_PATH = os.path.expanduser("~/ouyangrong1313/MyAIWiki")
LOG_PATH = os.path.join(WIKI_PATH, "log.md")
RAW_PATH = os.path.join(WIKI_PATH, "raw")
WIKI_DIR = os.path.join(WIKI_PATH, "wiki")

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



def get_new_raw_files():
    """查找 24 小时内新增的 raw 文件"""
    new_files = []
    yesterday = datetime.now() - timedelta(days=1)
    try:
        for root, dirs, files in os.walk(RAW_PATH):
            if "inbox" in root or "articles" in root:
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



def extract_bullets(text: str, max_items: int = 4):
    bullets = []
    bad_prefix = (
        "你是谁",
        "你在做什么项目",
        "你使用的每个",
        "每个待办任务",
        "每篇写过的文章",
        "每个捕捉过的想法",
    )
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(("- ", "* ")):
            item = s[2:].strip()
            if (
                item
                and len(item) <= 120
                and not item.startswith(bad_prefix)
                and "链接：" not in item
            ):
                bullets.append(item)
        if len(bullets) >= max_items:
            break
    return bullets



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



def summarize_raw_file(rel_path: str):
    path = Path(RAW_PATH) / rel_path
    text = safe_read(path)
    if not text:
        return None

    title = rel_path
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    core = extract_section(text, "## 核心观点")
    summary = extract_section(text, "## 内容摘要")
    joined = (text or "").lower()

    thesis = None
    if "增量构建和维护一个持久的 wiki" in text:
        thesis = "不要把 LLM 只当问答器，而要让它持续维护一个会增长的持久 wiki。"
    elif "第二大脑" in text or "second brain" in joined:
        thesis = "AI 的价值不在单次回答，而在于逐步理解你的项目、任务和知识脉络，成为真正能协作的第二大脑。"
    elif "skill" in joined or "workflow" in joined:
        thesis = "真正有复利的不是一次回答，而是可复用、可验证、可持续维护的工作流。"
    else:
        core_lines = [l.strip() for l in core.splitlines() if l.strip()]
        if core_lines:
            thesis = core_lines[0]

    bullets = []
    if thesis:
        bullets.append(thesis)

    if "三层架构" in text or "raw sources" in joined:
        bullets.append("它把知识系统拆成 Raw sources / Wiki / Schema 三层：原始资料、结构化知识、维护规则各司其职。")
    if "ingest" in joined or "lint" in joined or "query" in joined:
        bullets.append("它强调通过 Ingest、Query、Lint 形成持续更新的知识闭环，而不是一次性整理。")
    if "从头发现知识" in text or "rag" in joined:
        bullets.append("它和常见 RAG 的差异在于：不是每次从零检索，而是让知识持续积累、交叉引用并修正旧结论。")

    if len(bullets) < 3:
        for marker in ["### 核心思想", "### 三层架构", "### 操作"]:
            sec = extract_section(text, marker)
            if sec:
                sec_lines = [l.strip() for l in sec.splitlines() if l.strip()]
                for line in sec_lines[:2]:
                    clean = re.sub(r"^[*-]\s*", "", line).strip()
                    if 18 <= len(clean) <= 140 and clean not in bullets:
                        bullets.append(clean)
                    if len(bullets) >= 4:
                        break
            if len(bullets) >= 4:
                break

    if len(bullets) < 2:
        bullets.extend([b for b in extract_bullets(summary, 4 - len(bullets)) if b not in bullets])

    work_help = []
    think_more = []
    judgment = None
    tags = []

    if any(k in joined for k in ["wiki", "schema", "ingest", "lint", "query", "second brain", "第二大脑"]):
        tags.append("知识库")
        work_help.append("对 MyAIWiki 有直接帮助：更适合把知识库当持续维护的系统，而不是文章仓库。")
        work_help.append("提醒你把“好的分析结论回写 wiki”设成默认动作，这样知识不会只停留在聊天历史里。")
        think_more.append("哪些页面应该从“文章摘要”升级成“操作手册 / 检查清单 / 决策依据”？")

    if any(k in joined for k in ["agent", "skill", "workflow", "harness", "memory"]):
        tags.append("AI Agent")
        work_help.append("对 AI Agent 驱动研发流程有帮助：真正值得沉淀的是 Skill、上下文规则和工作流，而不只是 prompt。")
        think_more.append("最近哪些高频动作已经值得抽成 Skill，例如编译知识库、需求澄清、分析回写？")

    if any(k in joined for k in ["产品", "app", "feedback", "version", "迭代", "需求", "埋点"]):
        tags.append("APP研发")
        work_help.append("对 APP 产品开发有帮助：适合把需求、埋点、反馈、复盘结论沉淀成版本资产，减少每次复盘重新翻资料。")
        think_more.append("能不能把用户反馈、埋点指标、版本质量、需求决策串成一条持续更新的产品知识链？")

    if "第二大脑" in text or "second brain" in joined:
        judgment = "这篇最值得借的，不是“Obsidian + Claude”这个表层组合，而是“知识持续回写、系统持续变聪明”的工作方式。"
    elif "skill" in joined or "workflow" in joined:
        judgment = "这篇更适合落成工作流或 Skill，不适合只停留在阅读摘抄。"
    elif "wiki" in joined or "schema" in joined:
        judgment = "这篇更像知识系统设计原则，适合反过来校准你现在的 MyAIWiki 和 OpenClaw 分工。"
    else:
        judgment = "这篇值得看的点，不在信息量，而在它能不能推动你现有系统往前走一步。"

    if not work_help:
        work_help.append("先别把它当“读过一篇文章”，而是想清楚它能否转成你每天会复用的方法。")
    if not think_more:
        think_more.append("今天最值得做的，不是收藏这篇内容，而是挑一条真正进入你的工作流。")

    action = "把这篇内容编译成正式 wiki 页面，并补一条可执行方法，服务你的知识库 / 产品研发 / Agent 工作流。"
    if "second brain" in joined or "第二大脑" in joined:
        action = "补一页“第二大脑工作分层”说明：MyAIWiki 管知识、OpenClaw 管执行、Skill 管流程、Memory 管持续性。"
    elif "skill" in joined or "workflow" in joined:
        action = "从这篇内容里抽 1 条可复用流程，补成 Skill 或检查清单，而不是只留摘要。"

    return {
        "title": title,
        "path": rel_path,
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



def get_editor_view(info_list):
    """像主编一样，给今天的新增内容做一个总判断"""
    joined = "\n".join(
        " ".join(item.get("tags", []) + item.get("bullets", []) + item.get("work_help", []))
        for item in info_list
    )
    text = joined.lower()

    if any(k in text for k in ["知识库", "wiki", "第二大脑", "ingest", "schema"]):
        return {
            "theme": "今天新增内容的共同主题，是把知识从“收集”推进到“系统化维护”。",
            "priority": "优先级判断：更适合投入到 MyAIWiki / OpenClaw / Skill 的衔接，而不是继续找更多新工具。",
        }
    if any(k in text for k in ["agent", "skill", "workflow", "harness"]):
        return {
            "theme": "今天新增内容的共同主题，是让 AI 从“会回答”升级为“会工作”。",
            "priority": "优先级判断：最值得推进的是高频动作 Skill 化，而不是继续优化单次 prompt。",
        }
    if any(k in text for k in ["产品", "app", "埋点", "反馈", "版本"]):
        return {
            "theme": "今天新增内容的共同主题，是产品研发闭环：需求、埋点、反馈、复盘要进入统一知识系统。",
            "priority": "优先级判断：更适合服务版本复盘和研发协同，而不是停留在知识收藏层。",
        }
    return {
        "theme": "今天新增内容更偏方法论输入，关键在于挑一条接进你当前的工作流。",
        "priority": "优先级判断：少看一点、多落一点，会比继续囤资料更有复利。",
    }



def get_personal_focus_hint(info_list):
    """贴近用户当前工作的晨间提醒"""
    joined = "\n".join(
        " ".join(item.get("tags", []) + item.get("bullets", []) + item.get("work_help", []))
        for item in info_list
    ).lower()

    if any(k in joined for k in ["知识库", "wiki", "第二大脑"]):
        return "你今天最值得推进的，不是再读一篇，而是让一条知识真正进入 MyAIWiki → OpenClaw → Skill 的协作链。"
    if any(k in joined for k in ["产品", "app", "版本", "反馈", "埋点"]):
        return "你今天最值得推进的，是把产品研发里的一个真实问题沉淀成持续可复用的知识资产。"
    if any(k in joined for k in ["agent", "skill", "workflow"]):
        return "你今天最值得推进的，是把最近反复做的事情抽成流程，让 AI 真正替你承接工作。"
    return "你今天最值得推进的，是让旧知识进入工作流，而不是继续停留在阅读层。"



def get_opportunity_and_risk(info_list, has_new_files: bool):
    joined = "\n".join(
        " ".join(item.get("tags", []) + item.get("bullets", []) + item.get("work_help", []) + item.get("think_more", []))
        for item in info_list
    ).lower()

    opportunity = "今天最好的机会，是把一条新知识转成可复用的方法，而不是停留在阅读层。"
    risk = "今天最大的风险，是看完觉得有启发，但没有真正接进知识库、流程或研发工作。"

    if any(k in joined for k in ["知识库", "wiki", "第二大脑", "schema", "ingest"]):
        opportunity = "今天最好的机会，是把知识库再往前推一步：从“整理内容”升级成“维护系统”。"
        risk = "今天最大的风险，是继续把 wiki 当文章仓库，而不是把它变成能支持决策和执行的工作系统。"
    elif any(k in joined for k in ["agent", "skill", "workflow"]):
        opportunity = "今天最好的机会，是把最近高频动作抽成 Skill，让 AI 真正开始替你承接一段流程。"
        risk = "今天最大的风险，是继续优化单次 prompt，却没有沉淀出稳定可复用的流程。"
    elif any(k in joined for k in ["产品", "app", "埋点", "反馈", "版本"]):
        opportunity = "今天最好的机会，是把产品研发里的真实问题沉淀成知识资产，服务后续版本和团队协作。"
        risk = "今天最大的风险，是需求、埋点、反馈、复盘仍然散落在聊天、表格和脑子里，没有形成复利。"

    if not has_new_files:
        risk = "今天最大的风险，不是没有新增内容，而是旧知识一直没有真正进入你的工作流。"

    return opportunity, risk



def get_workflow_priority(info_list, has_new_files: bool):
    joined = "\n".join(
        " ".join(item.get("tags", []) + item.get("bullets", []) + item.get("work_help", []))
        for item in info_list
    ).lower()

    if any(k in joined for k in ["产品", "app", "埋点", "反馈", "版本"]):
        return "如果今天要只推进一件事，优先把一个真实版本问题补成“需求—埋点—反馈—复盘”的闭环页面。"
    if any(k in joined for k in ["agent", "skill", "workflow"]):
        return "如果今天要只推进一件事，优先把一个重复动作抽成 Skill 或检查清单，先拿到可复用性。"
    if any(k in joined for k in ["知识库", "wiki", "第二大脑"]):
        return "如果今天要只推进一件事，优先补齐一页能连接 MyAIWiki、OpenClaw、Skill、Memory 的工作分层说明。"
    if has_new_files:
        return "如果今天要只推进一件事，优先让今天新增内容真正进入系统，而不是只停留在阅读层。"
    return "如果今天要只推进一件事，优先从旧知识里抽一条能直接指导今天工作的结论。"



def generate_markdown():
    today = datetime.now().strftime("%Y-%m-%d")

    lines = []
    lines.append("# 📚 AI Wiki 晨间简报")
    lines.append(f"**日期：{today}**")
    lines.append("")
    lines.append("---")
    lines.append("")

    entries = get_recent_log_entries()
    new_files = get_new_raw_files()

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

    if new_files:
        lines.append(f"## 🆕 今天新增了什么")
        for f in new_files[:5]:
            lines.append(f"- {f}")
        lines.append("")

        info_list = []
        for rel in new_files[:2]:
            info = summarize_raw_file(rel)
            if info:
                info_list.append(info)

        if info_list:
            editor = get_editor_view(info_list)
            opportunity, risk = get_opportunity_and_risk(info_list, has_new_files=True)
            workflow_priority = get_workflow_priority(info_list, has_new_files=True)
            lines.append("## 🧭 主编视角")
            lines.append(f"- {editor['theme']}")
            lines.append(f"- {editor['priority']}")
            lines.append("")
            lines.append("## 📈 今日机会提醒")
            lines.append(f"- {opportunity}")
            lines.append("")
            lines.append("## ⚠️ 今日风险提醒")
            lines.append(f"- {risk}")
            lines.append("")

        lines.append("## 🎯 今天最值得看的内容")
        for info in info_list:
            lines.append(f"### {info['title']}")
            if info.get("tags"):
                lines.append(f"**标签**：{' / '.join(info['tags'])}")
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

        lines.append("## 🎯 结合你当前工作的今日重点")
        lines.append(f"- {get_personal_focus_hint(info_list)}")
        lines.append(f"- {workflow_priority}")
        lines.append("")
    else:
        topic = pick_fallback_topic()
        opportunity, risk = get_opportunity_and_risk([], has_new_files=False)
        workflow_priority = get_workflow_priority([], has_new_files=False)
        lines.append("## 🧠 今日发散思考（24 小时内无新增）")
        lines.append(f"### {topic['title']}")
        lines.append("")
        lines.append("## 📈 今日机会提醒")
        lines.append(f"- {opportunity}")
        lines.append("")
        lines.append("## ⚠️ 今日风险提醒")
        lines.append(f"- {risk}")
        lines.append("")
        lines.append("**核心启发**")
        for t in topic["thinking"]:
            lines.append(f"- {t}")
        lines.append("")
        lines.append("**这对你今天的工作有什么帮助**")
        for hp in topic["work_help"]:
            lines.append(f"- {hp}")
        lines.append("")
        lines.append("**我的判断**")
        if "产品" in topic["title"] or "APP" in topic["title"]:
            lines.append("- 你现在最该补的，不是再看更多文章，而是把产品研发闭环真正沉淀进知识库和 Agent 工作流。 ")
        elif "Skill" in topic["title"] or "Agent" in topic["title"]:
            lines.append("- 你现在的复利点在于把重复动作抽成 Skill，而不是继续依赖临场发挥。")
        else:
            lines.append("- 这条主题最有价值的地方，在于它能否进入你的日常系统，而不是停留在理念层。")
        lines.append("")
        lines.append("**今天建议动作**")
        if "产品" in topic["title"] or "APP" in topic["title"]:
            lines.append("- 挑一个当前版本问题，把“需求—埋点—反馈—复盘”补成一页持续更新的产品知识页面。 ")
        elif "Skill" in topic["title"] or "Agent" in topic["title"]:
            lines.append("- 从最近一周重复做过 3 次以上的动作里，挑 1 个抽成 Skill 或检查清单。")
        else:
            lines.append("- 从现有 wiki 里挑 1 个高频主题，补一条“可执行方法”或“检查清单”，让知识进入工作流。")
        lines.append("")
        lines.append("## 🎯 结合你当前工作的今日重点")
        lines.append(f"- {workflow_priority}")
        lines.append("")

    lines.append("## ☕ 晨间一句话")
    if new_files:
        lines.append("- 今天更值得做的是“把新增内容接进你的系统”，而不是只把它读完。")
        lines.append("- 真正的复利，来自知识回写、流程沉淀和工作流持续进化。")
    else:
        lines.append("- 今天更值得做的是“让旧知识进入工作流”，而不是继续囤新资料。")
        lines.append("- 旧知识一旦被接进产品研发和 Agent 流程，才会真正开始产生价值。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("💡 提示：用 /compile 编译新文章，用 /lint 检查知识库健康")
    lines.append("")

    return "\n".join(lines)



def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        import json
        entries = get_recent_log_entries()
        new_files = get_new_raw_files()
        payload = {
            "entries": entries,
            "new_files": new_files,
            "preview": generate_markdown(),
        }
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(generate_markdown())


if __name__ == "__main__":
    main()
