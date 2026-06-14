from pathlib import Path
import runpy


# Compatibility entry point: forwards to the existing converter script.
if __name__ == "__main__":
    target = Path(__file__).with_name("make_audition_markers.py")
    if not target.exists():
        raise FileNotFoundError(f"Required script not found: {target}")
    runpy.run_path(str(target), run_name="__main__")
