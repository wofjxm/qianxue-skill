---
name: cross-border-ecom-codex-skills
description: 跨境电商 AI 工具与 Codex Skills 实用指南（卖家精灵/LinkFox/Self-Improving Agent 等真实类型拆解与本地安装）。当用户要在 Codex 中接入跨境电商 AI 工具、避免装错/买错/泄露密钥时使用。
agent_created: true
---

# 跨境电商 AI 工具与 Codex Skills 实用指南

来源（飞书）：https://ccnope4jr4h4.feishu.cn/wiki/JFSiwk0zAi4weJktGHGcIPqXnnc

## 先说结论
这 6 个名称并不是 6 个同类、同来源的“Codex 官方 Skill”。它们混合了 SaaS、托管 Agent、第三方社区 Skill 和 Skill 市场。按可验证的真实类型拆开说明，避免装错、买错或把账号密钥交给不明脚本。

## 一页看懂：6 个名称到底是什么
| 名称 | 真实类型 | 在 Codex 中的使用方式 |
|------|----------|----------------------|
| Seller Sprite 卖家精灵 | 官方 SaaS + 第三方数据 Skill 家族 | 可打开卖家精灵网页；也可从 LinkFox Skills 安装 4 个细分 Skill |
| LinkFox AI | SaaS + 可安装社区 Skill | 网页直接做图/视频；或安装 linkfox-ai，用 API Key 在 Codex 中调用 |
| LinkFox Agent | 托管式 Agent / SaaS | 在 os.linkfox.com 登录后对话使用；不是本地 Skill 包 |
| Amazon Reviews | 可安装社区 Skill | 安装 linkfox-amazon-reviews-list；负责抓取评论，再让 Codex 做归因与建议 |
| Self-Improving Agent | 通用社区 Skill | 目录可见；安装前检查包、权限和写入范围，不是电商专属 |
| LinkFox Skills | 第三方 Skill 市场 + CLI | 先安装 linkfoxskill 命令行，再搜索、审查并装入 Codex |

## 统一准备：把第三方 Skill 装进 Codex
- 先安装 Node.js 18+。使用 `--agents codex` 会装到当前用户的 `.codex/skills`；安装后新建任务或重启 Codex。
- LinkFox Skills 是第三方市场；安装前审查 SKILL.md、脚本、环境变量与网络请求。API Key 仅注入当前终端，`--workdir` 不与 `--agents` 混用。

```
npm install -g linkfoxskill@latest
linkfoxskill init --agents codex
```

## 在 WorkBuddy 中的使用方式
WorkBuddy 可参考上述“先审查再安装”的原则：需要接入跨境电商 AI 工具时，优先核实来源类型与权限范围，避免把密钥交给不明脚本。具体 Skill 包请在能联网的机器上按官方渠道获取后安装。
