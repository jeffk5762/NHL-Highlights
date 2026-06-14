param(
    [switch]$SkipImportCheck
)

$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$venvPath = Join-Path $PSScriptRoot '.venv'
$pythonExe = Join-Path $venvPath 'Scripts\python.exe'
$requirementsPath = Join-Path $PSScriptRoot 'requirements.txt'

Write-Host '=== NHL Cues setup ===' -ForegroundColor Cyan
Write-Host "Project: $PSScriptRoot"

if (-not (Test-Path $requirementsPath)) {
    Write-Host 'requirements.txt not found in project root.' -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $pythonExe)) {
    Write-Host 'Creating virtual environment (.venv)...' -ForegroundColor Yellow
    try {
        py -m venv .venv
    }
    catch {
        Write-Host 'Could not run "py -m venv .venv". Make sure Python is installed and the py launcher is available.' -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host 'Virtual environment already exists. Reusing .venv' -ForegroundColor Green
}

if (-not (Test-Path $pythonExe)) {
    Write-Host 'Virtual environment creation failed: .venv\Scripts\python.exe not found.' -ForegroundColor Red
    exit 1
}

Write-Host 'Upgrading pip...' -ForegroundColor Yellow
& $pythonExe -m pip install --upgrade pip

Write-Host 'Installing requirements...' -ForegroundColor Yellow
& $pythonExe -m pip install -r $requirementsPath

if (-not $SkipImportCheck) {
    Write-Host 'Verifying imports...' -ForegroundColor Yellow
    & $pythonExe -c "import requests, pyautogui, pygetwindow; print('imports ok')"
}

Write-Host ''
Write-Host 'Setup complete.' -ForegroundColor Green
Write-Host 'Next steps:'
Write-Host '1) In VS Code: Python: Select Interpreter -> .venv\Scripts\python.exe'
Write-Host '2) Run: powershell -ExecutionPolicy Bypass -File .\Run-NHL-Cues.ps1'
