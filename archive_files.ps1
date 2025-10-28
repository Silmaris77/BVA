# BVA Application Archive Script
# Date: October 27, 2025
# Purpose: Archive test files and documentation

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
Write-ColorOutput Green "  BVA Archive Script - Tests & Documentation"
Write-ColorOutput Green "  Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-ColorOutput Green "=================================================="
Write-Output ""

# Preparation
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$archiveLog = "archive_log_$timestamp.txt"

# Create archive folders
$testsArchive = "tests\archive"
$docsArchive = "docs\archive"

if (-not (Test-Path $testsArchive)) {
    New-Item -ItemType Directory -Path $testsArchive -Force | Out-Null
    Write-ColorOutput Green "Created: $testsArchive"
}

if (-not (Test-Path $docsArchive)) {
    New-Item -ItemType Directory -Path $docsArchive -Force | Out-Null
    Write-ColorOutput Green "Created: $docsArchive"
}

"BVA Archive Log - $timestamp" | Out-File $archiveLog
"=" * 60 | Out-File $archiveLog -Append
"" | Out-File $archiveLog -Append

Write-Output ""

# ======================================================================
# STEP 1: Archive test files
# ======================================================================

Write-ColorOutput Cyan "STEP 1: Archiving test files..."

$testFiles = @(
    "test_ai_conversation_flow.py",
    "test_ai_evaluation.py",
    "test_anti_cheat.py",
    "test_backward_compatibility.py",
    "test_business_games.py",
    "test_dev_mode.py",
    "test_elevenlabs.py",
    "test_engagement_v2.py",
    "test_evaluation_mode.py",
    "test_evaluation_system.py",
    "test_gemini_api_key.py",
    "test_lesson_coins.py",
    "test_mi_implementation.py",
    "test_mi_profiles.py",
    "test_new_charts.py",
    "test_radar_chart.py",
    "test_simulator_import.py",
    "test_split.py",
    "test_weasyprint.py",
    "test_who_am_i_report.py",
    "test_xhtml2pdf.py"
)

$movedTests = 0
foreach ($test in $testFiles) {
    if (Test-Path $test) {
        try {
            Move-Item $test "$testsArchive\$test" -Force
            Write-ColorOutput Green "Archived: $test"
            "ARCHIVED: $test" | Out-File $archiveLog -Append
            $movedTests++
        }
        catch {
            Write-ColorOutput Red "Error: $test - $_"
            "ERROR: $test - $_" | Out-File $archiveLog -Append
        }
    }
}

Write-ColorOutput Yellow "Moved $movedTests test files"
Write-Output ""

# ======================================================================
# STEP 2: Archive old documentation MD files
# ======================================================================

Write-ColorOutput Cyan "STEP 2: Archiving old documentation..."

# Files to KEEP in root (important/current)
$keepInRoot = @(
    "README.md",
    "CHANGELOG_2025_10_27.md",
    "CLEANUP_ANALYSIS.md",
    "BETA_READY_SUMMARY.md",
    "BETA_TESTING_CHECKLIST.md",
    "BETA_TESTER_GUIDE.md"
)

Write-ColorOutput Yellow "Keeping in root:"
foreach ($keep in $keepInRoot) {
    Write-Output "  - $keep"
}
Write-Output ""

# Old documentation to archive
$docsToArchive = @(
    "AI_CONVERSATION_CLEANUP.md",
    "AI_CONVERSATION_READY.md",
    "AI_CONVERSATION_USER_FIX.md",
    "AUDIO_DUPLICATION_FIX.md",
    "AUDIO_DYNAMIC_RERENDER_FIX.md",
    "AUDIO_INPUT_UPGRADE.md",
    "BUSINESS_GAMES_COACHING_SPLIT.md",
    "BUSINESS_GAMES_GUIDE.md",
    "ELEVENLABS_QUICKSTART.md",
    "ELEVENLABS_SETUP.md",
    "FMCG_IMPLEMENTATION_STATUS.md",
    "GEMINI_COST_ANALYSIS.md",
    "GOOGLE_FORMS_TEMPLATE.md",
    "MATERIALY_PROMOCYJNE.md",
    "MECHANIKA_VS_CONTENT_DECISION.md",
    "MIND_MAP_CONTROLS.md",
    "MVP_MONETIZATION_STRATEGY.md",
    "NEXT_STEPS.md",
    "PERFORMANCE_REPORT.md",
    "PRICING_STRATEGY.md",
    "PRIORYTET_1_PROGRESS_REPORT.md",
    "REFACTORING_PLAN.md",
    "REFACTORING_STATUS.md",
    "SALES_PITCH_DECK.md",
    "SALES_SCRIPT.md",
    "SALES_SCRIPT_B2B_FOCUS.md",
    "SECRETS_SETUP.md",
    "URGENT_KEY_ROTATION.md"
)

$movedDocs = 0
foreach ($doc in $docsToArchive) {
    if (Test-Path $doc) {
        try {
            Move-Item $doc "$docsArchive\$doc" -Force
            Write-ColorOutput Green "Archived: $doc"
            "ARCHIVED: $doc" | Out-File $archiveLog -Append
            $movedDocs++
        }
        catch {
            Write-ColorOutput Red "Error: $doc - $_"
            "ERROR: $doc - $_" | Out-File $archiveLog -Append
        }
    }
}

Write-ColorOutput Yellow "Moved $movedDocs documentation files"
Write-Output ""

# ======================================================================
# STEP 3: Archive helper scripts
# ======================================================================

Write-ColorOutput Cyan "STEP 3: Archiving helper scripts..."

$scriptsArchive = "scripts\archive"
if (-not (Test-Path $scriptsArchive)) {
    New-Item -ItemType Directory -Path $scriptsArchive -Force | Out-Null
}

$helperScripts = @(
    "check_contracts.py",
    "debug_ai_contracts.py",
    "delete_mick.py",
    "find_fstrings.py",
    "find_singles.py",
    "list_gemini_models.py",
    "migrate_contract_types.py",
    "set_ai_mode.py",
    "temp_fix_tabs.py"
)

$movedScripts = 0
foreach ($script in $helperScripts) {
    if (Test-Path $script) {
        try {
            Move-Item $script "$scriptsArchive\$script" -Force
            Write-ColorOutput Green "Archived: $script"
            "ARCHIVED: $script" | Out-File $archiveLog -Append
            $movedScripts++
        }
        catch {
            Write-ColorOutput Red "Error: $script - $_"
        }
    }
}

Write-ColorOutput Yellow "Moved $movedScripts helper scripts"
Write-Output ""

# ======================================================================
# STEP 4: Archive recent cleanup/fix scripts
# ======================================================================

Write-ColorOutput Cyan "STEP 4: Archiving recent cleanup scripts..."

$cleanupScripts = @(
    "fix_json_error.py",
    "fix_json_newline.py",
    "fix_json_precise.py",
    "cleanup_app.ps1"
)

foreach ($script in $cleanupScripts) {
    if (Test-Path $script) {
        $choice = Read-Host "Archive $script? (y/n)"
        if ($choice -eq "y" -or $choice -eq "Y") {
            try {
                Move-Item $script "$scriptsArchive\$script" -Force
                Write-ColorOutput Green "Archived: $script"
                "ARCHIVED: $script" | Out-File $archiveLog -Append
                $movedScripts++
            }
            catch {
                Write-ColorOutput Red "Error: $script - $_"
            }
        }
    }
}

Write-Output ""

# ======================================================================
# Final Report
# ======================================================================

Write-ColorOutput Cyan "Generating final report..."

$totalMoved = $movedTests + $movedDocs + $movedScripts

"" | Out-File $archiveLog -Append
"=" * 60 | Out-File $archiveLog -Append
"ARCHIVE SUMMARY" | Out-File $archiveLog -Append
"=" * 60 | Out-File $archiveLog -Append
"Completed: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File $archiveLog -Append
"Test files archived: $movedTests" | Out-File $archiveLog -Append
"Documentation archived: $movedDocs" | Out-File $archiveLog -Append
"Scripts archived: $movedScripts" | Out-File $archiveLog -Append
"Total files: $totalMoved" | Out-File $archiveLog -Append
"" | Out-File $archiveLog -Append
"Archive locations:" | Out-File $archiveLog -Append
"  - Tests: $testsArchive" | Out-File $archiveLog -Append
"  - Docs: $docsArchive" | Out-File $archiveLog -Append
"  - Scripts: $scriptsArchive" | Out-File $archiveLog -Append

Write-Output ""
Write-ColorOutput Green "=================================================="
Write-ColorOutput Green "  ARCHIVING COMPLETED!"
Write-ColorOutput Green "=================================================="
Write-Output ""
Write-ColorOutput Yellow "STATISTICS:"
Write-Output "   - Test files: $movedTests -> $testsArchive"
Write-Output "   - Documentation: $movedDocs -> $docsArchive"
Write-Output "   - Scripts: $movedScripts -> $scriptsArchive"
Write-Output "   - Total: $totalMoved files archived"
Write-Output ""
Write-ColorOutput Cyan "Log saved to: $archiveLog"
Write-Output ""
Write-ColorOutput Yellow "ROOT FOLDER NOW CONTAINS:"
Write-Output "   - README.md (main documentation)"
Write-Output "   - CHANGELOG_2025_10_27.md (recent changes)"
Write-Output "   - CLEANUP_ANALYSIS.md (cleanup report)"
Write-Output "   - Beta testing docs (3 files)"
Write-Output "   - Application files (main.py, requirements.txt, etc.)"
Write-Output ""
Write-ColorOutput Green "Your workspace is now clean and organized!"
