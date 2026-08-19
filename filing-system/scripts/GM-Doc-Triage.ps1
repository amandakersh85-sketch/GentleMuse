<#
  GM-Doc-Triage.ps1  —  Run 5 document module for the Gentle Muse filing system
  -----------------------------------------------------------------------------
  Third module after video (Run 3) and photos (Run 4). Documents invert the
  model: with photos the picture is the evidence. With documents the CONTENT is
  the sensitive part, so nothing readable leaves the machine by default.

  Handles the 4 things that make documents different:
    1. Versions, not duplicates. v1/v2/final/(1)/copy. NEWEST wins, not largest.
    2. Sensitive data is the dominant risk. Bank, tax, EIN, ID, medical.
       Those are HOLD. Never auto-routed, never redacted-out to a shareable file.
    3. Three separate LLCs. Misrouting a tax doc between GM, KV and FS is a
       real problem, not a tidiness problem.
    4. Retention. A 2023 statement isn't junk. It's ARCHIVE, not CUT.

  PROPOSE-ONLY by default. -Execute moves to _QUARANTINE. Never deletes.

  USAGE
    .\GM-Doc-Triage.ps1 -Root "$env:USERPROFILE\Downloads"
    .\GM-Doc-Triage.ps1 -Root "D:\Takeout" -Execute
#>

[CmdletBinding()]
param(
  [string]$Root = "$env:USERPROFILE\Downloads",
  [string]$Out  = "$env:USERPROFILE\Desktop\GM-Doc-Triage",
  [int]$ArchiveOlderThanYears = 1,
  [switch]$NoRedact,
  [switch]$Execute
)

$ErrorActionPreference = 'Continue'
$DocExt     = @('.pdf','.docx','.doc','.xlsx','.xls','.csv','.txt','.md','.rtf','.pptx','.odt','.ods','.pages','.numbers')
$InstallExt = @('.exe','.msi','.dmg','.pkg','.appx','.deb')
$ArchiveExt = @('.zip','.rar','.7z','.tar','.gz')

# sensitive -> HOLD. never auto-routed, never written to the shareable CSV.
$SensitiveRx = '(?i)statement|bank|credit.?union|tax|1099|w-?9\b|w-?2\b|irs|\bein\b|ssn|social.?security|payroll|insurance|premium|medical|health|dental|prescription|passport|driver.?licen|birth.?cert|mortgage|lease|loan|credit.?report|routing|account.?number|voided.?check'

# Your specific banks, insurers and providers do NOT belong in a public repo.
# Put them in sensitive-extra.txt next to this script, 1 term per line.
# That file is gitignored. See sensitive-extra.example.txt.
$extraPath = Join-Path $PSScriptRoot 'sensitive-extra.txt'
if (Test-Path -LiteralPath $extraPath) {
  $terms = Get-Content -LiteralPath $extraPath -ErrorAction SilentlyContinue |
           Where-Object { $_.Trim() -and $_ -notmatch '^\s*#' } |
           ForEach-Object { [regex]::Escape($_.Trim()) }
  if ($terms) { $SensitiveRx = $SensitiveRx + '|' + ($terms -join '|') }
  Write-Host "  Loaded $($terms.Count) local sensitive terms." -ForegroundColor Green
} else {
  Write-Host "  No sensitive-extra.txt found. Add your institutions there for stronger detection." -ForegroundColor DarkYellow
}
$LegalRx     = '(?i)certificate.?of.?organization|articles.?of|operating.?agreement|llc|filing|secretary.?of.?state|trademark|contract|agreement|nda|invoice|w-?9'
$ReceiptRx   = '(?i)receipt|order.?confirm|invoice|purchase|amazon|walmart|paypal|refund'

Write-Host ""
Write-Host "  GENTLE MUSE - DOCUMENT TRIAGE (RUN 5)" -ForegroundColor Magenta
if ($Execute) { Write-Host "  MODE: EXECUTE - moves CUT to _QUARANTINE, no deletions" -ForegroundColor Yellow }
else          { Write-Host "  MODE: PROPOSE-ONLY - nothing will be touched" -ForegroundColor DarkGray }
Write-Host "  Sensitive files are HELD and never written to the shareable report." -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path -LiteralPath $Root)) { Write-Host "  Can't find: $Root" -ForegroundColor Red; exit 1 }
New-Item -ItemType Directory -Force -Path $Out | Out-Null

function Get-Entity([string]$path) {
  $p = $path.ToLower()
  if ($p -match 'princesa|cesa|golden.?year')                 { return 'CGY' }
  if ($p -match 'kersh|vending|\bkv\b')                       { return 'KV' }
  if ($p -match 'fresh.?spin|laundry|\bfs\b')                 { return 'FS' }
  if ($p -match 'gentle.?muse|\bgm\b|payhip|manychat|blotato'){ return 'GM' }
  if ($p -match 'family|memories|personal|resume')            { return 'Personal' }
  return 'UNSORTED'
}

# strip version noise so v1 / v2 / final / (1) / copy collapse into one family
function Get-VersionKey([string]$base) {
  $b = $base.ToLower()
  $b = $b -replace '\s*[-_ ]?\(\d+\)\s*$',''
  $b = $b -replace '\s*[-_ ]?copy\s*$',''
  $b = $b -replace '\s*[-_ ]?(final|draft|rev|revised|updated|new|latest)\s*$',''
  $b = $b -replace '\s*[-_ ]?v(er|ersion)?\s?\d+(\.\d+)?\s*$',''
  $b = $b -replace '\s*[-_ ]?\d{1,2}[-_]\d{1,2}[-_]\d{2,4}\s*$',''
  $b = $b -replace '[\s_\-]+',' '
  return $b.Trim()
}

function Protect-Text([string]$s) {
  if ($NoRedact) { return $s }
  $t = $s -replace '\d{4,}','####'
  $t = $t -replace '(?i)(acct|account|routing|ein|ssn)[\s:_\-]*[\dxX\-]+','$1 ####'
  return $t
}

Write-Host "  Scanning $Root ..." -ForegroundColor Cyan
$all = Get-ChildItem -LiteralPath $Root -Recurse -File -ErrorAction SilentlyContinue
$files = $all | Where-Object { ($DocExt + $InstallExt + $ArchiveExt) -contains $_.Extension.ToLower() }
$total = ($files | Measure-Object).Count
if ($total -eq 0) { Write-Host "  Nothing to triage." -ForegroundColor Yellow; exit 0 }
Write-Host "  $total documents found." -ForegroundColor Green

Write-Host "  Hashing size-collisions..." -ForegroundColor Cyan
$hashOf = @{}
foreach ($g in ($files | Group-Object Length | Where-Object { $_.Count -gt 1 })) {
  foreach ($f in $g.Group) { try { $hashOf[$f.FullName] = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash } catch {} }
}
$hashCount = @{}
foreach ($h in $hashOf.Values) { if ($h) { if ($hashCount.ContainsKey($h)) { $hashCount[$h]++ } else { $hashCount[$h]=1 } } }

# version families: newest wins, unlike photo bursts where largest wins
Write-Host "  Grouping version families..." -ForegroundColor Cyan
$vkey = @{}
foreach ($f in $files) { $vkey[$f.FullName] = "{0}|{1}" -f (Get-VersionKey $f.BaseName), $f.Extension.ToLower() }
$vGroups = $files | Group-Object { $vkey[$_.FullName] } | Where-Object { $_.Count -gt 1 }
$vNewest = @{}
foreach ($g in $vGroups) { $vNewest[$g.Name] = ($g.Group | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName }

$rows = New-Object System.Collections.Generic.List[object]
$seen = @{}
$cutoff = (Get-Date).AddYears(-$ArchiveOlderThanYears)
$i = 0

foreach ($f in $files) {
  $i++
  if ($i % 25 -eq 0 -or $i -eq $total) { Write-Progress -Activity "Classifying" -Status "$i / $total" -PercentComplete (($i/$total)*100) }

  $ext = $f.Extension.ToLower()
  $hay = "$($f.Name) $($f.DirectoryName)"
  $isSensitive = $hay -match $SensitiveRx
  $isLegal     = $hay -match $LegalRx
  $isReceipt   = $hay -match $ReceiptRx
  $isInstaller = $InstallExt -contains $ext
  $isArchiveF  = $ArchiveExt -contains $ext

  $hash = $hashOf[$f.FullName]
  $dupeRole = ''
  if ($hash -and $hashCount[$hash] -gt 1) {
    if ($seen.ContainsKey($hash)) { $dupeRole = 'DUPLICATE-COPY' } else { $seen[$hash] = $f.Name; $dupeRole = 'KEEPER' }
  }

  $vk = $vkey[$f.FullName]
  $inFamily = $vNewest.ContainsKey($vk)
  $isNewest = $inFamily -and ($vNewest[$vk] -eq $f.FullName)

  $category =
    if ($isInstaller)    { 'Installer' }
    elseif ($isSensitive){ 'Sensitive record' }
    elseif ($isLegal)    { 'Legal / entity' }
    elseif ($isReceipt)  { 'Receipt' }
    elseif ($isArchiveF) { 'Archive bundle' }
    else                 { 'Document' }

  # HOLD outranks everything. Sensitive is never auto-anything.
  $verdict=''; $why=''
  if ($isSensitive) {
    $verdict='HOLD'; $why='sensitive record, route by hand, never automated'
  }
  elseif ($isInstaller) {
    $verdict='CUT'; $why='installer, re-downloadable'
  }
  elseif ($dupeRole -eq 'DUPLICATE-COPY') {
    $verdict='CUT'; $why="exact duplicate of $($seen[$hash])"
  }
  elseif ($inFamily -and -not $isNewest) {
    $verdict='CUT'; $why='older version, newest kept'
  }
  elseif ($isLegal) {
    $verdict='FILE'; $why='entity document, belongs in the Hub'
  }
  elseif ($f.LastWriteTime -lt $cutoff -and $isReceipt) {
    $verdict='ARCHIVE'; $why='aged receipt, keep for records not for the desktop'
  }
  elseif ($f.Length -lt 5KB) {
    $verdict='CUT'; $why='tiny / likely broken or empty'
  }
  elseif ($isReceipt) {
    $verdict='FILE'; $why='current receipt'
  }
  else {
    $verdict='REVIEW'; $why='needs a human call'
  }

  $rows.Add([pscustomobject]@{
    'Asset Name'       = $f.Name
    'Type'             = if ($ext -eq '.pdf') {'PDF'} elseif ($ext -in @('.xlsx','.xls','.csv')) {'Sheet'} else {'Doc'}
    'Lane'             = (Get-Entity $f.FullName)
    'Category / Use'   = $category
    'Lives On'         = 'Local'
    'Folder / Location'= $f.DirectoryName
    'Direct Link'      = ''
    'Status'           = if ($verdict -eq 'HOLD') {'Hold'} elseif ($verdict -eq 'ARCHIVE') {'Archive'} else {'Review'}
    'Needs Filing?'    = if ($verdict -in @('FILE','ARCHIVE')) {'YES'} else {'No'}
    'Verdict'          = $verdict
    'Why'              = $why
    'Sensitive'        = if ($isSensitive) {'HOLD'} else {''}
    'VersionFamily'    = if ($inFamily) { (Get-VersionKey $f.BaseName) } else { '' }
    'Modified'         = $f.LastWriteTime.ToString('yyyy-MM-dd')
    'SizeKB'           = [math]::Round($f.Length/1KB,0)
    'FullPath'         = $f.FullName
    'SHA256'           = $hash
  })
}
Write-Progress -Activity "Classifying" -Completed

# --- two reports. one stays home, one is safe to send. ---
$localCsv = Join-Path $Out 'doc-triage-LOCAL-ONLY.csv'
$rows | Export-Csv -LiteralPath $localCsv -NoTypeInformation -Encoding UTF8

$shareable = $rows | Where-Object { $_.Verdict -ne 'HOLD' } | ForEach-Object {
  [pscustomobject]@{
    'Asset Name'     = (Protect-Text $_.'Asset Name')
    'Type'           = $_.Type
    'Lane'           = $_.Lane
    'Category / Use' = $_.'Category / Use'
    'Status'         = $_.Status
    'Needs Filing?'  = $_.'Needs Filing?'
    'Verdict'        = $_.Verdict
    'Why'            = $_.Why
    'VersionFamily'  = (Protect-Text $_.VersionFamily)
    'Modified'       = $_.Modified
    'SizeKB'         = $_.SizeKB
  }
}
$shareCsv = Join-Path $Out 'doc-triage-SHAREABLE.csv'
$shareable | Export-Csv -LiteralPath $shareCsv -NoTypeInformation -Encoding UTF8

$hold=@($rows|Where-Object{$_.Verdict -eq 'HOLD'}); $cut=@($rows|Where-Object{$_.Verdict -eq 'CUT'})
$file=@($rows|Where-Object{$_.Verdict -eq 'FILE'}); $arch=@($rows|Where-Object{$_.Verdict -eq 'ARCHIVE'})
$rev=@($rows|Where-Object{$_.Verdict -eq 'REVIEW'})
$freeMB=[math]::Round((($cut|Measure-Object SizeKB -Sum).Sum)/1024,1)
$byLane = ($rows | Group-Object Lane | Sort-Object Count -Descending | ForEach-Object { "  $($_.Name.PadRight(10)) $($_.Count)" }) -join "`n"

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
GENTLE MUSE - DOCUMENT TRIAGE, RUN 5
Scanned : $Root
When    : $(Get-Date -Format 'yyyy-MM-dd HH:mm')
Mode    : $(if($Execute){'EXECUTE'}else{'PROPOSE-ONLY'})

Total documents ...... $total
HOLD, sensitive ...... $($hold.Count)   route by hand, never automated
FILE, to the Hub ..... $($file.Count)
ARCHIVE .............. $($arch.Count)
REVIEW ............... $($rev.Count)
CUT .................. $($cut.Count)   ($freeMB MB)
$(if($Execute){"Moved to _QUARANTINE  $moved  (nothing deleted)"}else{"Nothing moved. Re-run with -Execute to quarantine the CUT list."})

BY ENTITY
$byLane

REPORTS
  doc-triage-LOCAL-ONLY.csv   full names and paths. Never send this file.
  doc-triage-SHAREABLE.csv    HOLD rows removed, digits masked. Safe to send.

NEXT -> send only doc-triage-SHAREABLE.csv to Claude.
The HOLD pile stays on this machine. Amanda routes those by hand.
"@
$summary | Set-Content -LiteralPath (Join-Path $Out 'SUMMARY.txt') -Encoding UTF8
Write-Host ""; Write-Host $summary -ForegroundColor White
Write-Host "  Done." -ForegroundColor Green; Write-Host ""
