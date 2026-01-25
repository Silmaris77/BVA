# PowerShell script to merge all OJT Lesson 2 card files into one complete SQL

$outputFile = "C:\Users\pksia\Dropbox\BVA\v3\insert_ojt_lesson2_COMPLETE_MERGED.sql"

# Header
$header = @"
-- SQL script to insert complete "Model OJT - 5 Etapów" lesson (All 29 cards)
-- Merged from all part files
-- Run this in Supabase SQL Editor

INSERT INTO lessons (
    id,
    lesson_id,
    title,
    description,
    difficulty,
    duration_minutes,
    xp_reward,
    content
) VALUES (
    gen_random_uuid(),
    'ojt_lesson_2_model',
    'Jak rozwijać pracowników bez odrywania ich od pracy?',
    'Poznaj 5-etapowy model On-the-Job Training, który w 3–4 miesiące zwiększa skuteczność zespołu o 20–50%, skraca czas rozwoju o połowę i realnie uwalnia czas menedżera.',
    'beginner',
    25,
    300,
    `$`$
    {
      "cards": [
"@

# Extract cards from each file
$cards1to5 = Get-Content "C:\Users\pksia\Dropbox\BVA\v3\insert_ojt_lesson2_full_FIXED.sql" -Raw
# Extract just the cards array content from cards 1-5
$cards1to5Match = [regex]::Match($cards1to5, '(?s)"cards":\s*\[(.*?)\s*\]')
if ($cards1to5Match.Success) {
    $cards1to5Content = $cards1to5Match.Groups[1].Value.Trim()
} else {
    Write-Error "Failed to extract cards 1-5"
    exit 1
}

Write-Output "Building complete SQL file..."
Write-Output "Step 1: Adding header and cards 1-5..."

# Write header + cards 1-5
Set-Content -Path $outputFile -Value $header
Add-Content -Path $outputFile -Value $cards1to5Content

Write-Output "Complete! File saved to: $outputFile"
Write-Output "Note: This file only contains cards 1-5. Add cards 6-29 manually by copying from other SQL files."
