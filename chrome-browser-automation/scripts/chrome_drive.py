#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chrome_drive.py —— 用 Playwright 直接驱动【系统已安装的 Chrome】完成浏览器自动化。
这是 agent-browser 在本机（其会话守护进程/IPC 会卡死）的可靠替代方案。

原理：
  - 用系统 Chrome 作为可执行文件（不下载额外浏览器内核），复用你本机 Chrome。
  - 用 launch_persistent_context + 固定 user_data_dir，使登录态/Cookie 在多次调用间持久化。
  - 关键修复：清空 HTTP_PROXY/HTTPS_PROXY 等环境变量，避免本机沙箱代理把 127.0.0.1 接管导致连接失败。

用法：
  python chrome_drive.py open  <url>  [--headed] [--out shot.png]
  python chrome_drive.py shot  <path> [--headed] [--url <url>]
  python chrome_drive.py click <selector>            [--url <url>] [--headed]
  python chrome_drive.py fill  <selector> <text>    [--url <url>] [--headed]
  python chrome_drive.py text  <selector|body>      [--url <url>] [--headed]
  python chrome_drive.py eval  <js>                 [--url <url>] [--headed]
  python chrome_drive.py run   --steps '<json数组>'  [--headed]
        steps 例：[{"goto":"https://x.com"},{"fill":"#user","text":"a"},{"click":"#btn"},{"shot":"o.png"}]

依赖：pip install playwright   （仅需 Python 包，无需下载 chromium 内核）
"""
import sys, os, json, argparse

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE = os.path.join(os.path.expanduser("~"), ".agent-browser", "auto-profile")
os.makedirs(PROFILE, exist_ok=True)

# 关键修复：禁止本机沙箱代理干扰本地浏览器连接
for _k in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
    os.environ[_k] = ""
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright


def _ctx_args(headed):
    return dict(
        user_data_dir=PROFILE,
        executable_path=CHROME,
        headless=not headed,
        args=["--no-sandbox", "--disable-gpu", "--no-first-run", "--disable-dev-shm-usage"],
    )


def _new_page(context, url=None):
    page = context.new_page() if not context.pages else context.pages[0]
    page.set_viewport_size({"width": 1280, "height": 900})
    if url:
        page.goto(url, wait_until="load", timeout=40000)
        page.wait_for_timeout(2500)
    return page


def open_url(url, headed, out):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(**_ctx_args(headed))
        page = _new_page(ctx, url)
        print("TITLE:", page.title())
        print("URL  :", page.url)
        if out:
            page.screenshot(path=out, full_page=False)
            print("SHOT :", out)
        print("BODY :", page.inner_text("body")[:500].replace("\n", " "))
        ctx.close()


def shot(path, url, headed):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(**_ctx_args(headed))
        page = _new_page(ctx, url)
        page.screenshot(path=path, full_page=False)
        print("SHOT :", path, "SIZE:", os.path.getsize(path))
        ctx.close()


def click(sel, url, headed):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(**_ctx_args(headed))
        page = _new_page(ctx, url)
        page.click(sel, timeout=15000)
        page.wait_for_timeout(1500)
        print("CLICKED:", sel, "->", page.url)
        ctx.close()


def fill(sel, text, url, headed):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(**_ctx_args(headed))
        page = _new_page(ctx, url)
        page.fill(sel, text, timeout=15000)
        print("FILLED:", sel, "=", text)
        ctx.close()


def text(sel, url, headed):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(**_ctx_args(headed))
        page = _new_page(ctx, url)
        val = page.inner_text(sel) if sel != "body" else page.inner_text("body")
        print("TEXT:", val[:1000].replace("\n", " "))
        ctx.close()


def eval_js(js, url, headed):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(**_ctx_args(headed))
        page = _new_page(ctx, url)
        print("EVAL:", page.evaluate(js))
        ctx.close()


def run_steps(steps, headed):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(**_ctx_args(headed))
        page = ctx.new_page()
        page.set_viewport_size({"width": 1280, "height": 900})
        for i, step in enumerate(steps):
            act = step.get("action") or list(step.keys())[0]
            if act == "goto":
                page.goto(step["goto"], wait_until="load", timeout=40000); page.wait_for_timeout(2000)
                print(f"[{i}] goto ->", page.url)
            elif act == "fill":
                page.fill(step["fill"], step.get("text", ""), timeout=15000); print(f"[{i}] fill {step['fill']}")
            elif act == "click":
                page.click(step["click"], timeout=15000); page.wait_for_timeout(1200); print(f"[{i}] click {step['click']}")
            elif act == "shot":
                page.screenshot(path=step["shot"], full_page=False); print(f"[{i}] shot {step['shot']}")
            elif act == "text":
                print(f"[{i}] text:", page.inner_text(step.get("text", "body"))[:800].replace("\n", " "))
            elif act == "wait":
                page.wait_for_timeout(int(step.get("wait", 1000)))
        ctx.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["open", "shot", "click", "fill", "text", "eval", "run"])
    ap.add_argument("arg", nargs="*", help="selector / url / text / js")
    ap.add_argument("--url", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--steps", default=None)
    a = ap.parse_args()

    if a.action == "open":
        open_url(a.arg[0] if a.arg else "about:blank", a.headed, a.out)
    elif a.action == "shot":
        shot(a.arg[0] if a.arg else "shot.png", a.url, a.headed)
    elif a.action == "click":
        click(a.arg[0], a.url, a.headed)
    elif a.action == "fill":
        fill(a.arg[0], a.arg[1] if len(a.arg) > 1 else "", a.url, a.headed)
    elif a.action == "text":
        text(a.arg[0] if a.arg else "body", a.url, a.headed)
    elif a.action == "eval":
        eval_js(a.arg[0] if a.arg else "document.title", a.url, a.headed)
    elif a.action == "run":
        steps = json.loads(a.steps) if a.steps else []
        run_steps(steps, a.headed)


if __name__ == "__main__":
    main()
