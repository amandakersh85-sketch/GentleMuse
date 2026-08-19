<#
  GM-Photo-Triage.ps1  —  Run 4 photo module for the Gentle Muse filing system
  ----------------------------------------------------------------------------
  Companion to asset_scanner.py and GM-Video-Triage.ps1. Photos are NOT video:
  volume is 10x to 100x higher, the real enemy is BURST near-duplicates rather
  than exact copies, Google Takeout ships sidecar JSON and -edited twins, and
  screenshots masquerade as content. This handles all four.

  PROPOSE-ONLY by default. -Execute moves to _QUARANTINE. Never deletes.

  USAGE
    .\GM-Photo-Triage.ps1 -Root "D:\Takeout\Google Photos"
    .\GM-Photo-Triage.ps1 -Root "D:\Photos" -Lane CGY
    .\GM-Photo-Triage.ps1 -Root "D:\Photos" -Execute
#>

[CmdletBinding()]
param(
  [string]$Root = "D:\",
  [string]$Out  = "$env:USERPROFILE\Desktop\GM-Photo-Triage",
  [ValidateSet('auto','GM','KV','CGY','FS','OF','Personal')]
  [string]$Lane = 'auto',
  [int]$MinMegapixels = 1,
  [int]$SheetCols = 6,
  [int]$SheetRows = 6,
  [switch]$NoSheets,
  [switch]$Execute
)

$ErrorActionPreference = 'Continue'
$PhotoExt = @('.jpg','.jpeg','.png','.heic','.heif','.webp','.bmp','.tif','.tiff','.dng','.cr2','.nef','.arw','.gif')

# common phone/desktop screen sizes -> screenshot tell
$ScreenSizes = @('1080x1920','1920x1080','1080x2400','2400x1080','1440x2560','1170x2532','1284x2778',
                 '828x1792','750x1334','2560x1440','1366x768','1536x2048','2048x1536','1179x2556',
                 '1290x2796','1440x3200','1080x2340','1600x900','1280x720','3840x2160')

Write-Host ""
Write-Host "  GENTLE MUSE - PHOTO TRIAGE (RUN 4)" -ForegroundColor Magenta
if ($Execute) { Write-Host "  MODE: EXECUTE - moves flagged to _QUARANTINE, no deletions" -ForegroundColor Yellow }
else          { Write-Host "  MODE: PROPOSE-ONLY - nothing will be touched" -ForegroundColor DarkGray }
Write-Host ""

if (-not (Test-Path -LiteralPath $Root)) {
  Write-Host "  Can't find: $Root" -ForegroundColor Red; exit 1
}
New-Item -ItemType Directory -Force -Path $Out | Out-Null
$ThumbDir = Join-Path $Out 'thumbs'
$SheetDir = Join-Path $Out 'contact-sheets'
if (-not $NoSheets) { New-Item -ItemType Directory -Force -Path $ThumbDir,$SheetDir | Out-Null }

function Find-Tool([string]$n) {
  $c = Get-Command $n -ErrorAction SilentlyContinue; if ($c) { return $c.Source }
  foreach ($p in @("$env:ProgramData\chocolatey\bin\$n.exe","$env:LOCALAPPDATA\Microsoft\WinGet\Links\$n.exe",
                   "C:\ffmpeg\bin\$n.exe","$env:ProgramFiles\ffmpeg\bin\$n.exe")) { if (Test-Path -LiteralPath $p) { return $p } }
  return $null
}
$ffprobe = Find-Tool 'ffprobe'; $ffmpeg = Find-Tool 'ffmpeg'
if ($ffprobe) { Write-Host "  ffprobe OK - dimensions ON" -ForegroundColor Green }
else { Write-Host "  ffprobe missing - dimensions OFF.  winget install Gyan.FFmpeg" -ForegroundColor Yellow }

function Get-Lane([string]$path) {
  if ($Lane -ne 'auto') { return $Lane }
  $p = $path.ToLower()
  if ($p -match 'princesa|cesa|golden.?year') { return 'CGY' }
  if ($p -match 'kersh|vending')              { return 'KV' }
  if ($p -match 'fresh.?spin|laundry')        { return 'FS' }
  if ($p -match '\bof\b|onlyfans')            { return 'OF' }
  if ($p -match 'family|memories|personal')   { return 'Personal' }
  return 'GM'
}

# --- Google Takeout sidecar JSON: real capture time + GPS ---
function Get-Sidecar($file) {
  foreach ($cand in @("$($file.FullName).json",
                      "$($file.FullName).supplemental-metadata.json",
                      (Join-Path $file.DirectoryName ($file.BaseName + '.json')))) {
    if (Test-Path -LiteralPath $cand) {
      try { return Get-Content -LiteralPath $cand -Raw -ErrorAction Stop | ConvertFrom-Json } catch { }
    }
  }
  return $null
}

Write-Host ""; Write-Host "  Scanning $Root ..." -ForegroundColor Cyan
$files = Get-ChildItem -LiteralPath $Root -Recurse -File -ErrorAction SilentlyContinue |
         Where-Object { $PhotoExt -contains $_.Extension.ToLower() }
$total = ($files | Measure-Object).Count
if ($total -eq 0) { Write-Host "  No photos found." -ForegroundColor Yellow; exit 0 }
Write-Host "  $total photos found." -ForegroundColor Green

# --- exact duplicates: hash only size collisions ---
Write-Host "  Hashing size-collisions..." -ForegroundColor Cyan
$hashOf = @{}
foreach ($g in ($files | Group-Object Length | Where-Object { $_.Count -gt 1 })) {
  foreach ($f in $g.Group) { try { $hashOf[$f.FullName] = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash } catch {} }
}
$hashCount = @{}
foreach ($h in $hashOf.Values) { if ($h) { if ($hashCount.ContainsKey($h)) { $hashCount[$h]++ } else { $hashCount[$h]=1 } } }

# --- pass 1: gather facts ---
Write-Host "  Reading metadata..." -ForegroundColor Cyan
$info = @{}
$i = 0
foreach ($f in $files) {
  $i++
  if ($i % 25 -eq 0 -or $i -eq $total) { Write-Progress -Activity "Reading photos" -Status "$i / $total" -PercentComplete (($i/$total)*100) }

  $w=0; $h=0
  if ($ffprobe) {
    try {
      $p = & $ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=noprint_wrappers=1:nokey=0 -- "$($f.FullName)" 2>$null
      foreach ($ln in $p) { if ($ln -match '^width=(\d+)') { $w=[int]$Matches[1] }; if ($ln -match '^height=(\d+)') { $h=[int]$Matches[1] } }
    } catch {}
  }

  $side = Get-Sidecar $f
  $taken = $f.LastWriteTime; $gps = ''
  if ($side) {
    if ($side.photoTakenTime.timestamp) {
      try { $taken = [DateTimeOffset]::FromUnixTimeSeconds([int64]$side.photoTakenTime.timestamp).LocalDateTime } catch {}
    }
    if ($side.geoData -and ($side.geoData.latitude -ne 0 -or $side.geoData.longitude -ne 0)) { $gps = 'GPS' }
  }

  $info[$f.FullName] = [pscustomobject]@{
    File=$f; W=$w; H=$h; Taken=$taken; GPS=$gps
    Res = if ($w -and $h) { "$($w)x$($h)" } else { '' }
    MP  = if ($w -and $h) { [math]::Round(($w*$h)/1MB,1) } else { 0 }
    IsEdited = ($f.BaseName -match '-edited$|\(edited\)$')
    IsScreenshot = ($f.Name -match '(?i)screen\s?shot|screenshot|snipaste|^capture[_\-\s]') -or
                   ($w -and $h -and ($ScreenSizes -contains "$($w)x$($h)"))
  }
}
Write-Progress -Activity "Reading photos" -Completed

# --- burst grouping: same minute + same dimensions ---
Write-Host "  Grouping bursts..." -ForegroundColor Cyan
$burstKey = @{}
foreach ($k in $info.Keys) {
  $x = $info[$k]
  $burstKey[$k] = "{0}|{1}" -f $x.Taken.ToString('yyyyMMddHHmm'), $x.Res
}
$burstGroups = $info.Keys | Group-Object { $burstKey[$_] } | Where-Object { $_.Count -gt 1 -and $_.Name -notmatch '\|$' }
$burstBest = @{}
foreach ($g in $burstGroups) {
  # largest file in the burst is usually the least-compressed / sharpest keeper
  $best = ($g.Group | Sort-Object { $info[$_].File.Length } -Descending | Select-Object -First 1)
  $burstBest[$g.Name] = $best
}

# --- pass 2: verdicts ---
$rows = New-Object System.Collections.Generic.List[object]
$seenHash = @{}
$i = 0
foreach ($f in $files) {
  $i++
  $x = $info[$f.FullName]
  $hash = $hashOf[$f.FullName]

  $dupeRole = ''
  if ($hash -and $hashCount[$hash] -gt 1) {
    if ($seenHash.ContainsKey($hash)) { $dupeRole = 'DUPLICATE-COPY' } else { $seenHash[$hash] = $f.Name; $dupeRole = 'KEEPER' }
  }

  $bk = $burstKey[$f.FullName]
  $inBurst = $burstBest.ContainsKey($bk)
  $isBurstBest = $inBurst -and ($burstBest[$bk] -eq $f.FullName)

  $verdict=''; $why=''
  if ($dupeRole -eq 'DUPLICATE-COPY')          { $verdict='CUT';    $why="exact duplicate of $($seenHash[$hash])" }
  elseif ($inBurst -and -not $isBurstBest)     { $verdict='CUT';    $why='burst near-duplicate, better frame kept' }
  elseif ($x.IsScreenshot)                     { $verdict='CUT';    $why='screenshot, not content' }
  elseif ($f.Length -lt 30KB)                  { $verdict='CUT';    $why='tiny / likely thumbnail or broken' }
  elseif ($x.MP -gt 0 -and $x.MP -lt $MinMegapixels) { $verdict='CUT'; $why="under $MinMegapixels MP, too small to post" }
  elseif ($x.GPS -eq 'GPS')                    { $verdict='REVIEW'; $why='carries GPS location, strip before posting' }
  elseif ($x.IsEdited)                         { $verdict='KEEP';   $why='Takeout edited version, deliberate edit' }
  elseif ($x.W -and $x.H -and $x.H -ge $x.W)   { $verdict='KEEP';   $why='vertical or square, post ready' }
  else                                         { $verdict='REVIEW'; $why='landscape or unreadable, needs eyes' }

  $rows.Add([pscustomobject]@{
    'Asset Name'       = $f.Name
    'Type'             = 'Image'
    'Lane'             = (Get-Lane $f.FullName)
    'Category / Use'   = if ($x.IsScreenshot) {'Screenshot'} elseif ($x.IsEdited) {'Edited photo'} else {'Content photo'}
    'Lives On'         = 'Local'
    'Folder / Location'= $f.DirectoryName
    'Direct Link'      = ''
    'Status'           = if ($verdict -eq 'KEEP') {'Active'} else {'Review'}
    'Needs Filing?'    = if ($verdict -eq 'KEEP') {'YES'} else {'No'}
    'Verdict'          = $verdict
    'Why'              = $why
    'Resolution'       = $x.Res
    'Megapixels'       = $x.MP
    'TakenDate'        = $x.Taken.ToString('yyyy-MM-dd')
    'BurstGroup'       = if ($inBurst) { $bk } else { '' }
    'Privacy'          = $x.GPS
    'SizeKB'           = [math]::Round($f.Length/1KB,0)
    'Thumb'            = ''
    'FullPath'         = $f.FullName
    'SHA256'           = $hash
  })
}

# --- contact sheets: only for what a human still has to judge ---
$needEyes = @($rows | Where-Object { $_.Verdict -ne 'CUT' })
$sheets = 0
if ($ffmpeg -and -not $NoSheets -and $needEyes.Count -gt 0) {
  Write-Host "  Building contact sheets for $($needEyes.Count) survivors..." -ForegroundColor Cyan
  $per = $SheetCols * $SheetRows
  $tmp = Join-Path $Out '_tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null
  $batch = 0
  for ($s = 0; $s -lt $needEyes.Count; $s += $per) {
    $batch++
    Get-ChildItem -LiteralPath $tmp -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    $slice = $needEyes[$s..([math]::Min($s+$per-1, $needEyes.Count-1))]
    $n = 0
    foreach ($r in $slice) {
      $n++
      $dst = Join-Path $tmp ("t{0:D3}.jpg" -f $n)
      try { & $ffmpeg -y -v error -i "$($r.FullPath)" -vf "scale=240:240:force_original_aspect_ratio=decrease,pad=240:240:(ow-iw)/2:(oh-ih)/2:color=white" -frames:v 1 -- "$dst" 2>$null | Out-Null } catch {}
    }
    if ((Get-ChildItem -LiteralPath $tmp -Filter 't*.jpg' -ErrorAction SilentlyContinue).Count -gt 0) {
      $sheet = Join-Path $SheetDir ("sheet-{0:D3}.jpg" -f $batch)
      try {
        & $ffmpeg -y -v error -pattern_type sequence -start_number 1 -i (Join-Path $tmp 't%03d.jpg') `
          -vf "tile=$($SheetCols)x$($SheetRows):margin=6:padding=4:color=white" -frames:v 1 -q:v 4 -- "$sheet" 2>$null | Out-Null
        if (Test-Path -LiteralPath $sheet) { $sheets++ }
      } catch {}
    }
  }
  Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue
}

$csv = Join-Path $Out 'photo-triage.csv'
$rows | Export-Csv -LiteralPath $csv -NoTypeInformation -Encoding UTF8

$cut=@($rows|Where-Object{$_.Verdict -eq 'CUT'}); $keep=@($rows|Where-Object{$_.Verdict -eq 'KEEP'})
$rev=@($rows|Where-Object{$_.Verdict -eq 'REVIEW'}); $gps=@($rows|Where-Object{$_.Privacy -eq 'GPS'})
$shots=@($rows|Where-Object{$_.'Category / Use' -eq 'Screenshot'})
$freeMB=[math]::Round((($cut|Measure-Object SizeKB -Sum).Sum)/1024,1)

$moved = 0
if ($Execute -and $cut.Count -gt 0) {
  $q = Join-Path $Out '_QUARANTINE'; New-Item -ItemType Directory -Force -Path $q | Out-Null
  foreach ($r in $cut) {
    try {
      $dest = Join-Path $q $r.'Asset Name'; $n=1
      while (Test-Path -LiteralPath $dest) { $dest = Join-Path $q ("{0}_{1}{2}" -f [IO.Path]::GetFileNameWithoutExtension($r.'Asset Name'),$n,[IO.Path]::GetExtension($r.'Asset Name')); $n++ }
      Move-Item -LiteralPath $r.FullPath -Destination $dest -ErrorAction Stop; $moved++
    } catch { Write-Host "  could not move: $($r.'Asset Name')" -ForegroundColor DarkYellow }
  }
}

$summary = @"
GENTLE MUSE - PHOTO TRIAGE, RUN 4
Scanned : $Root
When    : $(Get-Date -Format 'yyyy-MM-dd HH:mm')
Mode    : $(if($Execute){'EXECUTE'}else{'PROPOSE-ONLY'})

Total photos ......... $total
KEEP ................. $($keep.Count)   (vertical or square, post ready)
REVIEW ............... $($rev.Count)
CUT .................. $($cut.Count)   ($freeMB MB)
  of which screenshots $($shots.Count)
  burst near-dupes     $(@($cut|Where-Object{$_.Why -match 'burst'}).Count)
PRIVACY, carries GPS . $($gps.Count)   strip before posting
Contact sheets ....... $sheets
$(if($Execute){"Moved to _QUARANTINE  $moved  (nothing deleted)"}else{"Nothing moved. Re-run with -Execute to quarantine the CUT list."})

Report : $csv
Sheets : $SheetDir

NEXT -> send the contact-sheets folder and the CSV to Claude.
Sheets only cover KEEP and REVIEW. The CUT pile needs no eyes.
"@
$summary | Set-Content -LiteralPath (Join-Path $Out 'SUMMARY.txt') -Encoding UTF8
Write-Host ""; Write-Host $summary -ForegroundColor White
Write-Host "  Done." -ForegroundColor Green; Write-Host ""
