# Matt Pocock Skills — 拆解分析

## 核心观点

1. **AI工具需要"固化工作流"而非"教规矩"** — 每天重复口述工作流是效率杀手，Matt的方案是直接把工作流打包成AI可执行的Skill
2. **"帮你干活"vs"教你干活"是本质区别** — 不教AI该怎么做，而是让AI直接执行完整工作流
3. **Skill有态度才有用** — 好用不是因为通用，是因为有强烈的个人工作偏好（信TDD、反对水平切片、信设计前多画几版）
4. **tracer bullet > 水平切片** — 先写所有测试再写所有代码是"crap tests"，正确做法是小步端到端
5. **design-it-twice原则** — 并行多Agent从不同约束出发设计，再对比组合，比单次设计质量高

---

## 分析角度

### 角度1：痛点共鸣
- 每个用Claude Code的工程师都经历过：重复对接口、重复讲测试、重复教Triage
- "明明是同一套活，每次都要重新对一遍" — 这个痛点精准
- 触发条件：技术博主粉丝，用过Claude Code有过挫败感

### 角度2：方案对比
- 市面已有方案：Addy Osmani agent-skills（工程纪律，教规矩）
- Matt方案：直接执行，不教规矩
- 对比表格清晰，立场鲜明

### 角度3：Skill分类展示
- 四分类（计划/编码/写作知识/元Skill）覆盖完整工作流
- 每个Skill名字即功能，清晰易懂
- 列举但不深入，留悬念

### 角度4：深度解读2-3个亮点Skill
- grill-me：解决AI动不动就问用户的毛病
- tdd：硬核观点"水平切片是crap tests"
- git-guardrails：连确认机会都不给

### 角度5：安装门槛低
- `npx skills@latest add xxx`
- 独立安装，不用一次装一堆
- 降低尝试门槛

### 角度6：与现有生态叠加
- 装了Addy Osmani？可以叠加
- agent-skills管"怎么做"，这套帮"做什么"
- 消除"装了会不会冲突"的顾虑

### 角度7：总结升华
- "好用不是因为通用，反而是因为有态度"
- "相当于把TypeScript大佬的工作习惯装进你的Claude Code"
- 有画面感，易传播

---

## 开头钩子

1. 用Claude Code写代码时，有没有过这种感觉——明明是同一套活，每次都要重新对一遍？

2. 你知道吗，TypeScript大神Matt Pocock把整套.claude目录开源了，30k star

3. 市面上的Claude Code Skill都在教AI"该怎么做"，但Matt Pocock做了一件相反的事——

4. AI写得太"自由"了：测试批量生成跟业务脱节，PRD没人整理，git push force直接把main送走

5. 为什么你装了那么多AI工具，效率还是上不去？

6. 一个观点正在传播：Skill有态度才有用，太通用的工具反而是浪费

7. 想象一下，如果把你的工作习惯直接"安装"进Claude Code——

8. 水平切片是TDD的毒药，这个TypeScript大神说出来了

9. git push --force谁都会，但怎么让Claude Code永远不给你机会按那个按钮？

10. design-it-twice原则：用3个Agent同时设计接口，然后对比挑最好的

11. 从"水平切片"到"tracer bullet"，一个认知升级

12. Matt Pocock的Skill不教你规矩，直接替你干活

13. 为什么GPT写代码比你快，但你总觉得"差那么一点"？

14. 一个问题：你的Claude Code装了多少Skill，但有多少是真正在用的？

15. "如果某个问题可以通过探索代码库得到答案，那就去探索代码库，不要问我。"——这句话解决了一个大问题

16. 装了Addy Osmani的agent-skills？别急着替换，这两套可以叠加

17. 你以为缺的是更多的AI工具，其实缺的是把你的工作流固化下来

18. 从"水平切片"到"垂直切片"，测试驱动开发的认知升级

19. 为什么说Skill不需要通用，需要有态度？

20. 想象你有一个TypeScript大神的工作习惯，24小时在线，永远不累

---

## 标签
#主题/AI Coding #主题/Claude Code #场景/技术博客 #手法/对比冲突 #手法/教程型

## 相关链接
- GitHub仓库：https://github.com/mattpocock/skills
- 原文：https://mp.weixin.qq.com/s/35B5cAQ9kA0LGAbFXrxCuQ