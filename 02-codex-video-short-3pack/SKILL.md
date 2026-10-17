---
name: codex-video-short-3pack
description: Codex 短视频创作三件套（飓风开场 / ImageGen / HyperFrames）。当用户要做短视频脚本、AI 配图或 MG 动画成片时使用。
agent_created: true
---

# Codex 短视频创作：3 个 Skill 包

来源（飞书，包为附件，需登录下载）：
https://ccnope4jr4h4.feishu.cn/wiki/YWmywcjGGiXyapklUw4cI4NDnzG

## 包含什么（来自文档）
安装包：`codex-video-skills-20260915.zip`（约 273KB，飞书附件）
1. **飓风开场**：视频开场策划技能，含完整 SKILL.md，用于选择开场切入方式并展开脚本、分镜和拍摄要点。
2. **imagegen/**：Codex ImageGen 技能，含 SKILL.md、脚本、参考资料、图标及 LICENSE.txt。
3. **hyperframes/**：HyperFrames 0.1.2 完整插件目录，含插件清单、品牌资源，以及 hyperframes / hyperframes-cli / hyperframes-registry / gsap / website-to-hyperframes 五个配套技能。
- `manifest.json` 记录原始文件的相对路径、大小和 SHA-256，可用于核对文件完整性。

## 推荐安装方式
解压后，将解压目录交给 Codex，发送：
> 请先阅读这个目录里的“安装与使用说明.md”，检查我已安装的技能与当前 Codex 支持的安装方式。安装缺少的飓风开场、ImageGen 和 HyperFrames 技能；保留已有版本，避免重复安装。HyperFrames 的五个配套技能请一起处理。最后列出成功识别的技能，以及仍需准备的运行环境。

- 第一、第二项是独立技能目录；第三项是插件目录，结构不同。
- 以技能方式安装 HyperFrames 时，使用 `hyperframes/skills/` 下五个独立文件夹，保持相对结构；以插件方式导入时，使用包含 `.codex-plugin/plugin.json` 的完整 `hyperframes/` 目录。
- ImageGen 在部分 Codex 环境中已自带，已可调用时无需重复安装。

## 运行前准备
- 飓风开场：依赖 Codex 文本能力，技能文件本身不要求额外 API Key。
- 示例：使用飓风开场。我的选题是“AI 能不能替我处理一天的重复工作”，目标观众是普通上班族。请先给我三种不同的开场路线，再根据我的选择展开前十五秒脚本。

## 说明
原包为飞书附件，本机工具无法直接下载。请在能登录飞书的客户端下载 zip 后，将其中的技能目录放入本技能目录（覆盖本说明）即可使用。
