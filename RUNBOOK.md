# NHL Reaper Cues - Beginner Runbook

Use this when starting on a new PC or after environment issues.

## What you are setting up (simple model)

1. **Project files** (your `.py`, `.ps1`, `.md` files)
2. **Python interpreter** (the engine)
3. **Virtual environment** (`.venv`) = project-specific package toolbox

Most errors happen when #2 and #3 do not match.

---

## 1) Open PowerShell in this project folder

Use the folder path that exists on this PC:

`C:\Users\PROD A 1\OneDrive - The Walt Disney Company\NHL Py V11 This One`

or

`C:\Users\Nancy\OneDrive - The Walt Disney Company\NHL Py V11 This One`

Quick check:

```powershell
Get-Location
```

---

## Fast setup (new PC, one command)

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

What it does:

1. Creates `.venv` if missing
2. Upgrades `pip`
3. Installs `requirements.txt`
4. Verifies core imports

---

## 2) Create `.venv` (first time on this PC)

```powershell
py -m venv .venv
```

Why: creates a local project environment for packages.

---

## 3) Install dependencies into `.venv`

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Why: installs the required modules for this project on this machine.

---

## 4) Verify required imports

```powershell
.\.venv\Scripts\python.exe -c "import requests, pyautogui, pygetwindow; print('imports ok')"
```

Expected output: `imports ok`

---

## 5) In VS Code, pick the right interpreter (important)

1. Press `Ctrl+Shift+P`
2. Run `Python: Select Interpreter`
3. Choose `.venv\Scripts\python.exe`

Why: this fixes Pylance errors like *Import could not be resolved*.

---

## 6) Run options

### A) VS Code task (recommended in editor)

`Ctrl+Shift+P` → `Tasks: Run Task` →

- `Run NHL Cues (interactive)`
- `Run NHL Cues (prompt Game ID)`

### B) PowerShell launcher with prompts

```powershell
powershell -ExecutionPolicy Bypass -File .\Run-NHL-Cues.ps1
```

### C) PowerShell launcher with explicit game ID

```powershell
powershell -ExecutionPolicy Bypass -File .\Run-NHL-Cues.ps1 -GameId 2024020001 -FromStart
```

### D) Direct Python run (advanced)

```powershell
.\.venv\Scripts\python.exe .\nhl_live_reaper_cues_Version11.py 2024020001 --send-hotkey
```

---

## Output files

Created in this folder:

- `nhl_cues_<game_id>.csv`
- `seen_<game_id>.json`
- `nhl_debug_<game_id>.json` (only with `--debug-json`)

---

## New PC checklist (copy/paste)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Then select interpreter in VS Code: `.venv\Scripts\python.exe`.

---

## Important rule for OneDrive / flash drive

- Sync/copy **code files**.
- Do **not** copy `.venv`, `.venv-1`, `.venv-2`, etc. between PCs.
- Recreate `.venv` on each PC from `requirements.txt`.

---

## Quick troubleshooting

### Error: `did not find executable at C:\Users\Nancy\...\python.exe`

Cause: old copied virtual environment path from another PC.

Fix:

1. Select `.venv\Scripts\python.exe` in VS Code.
2. Recreate `.venv` if needed using the New PC checklist above.

### Error: `Import "pyautogui" could not be resolved`

Cause: VS Code interpreter is not `.venv`.

Fix:

```powershell
.\.venv\Scripts\python.exe -m pip install pyautogui
```

Then reload VS Code window.
