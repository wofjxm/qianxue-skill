#!/bin/zsh
# 倒排期：每天 9:05 由 launchd 触发
# 部署：替换 {{VAULT_PATH}} 和 {{AGENT_CLI}} 后放到 ~/.local/bin/，chmod +x
set -e
VAULT="{{VAULT_PATH}}"
AGENT="{{AGENT_CLI}}"
INSTRUCTION="$VAULT/时间管理/_早间排期指令.md"
LOG="/tmp/wb-schedule.log"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
echo "[$(date '+%F %T')] wb-schedule start" >> "$LOG"
"$AGENT" \
  -p "请严格按 $INSTRUCTION 跑早间排期任务。扫「📥 选题池」列所有写了 📅 日期的卡, 按节奏倒推各环节日期, 生成日历事件到 $VAULT/内容日历/流程日历/、环节笔记到 $VAULT/环节档案/、每日小记 #task, 看板追加 4 张分卡, 原卡勾选归档到「📦 已排期」。没写日期的卡留在选题池不动。汇报: 为哪几张选题排了期、缺日期/冲突的选题。" \
  --add-dir "$VAULT" \
  >> "$LOG" 2>&1
echo "[$(date '+%F %T')] wb-schedule done" >> "$LOG"
