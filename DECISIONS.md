# Project Decisions

This file captures important decisions so setup/debug context survives across PCs.

## Current decisions

- Use **one virtual environment per project** named `.venv`.
- Do **not** sync/copy virtual env folders between PCs (`.venv`, `.venv-1`, `.venv-2`, etc.).
- Always run installs and scripts with `.venv\Scripts\python.exe`.
- VS Code interpreter should be set to `.venv\Scripts\python.exe`.
- Preferred run path in editor: VS Code Tasks (`Run NHL Cues (interactive)` / `Run NHL Cues (prompt Game ID)`).
- Keep setup commands in `RUNBOOK.md` and use `setup.ps1` for one-command bootstrap.

## Rationale

- Avoids broken absolute paths from other machines (example: `C:\Users\Nancy\...\python.exe`).
- Keeps Pylance import resolution aligned with installed packages.
- Reduces repeated onboarding steps on new PCs.

## Change log

- 2026-05-31: Added environment and launcher standards for multi-PC workflow.
