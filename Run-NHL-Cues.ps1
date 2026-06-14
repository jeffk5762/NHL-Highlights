param(
    [string]$GameId,
    [switch]$FromStart,
    [switch]$SendHotkey,
    [double]$Poll = 2,
    [double]$MarkerDelay = 0.0
)

$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$pythonExe = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$scriptPath = Join-Path $PSScriptRoot 'nhl_live_reaper_cues_Version11.py'

if (-not (Test-Path $pythonExe)) {
    Write-Host 'Virtual environment not found at .venv\Scripts\python.exe' -ForegroundColor Yellow
    Write-Host 'Run these commands once:'
    Write-Host '  py -m venv .venv'
    Write-Host '  .\.venv\Scripts\Activate.ps1'
    Write-Host '  python -m pip install -r requirements.txt'
    exit 1
}

if (-not (Test-Path $scriptPath)) {
    Write-Host 'Could not find nhl_live_reaper_cues_Version11.py in this folder.' -ForegroundColor Red
    exit 1
}

if (-not $GameId) {
    $GameId = Read-Host 'Enter NHL game ID (example: 2024020001)'
}

if (-not $GameId) {
    Write-Host 'Game ID is required.' -ForegroundColor Red
    exit 1
}

if (-not $PSBoundParameters.ContainsKey('FromStart')) {
    $fromStartAnswer = Read-Host 'Process full history once and exit? (y/n, default y)'
    if ([string]::IsNullOrWhiteSpace($fromStartAnswer) -or $fromStartAnswer.Trim().ToLower() -eq 'y') {
        $FromStart = $true
    }
}

if (-not $PSBoundParameters.ContainsKey('SendHotkey')) {
    $hotkeyAnswer = Read-Host "Send marker hotkey to Reaper? (y/n, default n)"
    if ($hotkeyAnswer.Trim().ToLower() -eq 'y') {
        $SendHotkey = $true
    }
}

$argsList = @($scriptPath, $GameId, '--poll', $Poll.ToString(), '--marker-delay', $MarkerDelay.ToString())
if ($FromStart) {
    $argsList += '--from-start'
}
if ($SendHotkey) {
    $argsList += '--send-hotkey'
}

Write-Host ''
Write-Host 'Running command:' -ForegroundColor Cyan
Write-Host "& \"$pythonExe\" $($argsList -join ' ')"
Write-Host ''

& $pythonExe @argsList
$exitCode = $LASTEXITCODE

$csvPath = Join-Path $PSScriptRoot ("nhl_cues_{0}.csv" -f $GameId)

Write-Host ''
Write-Host "Process finished with exit code: $exitCode"
Write-Host "Expected CSV: $csvPath"
if (Test-Path $csvPath) {
    $csvInfo = Get-Item $csvPath
    Write-Host ("CSV found. Last write: {0}" -f $csvInfo.LastWriteTime)
}
else {
    Write-Host 'CSV not found yet. If running live mode, file may appear after save events are detected.' -ForegroundColor Yellow
}
if ($Host.Name -like '*ConsoleHost*') {
    Read-Host 'Press Enter to close'
}

exit $exitCode
