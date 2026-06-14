# PC Switch Checklist

Use this every time you move between PCs.

## Before leaving current PC

1. Save all files in VS Code.
2. Wait for OneDrive sync to finish.
3. If using Git, commit/push changes.
4. Close running scripts/terminals.

## After opening on the other PC

1. Wait for OneDrive sync to finish fully.
2. Open project folder in VS Code.
3. Run bootstrap setup:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

4. Select interpreter:
   - `Ctrl+Shift+P` → `Python: Select Interpreter`
   - Choose `.venv\Scripts\python.exe`
5. Run task:
   - `Ctrl+Shift+P` → `Tasks: Run Task` → `Run NHL Cues (prompt Game ID)`

## Quick health check

```powershell
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable)"
```

Expected ending: `\.venv\Scripts\python.exe`

## If something breaks

- Open `TROUBLESHOOTING.md`
- Re-run `setup.ps1`
- Confirm interpreter is `.venv\Scripts\python.exe`
