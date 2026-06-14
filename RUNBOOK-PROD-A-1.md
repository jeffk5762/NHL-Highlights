# NHL Reaper Cues - Quick Runbook

This file keeps the exact setup and run commands so you can restart quickly on this or another PC.

## 1) Open PowerShell in this folder

`C:\Users\PROD A 1\OneDrive - The Walt Disney Company\NHL Py V11 This One`

## 2) Create and activate virtual environment (first time only)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```


## 3) Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 4) Verify imports

```powershell
.\.venv\Scripts\python.exe -c "import requests, pyautogui, pygetwindow; print('imports ok')"
```

## 5) Run the script

- Double-click launcher (recommended for File Explorer):

```powershell
.\Run-NHL-Cues.bat
```

- One-click launcher with prompts (recommended):

```powershell
powershell -ExecutionPolicy Bypass -File .\Run-NHL-Cues.ps1
```

- One-click launcher with direct game ID:

```powershell
powershell -ExecutionPolicy Bypass -File .\Run-NHL-Cues.ps1 -GameId 2024020001 -FromStart
```

- Live polling mode:

```powershell
.\.venv\Scripts\python.exe .\nhl_live_reaper_cues_Version11.py 2024020001
```

- Process full history once, then exit:

```powershell
.\.venv\Scripts\python.exe .\nhl_live_reaper_cues_Version11.py 2024020001 --from-start
```

- Send marker key to Reaper when save events occur:

```powershell
.\.venv\Scripts\python.exe .\nhl_live_reaper_cues_Version11.py 2024020001 --send-hotkey
```

## Output files

Generated in this same folder:

- `nhl_cues_<game_id>.csv`
- `seen_<game_id>.json`
- `nhl_debug_<game_id>.json` (only when `--debug-json` is used)

## Notes for another PC

1. Let OneDrive finish syncing this folder.
2. Recreate `.venv` on that PC (do not copy virtual env between machines).
3. Run install from `requirements.txt`.
4. Run script with the target game ID.
