# Warp CEO 的 Claude 实战教程：两个 Skill 让 Agent 自我改进

**来源：** 微信公众号「Datawhale」
**作者：** Warp CEO（Datawhale 整理）
**发布日期：** 2026-08-31 22:30
**链接：** https://mp.weixin.qq.com/s/vIJ5uP5dcUd87Smi2BuP-w
**原始案例：** https://claude.com/blog/how-warp-builds-self-improving-agents-on-claude

---

## 正文

Warp 公开了自己搭自我改进 Agent 的实战方法：两个 Skill 文件，中间夹一条人类反馈，就能让 Agent 从每次错误里沉淀知识、越用越聪明。Warp 的开发团队用这套框架改进了一个噪声缠身的 code review Agent。

该 Agent 第一轮约有 80% 的评论正确，剩余 20% 却是不相关评论、误判代码库惯例或低质量修改建议。工程师仍要在大量无用评论中筛选，负担反而很高。团队曾手动修改 prompt、补充 AGENTS.md；这些做法有帮助，却无法规模化。根因是反馈随单次对话结束而消失，下一轮 Agent 不会保留此前的教训。

### 两个 Skill 与一次反馈

Warp 用 Agent Skills 组织一个自我改进循环。Skill 是基于文件的程序性知识，Agent 可以在执行时查阅。

- **内层 Skill（base skill）**：保存特定任务的领域知识和指令。PR 打开时，code review Agent 用它和任务上下文完成审查。
- **人类反馈**：循环的关键输入。反馈越明确越有效，例如不只说“变量不该重命名”，还说明该代码库中此类全局变量有特定命名上下文。
- **外层 Skill（improver skill）**：按计划运行的观察者 Agent。它汇集人类反馈，比较原建议与人的回应，提出对 base skill 的最小、聚焦编辑。

Skill 是普通文件，因此改动可以像代码一样经由 PR、review、批准和合并。下一次执行自动继承已批准的改进。

Warp 将 Skill 与 Memory 区分开：Skill 是稳定、程序性的任务规范，改动是刻意且可版本化的；Memory 是 Agent 推理过程中的动态记录。像“如何做好 code review”这样的稳定知识应放入 Skill，以便审查和复用。该模式已用于 Warp 开源仓库的 spec-writing、review 和 triage Agent。

### Issue triage 案例

Warp 的 issue triage Agent 在 GitHub 新 issue 创建时启动，判断复杂度与可行性、添加标签并建议修复方向。其内层 Skill 定义标签含义及研究代码库的步骤。

一次分诊遗漏了 `ready to spec` 标签。维护者在 issue 上指出：当问题真实存在、即使 UI/UX 形态尚未确定，也应加上该标签，让贡献者可以开始产品和技术规格工作。

improver skill 在 Warp 的 Agent 编排平台 Oz 上按计划运行。它认证 GitHub，运行打包的 Python 脚本拉取近期有反馈的 issue，将信息汇总为 JSON 后读入上下文。随后 Agent 识别反馈信号，提出最小编辑，并创建修改内层 Skill 的 PR：满足上述条件的 issue 应打上 `ready to spec`。PR 描述信号来源和修改内容，经人工 review、批准、合并后，后续 triage 会继承这条知识。

### 六条 Skill 纪律

1. **写原则，不穷举规则**：把 Skill 当作教给聪明人的指导，例如“关注重复代码”，而不是列尽所有变量命名规则。
2. **解释 why**：给出规则理由，让 Agent 能在未见过的场景中推理和泛化。
3. **让反馈零摩擦**：在 PR、issue 等已有工作现场收集反馈，避免额外提交步骤。
4. **保持 Skill 小且渐进披露**：引用资源文件和脚本，不要一次塞入全部上下文。
5. **重质量，也积累数量**：少量资深工程师的可解释领域反馈，通常比大量点赞更有价值；同时需要足够语料使改进稳定。
6. **重投入 improver skill**：它的结构跨 Agent 高度可复用，值得单独投入设计质量。

### 自我改进的边界

Warp 明确提醒：反馈可能错误，Agent 不应盲目接受。系统需要让 Agent 做合理性检查，过滤反馈来源，并在过滤或最终 review 保留人类在环。

领域也应具有验证路径。可验证任务应先建 harness，使用参考语料比较输出、修改并重复验证；存在 golden output 时优先用确定性评测。若必须依赖人类反馈，应限制为领域专家反馈。也不必让每个 Agent 都拥有独立 improver：可复用的 base loop 负责共性，再叠加领域权重，由少数 improver 管理多个 Agent。

自我改进不是只要建立循环就能自动变好。反馈质量、领域可验证性和人类控制位置若失守，系统会把错误经验系统化。

标签： #主题/AI-Agent #主题/自我改进 #主题/Skill #主题/人类反馈 #主题/Harness #场景/公众号长文
