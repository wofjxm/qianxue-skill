---
name: workbuddy-obsidian-ai-agent
description: 部署「AI 经纪人」Obsidian 内容流水线：手机随手录灵感 → 每天 9:00 自动入库生成选题卡 → 9:05 倒排期（脚本/拍摄/剪辑/发布）→ 9:10 同步苹果日历 → 21:00 同步完成状态。含 vault 目录结构、7 份核心配置、4 个自动化脚本和 launchd 定时任务模板。触发词：AI经纪人、内容流水线、Obsidian排期、选题入库、倒排期、灵感自动入库。
agent_created: true
---

# AI 经纪人 · Obsidian 内容流水线部署

一套「Obsidian 内容流水线」的完整安装包。灵感记进手机后，AI 经纪人每天自动帮你入库、写大纲、倒排期、同步苹果日历，你只管照着日历创作。

## 平台前提（重要）

- **macOS + iPhone**（同一 Apple ID 登录 iCloud），定时任务只在 Mac 开机时运行
- 已安装 Obsidian（安装教程见姊妹技能 `08-obsidian-workbuddy-setup`）
- AI agent CLI 可用（WorkBuddy 内置 codebuddy 或用户安装的 codex 等），需支持非交互模式 `-p "prompt"` 和 `--add-dir` 参数
- Python 3 可用（日历同步脚本需要）

## 核心原则

**Obsidian 是唯一数据源头。** 所有时间改动只在 Obsidian 里做，苹果日历是只读看板——在手机日历上手动改的会被次日 9:10 的同步覆盖。

## 日常节奏

| 时段 | 动作 | 耗时 |
|---|---|---|
| 随时（碎片） | 打开 Obsidian → 星标文件「随手录入」→ 顶部空行写一条。链接/口述/截图描述都行 | 30 秒/条 |
| 早上（可选） | 看手机日历或「任务总览」，知道今天该干嘛 | 30 秒 |
| 晚上（收工） | 打开当天「每日小记」→ 做完的任务勾 [x] → 21:00 自动同步 | 1 分钟 |
| 每周日 | 「任务总览」→ Timeline 未来 14 天 → 调发布日期 | 5 分钟 |

```
📱 手机                           🖥 Mac（全自动，无需操作）
────────                        ──────────────────────
随手录入灵感 ── iCloud 同步 ──→ 每天 9:00 灵感入库（生成选题卡）
  (30 秒)                        每天 9:05 倒排期（脚本 → 拍/素材 → 剪 → 发）
                                每天 9:10 同步苹果日历（手机可见）
看板/日历/每日小记 ←────────── 全部落回 Obsidian，手机随时查看
晚上勾掉当天任务 ──→ 21:00 同步完成状态（看板移「已完成」+ 日历打勾）
```

## 怎么用这份技能

把整份文档发给你的 AI agent（WorkBuddy、Codex 或任何能操作你电脑的 agent），对它说「照着这份文档帮我部署」，然后回答它问的几个问题，剩下的它全包。

**部署前先问用户这 4 个问题**（答案代后文所有 `{{占位符}}`）：

1. 知识库名字叫什么？（建议：我的知识库；记为 `{{VAULT_NAME}}`）
2. vault 放在哪？建议在 iCloud 云盘下新建文件夹（默认 `~/Library/Mobile Documents/com~apple~CloudDocs/{{VAULT_NAME}}`；记为 `{{VAULT_PATH}}`）
3. 同步到哪个苹果日历？必须选 iCloud 账户下的日历（本地日历不进 iCloud，手机看不到）。建议在 iCloud 下新建一个名为「内容排期」的日历（记为 `{{CAL_NAME}}`）
4. 默认发布时间？（默认 18:00，记为 `{{PUBLISH_TIME}}`）

**前置检查**（不满足先报告，不要硬装）：

1. macOS（依赖 launchd 定时任务和 osascript 日历脚本）
2. iCloud Drive 已登录（vault 必须放在 iCloud 路径下才能手机电脑同步）
3. Obsidian 已安装
4. AI agent CLI 可用的绝对路径（记为 `{{AGENT_CLI}}`）
5. Python 3 可用

## 部署步骤（Step 1–5）

### Step 1 · 创建 vault 与目录结构

在 `{{VAULT_PATH}}` 创建 vault，目录结构：

```
{{VAULT_NAME}}/（vault 根目录）
├── 选题灵感库/
│   ├── 0-随手录入.md          ← 手机端唯一灵感入口
│   └── _早间入库说明.md        ← 9:00 入库任务的 agent 指令
├── 时间管理/
│   ├── _早间排期指令.md        ← 9:05 倒排期 + 21:00 状态同步的 agent 指令
│   └── 3-内容流程看板.md       ← Kanban 看板
├── 环节档案/                   ← 写脚本/拍摄/剪辑笔记（自动生成）
├── 每日小记/                   ← 每天任务清单，晚上在这里勾 ✅
├── 内容日历/
│   └── 流程日历/               ← 日历事件笔记（自动生成）
├── 模板/
│   ├── 选题灵感卡.md
│   └── 每日小记.md
└── 附件/                       ← 分镜表粘贴图片自动存这里
```

### Step 2 · 写入核心文件（共 7 份）

全部在 `assets/` 目录，原样复制到 vault 对应位置：

| 文件 | assets/ 中对应 | 用途 |
|---|---|---|
| 选题灵感库/0-随手录入.md | `assets/0-随手录入.md` | 手机端灵感入口，每条一行 `- [ ] 内容` |
| 选题灵感库/_早间入库说明.md | `assets/_早间入库说明.md` | 9:00 入库任务的 agent 指令 |
| 时间管理/_早间排期指令.md | `assets/_早间排期指令.md` | 9:05 倒排期 + 21:00 状态同步指令 |
| 时间管理/3-内容流程看板.md | `assets/3-内容流程看板.md` | Kanban 看板 |
| 模板/选题灵感卡.md | `assets/模板-选题灵感卡.md` | 选题卡模板 |
| 模板/每日小记.md | `assets/模板-每日小记.md` | 每日小记模板 |
| .obsidian/snippets/no-task-strikethrough.css | `assets/no-task-strikethrough.css` | 任务勾选后去掉删除线 |

### Step 3 · 配置 Obsidian

1. **核心设置**：设置 → 文件与链接 → 附件默认存放路径 = 「在指定的文件夹」→ 填 `附件`
2. **启用 CSS**：设置 → 外观 → CSS 代码片段 → 刷新 → 打开 `no-task-strikethrough` 开关
3. **安装并启用 6 个社区插件**（设置 → 第三方插件 → 关闭安全模式 → 浏览）：

| 插件 | 用途 | 关键配置 |
|---|---|---|
| Kanban | 内容流程看板 | 无需额外配置，看板文件已带 `kanban-plugin: board` |
| Tasks | 任务勾选/查询 | 全局任务过滤器设为 `#task` |
| Dataview | 任务总览/时间线视图 | 开启 JavaScript 查询（后续按需） |
| Day Planner | 每日小记的日历时间轴 | 模式选「Day Planner」 |
| Full Calendar | 周日历视图 | 添加「Full note」日历源，目录指向 `内容日历/流程日历` |
| Buttons | 手动触发按钮 | 高级用法，可先不装 |

4. **手机端**：iPhone 安装 Obsidian → 登录同一 Apple ID → vault 自动出现 → 把 `选题灵感库/0-随手录入.md` 设为星标

### Step 4 · 部署自动化脚本与定时任务

`scripts/` 目录 4 个脚本放到 `~/.local/bin/`，全部 `chmod +x`，先把占位符替换成第 3 节问到的答案：

| 脚本 | 触发时间 | 职责 |
|---|---|---|
| `wb-import.sh` | 9:00 | 灵感入库：扫 `0-随手录入.md` 未勾选行 → 生成选题卡 → 推选题池或直接排期 |
| `wb-schedule.sh` | 9:05 | 倒排期：扫看板带 📅 日期的卡 → 生成环节笔记/日历事件/每日小记/看板分卡 |
| `wb-sync-ical.py` | 9:10 | 单向同步苹果日历（osascript JXA，事件备注附 obsidian:// 链接） |
| `wb-status.sh` | 21:00 | 状态同步：扫每日小记已勾选任务 → 日历 complete:true + 看板移「已完成」 |

注册 launchd：在 `~/Library/LaunchAgents/` 创建 4 个 plist（模板见 `scripts/plists/`），然后：

```bash
launchctl load ~/Library/LaunchAgents/com.content.import.plist
launchctl load ~/Library/LaunchAgents/com.content.schedule.plist
launchctl load ~/Library/LaunchAgents/com.content.sync-ical.plist
launchctl load ~/Library/LaunchAgents/com.content.status.plist
```

### Step 5 · 试运行验证（部署完成前必做）

1. 在手机或电脑的 `0-随手录入.md` 里写一条测试灵感：`- [ ] 测试选题，9月30日发布`
2. 手动跑 `~/.local/bin/wb-import.sh`，等待完成后检查 5 处产物：
   - `选题灵感库/` 出现 `YYYY-MM-DD 测试选题.md`（状态 🟢 已排期，含原始口述）
   - `环节档案/` 出现 3 份环节笔记（写脚本/拍摄或素材整理/剪辑）
   - `内容日历/流程日历/` 出现 4 个事件笔记
   - `每日小记/` 对应日期出现 `#task` 任务行
   - 看板「📦 已排期」出现归档卡，「📝 写脚本」等 4 列出现分卡
3. 手动跑 `~/.local/bin/wb-sync-ical.py`，检查苹果日历 App「{{CAL_NAME}}」出现 4 个事件，点开备注有 obsidian:// 链接
4. 在每日小记里勾掉一个测试任务，手动跑 `~/.local/bin/wb-status.sh`，检查看板卡片移入「✅ 已完成」
5. 全部通过 → 删除测试数据，告诉用户：明天早上 9 点开始，系统全自动运行

## 验收清单（全绿 = 部署成功）

- [ ] vault 在 iCloud 路径下，手机能看到并已星标「0-随手录入」
- [ ] 6 个插件装好，看板正常渲染，CSS 去删除线生效
- [ ] 4 个脚本可手动跑通，产物齐全
- [ ] 4 个 launchd 任务已 load（`launchctl list | grep com.content` 可见）
- [ ] 苹果日历事件带 obsidian:// 链接，手机点开能跳回 Obsidian
- [ ] 试运行 5 处产物验证通过，测试数据已清理

## 关键业务规则（改规则 = 改文档，不用碰代码）

- **状态流转**：💡 灵感 → 🟡 可评估 → 🟠 已立项 → 🟢 已排期 → 🎬 脚本草稿 → 🎥 拍摄中 → ✂ 剪辑中 → ✅ 已发布
- **灵感带发布日期 = 直接排期**：识别 `📅 2026-09-20`、`9月20日`、`09/20` 等格式 → 跳过选题池，直接倒排
- **拍摄 vs 素材整理二选一**：真人出镜/实拍用「拍摄」；纯拆解/口播不露脸/录屏/混剪用「素材整理」
- **剪辑天数**：默认 1 天；卡片写 `剪辑:2天` 或成片明显复杂 → 2 天
- **环节节奏表**见 `assets/_早间排期指令.md` 第三节，agent 每次任务重新读——改文档就是改规则
- **原始口述逐字保留**：每张选题卡必须带 `## 🎙 原始口述` 区块，不改写不缩写
- **看板卡片必须是单行 `- [ ]` 列表项**，否则 Kanban 插件渲染出错；改完看板文件需 Cmd+Q 重启 Obsidian

## 常见问题

**Q：Mac 关机/睡眠定时任务还跑吗？**
不跑。launchd 只在开机时触发当天错过的日历任务一次（默认行为）。灵感不会丢，下次开机 9:00 会一并处理。

**Q：手机上改了灵感，电脑多久能读到？**
iCloud 通常几秒内同步；偶尔延迟，9:00 前同步到即可。

**Q：看板卡片显示成乱码/纯文本？**
卡片必须是单行列表项；改完看板文件后重启 Obsidian（Cmd+Q 再打开）。

**Q：日历事件重复了？**
`wb-sync-ical.py` 每次全量重建带 `[Obsidian 内容]` 标记的事件，重复说明目标日历名配错或手动建过同名事件。检查 `CAL_NAME`。

**Q：想改环节节奏/时长？**
直接编辑 `时间管理/_早间排期指令.md` 第三节的表格。

## 来源

飞书文档《AI经纪人部署文档（粉丝版）》v1.0（2026-09）：https://ccnope4jr4h4.feishu.cn/wiki/UtvZwYu6siLBhTk8Z65cWwCGnLf
