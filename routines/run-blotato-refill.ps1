<#
  Daily Blotato queue top-up for The Gentle Muse - local runner.

  Called by the Windows Task Scheduler job "GM Blotato Daily Refill".
  Runs Claude Code headless against routines/RUN_blotato-refill.md.

  Repo root is hard-coded below, resolved at install time, NOT $PWD, so the
  task works no matter what directory the scheduler starts it in.

  Exits non-zero when the run fails so the scheduler surfaces it.
#>

$ErrorActionPreference = 'Continue'

# Resolved at install time (2026-09-02). Do not switch this to $PWD.
$RepoRoot   = 'D:\Claude Projects\GentleMuse'
$PromptFile = Join-Path $RepoRoot 'routines\RUN_blotato-refill.md'
$LogDir     = Join-Path $RepoRoot 'routines\logs'
$Stamp      = Get-Date -Format 'yyyy-MM-dd'
$LogFile    = Join-Path $LogDir "blotato-refill-$Stamp.log"

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Force -Path $LogDir | Out-Null }

function Write-Log { param([string]$m) Add-Content -Path $LogFile -Value $m -Encoding utf8 }

Write-Log ""
Write-Log "==================================================================="
Write-Log "RUN START  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss K')  (local time)"
Write-Log "==================================================================="

if (-not (Test-Path $PromptFile)) {
    Write-Log "FATAL: prompt file not found at $PromptFile"
    exit 1
}

Set-Location $RepoRoot

# Keep the local copy current. A failed pull is not fatal for a local run:
# the working tree is authoritative here.
$pull = & git pull --ff-only 2>&1 | Out-String
Write-Log "git pull: $($pull.Trim())"

$prompt = Get-Content -Path $PromptFile -Raw -Encoding utf8

# Explicit allowlist. Deliberately NOT --dangerously-skip-permissions.
# Blotato tool prefix verified headless on this machine 2026-09-02.
$allowed = @(
    'mcp__claude_ai_Blotato__blotato_list_accounts',
    'mcp__claude_ai_Blotato__blotato_list_posts',
    'mcp__claude_ai_Blotato__blotato_create_post',
    'mcp__claude_ai_Blotato__blotato_get_post_status',
    'mcp__claude_ai_Google_Drive__search_files',
    'mcp__claude_ai_Google_Drive__create_file',
    'mcp__claude_ai_Google_Drive__read_file_content',
    'Read', 'Write', 'Edit', 'Glob', 'Grep',
    'Bash(python *)',
    'Bash(git *)'
)

Write-Log "invoking claude headless..."
$started = Get-Date

# stdout and stderr both land in the day's log.
& claude -p $prompt `
    --permission-mode acceptEdits `
    --allowedTools $allowed `
    --add-dir $RepoRoot 2>&1 |
  ForEach-Object { Add-Content -Path $LogFile -Value $_ -Encoding utf8 }

$code = $LASTEXITCODE
$mins = [math]::Round(((Get-Date) - $started).TotalMinutes, 1)

Write-Log ""
Write-Log "RUN END    $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss K')  exit=$code  ${mins} min"

if ($code -ne 0) {
    Write-Log "FAILED with exit code $code"
    exit $code
}
exit 0
