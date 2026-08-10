---
title: 实战从零开始构建一个Coding Agent：Violin
slug: 实战从零开始构建一个Coding-Agent-Violin
source: 微信公众号 / 得物技术
url: https://mp.weixin.qq.com/s/yFHRoAi6fe2dduXXlM8Tzw
pub_date: 2026-08-05
fetch_date: 2026-08-06
公众号名: 得物技术
作者: 酒米
---

# 实战从零开始构建一个Coding Agent：Violin

> 原文作者从零实现一个 Zig coding agent「Violin」，用它拆解现代 coding agent 的核心构件。本文保留正文、关键伪代码与协议示例；原文中的架构图、工具清单和部分代码截图以图片资源链接保留。

## 目录

1. 背景
2. 效果预览
3. 整体架构
4. 分层实现介绍
5. 总结

## 一、背景

从 24 年冬天开始，各类 coding agent 层出不穷——从 Gemini CLI 的起步，到 Claude Code 的尝试，再到如今 Codex、OpenCode、PI、Qoder 等百花齐放。

短短一年多的时间，agent 从大模型的一个附属品，逐渐演变成模型能力的放大器，成为 AI 工程化的关键载体。市面上各类业务 agent——客服、数据分析、工作流编排等——追根溯源，基本都是 coding agent 的泛化变种。

理解了 coding agent 的构建原理，也就掌握了理解其他 agent 的一把钥匙。笔者对每天都在使用的 agent 原理很感兴趣，于是决定自己写一个：Violin。

## 二、效果预览

虽然有点丑，但是基本的功能（多模态、skill、插件）已经完备了。

## 三、整体架构

Violin 的架构设计深度借鉴了 Pi 的设计理念。Pi 作为一个 TypeScript 实现的 AI coding agent，其最突出的特点是简洁而可扩展的架构：三层分离（模型适配层 / 内核层 / 产品层）、EventBus 事件驱动、工具注册表和插件系统，每个模块各司其职且松耦合。

Pi 的代码完全开源，不仅让 Violin 有了一个扎实的参考蓝本，也让它本身成为一个 Agent 工程学习范本：代码结构清晰、注释详尽、每层职责明确。作者推荐通过 `how-pi-agent-works` 学习 Pi 架构。

Violin 保持这一架构精髓，同时用 Zig 替换 TypeScript，在内存安全和性能上做进一步探索。

### Why Zig?

既然每一层通过接口或网络协议解耦，不同层使用不同语言是可行的，不需要也不可能全部用一种语言写完。

- Agent Loop、模型适配、会话管理等底层引擎用 Zig 实现，追求性能和内存可控性。
- Client 端用 Python 实现，利用 Python 生态快速搭建终端交互 UI。
- 两者通过 TCP + JSON Lines 协议通信，Server 不关心 Client 使用什么语言。

### 每层为什么存在

#### ai：把供应商拍平

不同模型 API 对工具调用、推理内容、缓存、错误、OAuth、流式协议的表达都不同。Violin 把这些差异统一成 `Message`、`Tool`、`AssistantMessageEvent` 和 `streamSimple()`，上层 Agent Loop 不需要知道是 Anthropic 的 `tool_use` 还是 OpenAI Responses 的 `function call`，只处理统一后的 `toolCall` 内容块。

#### agent-core：只管 Agent 运行时

内核层只负责 Agent 的运行循环，不关心消息从哪里来，也不关心执行结果存到哪里。

#### product：把 Agent 变成可用产品

写一个 Agent Loop 不难，难的是把它变成每天能用的开发工具。产品层负责会话历史加载和保存、上下文压缩后的重试、Arena 内存管理等麻烦但关键的事情。

#### server：把 Agent 能力包装为 TCP Server

为了让客户端实现与语言无关，需要把 agent 能力包装为通信协议和 TCP Server。TCP Server 具备流式通信和全双工能力，适合这个场景。

## 四、分层实现介绍

### 1. Agent Loop：一切的核心

Agent Loop 是一个 while 循环，在「问模型」和「执行工具」之间来回切换，直到模型给出最终答案。它不关心模型是 OpenAI 还是 Anthropic，也不关心工具是读文件还是跑命令，只关心两件事：模型要不要调工具；如果要，调完继续问，如果不要，结束。

核心伪代码：

```zig
while (turn < max_turns) : (turn += 1) {
    const assistant = try model.complete(.{
        .messages = messages.items,
        .tools = tool_registry.definitions(),
    });

    const has_tool_calls = assistant.toolCalls().len > 0;
    if (!has_tool_calls) break;

    for (assistant.content) |block| {
        if (block == .tool_call) {
            const result = tool_registry.execute(tc.name, tc.args);
            messages.append(result); // 回写给模型
        }
    }
}
```

需要注意：

- `max_turns` 是安全阀，防止模型陷入无限工具循环。
- 工具结果必须追加回 `messages`，模型需要看到结果才能决定下一步。
- `tools` 定义要传给 `complete()`，模型必须提前知道可用工具。
- LLM 调用和工具调用都可能失败，Agent Loop 需要先区分错误类别，再决定是否重试。

Agent Loop 只关心循环。会话历史的加载和保存、上下文压缩后的重试、Arena 内存管理由产品层 `product/agent.zig` 封装：它调用 `loop.run()` 时传入历史消息，返回后把新消息持久化到 Session，并在 `ContextOverflow` 时截断上下文后重试。

### 2. AI 模型适配层：Agent Loop 调用的是谁

模型适配层的职责是把不同 LLM Provider 的 API 差异封装在一个 `Model.complete()` 接口后面。Agent Loop 只认这个接口，不关心背后是 OpenAI 还是 Anthropic。

```text
interface ModelAdapter {
    complete(input: CompleteInput) -> AssistantMessage
    name() -> string
}

struct CompleteInput {
    system_prompt: string
    messages: Message[]
    tools: ToolDefinition[]
    max_tokens: int
    temperature: float
    stream_callback: optional callback
}
```

Zig 没有 trait 和虚函数，实际实现使用函数指针表。每个适配器提供 `complete`、`name`、`deinit` 三个函数指针，通过统一接口调用；适配器内部状态（如 `base_url`、`api_key`）通过类型擦除的指针在回调中还原。

Violin 适配了两种主流 LLM 协议。两个适配器都要处理 JSON 序列化、HTTP 请求、SSE 流式解析和错误映射，差异主要在：

- 请求体格式：OpenAI 使用 `messages[]`，Anthropic 使用 `content[]`。
- 工具调用结构：OpenAI 使用 `tool_calls[]`，Anthropic 使用 `content[]` 中的 `tool_use` block。
- 流式协议：OpenAI 使用 `data:` 行，Anthropic 使用 `event:` 行。

为了避免用户等待完整回答，Violin 采用 SSE 流式输出：模型适配器收到每个 chunk 后调用 `stream_callback`，Agent Loop 通过 EventBus 发射 `message_update`，Client 收到事件后实时追加到终端显示。

模型配置不内置在程序中，而是从 `~/.violin/agent/models.json` 加载，再由客户端决定使用哪个模型：

```json
{
  "providers": {
    "openai": {
      "base_url": "https://api.openai.com/v1",
      "api": "openai-completions",
      "api_key": "$OPENAI_API_KEY",
      "models": [
        {"id": "gpt-4o", "name": "GPT-4o", "contextWindow": 128000}
      ]
    }
  }
}
```

### 3. Tool System：Agent Loop 的手和脚

模型适配层让 Agent Loop 可以调用任何模型，工具系统让 Agent Loop 可以做任何事。

工具定义包含名称、描述、JSON Schema 参数和执行函数：

```zig
pub const Tool = struct {
    name: []const u8,
    description: []const u8,
    parameters: []const u8, // JSON Schema
    execute: ToolExecuteFn,
};
```

Violin 内置 6 个基本工具，和 Pi 的设计保持一致。工具注册表使用 HashMap 按名称存储工具；`definitions()` 把工具列表编码为模型可识别的 JSON Schema，`execute()` 按名称找到工具并执行。

```text
register(name, description, execute_fn)
get(name) -> Tool
definitions() -> ToolDefinition[]
execute(name, args) -> ToolResult
```

### 4. Product 层：循环之外的事

#### agent.zig：胶水层，但最关键

`product/agent.zig` 只有 123 行，却把整个项目粘起来：

1. 从 Session 加载历史消息。
2. 传给 `loop.run()` 执行。
3. loop 返回后，把新消息保存到 Session。
4. 如果 loop 抛出 `ContextOverflow`，调用 compaction 压缩后重试。

```text
history = load_history(config.session)
while True:
    loop_result = loop.run(model, history, user_input)
    if loop_result == ContextOverflow:
        compact_session()
        continue
    for msg in loop_result.new_messages:
        session.appendMessage(msg)
    return AgentResult(text=loop_result.final_text)
```

#### session.zig：对话的记忆

没有 Session，Agent 每次对话都是失忆的。Violin 使用 JSONL 存储会话：第一行是会话头（`id`、`created_at`、`cwd`、`model`），后续每行是一条消息。消息通过 `parent_id` 组成树结构。

`SessionStore` 包含：

- `file_path`：JSONL 文件路径。
- `entries`：按 ID 索引消息，支持随机访问。
- `leaf_id`：当前叶子节点。
- `next_id`：生成新消息 ID。
- `header`：会话头信息。

实际 Zig 实现使用 ArenaAllocator 统一管理内存，`deinit` 时一次释放。写入时先序列化成 JSON 行并写临时文件，再追加到会话文件；恢复时遇到损坏消息行会记录日志并跳过，不让整个会话崩溃。Pi 的 Session 也是 JSONL + 树结构，支持分支 fork 和回滚，Violin 继承了这些能力。

#### compaction.zig：对话的脑容量管理

当 token 超过阈值时，把旧消息压缩成一条摘要，保留最近 N 条消息。默认阈值是 100K token，保留最近 10 条消息，摘要目标长度为 500 token。

为了避免引入 tokenizer，Violin 用字符数除以 4 近似 token 数：

```zig
pub fn estimateTokens(text: []const u8) usize {
    return text.len / 4;
}
```

压缩前是 `[消息1] [消息2] ... [消息N]`，压缩后是 `[摘要：之前讨论的要点] [消息N-9] ... [消息N]`。旧消息会被拼接后交给模型生成摘要，再与最近消息一起继续执行 loop。

### 5. Resources：为 Agent 注入规则和技能

`resources.zig` 从文件系统加载项目规则和技能，解析 frontmatter，并格式化成 system prompt 注入 LLM，让模型知道可用工具和能力。

项目规则优先级从高到低：

```text
{cwd}/AGENTS.md
{cwd}/CLAUDE.md
~/.violin/agent/AGENTS.md
~/.violin/agent/CLAUDE.md
```

技能路径是项目先、全局后，同名冲突时项目赢：

```text
{cwd}/.agent/skills/*/SKILL.md
{cwd}/.agents/skills/*/SKILL.md
~/.violin/agent/skills/*/SKILL.md
```

每个 Skill 包含名称、描述、文件路径、来源（global/project）和原文内容。`SKILL.md` 的 YAML frontmatter 会被解析并构造成 XML，注入到系统提示词的 `<available_skills>` 中。

### 6. Event System：插件实现的基础

Agent Loop 运行时，外界需要知道它进行到哪一步。事件系统让 Agent Loop 在开始一轮、生成 token、调用工具时向 EventBus 发事件，关心事件的组件注册回调。

作者最终选择 Lua 作为插件语言，不是因为 Lua 最好，而是因为它是最小的正确选择：约 500KB 运行时、长期嵌入场景成熟、可以通过 C 函数调用，适合 Zig 项目。

EventBus 有三个回调槽：`agent`、`session`、`compaction`。`install()` 保存原回调并换成自己的 dispatch 包装函数：先执行原回调（例如把流式结果写给客户端），再遍历已注册 Lua 插件，逐个调用 hook。

示例插件 `bash-guard`：

```lua
return {
  name = "bash-guard",
  version = "0.2.0",
  description = "拦截危险 bash 命令，自动加安全前缀",
  on_tool_start = function(event)
    if event.tool_name == "bash" then
      if event.arguments:find("rm -rf", 1, true) then
        return { action = "block", reason = "危险命令已阻止" }
      end
      return { action = "modify", arguments = "set -e; " .. event.arguments }
    end
  end,
  on_context = function(event)
    return { action = "modify", inject_text = "使用 bash 时注意安全", inject_role = "system" }
  end,
}
```

插件可以在工具执行前阻止或修改参数、在工具执行后修改结果、在 LLM 调用前注入系统指令，也可以阻止 Agent 启动或手动压缩会话。

### 7. 网络层：客户端实现的基础

网络层定义 Violin 客户端与服务端的通信：客户端发送消息，服务端把思考过程、工具调用和最终回答逐条推送。

大多数 Coding Agent 是一体式进程，Agent 引擎、UI、会话、模型和工具都在一起。Violin 选择前后端分离：

```text
一体式：[agent + UI + 会话] —— 一个本地进程
Violin：[Zig 服务端 daemon] <— TCP/JSON-Lines —> [Python TUI 客户端]
```

这个设计受到 ACP 协议启发，但由于 ACP 复杂且 Zig 缺少成熟实现，Violin 这个 toy 项目选择了更小、更容易实现的 TCP + JSON Lines。只要把通信协议交给 AI，也可以用其他语言实现客户端。

核心协议包括：

#### 握手

```json
// 客户端 -> 服务端
{"type":"handshake","cwd":"/home/user/project/violin"}

// 服务端 -> 客户端
{"type":"models_result","models":[...],"default":"deepseek-v4-flash"}
{"type":"skills_result","global_skills":[...],"project_skills":[...]}
```

`cwd` 用于加载 `{cwd}/.agent/skills/` 并注入系统提示词。

#### 聊天请求

```json
{"type":"chat","content":"列出目录下文件","model":"deepseek-v4-flash"}
```

可选字段包括 `session_id`、`temperature`、`max_tokens`、`system_prompt` 和 `images`。

#### 事件流

Violin 设计了 8 个事件类型来支持完整对话：`turn_start`、`delta`、`tool_start`、`tool_end`、`turn_end`、`result`，以及错误和保活相关的 `error`、`ping`。

一个完整流大致是：客户端发送 `chat`；服务端发 `turn_start` 和上下文用量；连续发 `delta`；工具执行前发 `tool_start`，执行后发 `tool_end`；继续发 `delta`；最后发 `turn_end` 和 `result`。

### 8. Python Client 实现

Python Client 的核心是 async TCP 连接和事件分发器：

```python
class ViolinClient:
    def __init__(self, host="127.0.0.1", port=9877):
        self.reader = None
        self.writer = None
        self.models = []
        self.session_id = ""
        self.on_delta = None
        self.on_tool_start = None
        self.on_tool_end = None
        self.on_result = None

    async def connect(self, retries=3):
        for i in range(retries):
            try:
                self.reader, self.writer = await asyncio.open_connection(*self.addr)
                await self._send({"type": "handshake", "cwd": os.getcwd()})
                msg = await self._read_msg()
                if msg and msg.get("type") == "models_result":
                    self.models = msg.get("models", [])
                    return True
            except ConnectionRefusedError:
                await asyncio.sleep(0.5 * (2 ** i))
        return False
```

事件分发器持续读取 socket，按 `type` 调用 `on_delta`、`on_tool_start`、`on_tool_end` 和 `on_result` 回调；收到 `error` 返回错误，收到 `ping` 则发送 `pong`。

## 五、总结

coding agent 的核心没有什么魔法。剥开花哨的 UI 和功能，底层就是一个 while 循环：问模型、拿结果、判断要不要调工具、调完再问。Violin 的每一层都是在给这个循环补齐工程能力：

- 模型适配层解决「问谁」。
- 工具系统解决「能干嘛」。
- 资源层解决「记不记得住、SKILL 在哪」。
- 插件解决「能力扩充」。

这个玩具距离成熟 Coding Agent 还有未填的坑：`buildJson` 里的 tools 参数还没有序列化，模型根本收不到工具定义；插件没有权限隔离，Lua 可以做任何事；ACP 协议也没有接入，暂时只能自己跟自己玩。

但作为一个从零搭起来的 toy agent，项目的目的不是交付商用产品，而是验证一个判断：理解 coding agent 的构建原理，也就掌握了理解其他 agent 的一把钥匙。

模型统一适配、工具注册与调度、会话持久化与恢复、上下文压缩与保留、插件注入与拦截，看似互不相干，底层都收敛到同一个循环：问模型、调工具、再问。客服 agent 的会话管理、数据分析 agent 的工具链编排、工作流 agent 的状态机设计，都是这个循环在不同场景下的变形。

剩下的坑既是项目当前的边界，也是下一段探索的起点。把 toy 项目一路补到能真正落地，过程本身就是学习方式。

## 原文图片资源

原文包含 22 张图片/截图，以下保留资源地址，供回看架构图、工具清单和代码截图：

1. http://mmbiz.qpic.cn/mmbiz_gif/AAQtmjCc74DZeqm2Rc4qc7ocVLZVd8FOASKicbMfKsaziasqIDXGPt8yR8anxPO3NCF4a4DkYCACam4oNAOBmSbA/640?wx_fmt=gif&wxfrom=5&wx_lazy=1
2. https://mmbiz.qpic.cn/mmbiz_png/FMFU1P6sHHtu8A0jXbeU0vhiavdvI612Kq9dNExlibC9KtCr7jahnBIWecLMC4FAE8wdPL2WV7rn2ZEGXC7N95UUIpfrEkflhL4ichKmceeHFQ/640?wx_fmt=png&from=appmsg
3. https://mmbiz.qpic.cn/sz_mmbiz_png/FMFU1P6sHHvmhFXdiafsvdcOP4WJ9scNLK1YibpdDNCDf8Y9nTYC0TAg7vK11JhrKL3PrtTJSsHlzZWTaGE2icj1w1pHtqh3NSxxmMpYPCSszo/640?wx_fmt=png&from=appmsg
4. https://mmbiz.qpic.cn/mmbiz_png/FMFU1P6sHHvSosQz3tUF7ndghx1qhNVrg9m5NfyuDFJqzDiaV8zTDOtoCfwIPib8ib7cB5g8DPmadGQdY9GYlztyGqIxoCHg0iaoBxWoSDIYG84/640?wx_fmt=png&from=appmsg
5. https://mmbiz.qpic.cn/sz_mmbiz_jpg/FMFU1P6sHHsvMkdOD8WXHsiboZUq6dD5M7VUicUicNxjgvgAhBC5JusiaLaKOTazn583Bicibujt83NwRurxNaicylIEnZaxBTYmbXRudfzd4OibOs0/640?wx_fmt=jpeg&from=appmsg
6. https://mmbiz.qpic.cn/sz_mmbiz_jpg/FMFU1P6sHHsKmjoF9ziaLXayzG5R1HVvib5Xeich6JACd5qMUGibiaX01aFyesNSiaEpicHwoDgd7gIW4SxXxNww9t2h7LmxcNqLdtZicj54GkFibicbw/640?wx_fmt=jpeg&from=appmsg
7. https://mmbiz.qpic.cn/sz_mmbiz_png/FMFU1P6sHHsBXa73ySKxmcbAhrWPzVO14iaqvaQxUBxAOc6SoSZiahJI6djqkvibNd5apDZFuTzTbyveDKr1VYkOdGcI16ibA1rZg5h2Oicl6mBM/640?wx_fmt=png&from=appmsg
8. https://mmbiz.qpic.cn/mmbiz_png/FMFU1P6sHHtLZJhn3MkldSMDoLHwsLbric9tsq4kucPNbpJ061CZRS1lmibJNc02H4lpl4IoEBKnqsNAtPTVnbmrJLUrJ76dUrEYTApPejqBk/640?wx_fmt=png&from=appmsg
9. https://mmbiz.qpic.cn/sz_mmbiz_png/FMFU1P6sHHsrM4S0klGLDv874wlhOqlDWl96CNR6eZLZNzrF8eBL6Z6vZMbOv47akicOCiaPofEDcOn2By52DeC9osylS9ZPxI3VnQmIlesxs/640?wx_fmt=png&from=appmsg
10. https://mmbiz.qpic.cn/sz_mmbiz_png/FMFU1P6sHHvZZhaQgoPNdxcmcoLftK0jQyUSjryiaTjTAFLXPrsxd8UB3MkAhcWMQUuxYaOWeQsxIicqLoYHURY2lnGx7wyoAGtBibISI0Hnck/640?wx_fmt=png&from=appmsg
11. https://mmbiz.qpic.cn/sz_mmbiz_png/FMFU1P6sHHvODE8TMmQDKNibvW3dvMvm2iay12cYwWJicH4L5WdHptjhuZ1mfZLicAVRhH9HguapIticRpHAwUYxaicz0UcqOyUTvhqBtrgJn1kGA/640?wx_fmt=png&from=appmsg
12. https://mmbiz.qpic.cn/mmbiz_png/FMFU1P6sHHs9LYbNUNdHricK0XcugqIVb1BXQyo9UHiaWC6OiaQstG24icS6aQqXLH8csHc0piaDKjgBUhy8lxrEZ6tMrxGTjymCMFibfNuHoVpuA/640?wx_fmt=png&from=appmsg
13. https://mmbiz.qpic.cn/mmbiz_png/FMFU1P6sHHsQgdnFWqZXadPzYjagpiaJrcCibLpqGzETTg27yIAjroGgs9Snz20icHGyHQu6ia0IzMqwqKZ1TNYrgpj124IZmHaeiaDt9ibg3Iicog/640?wx_fmt=png&from=appmsg
14. https://mmbiz.qpic.cn/sz_mmbiz_png/FMFU1P6sHHvdQyY9ao8o0x2RicPBwCsriaZG0gBqoJGOoEJTIicJDTLY5UeibZX6TV9CQciayxgzMHfbYF1AkI0jLkTflpyY0UCKTYP3ZfuGwIT4/640?wx_fmt=png&from=appmsg
15. https://mmbiz.qpic.cn/sz_mmbiz_png/FMFU1P6sHHuPuzExCNTS0iaw2vHiaiaVicaibPSnK4qdgaQk1IUG7J1gAe295od0c4mzic0xYcQLNcKTcnwyOic9UDG67BL4yGnn6lU9ksup8YPibFU/640?wx_fmt=png&from=appmsg
16. https://mmbiz.qpic.cn/sz_mmbiz_png/FMFU1P6sHHvpE8iaQznJLwDNwqibezia4HS9vq0jskyaCpVlQCrP9zM8B96icdP3lf6rGUiboLVglkWJXCfdCZGuYBDzBGBSbibrz2yOoibZdibRudw/640?wx_fmt=png&from=appmsg
17. https://mmbiz.qpic.cn/sz_mmbiz_png/FMFU1P6sHHsvTEhFslr49614ClDc3IiahgeAc7hIia1p8uY9xuuJOMu7fKI9QwKagCjpMiaMFrBMLIwW76ZQGOxDpR9Gj6ULXLGRtYAwHkPWr4/640?wx_fmt=png&from=appmsg
18. https://mmbiz.qpic.cn/mmbiz_jpg/FMFU1P6sHHus07xjDkXDdt6kW7ws6gU6y9HrQ2nWpO9FY8pLuqXb7zicOevqAOQfKxuicdHBbiczUribJGnIqicO3ZJXcr2SYdGJKXf1LhEDRYMw/640?wx_fmt=jpeg&from=appmsg
19. https://mmbiz.qpic.cn/sz_mmbiz_png/FMFU1P6sHHuibT7zfuHxKX5hllkzPIrSnuynqiauqbSn1IxuoE0cBia38N4ib2rSLz1E2mDUtt8mdibmxmibmIDfx68PbwzajVCN9dQjSsnkW7ibnQ/640?wx_fmt=png&from=appmsg
20. https://mmbiz.qpic.cn/sz_mmbiz_png/FMFU1P6sHHs9kjCeicQUk035BKLOpATuk8SakTSbnZGfiblbRCoa2nqMOT7t6k63v5P7YN9YFeDHRHmmianxTsPrJsKYbVUOicVo5n5E18ibL9gY/640?wx_fmt=png&from=appmsg
21. https://mmbiz.qpic.cn/mmbiz_png/FMFU1P6sHHspMj37LxD2rw4TxDGYP7VMWoItQwOv2aUTlm4MXhib46zOiaCvOwnmr9oq1XwYtaXYNqOOdTfh7d1qicT4pkERetVFf0icZqpVB6k/640?wx_fmt=png&from=appmsg
22. https://mmbiz.qpic.cn/mmbiz_jpg/FMFU1P6sHHtsvIX9aTv3uzeDWKTQIicFd2A5htgQhAXSk8mlFkmqxznOZP2oTOf7atSxjOrjdxLAiaQmibicBVI5c9C9XIzTAaa7Ot2iaB36pwUA/640?wx_fmt=jpeg&from=appmsg

标签：#主题/AI-Agent #主题/AI-Coding #主题/Agent-Loop #主题/Agent-架构 #主题/Skill #主题/插件系统 #节点/Agent-Loop #节点/模型适配 #节点/Tool-System #节点/Session #节点/Context-Compaction #节点/EventBus #节点/TCP-JSON-Lines #场景/公众号长文
