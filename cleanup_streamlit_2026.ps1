# BVA Streamlit Cleanup Script - January 2026
# Moves old one-off scripts, docs, and mockups to archive folder

$archiveDir = "archive_2026_01_30"
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"

Write-Host "=== BVA Streamlit Cleanup ===" -ForegroundColor Cyan
Write-Host "Archive folder: $archiveDir"

# Create archive subdirectories
$subdirs = @(
    "$archiveDir/scripts_oneoff",
    "$archiveDir/docs_old", 
    "$archiveDir/html_mockups",
    "$archiveDir/tests_old",
    "$archiveDir/temp_backup"
)

foreach ($dir in $subdirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# === 1. ONE-OFF PYTHON SCRIPTS ===
Write-Host "`n[1/5] Moving one-off Python scripts..." -ForegroundColor Yellow

$oneOffPatterns = @(
    "add_*.py",
    "migrate_*.py",
    "test_*.py",
    "verify_*.py",
    "fix_*.py",
    "cleanup_*.py",
    "create_*.py",
    "delete_*.py",
    "drop_*.py",
    "extract_*.py",
    "find_*.py",
    "move_*.py",
    "remove_*.py",
    "rename_*.py",
    "update_*.py",
    "convert_*.py",
    "analyze_*.py",
    "diagnose_*.py",
    "indent_*.py",
    "refactor_*.py",
    "reorganize_*.py",
    "seed_*.py",
    "show_*.py",
    "apply_*.py",
    "compare_*.py",
    "complete_*.py",
    "count_*.py",
    "depth_*.py",
    "detailed_*.py",
    "hr_*.py",
    "clear_*.py"
)

$movedScripts = 0
foreach ($pattern in $oneOffPatterns) {
    $files = Get-ChildItem -Path "." -Name $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        if (Test-Path $file) {
            Move-Item $file "$archiveDir/scripts_oneoff/" -Force
            $movedScripts++
        }
    }
}
Write-Host "  Moved $movedScripts scripts"

# === 2. OLD DOCUMENTATION ===
Write-Host "`n[2/5] Moving old markdown docs..." -ForegroundColor Yellow

$oldDocs = @(
    "ACTION_PLAN_*.md",
    "ALEX_*.md",
    "ALTERNATYWNE_*.md",
    "ANALIZA_*.md",
    "AUDIO_*.md",
    "BETA_*.md",
    "CHANGELOG_*.md",
    "CLEANUP_*.md",
    "CONSULTING_*.md",
    "DELAYED_*.md",
    "FMCG_*.md",
    "HEINZ_*.md",
    "JSS_*.md",
    "LAYOUT_*.md",
    "LEKCJE_*.md",
    "MATEMATYKA_*.md",
    "MIGRATION_*.md",
    "MILWAUKEE_*.md",
    "PLATFORM_*.md",
    "REFACTORING_*.md",
    "RESOURCE_*.md",
    "SCENARIUSZ_*.md",
    "SYSTEM_*.md",
    "TASKS_*.md",
    "TEST_GUIDE_*.md"
)

$movedDocs = 0
foreach ($pattern in $oldDocs) {
    $files = Get-ChildItem -Path "." -Name $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        if (Test-Path $file) {
            Move-Item $file "$archiveDir/docs_old/" -Force
            $movedDocs++
        }
    }
}
Write-Host "  Moved $movedDocs markdown files"

# === 3. HTML MOCKUPS ===
Write-Host "`n[3/5] Moving HTML mockups..." -ForegroundColor Yellow

$htmlFiles = Get-ChildItem -Path "." -Name "*.html" -ErrorAction SilentlyContinue
$movedHtml = 0
foreach ($file in $htmlFiles) {
    # Keep index.html if it's important
    if ($file -ne "index.html") {
        Move-Item $file "$archiveDir/html_mockups/" -Force
        $movedHtml++
    }
}
Write-Host "  Moved $movedHtml HTML files"

# === 4. TEMP AND BACKUP FILES ===
Write-Host "`n[4/5] Moving temp/backup files..." -ForegroundColor Yellow

$tempFiles = @(
    "*.log",
    "*_backup_*.json",
    "*_backup_*.txt",
    "archive_log_*.txt",
    "cleanup_log_*.txt",
    "temp_*.json",
    "jss_rules_content.txt",
    "spis_*.txt",
    "milwaukee_section_updates.txt"
)

$movedTemp = 0
foreach ($pattern in $tempFiles) {
    $files = Get-ChildItem -Path "." -Name $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        if (Test-Path $file) {
            Move-Item $file "$archiveDir/temp_backup/" -Force
            $movedTemp++
        }
    }
}

# Move backup folders
if (Test-Path "cleanup_backup_20251027_233428") {
    Move-Item "cleanup_backup_20251027_233428" "$archiveDir/temp_backup/" -Force
    Write-Host "  Moved cleanup_backup folder"
}

if (Test-Path "temp") {
    Move-Item "temp" "$archiveDir/temp_backup/" -Force
    Write-Host "  Moved temp folder"
}

Write-Host "  Moved $movedTemp temp/backup files"

# === 5. OLD FOLDERS ===
Write-Host "`n[5/5] Moving old folders..." -ForegroundColor Yellow

# Move v3_mockups if exists
if (Test-Path "v3_mockups") {
    Move-Item "v3_mockups" "$archiveDir/" -Force
    Write-Host "  Moved v3_mockups folder"
}

# Move tests folder to archive (keep structure)
if (Test-Path "tests") {
    Move-Item "tests" "$archiveDir/tests_old/" -Force
    Write-Host "  Moved tests folder"
}

# === SUMMARY ===
Write-Host "`n=== CLEANUP COMPLETE ===" -ForegroundColor Green

$totalArchived = (Get-ChildItem -Path $archiveDir -Recurse -File).Count
Write-Host "Total files archived: $totalArchived"
Write-Host "Archive location: $archiveDir"

Write-Host "`n[!] Review the archive folder before deleting permanently." -ForegroundColor Yellow
Write-Host "[!] To undo: move files back from $archiveDir" -ForegroundColor Yellow

# Log cleanup
$logContent = @"
BVA Streamlit Cleanup Log
Date: $timestamp
Scripts archived: $movedScripts
Docs archived: $movedDocs
HTML archived: $movedHtml
Temp files archived: $movedTemp
Total: $totalArchived files
"@

$logContent | Out-File "$archiveDir/cleanup_log.txt"
Write-Host "`nLog saved to $archiveDir/cleanup_log.txt"
