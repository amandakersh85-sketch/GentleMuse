#!/usr/bin/env bash
# Daily Blotato queue top-up for The Gentle Muse - POSIX runner.
#
# On Amanda's Windows machine the scheduled task calls run-blotato-refill.ps1
# instead; this script is the bash-environment equivalent (Git Bash, WSL,
# Linux, macOS) and keeps the routine portable.
#
# Repo root is hard-coded, resolved at install time, NOT $PWD, so the job
# works from any starting directory.
#
# Exits non-zero when the run fails so the scheduler surfaces it.

set -uo pipefail

REPO_ROOT="D:/Claude Projects/GentleMuse"
PROMPT_FILE="$REPO_ROOT/routines/RUN_blotato-refill.md"
LOG_DIR="$REPO_ROOT/routines/logs"
LOG_FILE="$LOG_DIR/blotato-refill-$(date +%F).log"

mkdir -p "$LOG_DIR"

{
  echo ""
  echo "==================================================================="
  echo "RUN START  $(date '+%F %T %z')  (local time)"
  echo "==================================================================="
} >>"$LOG_FILE"

if [ ! -f "$PROMPT_FILE" ]; then
  echo "FATAL: prompt file not found at $PROMPT_FILE" >>"$LOG_FILE"
  exit 1
fi

cd "$REPO_ROOT" || { echo "FATAL: cannot cd to $REPO_ROOT" >>"$LOG_FILE"; exit 1; }

echo "git pull: $(git pull --ff-only 2>&1)" >>"$LOG_FILE"

# Explicit allowlist. Deliberately NOT --dangerously-skip-permissions.
# Blotato tool prefix verified headless on this machine 2026-09-02.
ALLOWED="mcp__claude_ai_Blotato__blotato_list_accounts,\
mcp__claude_ai_Blotato__blotato_list_posts,\
mcp__claude_ai_Blotato__blotato_create_post,\
mcp__claude_ai_Blotato__blotato_get_post_status,\
mcp__claude_ai_Google_Drive__search_files,\
mcp__claude_ai_Google_Drive__create_file,\
mcp__claude_ai_Google_Drive__read_file_content,\
Read,Write,Edit,Glob,Grep,Bash(python *),Bash(git *)"

echo "invoking claude headless..." >>"$LOG_FILE"
START=$(date +%s)

claude -p "$(cat "$PROMPT_FILE")" \
  --permission-mode acceptEdits \
  --allowedTools "$ALLOWED" \
  --add-dir "$REPO_ROOT" >>"$LOG_FILE" 2>&1
CODE=$?

MINS=$(( ($(date +%s) - START) / 60 ))
{
  echo ""
  echo "RUN END    $(date '+%F %T %z')  exit=$CODE  ${MINS} min"
} >>"$LOG_FILE"

if [ "$CODE" -ne 0 ]; then
  echo "FAILED with exit code $CODE" >>"$LOG_FILE"
  exit "$CODE"
fi
exit 0
