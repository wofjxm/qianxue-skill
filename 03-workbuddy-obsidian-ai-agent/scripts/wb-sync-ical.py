#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian 内容排期 → 苹果系统日历单向同步
- 扫 内容日历/流程日历/*.md 的 frontmatter
- 先删日历里 description 含标记 [Obsidian 内容] 的旧事件，再重建
- 每个事件 description 附 obsidian:// 链接
由 launchd 每天 9:10 触发，也可手动跑

部署：替换 {{VAULT_PATH}} / {{VAULT_NAME}} / {{CAL_NAME}} 后放到 ~/.local/bin/，chmod +x
注意：首次运行会弹出「日历」权限申请，必须点允许；如果目标日历名不存在会报错——
先确认 {{CAL_NAME}} 已在苹果日历 App 的 iCloud 账户下建好。
"""
import os, re, subprocess, urllib.parse, tempfile

VAULT = "{{VAULT_PATH}}"          # vault 绝对路径
CAL_DIR = os.path.join(VAULT, "内容日历/流程日历")
TOPIC_DIR = os.path.join(VAULT, "选题灵感库")
VAULT_NAME = "{{VAULT_NAME}}"     # vault 显示名（obsidian:// 链接用）
CAL_NAME = "{{CAL_NAME}}"         # iCloud 下的目标日历名
MARKER = "[Obsidian 内容]"
LOG = "/tmp/wb-sync-ical.log"

def log(msg):
    import datetime
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now():%F %T}] {msg}\n")

def obsidian_url(note_path):
    return "obsidian://open?vault=" + urllib.parse.quote(VAULT_NAME) + \
"&file=" + urllib.parse.quote(note_path)

def parse_frontmatter(content):
    fm = {}
    m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                fm[k.strip()] = v.strip()
    return fm

def topic_keyword(title):
    if '·' in title:
        return title.split('·', 1)[1].strip()
    return title.strip()

def find_topic_note(keyword):
    if not os.path.isdir(TOPIC_DIR):
        return None
    for fname in sorted(os.listdir(TOPIC_DIR)):
        if fname.endswith('.md') and keyword in fname:
            return fname[:-3]
    return None

def collect_events():
    events = []
    for fname in sorted(os.listdir(CAL_DIR)):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(CAL_DIR, fname)
        with open(path, encoding='utf-8') as f:
            content = f.read()
        fm = parse_frontmatter(content)
        title = fm.get('title', fname[:-3])
        date = fm.get('date', '')
        start = fm.get('startTime', '')
        end = fm.get('endTime', '')
        complete = (fm.get('complete', 'false') == 'true')
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        link = links[0].split('|')[0] if links else None
        if not link:
            topic = find_topic_note(topic_keyword(title))
            link = f"选题灵感库/{topic}" if topic else None
        if not date or not start:
            continue
        events.append({'title': title, 'date': date, 'start': start,
                       'end': end, 'complete': complete, 'link': link})
    return events

def build_jxa(events):
    lines = []
    lines.append('const app = Application("Calendar");')
    lines.append(f'const cal = app.calendars.byName("{CAL_NAME}");')
    lines.append('const evs = cal.events();')
    lines.append('for (const e of evs) {')
    lines.append('  try { if ((e.description()||"").includes("' + MARKER + \
'")) app.delete(e); } catch(err){}')
    lines.append('}')
    for ev in events:
        summary = ("✓ " if ev['complete'] else "") + ev['title']
        def esc(s):
            return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', \
'\\n')
        desc = MARKER + "\n" + (obsidian_url(ev['link']) if ev['link'] else \
"")
        start_iso = f"{ev['date']}T{ev['start']}:00"
        end_iso = f"{ev['date']}T{ev['end']}:00"
        lines.append(f'cal.events.push(app.Event({{summary:"{esc(summary)}",startDate:new Date("{start_iso}"),endDate:new Date("{end_iso}"),description:"{esc(desc)}"}}));')
    return '\n'.join(lines)

def main():
    events = collect_events()
    log(f"解析到 {len(events)} 个排期事件")
    jxa = build_jxa(events)
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, \
encoding='utf-8')
    tmp.write(jxa)
    tmp.close()
    try:
        r = subprocess.run(['osascript', '-l', 'JavaScript', tmp.name],
                           capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            log(f"osascript 错误: {r.stderr.strip()}")
            print(f"同步失败: {r.stderr.strip()}")
            return 1
        log(f"同步成功, 共 {len(events)} 个事件")
        print(f"同步成功: {len(events)} 个事件写入「{CAL_NAME}」")
        return 0
    finally:
        os.unlink(tmp.name)

if __name__ == '__main__':
    raise SystemExit(main())
