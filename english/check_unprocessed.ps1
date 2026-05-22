# check_unprocessed.ps1
# Scans all subfolders under english\ for PNG files that need (re)processing.
# A file needs processing if:
#   (a) no corresponding .md exists, OR
#   (b) the .png was modified more recently than its .md

param(
    [string]$Root = "$PSScriptRoot"
)

$needs = @()

Get-ChildItem -Path $Root -Recurse -Filter "*.png" | ForEach-Object {
    $png = $_
    $mdPath = Join-Path $png.DirectoryName ($png.BaseName + ".md")

    # Split-page scans (e.g. 164a.png + 164b.png) share a merged MD (164.md).
    # If exact-name MD missing and basename ends with a single letter, fall back to the base MD.
    if (-not (Test-Path $mdPath) -and $png.BaseName -match '^(.+\.\d+)([a-z])$') {
        $mergedMdPath = Join-Path $png.DirectoryName ($matches[1] + ".md")
        if (Test-Path $mergedMdPath) {
            $mdPath = $mergedMdPath
        }
    }

    if (-not (Test-Path $mdPath)) {
        $needs += [PSCustomObject]@{
            Status = "NEW"
            File   = $png.FullName
            Reason = "no MD found"
        }
    } elseif ($png.LastWriteTime -gt (Get-Item $mdPath).LastWriteTime) {
        $needs += [PSCustomObject]@{
            Status = "UPDATED"
            File   = $png.FullName
            Reason = "PNG modified $($png.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss')), MD last updated $((Get-Item $mdPath).LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))"
        }
    }
}

if ($needs.Count -eq 0) {
    Write-Host "All PNG files are up to date." -ForegroundColor Green
} else {
    Write-Host "$($needs.Count) file(s) need processing:" -ForegroundColor Yellow
    $needs | ForEach-Object {
        Write-Host "  [$($_.Status)] $($_.File)" -ForegroundColor Cyan
        Write-Host "         $($_.Reason)" -ForegroundColor Gray
    }
}
