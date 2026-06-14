# NHL Reaper Cues - Quick Runbook

This file keeps the exact setup and run commands so you can restart quickly on this or another PC.

## GitHub on another PC

1. Install Git and Python on the other PC.
2. Clone the GitHub repo.

```powershell
git clone https://github.com/jeffk5762/NHL-Highlights.git
cd NHL-Highlights
```

3. Create a new virtual environment on that PC.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies and run.

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\nhl_live_reaper_cues_Version11.py 2024020001 --from-start
```

If you want setup to open the launcher after install, use:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1 -LaunchAfterSetup
```

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

1. Let OneDrive finish syncing this folder if you are opening the same OneDrive copy.
2. If you are starting fresh, clone the GitHub repo instead of copying the folder.
3. Recreate `.venv` on that PC, do not copy the virtual env between machines.
4. Run install from `requirements.txt`.
5. Run script with the target game ID.
