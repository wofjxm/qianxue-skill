---
name: openmontage-guide
description: OpenMontage Windows 本地部署与使用完整指南：从解压源码、配置 Python/Node/FFmpeg 环境、一键安装脚本，到用自然语言让 AI 助手制作视频（提案→脚本→场景计划→素材→合成→自检交付）。含 3 种合成运行时选择（Remotion/HyperFrames/FFmpeg）、4 条可直接复制的使用提示词、成本安全清单与排障手册。触发词：OpenMontage、AI视频制作、本地视频生成、Remotion、HyperFrames、自然语言做视频、视频流水线。
agent_created: true
---

# OpenMontage · Windows 本地部署与使用指南

从解压源码、配置运行环境，到用自然语言完成视频制作。

- 上游仓库：https://github.com/calesthio/OpenMontage
- 快照提交：`4eab34c5cfcccaa4f1970554928feccce73ee930`｜许可证：GNU AGPLv3
- 适用系统：Windows 10 / 11 · 推荐 Node.js 22+ · Python 3.10+
- 说明：本指南按上述源码快照编写；上游更新后，界面、命令或依赖可能变化。

## 1. 先看结论

**最短使用路径**：解压源码 → 安装 Python、Node.js、FFmpeg → 运行「安装-Windows.ps1」→ 用 Codex 打开 OpenMontage-source → 用自然语言描述视频 → 在每个审批节点确认 → 从 `projects/<项目名>/renders/` 取走成片。

**交付包里有什么**：

| 目录/文件 | 用途 |
|---|---|
| `OpenMontage-source/` | 提交 4eab34c 的完整 Git 跟踪源码快照，含内置技能、脚本、测试、中文 README 与许可证 |
| `docs/OpenMontage本地部署与使用指南.docx` | 本手册，可直接交给同事阅读 |
| `安装-Windows.ps1` | 创建虚拟环境、安装 Python/Remotion/Piper 依赖、生成 .env |
| `检查环境-Windows.ps1` | 检查 Python、Node、FFmpeg、Piper、Remotion、HyperFrames 与工具注册表 |
| `版本与来源.txt` / `SHA256SUMS.txt` | 记录源码来源、快照提交、排除项和包内文件校验值 |

**为什么没有打包本机依赖**：未包含 .env（可能保存 API Key）；未包含 .venv、node_modules、浏览器缓存和 FFmpeg 可执行文件（与系统架构绑定）；未包含 projects/、渲染结果和 Piper 模型（生成数据或可再下载资源）；未包含 .git（版本已由版本文件和提交哈希固定）。

## 2. 部署前准备

| 组件 | 最低要求 | 本指南建议 | 验证命令 |
|---|---|---|---|
| Windows | Windows 10 / 11 | 64 位，保留 10 GB 以上空间 | `winver` |
| Python | 3.10+ | 3.12，安装时勾选 Add Python to PATH | `python --version` |
| Node.js | 18+ | 22+，以启用 HyperFrames | `node --version` |
| FFmpeg | 可执行文件在 PATH | 官方或可信发行版 | `ffmpeg -version` |
| Git | 可选 | 需要拉取/更新源码时安装 | `git --version` |
| AI 编程助手 | 能读写文件并执行命令 | Codex、Claude Code、Cursor 等 | 打开项目目录 |

**推荐安装命令**（PowerShell，逐项安装，完成后关闭并重新打开终端）：
```powershell
winget install --id Python.Python.3.12 --exact
winget install --id OpenJS.NodeJS.LTS --exact
winget install --id Gyan.FFmpeg --exact
winget install --id Git.Git --exact
```

**注意 Node 版本**：仓库基础要求 Node.js 18+，但 HyperFrames 运行时要求 Node.js 22+。为同时使用 Remotion 与 HyperFrames，建议直接安装 Node.js 22 或更高的 LTS。

**解压位置建议**：路径尽量短，例如 `D:\OpenMontage`；避免放在受 OneDrive 同步或公司安全软件强管控的目录。路径可以包含中文，但遇到旧工具异常时，优先改用纯英文路径。先右键 ZIP 查看属性，若出现「解除锁定」，勾选后再解压。

## 3. 一键部署（推荐）

将 ZIP 完整解压后，在包根目录打开 PowerShell：
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\安装-Windows.ps1
```

**脚本会做什么**：
1. 检查 Python、Node.js、npm 和 FFmpeg 是否可用；缺少时停止并给出安装提示
2. 在 OpenMontage-source 下创建 .venv，并安装 requirements.txt 与 piper-tts
3. 在 remotion-composer 下执行 `npm.cmd install`，生成 node_modules
4. 如果 .env 不存在，则从 .env.example 复制一份；不会覆盖已有 .env
5. 最后运行基础版本检查。HyperFrames 会在首次 npx 调用时下载并缓存

**执行后检查**：`.\检查环境-Windows.ps1`

「安装成功」与「功能可用」是两件事：脚本完成代表依赖安装步骤已执行；仍应以检查脚本的结果、工具注册表状态以及一次真实渲染为准。云端图像、视频、配音或素材服务还需要在 .env 中配置相应 API Key。

**激活虚拟环境**：
```powershell
Set-ExecutionPolicy -Scope Process Bypass
Set-Location .\OpenMontage-source
.\.venv\Scripts\Activate.ps1
$env:PATH = "$PWD\.venv\Scripts;$env:PATH"
```

## 4. 手动部署（脚本失败时使用）

```powershell
# 步骤 1：进入源码目录并创建虚拟环境
Set-Location .\OpenMontage-source
python -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip

# 步骤 2：安装 Python 与 Piper 依赖
python -m pip install -r requirements.txt
python -m pip install piper-tts
python -m pip check

# 步骤 3：安装 Remotion 依赖（Windows PowerShell 用 npm.cmd 避免执行策略拦截）
Set-Location .\remotion-composer
npm.cmd install
Set-Location ..

# 步骤 4：创建配置文件
if (-not (Test-Path .env)) { Copy-Item .env.example .env }

# 步骤 5：可选下载 Piper 英文离线音色
python -m piper.download_voices en_US-lessac-medium --download-dir .
```

零密钥也可使用 FFmpeg、Remotion、HyperFrames 和本地 Piper 路径；云服务需打开 .env 填入对应密钥。

**中文离线音色说明**：本机已验证的离线音色是英文 en_US-lessac-medium。中文 Piper 音色应先用下载工具查看当前可用列表并单独验证；不要把「Piper 已安装」当成「中文配音已可用」。

## 5. 环境验证与首次运行

```powershell
# 基础版本检查
python --version
node --version
npm.cmd --version
ffmpeg -version
python -m pip check
npx.cmd --yes hyperframes --version

# 工具注册表检查
$env:PATH = "$PWD\.venv\Scripts;$env:PATH"
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu_summary(), indent=2))"
```

重点查看 FFmpeg、Remotion、HyperFrames、Piper、字幕、音频处理和视频后期是否显示 available。未配置云密钥的提供商显示 unavailable 属于正常现象。可选运行仓库演示：`python render_demo.py`。

**已验证基线**：在交付机器上，提交 4eab34c 已完成 Python 依赖检查，并验证 FFmpeg、Remotion、HyperFrames、Piper、字幕、音频处理和视频后期。示例视频为 25.045 秒、1920×1080、30 fps、H.264 + AAC。该结果证明此快照曾在 Windows 上真实运行，但目标电脑仍需重新验证。

**验证通过的判定**：
- `python -m pip check` 输出 No broken requirements found
- `ffmpeg -version` 能显示版本，`where.exe ffmpeg` 能返回实际路径
- Remotion 依赖目录存在，HyperFrames 能输出版本或 doctor 结果
- 工具注册表能发现至少一个本地合成运行时
- 真实渲染能在 `projects/<项目名>/renders/` 下生成可播放 MP4

## 6. OpenMontage 怎么用

它不是传统「点按钮」软件。OpenMontage 是面向 AI 编程助手的 Agent 视频生产仓库。**正确入口**：让 Codex/Claude Code/Cursor 打开源码目录，读取 AGENTS.md 与 AGENT_GUIDE.md，然后用自然语言下达制作任务。

**标准工作流**：

| 阶段 | 你需要做什么 / 系统会做什么 |
|---|---|
| 1. 需求 | 说明题材、受众、平台、时长、画幅、语言、素材和目标 |
| 2. 提案 | 系统提出创意路线、预算和合成运行时；你确认后再继续 |
| 3. 脚本 | 生成旁白和画面逻辑；你可逐段修改并批准 |
| 4. 场景计划 | 确定每个镜头、素材类型、字幕和声音 |
| 5. 素材 | 生成或导入图片、视频、音频；云服务可能产生费用 |
| 6. 剪辑与合成 | 锁定 Remotion、HyperFrames 或 FFmpeg 路径并渲染 |
| 7. 自检与交付 | 检查编码、黑帧、音频、字幕和交付承诺，再输出成片 |

**关键规则**：
- 审批不是形式：提案、脚本、场景计划、素材和发布节点会暂停等待确认
- 同时检测到 Remotion 与 HyperFrames 时，系统必须展示两者的优点与取舍，不能静默替你决定
- 合成运行时在提案阶段锁定；渲染时若不可用，应明确报错并重新征得同意，不能偷偷降级
- 所有项目文件写入 `projects/<project-id>/`；最终成片通常位于 `renders/final.mp4`

## 7. 可直接复制的使用提示词

**A. 抖音 30 秒知识类 MG 短视频**
```
请使用 OpenMontage 为我制作一条 30 秒抖音竖屏视频。主题：[填写主题]
受众：[填写人群] 画幅：1080×1920，9:16
风格：高信息密度、动态排版、中文大字幕
开场：前 2 秒先展示具体结果或冲突
素材：优先本地与免密钥路径；任何付费调用前先报成本
流程：先给 3 条创意路线，再给脚本和场景计划；每个审批节点等我确认
合成：请同时说明 Remotion 与 HyperFrames 的适配性，再推荐一个
```

**B. 使用我已有的口播素材**
```
请检查我放在 [素材文件夹] 的视频和音频，先用 ffprobe 列出时长、分辨率、编码和音轨。
目标：剪成 60 秒以内的竖屏口播视频。
要求：删除停顿与重复句，保留真实语义；加入中文逐句字幕、重点词高亮、片头标题和 3 处信息卡；不要生成虚构 B-roll。
先给剪辑决策和删改清单，得到我批准后再合成。
```

**C. 只用真实素材的纪录片蒙太奇**
```
制作一条 45 秒纪录片蒙太奇，主题是 [主题]。
只使用真实动态素材，不要使用 AI 静态图或 Ken Burns 替代。
优先 Archive.org、NASA、Wikimedia Commons；需要第三方密钥时先询问。
先提交来源清单、版权/署名要求、脚本和镜头表，再开始下载与剪辑。
```

**D. 零密钥技术演示**
```
在不调用任何付费云 API 的前提下，制作一条 20 秒 16:9 技术演示。
使用本地 FFmpeg、Remotion 或 HyperFrames；不需要旁白，用动态排版和音效传达信息。
先确认本地可用运行时，再给两个视觉方案和预计输出路径。
```

## 8. 运行时选择与 Backlot 看板

**三种合成路径**：

| 运行时 | 适合 | 要求/取舍 |
|---|---|---|
| Remotion | React 场景、数据解释、卡片、图表、逐词字幕、现有模板栈 | Node.js + remotion-composer/node_modules；成熟稳定，但深度定制需写 React |
| HyperFrames | HTML/CSS/GSAP 动效、动态排版、产品短片、网页转视频、SVG 角色动画 | Node.js 22+、FFmpeg、npx；表现自由，首次使用会下载/缓存工具 |
| FFmpeg | 剪切、拼接、转码、字幕烧录、音频混合、简单合成 | 依赖最少、速度快；不适合需要复杂视觉动效的方案 |

**Backlot 项目看板**：从 `projects/<项目名>/` 读取项目状态和审批记录，用来观察工作流；看板失败不应阻断生产。
```powershell
python -m backlot open <project-id>
```

**项目目录结构**：
```
projects\<project-id>\
├─ project.json
├─ artifacts\        # 脚本、研究、场景计划等 JSON
├─ assets\           # 图片、视频、音频、字幕
├─ checkpoints\      # 阶段状态与审批记录
└─ renders\final.mp4 # 最终成片
```

输出路径必须明确：调用工具时应把 output_path 指向 `projects/<project-id>/` 之下。写到仓库根目录或临时目录的素材不会出现在 Backlot 中，也不符合项目约定。

## 9. API Key、成本与安全

**配置方法**：复制 .env.example 为 .env；只填写实际使用的供应商密钥（如 OPENAI_API_KEY、GOOGLE_API_KEY、FAL_KEY）；保存后重新打开终端或重启 Agent，再运行环境检查。不要把 .env 提交到 Git、发到群里或放进二次交付包。

**零密钥与需密钥能力**：

| 类别 | 典型能力 | 说明 |
|---|---|---|
| 本地/零密钥 | FFmpeg、Remotion、HyperFrames、本地 Piper、字幕与常规后期 | 不收云 API 费，但消耗本机算力、磁盘和时间 |
| 免费源/可能需免费 Key | Pexels、Pixabay、Unsplash 等 | 遵守各平台授权、频率限制和署名规则 |
| 云 API/付费 | 视频生成、图像生成、高质量 TTS、音乐、虚拟人 | 先确认价格、预算、区域可用性与内容许可 |

**安全检查清单**：
- 只从供应商官方控制台生成密钥，并启用额度限制或告警
- 任何云调用前，让 Agent 明确供应商、模型、预计次数和预算
- 上传真人素材前确认肖像权、声音授权、隐私与数据跨境要求
- 发布前核对音乐、字体、图片、视频素材的商业使用许可和署名要求
- 二次分发修改版源码时遵守 GNU AGPLv3；保留 LICENSE，并根据实际场景履行源码提供义务

**依赖审计提示**：此快照的 Remotion 构建链曾报告 nanoid 3.3.16 的高严重级别传递依赖告警，为保持上游锁文件未自动升级。对公网或生产环境使用前，请重新运行 npm audit，评估兼容性后更新依赖并完整回归测试。

## 10. 常见问题排查

| 现象 | 原因与处理 |
|---|---|
| Activate.ps1 被禁止 | 运行 `Set-ExecutionPolicy -Scope Process Bypass`，仅对当前 PowerShell 进程生效，然后再激活 .venv |
| npm.ps1 无法运行 | 使用 `npm.cmd` 和 `npx.cmd`，避免 PowerShell 执行策略拦截脚本 |
| npm install 报 EPERM | 关闭占用 node_modules 的进程；使用项目本地缓存：`npm.cmd install --cache ..\work\npm-cache` |
| 找不到 FFmpeg | 运行 `where.exe ffmpeg`；若无有效路径，重新安装 FFmpeg 并重开终端。不要只看开始菜单快捷方式 |
| 注册表说工具不可用 | 先激活 .venv，并把 `$PWD\.venv\Scripts` 放到 PATH 最前面，再重新 discover |
| Remotion 下载浏览器失败 | 检查代理/TLS；可运行 `npx.cmd remotion browser ensure`，或配置可用的本地 Chrome 可执行文件 |
| Git 报 SEC_E_NO_CREDENTIALS | 对公开仓库可尝试 `git -c http.sslBackend=openssl clone ...`；公司网络环境请按组织证书策略处理 |
| 控制台中文乱码 | 运行 `$env:PYTHONUTF8=1`；同时确认终端使用 UTF-8 |
| 没有 make | Windows 直接使用本指南的 PowerShell 命令；不要因为缺少 make 判断仓库不可用 |
| 中文 Piper 不工作 | Piper 安装成功不等于中文音色已下载；先查可用音色，下载对应 onnx/json，并做实际发声测试 |

**排障原则**：先看真实可执行文件路径，再看版本，不要只相信安装器的「完成」；先验证最小链路 Python → FFmpeg → 一个本地运行时 → 真实 MP4；保留完整错误文本和失败命令，不要只截图最后一行；升级依赖前复制项目或创建 Git 分支，一次只改变一个变量。

## 11. 交付、升级与验收

**源码完整性**：源码来自 Git 跟踪文件快照，「完整源码」指提交 4eab34c 中所有已跟踪文件；本机私有配置、下载依赖和生成数据不属于源码。包根目录 SHA256SUMS.txt 可用于核对内容是否被修改。

**升级方法**：
```powershell
git clone https://github.com/calesthio/OpenMontage.git
Set-Location OpenMontage
git log -1 --oneline
# 按新版本 README 重新安装依赖并回归验证
```

不要直接覆盖生产项目：上游快速迭代时，建议把新版本克隆到新目录，在复制 .env 之前先比较 .env.example；再用同一份测试提示词和素材做回归，确认输出质量、审批节点和运行时选择没有变化。

**最终验收清单**：
- [ ] ZIP 能正常解压，OpenMontage-source/ 含 LICENSE、AGENT_GUIDE.md、README_zh-CN.md、tools/、skills/ 和 tests/
- [ ] Python、Node、FFmpeg 版本符合要求；pip check 通过
- [ ] Remotion 或 HyperFrames 至少一个本地合成运行时可用
- [ ] .env 未泄露密钥；仅配置实际需要的供应商
- [ ] 工具注册表发现本地能力；付费服务调用前有预算审批
- [ ] 用真实任务完成一次渲染，MP4 可播放，画面、声音、字幕和时长符合预期
- [ ] 成片和项目工件位于 projects/<项目名>/ 下，便于 Backlot 追踪
- [ ] 对外分发前完成素材许可、肖像权、隐私和 AGPLv3 合规检查

**参考入口**：README_zh-CN.md（项目中文概览）/ AGENTS.md / AGENT_GUIDE.md（Agent 必须遵守的生产流程、审批、运行时与项目目录契约）/ PROJECT_CONTEXT.md（系统架构）/ PROMPT_GALLERY.md（官方提示词示例）/ docs/（架构、提供商、运营和开发参考）。

## 来源

飞书文档《OpenMontage本地部署与使用指南》：https://ccnope4jr4h4.feishu.cn/wiki/NORZwHjJpiFSTokzQa8cganrnrf
完整源码包（77MB，提交 4eab34c）：`assets/OpenMontage-完整源码与本地部署指南-2026-08-21.zip`
