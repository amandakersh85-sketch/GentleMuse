# pull-phone-footage.ps1
# Runs on Amanda's Windows machine, never in the cloud. Copies today's
# photos and videos straight off a USB-connected phone (MTP device, the
# kind with no drive letter) into a local inbox folder, skipping the
# Windows Photos import wizard entirely. If the inbox folder lives
# inside Google Drive for desktop, the files sync up on their own and
# the cloud session picks them up from Drive.
#
# Usage, from PowerShell:
#   powershell -ExecutionPolicy Bypass -File pull-phone-footage.ps1
#   powershell -ExecutionPolicy Bypass -File pull-phone-footage.ps1 -Days 3
#
# Nothing on the phone is deleted or moved. Copy only.

param(
    # How many days back to pull. 1 means since yesterday this time.
    [int]$Days = 2,
    # Where files land. Point this at a folder inside Google Drive for
    # desktop so they sync automatically.
    [string]$Dest = "$env:USERPROFILE\GentleMuse-Inbox"
)

$cutoff = (Get-Date).AddDays(-$Days)
New-Item -ItemType Directory -Force -Path $Dest | Out-Null

$shell = New-Object -ComObject Shell.Application
$thisPc = $shell.Namespace(17)  # "This PC", where MTP phones appear

$phones = @($thisPc.Items() | Where-Object { $_.IsFolder -and -not $_.Path.StartsWith('::{') -or $_.Type -match 'phone|portable' })
if (-not $phones) { $phones = @($thisPc.Items() | Where-Object { $_.IsFolder }) }

$copied = 0
function Walk($folder) {
    foreach ($item in $folder.Items()) {
        if ($item.IsFolder) {
            Walk $item.GetFolder
        } elseif ($item.Name -match '\.(jpg|jpeg|png|heic|mp4|mov)$') {
            $modRaw = $folder.GetDetailsOf($item, 3)
            $mod = $null
            if ([DateTime]::TryParse(($modRaw -replace '[^\x20-\x7E]', ''), [ref]$mod) -and $mod -lt $script:cutoff) { continue }
            $script:destFolder.CopyHere($item, 0x14)  # yes-to-all, no UI
            $script:copied++
            Write-Host ("  {0}" -f $item.Name)
        }
    }
}

$destFolder = $shell.Namespace($Dest)
foreach ($phone in $phones) {
    # Only descend into things that look like a phone: they carry DCIM.
    $root = $phone.GetFolder
    $storages = @($root.Items() | Where-Object { $_.IsFolder })
    foreach ($storage in $storages) {
        $dcim = $storage.GetFolder.Items() | Where-Object { $_.Name -eq 'DCIM' }
        if ($dcim) {
            Write-Host ("Pulling from {0} \ {1} ..." -f $phone.Name, $storage.Name)
            Walk $dcim.GetFolder
        }
    }
}

Write-Host ("Done. {0} files in {1}" -f $copied, $Dest)
Write-Host "If that folder is inside Google Drive for desktop, they are syncing now."
