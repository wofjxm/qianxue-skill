#!/bin/zsh
# 灵感入库：每天 9:00 由 launchd 触发
# 部署：替换 {{VAULT_PATH}} 和 {{AGENT_CLI}} 后放到 ~/.local/bin/，chmod +x
set -e
VAULT="{{VAULT_PATH}}"
AGENT="{{AGENT_CLI}}"
INSTRUCTION="$VAULT/选题灵感库/_早间入库说明.md"
LOG="/tmp/wb-import.log"
# launchd 环境没有用户 PATH，显式补上
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
echo "[$(date '+%F %T')] wb-import start" >> "$LOG"
"$AGENT" \
  -p "请严格按 $INSTRUCTION 第二节的流程跑灵感入库。读完后从 $VAULT/选题灵感库/0-随手录入.md 扫所有 - [ ] 未勾选行, 生成选题卡; 无发布日期的卡推入选题池, 带发布日期的卡按「直接排期」规则: 同时读 $VAULT/时间管理/_早间排期指令.md 执行倒排期(生成环节笔记/日历事件/每日小记任务/看板分卡), 原卡勾选归档到「📦 已排期」列; 最后标记原行已处理。汇报: 新增了几张卡、哪些直接排期了、跳过了哪些。" \
  --add-dir "$VAULT" \
  >> "$LOG" 2>&1
echo "[$(date '+%F %T')] wb-import done" >> "$LOG"
