# Troubleshooting

Quick fixes for common setup/run issues.

---

## 1) `Import "pyautogui" could not be resolved`

### Cause
VS Code is using the wrong interpreter.

### Fix

```powershell
.\.venv\Scripts\python.exe -m pip install pyautogui
```

Then in VS Code:
1. `Ctrl+Shift+P` → `Python: Select Interpreter`
2. Choose `.venv\Scripts\python.exe`
3. `Developer: Reload Window`

---

## 2) `did not find executable at C:\Users\Nancy\...\python.exe`

### Cause
A copied virtual environment from another PC points to a non-existent local path.

### Fix

1. Use `.venv\Scripts\python.exe` (not `.venv-1/.venv-2/...`).
2. Rebuild environment on this PC:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 3) Explorer launch opens separate command window

### Cause
Double-clicking `.bat` runs outside VS Code by design.

### Fix
Run through VS Code Task instead:
- `Ctrl+Shift+P` → `Tasks: Run Task` → `Run NHL Cues (interactive)`

---

## 4) Setup on a new PC

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

Then select interpreter: `.venv\Scripts\python.exe`

---

## 5) `Expected expression` with a line containing `&`

### Cause
`&` cannot stand alone in Python source.

### Fix
Delete the stray `&` line or replace with valid Python expression.
