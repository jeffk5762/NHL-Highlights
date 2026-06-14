import csv
import json
import time
import hashlib
import argparse
import requests # type: ignore
from datetime import datetime, timezone

try:
    import pygetwindow as gw  # type: ignore
except (ImportError, ModuleNotFoundError):

    gw = None

try:
    import pyautogui  # type: ignore
except ImportError:
    pyautogui = None


DEFAULT_POLL_SECONDS = 2
WRITE_JSON_DEBUG = False

REAPER_WINDOW_TITLE_CONTAINS = "REAPER"

CUE_CSV_TEMPLATE = "nhl_cues_{game_id}.csv"
SEEN_JSON_TEMPLATE = "seen_{game_id}.json"
DEBUG_JSON_TEMPLATE = "nhl_debug_{game_id}.json"


def now_utc_iso():
    return datetime.now(timezone.utc).isoformat()


def safe_get(dct, *keys, default=None):
    cur = dct
    for key in keys:
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur


def stable_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def period_time_to_game_seconds(period, time_in_period):
    try:
        period = int(period)
        mm, ss = map(int, time_in_period.split(":"))
        return (period - 1) * 1200 + mm * 60 + ss
    except Exception:
        return None


def load_seen_ids(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_seen_ids(path, seen_ids):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sorted(list(seen_ids)), f, indent=2)


def focus_reaper_window():
    if gw is None:
        print("pygetwindow not installed; cannot focus Reaper")
        return False

    try:
        windows = gw.getWindowsWithTitle(REAPER_WINDOW_TITLE_CONTAINS)
        if not windows:
            print(f"No window found containing title: {REAPER_WINDOW_TITLE_CONTAINS}")
            return False

        win = windows[0]
        if win.isMinimized:
            win.restore()
            time.sleep(0.1)

        win.activate()
        time.sleep(0.15)
        return True
    except Exception as e:
        print(f"Failed to focus Reaper window: {e}")
        return False


def send_reaper_marker_key():
    if pyautogui is None:
        print("pyautogui not installed; skipping hotkey send")
        return False

    focused = focus_reaper_window()
    if not focused:
        print("Could not focus Reaper window; skipping 'M' send")
        return False

    try:
        pyautogui.press("m")
        return True
    except Exception as e:
        print(f"Failed to send 'M' to Reaper: {e}")
        return False


def fetch_json(url):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


def fetch_play_by_play_new(game_id):
    url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play"
    return fetch_json(url), "new"


def fetch_play_by_play_legacy(game_id):
    url = f"https://statsapi.web.nhl.com/api/v1/game/{game_id}/feed/live"
    return fetch_json(url), "legacy"


def fetch_play_by_play_with_fallback(game_id):
    errors = []

    try:
        return fetch_play_by_play_new(game_id)
    except Exception as e:
        errors.append(f"new endpoint failed: {e}")

    try:
        return fetch_play_by_play_legacy(game_id)
    except Exception as e:
        errors.append(f"legacy endpoint failed: {e}")

    raise RuntimeError(" ; ".join(errors))


def get_plays_from_response(data, source_kind):
    if source_kind == "new":
        candidates = [
            safe_get(data, "plays", default=None),
            safe_get(data, "gameData", "plays", default=None),
        ]
        for c in candidates:
            if isinstance(c, list):
                return c

    if source_kind == "legacy":
        plays = safe_get(data, "liveData", "plays", "allPlays", default=None)
        if isinstance(plays, list):
            return plays

    candidates = [
        safe_get(data, "plays", default=None),
        safe_get(data, "liveData", "plays", "allPlays", default=None),
    ]
    for c in candidates:
        if isinstance(c, list):
            return c

    return []


def get_event_id(play):
    for key in ("eventId", "eventIdx", "sortOrder", "playId"):
        if key in play:
            return str(play[key])

    about = play.get("about", {})
    for key in ("eventId", "eventIdx"):
        if key in about:
            return str(about[key])

    raw = json.dumps(play, sort_keys=True)
    return "hash-" + stable_hash(raw)


def normalize_play(play):
    event_type = (
        play.get("typeDescKey")
        or safe_get(play, "result", "event")
        or play.get("event")
        or ""
    )

    period = (
        safe_get(play, "periodDescriptor", "number")
        or safe_get(play, "about", "period")
        or play.get("period")
    )

    time_in_period = (
        play.get("timeInPeriod")
        or safe_get(play, "about", "periodTime")
        or play.get("periodTime")
        or ""
    )

    description = (
        play.get("description")
        or safe_get(play, "result", "description")
        or ""
    )

    shot_type = (
        play.get("shotType")
        or safe_get(play, "result", "secondaryType")
        or ""
    )

    team = (
        safe_get(play, "details", "eventOwnerTeamAbbrev")
        or safe_get(play, "team", "triCode")
        or safe_get(play, "team", "name")
        or ""
    )

    shooter = ""
    goalie = ""

    details = play.get("details", {})
    if isinstance(details, dict):
        shooter = (
            details.get("shootingPlayerName")
            or details.get("shootingPlayer")
            or details.get("shooterName")
            or shooter
        )
        goalie = (
            details.get("goalieInNetName")
            or details.get("goalieName")
            or goalie
        )
        shot_type = details.get("shotType", shot_type)

    if (not shooter or not goalie) and "players" in play:
        for p in play.get("players", []):
            ptype = p.get("playerType", "")
            pname = safe_get(p, "player", "fullName", default="")
            if ptype == "Shooter" and not shooter:
                shooter = pname
            elif ptype == "Goalie" and not goalie:
                goalie = pname

    return {
        "event_id": get_event_id(play),
        "raw_event_type": str(event_type),
        "period": period,
        "time_in_period": time_in_period,
        "description": description,
        "shot_type": shot_type,
        "team": team,
        "shooter": shooter,
        "goalie": goalie,
        "raw": play,
    }


def is_save_event(nplay):
    et = (nplay["raw_event_type"] or "").strip().lower()

    positive = {
        "shot-on-goal",
        "shot",
    }

    negative = {
        "goal",
        "blocked-shot",
        "missed-shot",
        "blocked shot",
        "missed shot",
    }

    if et in negative:
        return False

    if et in positive:
        return True

    desc = (nplay["description"] or "").lower()
    if "saved by" in desc:
        return True
    if "shot on goal" in desc:
        return True

    return False


def build_marker_name(nplay):
    period = nplay["period"] if nplay["period"] is not None else "?"
    t = nplay["time_in_period"] or "??:??"
    goalie = nplay["goalie"] or "Goalie"
    shooter = nplay["shooter"] or "Shooter"
    shot_type = nplay["shot_type"]

    name = f"SAVE P{period} {t} {goalie} vs {shooter}"
    if shot_type:
        name += f" ({shot_type})"
    return name


def ensure_csv_header(path):
    try:
        with open(path, "x", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "detected_utc",
                "event_id",
                "period",
                "time_in_period",
                "game_elapsed_seconds",
                "team",
                "event_type",
                "goalie",
                "shooter",
                "shot_type",
                "marker_name",
                "description",
                "marker_key_sent"
            ])
    except FileExistsError:
        pass


def append_cue(path, nplay, marker_name, marker_key_sent):
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            now_utc_iso(),
            nplay["event_id"],
            nplay["period"],
            nplay["time_in_period"],
            period_time_to_game_seconds(nplay["period"], nplay["time_in_period"]),
            nplay["team"],
            nplay["raw_event_type"],
            nplay["goalie"],
            nplay["shooter"],
            nplay["shot_type"],
            marker_name,
            nplay["description"],
            marker_key_sent
        ])


def main():
    parser = argparse.ArgumentParser(description="Watch NHL play-by-play and mark saves in Reaper.")
    parser.add_argument("game_id", help="NHL game ID, e.g. 2024020001")
    parser.add_argument("--poll", type=float, default=DEFAULT_POLL_SECONDS, help="Polling interval in seconds")
    parser.add_argument("--send-hotkey", action="store_true", help="Send 'M' to Reaper on save events")
    parser.add_argument("--from-start", action="store_true", help="Process all existing plays instead of live-only start")
    parser.add_argument("--debug-json", action="store_true", help="Write latest raw response to debug JSON file")
    parser.add_argument("--marker-delay", type=float, default=0.0, help="Delay in seconds after each marker key send")
    args = parser.parse_args()

    game_id = args.game_id
    cue_csv = CUE_CSV_TEMPLATE.format(game_id=game_id)
    seen_json = SEEN_JSON_TEMPLATE.format(game_id=game_id)
    debug_json = DEBUG_JSON_TEMPLATE.format(game_id=game_id)

    ensure_csv_header(cue_csv)

    print(f"Watching NHL game {game_id}")
    print(f"Polling every {args.poll} seconds")
    print(f"Send 'M' to Reaper: {args.send_hotkey}")
    print(f"Live-only start: {not args.from_start}")
    print(f"Cue CSV: {cue_csv}")

    seen_ids = load_seen_ids(seen_json)
    initialized = False

    while True:
        try:
            data, source_kind = fetch_play_by_play_with_fallback(game_id)

            if args.debug_json or WRITE_JSON_DEBUG:
                with open(debug_json, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)

            plays = get_plays_from_response(data, source_kind)
            if not plays:
                print(f"[{now_utc_iso()}] No plays found from source={source_kind}")
                time.sleep(args.poll)
                continue

            normalized = [normalize_play(p) for p in plays]

            if not initialized and not args.from_start:
                for nplay in normalized:
                    seen_ids.add(nplay["event_id"])
                save_seen_ids(seen_json, seen_ids)
                initialized = True
                print(f"[{now_utc_iso()}] Initialized live-only mode with {len(normalized)} existing plays already seen.")
                time.sleep(args.poll)
                continue

            initialized = True
            new_count = 0
            save_count = 0

            for nplay in normalized:
                event_id = nplay["event_id"]
                if event_id in seen_ids:
                    continue

                seen_ids.add(event_id)
                new_count += 1

                if is_save_event(nplay):
                    save_count += 1
                    marker_name = build_marker_name(nplay)

                    marker_key_sent = False
                    if args.send_hotkey:
                        marker_key_sent = send_reaper_marker_key()
                        if args.marker_delay > 0:
                            time.sleep(args.marker_delay)

                    append_cue(cue_csv, nplay, marker_name, marker_key_sent)

                    print(
                        f"[{now_utc_iso()}] SAVE detected: "
                        f"event_id={nplay['event_id']} period={nplay['period']} "
                        f"time={nplay['time_in_period']} marker='{marker_name}'"
                    )

            save_seen_ids(seen_json, seen_ids)

            if new_count > 0 or save_count > 0:
                print(f"[{now_utc_iso()}] New plays: {new_count}, saves written: {save_count}")

            if args.from_start:
                print(f"[{now_utc_iso()}] from-start run complete. Exiting.")
                break

            time.sleep(args.poll)

        except Exception as e:
            print(f"[{now_utc_iso()}] Error fetching or processing plays: {e}")
            time.sleep(args.poll)
            continue


if __name__ == "__main__":
    main()
                  