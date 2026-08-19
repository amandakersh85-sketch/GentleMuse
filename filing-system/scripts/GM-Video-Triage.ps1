<#
  GM-Video-Triage.ps1  —  video module for Amanda's existing asset filing system
  ------------------------------------------------------------------------------
  This does NOT replace asset_scanner.py. It adds the layer that one can't do:
  video-specific triage (duration, resolution, orientation, thumbnails) and
  outputs rows in the EXACT Gentle Muse Master Asset Index schema so results
  paste straight into the card catalog.

  Follows the house rule from your Day 8 system: PROPOSE-ONLY by default.
  Nothing is moved or deleted unless you explicitly pass -Execute, and even
  then it only MOVES to a quarantine folder. It never hard-deletes. Ever.

  USAGE
    .\GM-Video-Triage.ps1 -Root "D:\Takeout"
    .\GM-Video-Triage.ps1 -Root "D:\Footage" -Lane GM
    .\GM-Video-Triage.ps1 -Root "D:\Footage" -Execute      # moves flagged -> _QUARANTINE
#>

[CmdletBinding()]
param(
  [string]$Root = "D:\",
  [string]$Out  = "$env:USERPROFILE\Desktop\GM-Video-Triage",
  [ValidateSet('auto','GM','KV','CGY','FS','OF','Personal')]
  [string]$Lane = 'auto',
  [int]$ThumbWidth = 320,
  [switch]$NoThumbs,
  [switch]$Execute            # opt-in: move flagged files to _QUARANTINE (never deletes)
)

$ErrorActionPreference = 'Continue'
$VideoExt = @('.mp4','.mov','.m4v','.avi','.mkv','.webm','.wmv','.mpg','.mpeg','.3gp','.mts','.m2ts','.flv')

Write-Host ""
Write-Host "  GENTLE MUSE - VIDEO TRIAGE" -ForegroundColor Magenta
if ($Execute) { Write-Host "  MODE: EXECUTE (moves flagged files to _QUARANTINE - no deletions)" -ForegroundColor Yellow }
else          { Write-Host "  MODE: PROPOSE-ONLY (nothing will be touched)" -ForegroundColor DarkGray }
Write-Host ""

if (-not (Test-Path -LiteralPath $Root)) {
  Write-Host "  Can't find: $Root" -ForegroundColor Red
  Write-Host "  Try:  .\GM-Video-Triage.ps1 -Root 'D:\Takeout'" -ForegroundColor Yellow
  exit 1
}

New-Item -ItemType Directory -Force -Path $Out | Out-Null
$ThumbDir = Join-Path $Out 'thumbs'
if (-not $NoThumbs) { New-Item -ItemType Directory -Force -Path $ThumbDir | Out-Null }

function Find-Tool([string]$name) {
  $c = Get-Command $name -ErrorAction SilentlyContinue
  if ($c) { return $c.Source }
  foreach ($p in @("$env:ProgramData\chocolatey\bin\$name.exe",
                   "$env:LOCALAPPDATA\Microsoft\WinGet\Links\$name.exe",
                   "C:\ffmpeg\bin\$name.exe",
                   "$env:ProgramFiles\ffmpeg\bin\$name.exe")) {
    if (Test-Path -LiteralPath $p) { return $p }
  }
  return $null
}
$ffprobe = Find-Tool 'ffprobe'
$ffmpeg  = Find-Tool 'ffmpeg'
if ($ffprobe) { Write-Host "  ffprobe OK - durations + resolution ON" -ForegroundColor Green }
else { Write-Host "  ffprobe missing - no durations.  winget install Gyan.FFmpeg" -ForegroundColor Yellow }

# --- lane inference, matching your GM / KV / CGY / FS / OF / Personal split ---
function Get-Lane([string]$path) {
  if ($Lane -ne 'auto') { return $Lane }
  $p = $path.ToLower()
  if ($p -match 'princesa|cesa|golden.?year')      { return 'CGY' }
  if ($p -match 'kersh|vending')                   { return 'KV' }
  if ($p -match 'fresh.?spin|laundry')             { return 'FS' }
  if ($p -match '\bof\b|onlyfans')                 { return 'OF' }
  if ($p -match 'family|memories|personal')        { return 'Personal' }
  return 'GM'
}

# raw camera-capture naming -> Status "Raw", otherwise "Review"
function Get-Status([string]$name) {
  if ($name -match '^(VID|PXL|IMG|MVI|DSC|GX|GOPR)[_\-]?\d' -or
      $name -match '^\d{4}-\d{2}-\d{2}' -or
      $name -match '^\d{8}_\d{6}') { return 'Raw' }
  return 'Review'
}

Write-Host ""
Write-Host "  Scanning $Root ..." -ForegroundColor Cyan
$files = Get-ChildItem -LiteralPath $Root -Recurse -File -ErrorAction SilentlyContinue |
         Where-Object { $VideoExt -contains $_.Extension.ToLower() }
$total = ($files | Measure-Object).Count
if ($total -eq 0) { Write-Host "  No videos found under $Root" -ForegroundColor Yellow; exit 0 }
Write-Host "  $total videos found." -ForegroundColor Green

# --- SHA-256 duplicate detection, size-collision first (same method as asset_scanner) ---
Write-Host "  Hashing size-collisions for exact duplicates..." -ForegroundColor Cyan
$hashOf = @{}
foreach ($g in ($files | Group-Object Length | Where-Object { $_.Count -gt 1 })) {
  foreach ($f in $g.Group) {
    try { $hashOf[$f.FullName] = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash } catch {}
  }
}
$hashCount = @{}
foreach ($h in $hashOf.Values) { if ($h) { if ($hashCount.ContainsKey($h)) { $hashCount[$h]++ } else { $hashCount[$h] = 1 } } }

$rows = New-Object System.Collections.Generic.List[object]
$seen = @{}
$i = 0

foreach ($f in $files) {
  $i++
  Write-Progress -Activity "Triaging video" -Status "$i / $total  $($f.Name)" -PercentComplete (($i/$total)*100)

  $dur=''; $w=''; $h=''
  if ($ffprobe) {
    try {
      $probe = & $ffprobe -v error -select_streams v:0 `
                 -show_entries format=duration:stream=width,height `
                 -of default=noprint_wrappers=1:nokey=0 -- "$($f.FullName)" 2>$null
      foreach ($ln in $probe) {
        if ($ln -match '^duration=([\d\.]+)') { $dur = [math]::Round([double]$Matches[1],1) }
        if ($ln -match '^width=(\d+)')  { $w = $Matches[1] }
        if ($ln -match '^height=(\d+)') { $h = $Matches[1] }
      }
    } catch {}
  }

  $orient=''
  if ($w -and $h) { $orient = if ([int]$h -gt [int]$w) {'vertical'} elseif ([int]$w -eq [int]$h) {'square'} else {'landscape'} }

  $hash = $hashOf[$f.FullName]
  $dupeRole = ''
  if ($hash -and $hashCount[$hash] -gt 1) {
    if ($seen.ContainsKey($hash)) { $dupeRole = 'DUPLICATE-COPY' } else { $seen[$hash] = $f.Name; $dupeRole = 'KEEPER' }
  }

  $verdict=''; $why=''
  if ($dupeRole -eq 'DUPLICATE-COPY')                     { $verdict='CUT';    $why="exact duplicate of $($seen[$hash])" }
  elseif ($f.Length -lt 200KB)                            { $verdict='CUT';    $why='tiny / likely broken' }
  elseif ($dur -ne '' -and [double]$dur -lt 1.5)          { $verdict='CUT';    $why='under 1.5s fragment' }
  elseif ($dur -ne '' -and [double]$dur -gt 900)          { $verdict='REVIEW'; $why='over 15min - needs cutting' }
  elseif ($orient -eq 'landscape')                        { $verdict='REVIEW'; $why='landscape - not reel-native' }
  elseif ($orient -eq 'vertical' -and $dur -ne '' -and [double]$dur -ge 5 -and [double]$dur -le 180) {
                                                            $verdict='KEEP';   $why='vertical, reel-length' }
  else                                                    { $verdict='REVIEW'; $why='needs eyes' }

  $thumb=''
  if ($ffmpeg -and -not $NoThumbs -and $dupeRole -ne 'DUPLICATE-COPY') {
    $safe = ($f.BaseName -replace '[^\w\-]','_'); if ($safe.Length -gt 55) { $safe = $safe.Substring(0,55) }
    $tp = Join-Path $ThumbDir ("{0:D4}_{1}.jpg" -f $i, $safe)
    try {
      $seek = 1; if ($dur -ne '' -and [double]$dur -gt 6) { $seek = [math]::Floor([double]$dur * 0.1) }
      & $ffmpeg -y -v error -ss $seek -i "$($f.FullName)" -frames:v 1 -vf "scale=$ThumbWidth`:-2" -q:v 6 -- "$tp" 2>$null | Out-Null
      if (Test-Path -LiteralPath $tp) { $thumb = Split-Path $tp -Leaf }
    } catch {}
  }

  # Master Asset Index schema + triage columns
  $rows.Add([pscustomobject]@{
    'Asset Name'      = $f.Name
    'Type'            = 'Video'
    'Lane'            = (Get-Lane $f.FullName)
    'Category / Use'  = if ((Get-Status $f.Name) -eq 'Raw') {'Raw footage'} else {'Finished video'}
    'Lives On'        = 'Local'
    'Folder / Location'= $f.DirectoryName
    'Direct Link'     = ''
    'Status'          = (Get-Status $f.Name)
    'Needs Filing?'   = if ($verdict -eq 'KEEP') {'YES'} else {'No'}
    'Verdict'         = $verdict
    'Why'             = $why
    'DurationSec'     = $dur
    'Resolution'      = if ($w -and $h) { "$($w)x$($h)" } else { '' }
    'Orientation'     = $orient
    'SizeMB'          = [math]::Round($f.Length/1MB,2)
    'Modified'        = $f.LastWriteTime.ToString('yyyy-MM-dd')
    'Thumb'           = $thumb
    'FullPath'        = $f.FullName
    'SHA256'          = $hash
  })
}
Write-Progress -Activity "Triaging video" -Completed

$csv = Join-Path $Out 'video-triage.csv'
$rows | Export-Csv -LiteralPath $csv -NoTypeInformation -Encoding UTF8

$cut    = @($rows | Where-Object { $_.Verdict -eq 'CUT' })
$keep   = @($rows | Where-Object { $_.Verdict -eq 'KEEP' })
$review = @($rows | Where-Object { $_.Verdict -eq 'REVIEW' })
$freeMB = [math]::Round((($cut | Measure-Object SizeMB -Sum).Sum),1)

# --- EXECUTE: move only, never delete ---
$moved = 0
if ($Execute -and $cut.Count -gt 0) {
  $q = Join-Path $Out '_QUARANTINE'
  New-Item -ItemType Directory -Force -Path $q | Out-Null
  foreach ($r in $cut) {
    try {
      $dest = Join-Path $q $r.'Asset Name'
      $n=1; while (Test-Path -LiteralPath $dest) { $dest = Join-Path $q ("{0}_{1}{2}" -f [IO.Path]::GetFileNameWithoutExtension($r.'Asset Name'), $n, [IO.Path]::GetExtension($r.'Asset Name')); $n++ }
      Move-Item -LiteralPath $r.FullPath -Destination $dest -ErrorAction Stop
      $moved++
    } catch { Write-Host "  could not move: $($r.'Asset Name')" -ForegroundColor DarkYellow }
  }
}

$summary = @"
GENTLE MUSE - VIDEO TRIAGE
Scanned : $Root
When    : $(Get-Date -Format 'yyyy-MM-dd HH:mm')
Mode    : $(if($Execute){'EXECUTE'}else{'PROPOSE-ONLY'})

Total videos ....... $total
KEEP ............... $($keep.Count)   (vertical, reel-length)
REVIEW ............. $($review.Count)
CUT ................ $($cut.Count)   ($freeMB MB)
$(if($Execute){"Moved to _QUARANTINE  $moved  (nothing deleted)"}else{"Nothing was moved. Re-run with -Execute to quarantine the CUT list."})

Report : $csv
Thumbs : $ThumbDir

NEXT -> zip this folder, send to Claude for the visual keep/cut pass.
CSV columns match the Master Asset Index, so approved rows paste straight in.
"@

$summary | Set-Content -LiteralPath (Join-Path $Out 'SUMMARY.txt') -Encoding UTF8
Write-Host ""; Write-Host $summary -ForegroundColor White
Write-Host "  Done." -ForegroundColor Green; Write-Host ""
