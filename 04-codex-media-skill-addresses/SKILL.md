---
name: codex-media-skill-addresses
description: Codex 自媒体相关 Skill 的地址与使用方法合集（如 Pongfi Research 选题研究等）。当用户要在 Codex 中安装自媒体类技能或做选题/对标研究时使用。
agent_created: true
---

# Codex 自媒体 Skill 地址与使用方法

来源（飞书）：https://ccnope4jr4h4.feishu.cn/wiki/KhDaw8lLKiTwPtkvcl1cIETkn0X

## 已知 Skill 地址（来自文档）
1. **Pongfi Research（选题与对标研究）**
   - 项目地址：https://github.com/s15039733700-cpu/Pongfi-Skills
   - Skill 地址：https://github.com/s15039733700-cpu/Pongfi-Skills/tree/main/skills/pongfi-research
   - 作用：研究公开的热门内容、对标账号、评论需求和选题机会。

## 安装方式（在 Codex 中）
> 调用 skill-installer，安装这个 Skill：
> https://github.com/s15039733700-cpu/Pongfi-Skills/tree/main/skills/pongfi-research
> 安装后检查 Python 环境，并告诉我是否需要重启 Codex。

## 使用前准备
首次使用 Pongfi Research 需申请 **TikHub API Key**，并在 Windows 用户环境变量中新增：
- 变量名：`TIKHUB_API_KEY`
- 变量值：自己的 API Key
保存后重启 Codex。TikHub 数据调用可能单独收费。

## 使用指令示例
> 调用 pongfi-research，研究这个抖音账号：[账号链接]。
> 分析最近 30 天可获取的作品、突出选题和评论需求，保留原链接和采集时间，缺失数据不要补猜。
> 先做 1—3 个请求的小样本，扩大调用前说明预计请求量。

## 说明
- 上述 GitHub 地址在本机网络环境下可能无法直接访问（GitHub 不通），请在能联网的机器上克隆/下载后，把技能目录放入本技能目录或对应工具。
- 文档中还可能列出更多自媒体 Skill 地址，建议在能登录飞书时补全到下方。
