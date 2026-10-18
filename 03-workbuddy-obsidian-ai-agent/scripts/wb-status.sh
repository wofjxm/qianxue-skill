#!/bin/zsh
# 状态同步：每天 21:00 由 launchd 触发，扫每日小记已勾选任务 → 同步看板和日历
# 部署：替换 {{VAULT_PATH}} 和 {{AGENT_CLI}} 后放到 ~/.local/bin/，chmod +x
set -e
VAULT="{{VAULT_PATH}}"
AGENT="{{AGENT_CLI}}"
LOG="/tmp/wb-status.log"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
echo "[$(date '+%F %T')] wb-status start" >> "$LOG"
"$AGENT" \
  -p "请严格按 $VAULT/时间管理/_早间排期指令.md 第 7 节「每晚同步完成状态」执行: 扫 $VAULT/每日小记/ 里已勾选 [x] 的 #task 任务行, 把对应 $VAULT/内容日历/流程日历/ 事件笔记的 complete 改为 true, 并把 $VAULT/时间管理/3-内容流程看板.md 对应卡片移到「✅ 已完成」列(发布环节直接删除该行)。汇报处理了哪些任务。" \
  --add-dir "$VAULT" \
  >> "$LOG" 2>&1
echo "[$(date '+%F %T')] wb-status done" >> "$LOG"
