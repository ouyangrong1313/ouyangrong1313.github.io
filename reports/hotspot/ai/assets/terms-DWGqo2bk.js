import{g as e,t}from"./framework-HyhFslbv.js";import{$n as n,Tn as r,_t as i,n as a,r as o,t as s,tr as c}from"./shared-D5bjLq0b.js";var l=`# 使用规则

这是开源框架自带的模板。上线前请按你的实际情况改写（运营主体、允许和不允许的用途、联系方式），必要时请专业人士审阅。

| 项 | 值 |
|---|---|
| 版本 | 请填写 |
| 生效日期 | 请填写 |
| 运营主体 | 请填写 |
| 联系方式 | 请填写 |

页首说明：

> 本站聚合公开信源，用模型生成中文摘要与精选，原文版权归各来源所有。网页、RSS、公开 API 与 MCP 均可匿名使用。

## 1. 内容与版权

本站展示的标题、摘要和推荐理由由模型根据公开来源生成，可能有误，重要信息请以原文为准。原文版权归各来源所有；站内只在来源允许时展示全文，其余只展示摘要和原文链接。

## 2. 来源方的更正与下架

如果你是来源方，希望更正、下架或调整展示方式，请通过反馈页联系我们，我们会尽快处理。

## 3. 使用本站的数据

请写明你允许的用途（例如个人阅读、组织内部使用），以及需要事先取得你同意的用途（例如商业产品、公开转载、批量再分发）。

## 4. 接口与频率

RSS、公开 API 和 MCP 为匿名只读接口。请按响应中的缓存时间轮询，遇到 429 请遵守 Retry-After，不要并发重试。

## 5. 免责

本站按“现状”提供，不保证内容完整、准确和持续可用。
`,u=t(),d={tab:`me`},f=o(l);function p(){return i({title:n.terms.name,description:n.terms.description,path:`/terms`,image:`/og/pages/terms.png`})}var m=e(function(){return(0,u.jsx)(s,{doc:f.doc,rendered:f.rendered,eyebrow:c.name,footer:(0,u.jsx)(a,{links:[{to:`/privacy`,label:`隐私说明`},{to:`/agent`,label:`Agent 接入页`},...r().flatMap(e=>e.termsLinks??[])],note:`${n.terms.name} ${f.doc.meta.版本??``} · ${f.doc.meta.生效日期??``}`})})});export{m as default,d as handle,p as meta};