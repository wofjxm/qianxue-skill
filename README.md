# WorkBuddy 技能归档库

本目录是 WorkBuddy **用户级技能**的本地归档，用于备份和迁移到其他电脑。

- 本机技能源目录：`C:\Users\lxj\.workbuddy\skills`
- 归档目录（本目录）：`D:\workbuddy\skill`

## 换电脑时怎么用

1. 把整个 `skill` 文件夹拷到新电脑（U 盘 / 网盘 / 移动硬盘均可）。
2. 在新电脑上打开 WorkBuddy，找到用户级技能目录：
   - Windows：`C:\Users\<你的用户名>\.workbuddy\skills`
   - macOS：`~/.workbuddy/skills`
3. 把本目录下各技能文件夹拷进去（**不要**拷 `_` 开头的文件）。
4. 重启 WorkBuddy，技能即被识别。

如果新电脑也用 Git Bash，进到本目录执行 `bash _sync_skills.sh restore` 可自动完成第 3 步。

## 已归档技能

| 技能 | 用途 | 是否需要额外配置 |
|---|---|---|
| `zw-summary` | B站 / YouTube / X / 抖音 / 小宇宙 视频与播客 → 结构化中文总结笔记 | 需 `yt_dlp`；无字幕视频还需自建 `whisper_venv`（约 500MB），可选配 `scripts/zw_config.json` |
| `smart-summarize` | 长文本 / TXT / MD / DOCX / PDF / 网页 URL → 结构化摘要 + 关键词 | 需 Python 依赖：requests、python-docx、jieba、beautifulsoup4、pypdf（本机 2026-10-09 已装并冒烟测试通过） |
| `summarize-oc` | 网页 / PDF / Word / TXT / 播客 / YouTube 智能摘要 | 开箱即用，无需配置 |
| `douyinvideo2text-ai` | 本地视频文件 + 抖音 / 小红书链接 → 转写与自定义 Prompt 总结 | **需付费**：环境变量 `GUAIKEI_API_TOKEN`，官网 guaikei.com 开通，0.6 元/分钟 |
| `huashu-design__skillhub` | 用 HTML 做高保真原型、交互 Demo、幻灯片、动画导出 MP4/GIF，兼设计方向顾问与专家评审 | 动画导出需 ffmpeg；配音动画需豆包 TTS 密钥（写在技能根目录 `.env`） |

## 同步脚本

```bash
bash /d/workbuddy/skill/_sync_skills.sh          # 本机技能 → 归档到这里
bash /d/workbuddy/skill/_sync_skills.sh restore  # 归档 → 恢复到本机技能目录
```

归档时自动排除 `__pycache__`、`node_modules`、`whisper_venv`、`.venv`、`.git`，避免大文件与缓存污染。

## 约定

以后每次安装新技能，都要同步归档到本目录。这条是长期规则，已写入 WorkBuddy 用户级长期记忆。

---

## 千雪 Feishu 合集（2026-10-18 新增 28 个）

来源合集（飞书）：https://ccnope4jr4h4.feishu.cn/wiki/LWwxwYCNai72u9k3qe2cRcWwnNe
这些技能**原为 Codex（OpenAI）设计**，已整理成 WorkBuddy 用户技能格式（SKILL.md），可直接被 WorkBuddy 调用。

**重要**：飞书文档多为「登录墙 + 附件形式」，**原 .skill 包 / zip / GitHub 仓库本机无法直接下载**（本机 GitHub 也不通）。所以：
- 标 ✅ 的已把实际提示词/流程写进 SKILL.md，可直接用；
- 标「占位」的只保留了飞书源链接 + 获取原包的方法，需在能登录飞书的设备下载后放进对应目录覆盖说明。

**2026-10-18 补全记录**：用户登录飞书后，用 Chrome 自动化（chrome-browser-automation 技能，Playwright 驱动系统 Chrome + 持久登录态）重新抓取了 4 个此前失败的文档——03（PDF 19 页全文 + 部署配置/脚本）、08（附件 md 全文）、10（DOCX 指南 + 77MB 源码 zip）、13（SSR shadow-DOM 里的提示词全文），均已写成完整技能并安装到本机。

| # | 技能目录 | 名称 | 完整度 | 类别 |
|---|----------|------|--------|------|
| 01 | 01-codex-psd-layered | Codex PSD 图片分层 | 占位（飞书附件） | 图像 |
| 02 | 02-codex-video-short-3pack | Codex 自媒体短视频 3 包 | ✅ 说明/安装法 | 视频 |
| 03 | 03-workbuddy-obsidian-ai-agent | WorkBuddy+Obsidian AI 经纪人 | ✅ 完整（含 7 份配置+4 脚本+plist） | 效率 |
| 04 | 04-codex-media-skill-addresses | Codex 自媒体 Skill 地址 | ✅ GitHub 地址 | 视频 |
| 05 | 05-workbuddy-four-step-setup | WorkBuddy 四步提效设置 | ✅ 含模板 | 设置 |
| 06 | 06-three-awesome-plugins | 三个神级 skill 插件 | ✅ GitHub 地址 | 效率 |
| 07 | 07-animation-plugin-pack | 动画插件 skill 包地址 | 占位（链接型） | 视频 |
| 08 | 08-obsidian-workbuddy-setup | Obsidian+WorkBuddy 搭建流程 | ✅ 完整教程+第二大脑方法论 | 效率 |
| 09 | 09-meishang-skill-pack | 美商 skill 包 | 占位（链接型） | 电商 |
| 10 | 10-openmontage-guide | OpenMontage 部署指南 | ✅ 完整（含 77MB 源码包，git 排除本机留存） | 视频 |
| 11 | 11-workbuddy-10-skills-guide | WorkBuddy 10 个 Skill 清单 | ✅ 选型链路 | 效率 |
| 12 | 12-workbuddy-instruction-template | WorkBuddy 自定义指令模板 | ✅ 指令原文 | 设置 |
| 13 | 13-portfolio-website-prompt | 高端个人作品集网站提示词 | ✅ 提示词+六步流程 | 图像 |
| 14 | 14-compound-os-life-workbench | COMPOUND.OS 人生工作台 | ✅ 思路/技术栈 | 效率 |
| 15 | 15-depth-video-motion-migration | 深度视频动作迁移提示词 | ✅ 提示词 | 视频 |
| 16 | 16-ai-one-click-video-edit | 千雪 AI 一键剪辑资料包 | ✅ 能力说明 | 视频 |
| 17 | 17-90000-skills-treasure | 9 万+ skill 宝藏网站 | 占位（链接型） | 效率 |
| 18 | 18-five-skills-share | 五个 skill 分享 | ✅ 清单 | 效率 |
| 19 | 19-gesture-tarot-cards-prompt | 手势卡牌完整提示词 | ✅ 分步提示词 | 图像 |
| 20 | 20-codex-pre-setup-instruction | Codex 用前设置自定义指令 | ✅ 指令原文 | 设置 |
| 21 | 21-cross-border-ecom-codex-skills | 跨境电商 AI 工具与 Skills | ✅ 选型/CLI | 电商 |
| 22 | 22-desktop-music-visualizer-prompt | 桌面屏保音乐律动提示词 | ✅ 提示词 | 效率 |
| 23 | 23-filter-gesture-interaction-prompt | 滤镜手势交互效果提示词 | ✅ 提示词 | 图像 |
| 24 | 24-codex-plugins-and-prompts | Codex 插件和提示词 | ✅ 清单/提示词 | 效率 |
| 25 | 25-codex-skill-install-guide | Codex skill 安装地址及方法 | ✅ 地址/命令 | 设置 |
| 26 | 26-game-character-transition-prompt | 游戏角色转场提示词 | ✅ 生图提示词 | 图像 |
| 27 | 27-codex-mg-animation-guide | Codex MG 动画生成流程 | ✅ 流程/提示词 | 视频 |
| 28 | 28-poem-cloud-prompt | 诗云提示词 | ✅ 提示词 | 效率 |

**复制到新电脑安装**：把本目录下对应的 `<编号>-<名称>` 文件夹整文件夹复制到目标机 `C:\Users\<用户名>\.workbuddy\skills\`，重启 WorkBuddy 即识别。
**补全原包**：在能登录飞书的设备打开上面合集链接，下载原 .skill 包/zip 放入对应目录覆盖说明文件即可。
