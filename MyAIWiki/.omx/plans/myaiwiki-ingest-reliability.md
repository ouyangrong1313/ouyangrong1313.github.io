# MyAIWiki 摄取可靠性优化计划

## 目标

在不引入来源未确认的 `WikiSkill` 或 `SKILL.state` 前提下，把现有 MyAIWiki 摄取流程升级为：原文可追溯、正式条目符合 schema、每一步可恢复、质量门禁可自动判定。

## 现状与依据

- `.ai-wiki-schema.md:24-43` 要求每次摄取写入完整原文、digest、带 frontmatter/关联图谱的 wiki 页面、索引和日志。
- `scripts/compile_wechat_to_wiki.py:166-208` 仍生成“自动编译草稿”、`## 要点列表` 和待补充关联，未满足上述正式页面合同。
- `scripts/ingest_wechat_article.py:31-42` 可直接覆盖 digest/wiki，且没有可恢复状态、产物哈希或发布门禁。
- `scripts/wiki-health-check.py:285-350` 已检查 frontmatter、链接和索引，但不验证 raw 是否为完整正文，也不区分草稿与可发布条目。

## 方案决策

采用“现有脚本增强 + repo 内显式状态文件”方案：以 `.wiki-state/ingests/<source-hash>.json` 保存可重建的摄取状态，不安装 `SKILL.state`；继续使用现有节点、图谱和 ripgrep 检索体系，不替换为外部 WikiSkill。

### 不选的方案

- **直接安装 WikiSkill / SKILL.state**：具体实现、维护状态和数据格式尚未确认，且 Wiki 方法论已被当前 schema、查询和健康检查覆盖。
- **仅靠 `log.md` 恢复**：日志适合审计，不包含阶段、输入哈希、产物哈希、失败原因和可安全重试条件。

## 验收标准

1. 对任一成功 WeChat 摄取，`raw/<slug>.md` 保存抓取到的完整正文、来源 URL、作者、发布时间、抓取时间与抓取方式；正文为空或异常页时零写入。
2. 正式 `wiki/<category>/<slug>.md` 具备 `title`、`category`、`tags`、`nodes`、`links`、`date`、`source`，且含“关联图谱”三个子段。
3. 每次摄取生成唯一状态文件，记录 `fetched`、`drafted`、`polished`、`validated`、`published` 或 `failed` 状态、输入 URL 哈希、产物路径/哈希与错误摘要。
4. 相同 URL 重跑默认复用已验证产物；正文哈希改变或显式 `--force` 才允许新版本/覆盖，并将原因写入状态和日志。
5. 发布前 health checker 对新条目零 error；未解析链接、缺少 inbound/索引、草稿标记或 raw 截断作为显式 warning/blocker，不以伪造关联消除告警。
6. 完整流程、失败重试和重复 URL 都有脚本级自动测试；不访问真实 WeChat 或个人浏览器数据。

## 实施步骤

1. **定义产物与状态合同**
   - 新增 `scripts/wiki_ingest_state.py`：状态读写、URL 规范化、SHA-256、原子写入和状态转移校验。
   - 新增 `.wiki-state/README.md`：仅保存元数据和哈希，不保存会话、Cookie、正文或凭据；将 `.wiki-state/*.json` 的保留/忽略策略写入 `.gitignore` 或仓库文档。
   - 更新 `.ai-wiki-schema.md`：明确 `raw` 是完整正文，定义 draft 与 published 的界线及状态文件字段。

2. **修复原文保真与幂等性**
   - 更新 `scripts/build_wechat_raw.py`、`scripts/write_wechat_raw.py`：优先使用 `content_text`，保存完整正文与 fetch metadata；检测空正文、环境异常、明显截断并在写入前失败。
   - 更新 `scripts/fetch_wechat_article.py`：输出稳定的正文来源字段和内容哈希输入，保留 isolated Chrome 作为临时 profile，不读取用户浏览器资料。
   - 为 slug 冲突和正文变更提供明确策略：默认跳过已验证同 URL，`--force` 仅在状态记录中写明覆盖原因。

3. **将编译脚本拆为草稿与发布两阶段**
   - 重构 `scripts/compile_wechat_to_wiki.py`：只负责结构化 draft，生成符合 frontmatter 的初始页面并标记 `status: draft`；不再把模板化摘要伪装成正式 wiki。
   - 更新 `scripts/ingest_wechat_article.py`：写入 `fetched -> drafted`，`--apply-polish-output` 先校验 Markdown 合同再转为 `polished`。
   - 更新 `scripts/build_wechat_polish_prompt.py` 和 `scripts/apply_wechat_polish_output.py`：要求 5-10 节点、真实现有内链、三段图谱、证据边界；禁止写入未通过解析的输出。

4. **建立发布门禁与健康检查扩展**
   - 扩展 `scripts/wiki-health-check.py`：新增 raw 正文长度/元数据检查、`status: draft` 检查、正式页面图谱段检查、`links` 存在性与新页面入站引用的报告。
   - 增加 `--scope <slug>`，使单篇摄取只检查受影响页面、索引和链接；全库 lint 保留现有行为。
   - `ingest_wechat_article.py` 只在 scoped health check 无 error 后更新分类索引、总索引和 `log.md`，然后将状态设为 `published`。

5. **补齐测试与迁移策略**
   - 新增 `scripts/tests/test_wiki_ingest_state.py`：合法/非法状态转移、URL 去重、哈希变化、原子状态文件恢复。
   - 新增 `scripts/tests/test_wechat_ingest_contract.py`：完整 raw、空正文拒绝、draft frontmatter、polish 输入校验、失败不污染索引/日志。
   - 新增 `scripts/tests/test_wiki_health_contract.py`：raw 缺失、draft 误发布、缺关联图谱、死链、索引遗漏、分类不匹配。
   - 保留存量页面兼容：只将新条目强制纳入发布合同；健康检查将历史债务分类报告，不自动大规模重写。

6. **把日常操作收敛为两个命令**
   - 更新 `.codex/skills/compile-link/SKILL.md`：`preflight -> ingest draft -> polish -> scoped validate -> publish`，而不是抓取成功就报告完成。
   - 更新 `.codex/skills/wiki-health/SKILL.md` 和 `CLAUDE.md`：说明单篇发布检查、每月全库 lint、状态恢复与日志职责。
   - 新增 `scripts/wiki-ingest-status.py <url-or-slug>`，输出当前阶段、产物、错误和下一条安全可执行命令。

## 验证顺序

1. 单元测试：`python3 -m unittest discover -s scripts/tests -p 'test_*.py'`。
2. fixture 集成测试：成功抓取、空正文、环境异常、重复 URL、polish 不合格、链接不存在、状态中断恢复。
3. 对一个现有 fixture 执行 dry run，确认不会写入真实 `raw/`、`wiki/`、索引或日志。
4. 对一篇新的低风险文章执行真实摄取，确认原文、状态、正式页、两个索引和日志一致。
5. 执行 `python3 scripts/wiki-health-check.py --strict` 与 `python3 scripts/normalize_raw_archive.py --check`；将历史遗留 warning 与本次引入 warning 分开报告。

## 风险与缓解

- **抓取正文被公众号截断**：以内容长度、异常词和标题/正文一致性作为失败门槛；失败不写正式产物。
- **过度严格阻塞旧库**：规则按 `status: published` 和新写入日期生效，存量只报告债务。
- **状态文件成为第二事实源**：状态仅记录过程和哈希；页面、索引和日志仍是知识库的内容事实源。
- **自动生成伪造关联**：只接受实际存在的页面链接；不确定时保留 warning 和人工待补项。

## 停止条件

当新文章能从抓取失败安全退出、从任一步恢复、在发布前通过结构门禁、在发布后可由状态/索引/日志交叉追溯时，优化完成。外部 `WikiSkill` 或 `SKILL.state` 只在拿到其具体 `SKILL.md` 后重新评估是否局部吸收。
