import argparse
import csv
from pathlib import Path


AUDITION_HEADERS = ["Name", "Start", "Duration", "Time Format", "Type", "Description"]
AUDITION_TIME_FORMAT = "decimal"
AUDITION_MARKER_TYPE = "Cue"


def seconds_to_audition_decimal(value: str | float | int) -> str:
    try:
        total = float(value)
    except (TypeError, ValueError):
        total = 0.0

    minutes = int(total // 60)
    seconds = total - (minutes * 60)
    return f"{minutes}:{seconds:06.3f}"


def find_default_input() -> Path | None:
    explicit_default = Path("reaper_markers.csv")
    if explicit_default.exists():
        return explicit_default

    candidates = sorted(
        (
            p for p in Path(".").glob("*markers*.csv")
            if p.name.lower() != "audition_markers.csv"
        ),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if candidates:
        return candidates[0]

    cue_candidates = sorted(Path(".").glob("nhl_cues_*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    return cue_candidates[0] if cue_candidates else None


def detect_format(input_csv: Path) -> str:
    with input_csv.open(mode="r", encoding="utf-8") as infile:
        first_line = infile.readline().strip().lower()

    if "marker_name" in first_line and "game_elapsed_seconds" in first_line:
        return "nhl_cues"

    if first_line.startswith("#,") or "start" in first_line:
        return "reaper"

    if input_csv.name.lower().startswith("nhl_cues_"):
        return "nhl_cues"

    return "reaper"


def convert_reaper_to_audition(input_csv: Path, output_csv: Path) -> None:
    with input_csv.open(mode="r", encoding="utf-8") as infile:
        sample = infile.read(2048)
        infile.seek(0)

        delimiter = ","
        if "\t" in sample and sample.count("\t") >= sample.count(","):
            delimiter = "\t"

        # REAPER typically exports: #, Name, Start, End, Length, Color
        reader = csv.reader(infile, delimiter=delimiter)
        next(reader, None)

        with output_csv.open(mode="w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile, delimiter="\t")
            writer.writerow(AUDITION_HEADERS)

            for row in reader:
                if not row or row[0].startswith("#"):
                    continue

                if len(row) < 5:
                    continue

                m_name = row[1]
                m_start = row[2]
                m_length = row[4]
                writer.writerow([m_name, m_start, m_length, AUDITION_TIME_FORMAT, AUDITION_MARKER_TYPE, ""])


def convert_nhl_cues_to_audition(input_csv: Path, output_csv: Path, default_duration: float) -> None:
    with input_csv.open(mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        with output_csv.open(mode="w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile, delimiter="\t")
            writer.writerow(AUDITION_HEADERS)

            duration_str = seconds_to_audition_decimal(default_duration)

            for row in reader:
                marker_name = (row.get("marker_name") or "Marker").strip()
                start = seconds_to_audition_decimal((row.get("game_elapsed_seconds") or "0").strip())
                writer.writerow([
                    marker_name,
                    start,
                    duration_str,
                    AUDITION_TIME_FORMAT,
                    AUDITION_MARKER_TYPE,
                    "",
                ])


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert marker CSV to Adobe Audition marker CSV")
    parser.add_argument("--input", help="Input CSV (default: reaper_markers.csv, newest *markers*.csv, or newest nhl_cues_*.csv)")
    parser.add_argument("--output", default="audition_markers.csv", help="Output Audition marker CSV path")
    parser.add_argument("--duration", type=float, default=0.0, help="Default duration seconds for nhl_cues rows (default: 0)")
    args = parser.parse_args()

    input_path = Path(args.input) if args.input else find_default_input()
    if input_path is None or not input_path.exists():
        print("No input marker CSV found. Provide --input or place reaper_markers.csv / nhl_cues_*.csv in this folder.")
        return

    output_path = Path(args.output)
    if input_path.resolve() == output_path.resolve():
        print("Input and output point to the same file. Use --input or --output with different names.")
        return

    input_format = detect_format(input_path)

    if input_format == "nhl_cues":
        convert_nhl_cues_to_audition(input_path, output_path, args.duration)
    else:
        convert_reaper_to_audition(input_path, output_path)

    print(f"Converted input: {input_path}")
    print(f"Detected format: {input_format}")
    print(f"Output file: {output_path}")


if __name__ == "__main__":
    main()