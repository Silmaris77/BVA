# BVA Application Cleanup Script
# Date: October 27, 2025

$ErrorActionPreference = "Stop"

function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Green "=================================================="
Write-ColorOutput Green "  BVA Application Cleanup Script"
Write-ColorOutput Green "  Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-ColorOutput Green "=================================================="
Write-Output ""

# Preparation
Write-ColorOutput Cyan "STEP 1: Preparation..."

$rootPath = Get-Location
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$cleanupLogFile = "cleanup_log_$timestamp.txt"
$deletedFilesBackup = "cleanup_backup_$timestamp"

# Create backup folder
if (-not (Test-Path $deletedFilesBackup)) {
    New-Item -ItemType Directory -Path $deletedFilesBackup | Out-Null
    Write-ColorOutput Green "Created backup folder: $deletedFilesBackup"
}

# Start log
"BVA Cleanup Log - $timestamp" | Out-File $cleanupLogFile
"=" * 60 | Out-File $cleanupLogFile -Append
"" | Out-File $cleanupLogFile -Append

Write-Output ""

# Safety backup
Write-ColorOutput Cyan "STEP 2: Creating safety backup..."

$criticalFiles = @(
    "users_data.json",
    "main.py",
    "requirements.txt"
)

foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Copy-Item $file "$deletedFilesBackup\$file.backup" -Force
        Write-ColorOutput Green "Backed up: $file"
    }
}

Write-Output ""

# Clean old JSON backups
Write-ColorOutput Cyan "STEP 3: Cleaning old JSON backups..."

$jsonBackups = Get-ChildItem -Path . -Filter "users_data_backup_*.json" | 
               Sort-Object LastWriteTime -Descending

if ($jsonBackups.Count -gt 1) {
    $newestBackup = $jsonBackups[0]
    Write-ColorOutput Yellow "Keeping newest backup: $($newestBackup.Name)"
    "KEPT: $($newestBackup.Name)" | Out-File $cleanupLogFile -Append
    
    $oldBackups = $jsonBackups | Select-Object -Skip 1
    
    foreach ($backup in $oldBackups) {
        try {
            Move-Item $backup.FullName "$deletedFilesBackup\$($backup.Name)" -Force
            Write-ColorOutput Green "Moved: $($backup.Name)"
            "REMOVED: $($backup.Name) (size: $([math]::Round($backup.Length / 1MB, 2)) MB)" | Out-File $cleanupLogFile -Append
        }
        catch {
            Write-ColorOutput Red "Error: $($backup.Name) - $_"
            "ERROR: $($backup.Name) - $_" | Out-File $cleanupLogFile -Append
        }
    }
}
else {
    Write-ColorOutput Yellow "Only 1 JSON backup found - skipping"
}

Write-Output ""

# Clean .bak files
Write-ColorOutput Cyan "STEP 4: Cleaning .bak files..."

$bakPath = "temp\import_backups"
if (Test-Path $bakPath) {
    $bakFiles = Get-ChildItem -Path $bakPath -Filter "*.bak"
    
    foreach ($bak in $bakFiles) {
        try {
            Move-Item $bak.FullName "$deletedFilesBackup\$($bak.Name)" -Force
            Write-ColorOutput Green "Moved: $($bak.Name)"
            "REMOVED: $($bak.Name)" | Out-File $cleanupLogFile -Append
        }
        catch {
            Write-ColorOutput Red "Error: $($bak.Name) - $_"
        }
    }
}
else {
    Write-ColorOutput Yellow "Folder temp/import_backups not found - skipping"
}

Write-Output ""

# Clean temp files
Write-ColorOutput Cyan "STEP 5: Cleaning temporary files..."

$tempFiles = @(
    "temp\npc_audio_*.mp3",
    "temp\Kolb_Raport_*.html",
    "temp\business_games_layout_prototype.html",
    "temp\dzwieki_timer.html"
)

foreach ($pattern in $tempFiles) {
    $files = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue
    
    foreach ($file in $files) {
        try {
            Move-Item $file.FullName "$deletedFilesBackup\$($file.Name)" -Force
            Write-ColorOutput Green "Moved: $($file.Name)"
            "REMOVED: $($file.Name)" | Out-File $cleanupLogFile -Append
        }
        catch {
            Write-ColorOutput Red "Error: $($file.Name) - $_"
        }
    }
}

Write-Output ""

# Clean debug logs
Write-ColorOutput Cyan "STEP 6: Cleaning debug logs..."

$logFiles = Get-ChildItem -Path . -Filter "*.log"

foreach ($log in $logFiles) {
    if ($log.Name -ne $cleanupLogFile) {
        try {
            Move-Item $log.FullName "$deletedFilesBackup\$($log.Name)" -Force
            Write-ColorOutput Green "Moved: $($log.Name)"
            "REMOVED: $($log.Name)" | Out-File $cleanupLogFile -Append
        }
        catch {
            Write-ColorOutput Red "Error: $($log.Name) - $_"
        }
    }
}

Write-Output ""

# Clean config backup
Write-ColorOutput Cyan "STEP 7: Cleaning config backup..."

if (Test-Path "config\settings.py.bak") {
    try {
        Move-Item "config\settings.py.bak" "$deletedFilesBackup\settings.py.bak" -Force
        Write-ColorOutput Green "Moved: config\settings.py.bak"
        "REMOVED: config\settings.py.bak" | Out-File $cleanupLogFile -Append
    }
    catch {
        Write-ColorOutput Red "Error: config\settings.py.bak - $_"
    }
}

Write-Output ""

# Clean old fix_* scripts
Write-ColorOutput Cyan "STEP 8: Cleaning old fix_* scripts..."
Write-ColorOutput Yellow "Keeping: fix_json_error.py, fix_json_newline.py, fix_json_precise.py (recent)"

$fixScriptsToDelete = @(
    "fix_comm_analyzer_emoji.py",
    "fix_emoji.py",
    "fix_encoding.py",
    "fix_html.py",
    "fix_lesson_emoji.py",
    "fix_lesson_remaining.py",
    "fix_plotly_chart.py",
    "fix_remaining.py",
    "fix_sections_emoji.py",
    "fix_simulator.py",
    "fix_tabs_order.py",
    "fix_tools_all_emoji.py",
    "fix_tools_emoji_part2.py",
    "fix_use_container_width.py",
    "fix_users_json.py"
)

foreach ($script in $fixScriptsToDelete) {
    if (Test-Path $script) {
        try {
            Move-Item $script "$deletedFilesBackup\$script" -Force
            Write-ColorOutput Green "Moved: $script"
            "REMOVED: $script" | Out-File $cleanupLogFile -Append
        }
        catch {
            Write-ColorOutput Red "Error: $script - $_"
        }
    }
}

Write-Output ""

# Clean PowerShell scripts
Write-ColorOutput Cyan "STEP 9: Cleaning PowerShell scripts..."

$psScripts = @(
    "fix_kolb_visualization.ps1",
    "replace_kolb_cards.ps1"
)

foreach ($ps in $psScripts) {
    if (Test-Path $ps) {
        try {
            Move-Item $ps "$deletedFilesBackup\$ps" -Force
            Write-ColorOutput Green "Moved: $ps"
            "REMOVED: $ps" | Out-File $cleanupLogFile -Append
        }
        catch {
            Write-ColorOutput Red "Error: $ps - $_"
        }
    }
}

Write-Output ""

# Clean HTML prototypes
Write-ColorOutput Cyan "STEP 10: Cleaning HTML prototypes..."

$htmlFiles = @(
    "Kolb_Raport_admin_20251016_103417.html",
    "test_html_report.html",
    "test_plotly_offline.html",
    "visualization_samples.html"
)

foreach ($html in $htmlFiles) {
    if (Test-Path $html) {
        try {
            Move-Item $html "$deletedFilesBackup\$html" -Force
            Write-ColorOutput Green "Moved: $html"
            "REMOVED: $html" | Out-File $cleanupLogFile -Append
        }
        catch {
            Write-ColorOutput Red "Error: $html - $_"
        }
    }
}

Write-Output ""

# Generate final report
Write-ColorOutput Cyan "STEP 11: Generating final report..."

$backupSize = (Get-ChildItem -Path $deletedFilesBackup -Recurse | 
               Measure-Object -Property Length -Sum).Sum / 1MB

"" | Out-File $cleanupLogFile -Append
"=" * 60 | Out-File $cleanupLogFile -Append
"CLEANUP SUMMARY" | Out-File $cleanupLogFile -Append
"=" * 60 | Out-File $cleanupLogFile -Append
"Completed: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File $cleanupLogFile -Append
"Files moved: $((Get-ChildItem $deletedFilesBackup).Count)" | Out-File $cleanupLogFile -Append
"Total size: $([math]::Round($backupSize, 2)) MB" | Out-File $cleanupLogFile -Append
"Backup location: $deletedFilesBackup" | Out-File $cleanupLogFile -Append
"" | Out-File $cleanupLogFile -Append
"NOTE: All files were MOVED to backup, not deleted!" | Out-File $cleanupLogFile -Append
"If everything works OK, you can delete folder: $deletedFilesBackup" | Out-File $cleanupLogFile -Append

Write-Output ""
Write-ColorOutput Green "=================================================="
Write-ColorOutput Green "  CLEANUP COMPLETED SUCCESSFULLY!"
Write-ColorOutput Green "=================================================="
Write-Output ""
Write-ColorOutput Yellow "STATISTICS:"
Write-Output "   - Files moved: $((Get-ChildItem $deletedFilesBackup).Count)"
Write-Output "   - Total size: $([math]::Round($backupSize, 2)) MB"
Write-Output "   - Backup location: $deletedFilesBackup"
Write-Output ""
Write-ColorOutput Cyan "Log saved to: $cleanupLogFile"
Write-Output ""
Write-ColorOutput Yellow "IMPORTANT:"
Write-Output "   1. Test the app: streamlit run main.py"
Write-Output "   2. If everything OK, delete folder: $deletedFilesBackup"
Write-Output "   3. If something broken, restore files from: $deletedFilesBackup"
Write-Output ""

$openBackup = Read-Host "Open backup folder? (y/n)"
if ($openBackup -eq "y" -or $openBackup -eq "Y") {
    Invoke-Item $deletedFilesBackup
}

Write-ColorOutput Green "Script completed"
