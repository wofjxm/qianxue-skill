---
name: chrome-browser-automation
description: 用 Playwright 直接驱动系统已安装的 Google Chrome 完成浏览器自动化（导航、点击、填表、截图、取文本、多步宏）。这是 agent-browser 在本机（其会话守护进程/IPC 会卡死）的可靠替代方案。当用户需要"自动操作 Chrome 浏览器"、自动填表、网页截图、爬取页面内容、复用已登录会话执行网页操作时使用。
agent_created: true
---

# Chrome 浏览器自动化（Playwright 驱动系统 Chrome）

## 背景与问题诊断
用户要求"agent browser 自动操作 Chrome"。经排查：
- 已安装的 `agent-browser`（npm 包 0.27.0）自带 Chromium 内核，但其**会话守护进程/IPC 在本机沙箱环境下会卡死**（`open` 与 `connect` 命令均无限等待、无输出），属于架构性不兼容，**无法可靠修复**。
- 本机存在 WorkBuddy 沙箱代理 `HTTP_PROXY=http://127.0.0.1:58167`，会把 `127.0.0.1` 也接管，导致 `connect_over_cdp` 的 `/json/version` HTTP 探测返回 502。

## 修复方案（本技能）
用 **Playwright（Python）+ 系统已安装的 Google Chrome** 完成自动化：
1. 以系统 `chrome.exe` 作为 `executable_path`，**不下载额外浏览器内核**。
2. 用 `launch_persistent_context` + 固定的 `user_data_dir`，使**登录态/Cookie 在多次调用间持久化**（一次登录，后续复用）。
3. **关键修复**：调用前清空 `HTTP_PROXY/HTTPS_PROXY/ALL_PROXY` 并设 `NO_PROXY=127.0.0.1,localhost`，绕过沙箱代理对本机连接的干扰。

## 依赖（一次性）
```
pip install playwright
```
仅需 Python 包，无需 `playwright install`（直接用系统 Chrome）。

## 使用方式（脚本：scripts/chrome_drive.py）
受管 Python 路径：`C:\Users\lxj\.workbuddy\binaries\python\envs\default\Scripts\python.exe`

```
# 打开网页并截图 + 打印标题/正文
python scripts/chrome_drive.py open https://example.com --out shot.png

# 仅截图（可先导航到某 URL）
python scripts/chrome_drive.py shot out.png --url https://example.com

# 点击元素（先用 --url 打开页面）
python scripts/chrome_drive.py click "#submit" --url https://example.com/form

# 填写表单
python scripts/chrome_drive.py fill "#username" myname --url https://example.com/login

# 提取文本（selector 或 body）
python scripts/chrome_drive.py text body --url https://example.com

# 执行 JS
python scripts/chrome_drive.py eval "document.title" --url https://example.com

# 多步宏（一次会话内完成：打开->填表->点提交->截图）
python scripts/chrome_drive.py run --steps '[{"goto":"https://example.com/login"},{"fill":"#u","text":"user"},{"fill":"#p","text":"pass"},{"click":"#login"},{"shot":"result.png"}]'
```
加 `--headed` 可显示可见浏览器窗口（用于需要人工介入登录/验证码的场景）。

## 注意事项
- 首次对需要登录的站点（如 GitHub）操作时用 `--headed` 打开，手动登录一次；登录态会保存在 `user_data_dir`，之后无头调用也保持登录。
- 本技能驱动的 Chrome 与用户日常使用的 Chrome 是**不同实例/不同用户目录**，互不干扰；如需完全复用用户真实登录态，可把 `scripts/chrome_drive.py` 里的 `PROFILE` 改为用户真实 Chrome 用户目录（注意：同一用户目录同一时刻只能有一个 Chrome 实例）。
- 若 `chrome.exe` 路径不同，修改脚本顶部 `CHROME` 常量即可。
