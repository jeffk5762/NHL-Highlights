import csv

INPUT_FILE = "audition_markers.csv"
OUTPUT_FILE = "clip_ranges.csv"

PRE_ROLL = 30.0
POST_ROLL = 15.0


def parse_audition_decimal_time(value: str) -> float:
    """
    Parse Adobe Audition-style decimal marker time like:
    1.1.00000000
    27.2.36303855
    4048.1.19111096

    Interpreted as:
    seconds.frames.fraction

    Since your file is marked 'decimal', we treat this as:
    seconds + fractional part reconstructed from the pieces.

    Example:
    27.2.36303855 -> 27.236303855
    """
    value = value.strip()
    if not value:
        return 0.0

    parts = value.split(".")
    if len(parts) == 1:
        return float(parts[0])

    whole = parts[0]
    frac = "".join(parts[1:])
    return float(f"{whole}.{frac}")


def format_seconds(seconds: float) -> str:
    return f"{seconds:.3f}"


def main():
    rows_out = []

    with open(INPUT_FILE, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for i, row in enumerate(reader, start=1):
            start_raw = (row.get("Start") or "").strip()
            if not start_raw:
                continue

            marker_time = parse_audition_decimal_time(start_raw)
            clip_start = max(0.0, marker_time - PRE_ROLL)
            clip_end = marker_time + POST_ROLL
            duration = clip_end - clip_start

            rows_out.append({
                "ClipName": f"SAVE_{i:03d}",
                "MarkerTime": format_seconds(marker_time),
                "ClipStart": format_seconds(clip_start),
                "ClipEnd": format_seconds(clip_end),
                "Duration": format_seconds(duration),
            })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["ClipName", "MarkerTime", "ClipStart", "ClipEnd", "Duration"]
        )
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Wrote {len(rows_out)} clip ranges to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()