import datetime
import json
import os
import sys
import urllib.parse
import urllib.request

API_URL = "https://ws.audioscrobbler.com/2.0/"
OUT_PATH = os.environ.get("OUTPUT", "assets/listening.json")
API_KEY = os.environ.get("LASTFM_API_KEY", "")
USERNAME = os.environ.get("LASTFM_USER", "takyon303")
SAMPLE = os.environ.get("LASTFM_SAMPLE", "")

FAKE = {
    "track": "weird fishes/arpeggi",
    "artist": "radiohead",
    "url": "https://www.last.fm/music/radiohead/_/Weird+Fishes%2FArpeggi",
}


def load_track():
    if not API_KEY:
        return None
    if SAMPLE == "playing":
        return FAKE | {"playing": True, "uts": None}
    if SAMPLE == "idle":
        return FAKE | {"playing": False, "uts": int(datetime.datetime.now(datetime.timezone.utc).timestamp())}

    query = urllib.parse.urlencode({
        "method": "user.getrecenttracks",
        "user": USERNAME,
        "api_key": API_KEY,
        "limit": "1",
        "format": "json",
    })
    request = urllib.request.Request(
        API_URL + "?" + query,
        headers={"User-Agent": "takyon303.github.io/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.load(response)

    tracks = (payload.get("recenttracks") or {}).get("track") or []
    if not tracks:
        return None

    entry = tracks[0]
    artist = entry.get("artist")
    artist = artist.get("#text") if isinstance(artist, dict) else artist
    date = entry.get("date") or {}
    return {
        "playing": (entry.get("@attr") or {}).get("nowplaying") == "true",
        "track": entry.get("name") or "",
        "artist": artist or "",
        "url": entry.get("url") or None,
        "uts": int(date["uts"]) if date.get("uts") else None,
    }


def write(track):
    os.makedirs(os.path.dirname(OUT_PATH) or ".", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as file:
        json.dump(track, file, separators=(",", ":"), ensure_ascii=False)
    print(f"listening: wrote {OUT_PATH}")


def main():
    try:
        track = load_track()
    except Exception as error:
        print(f"listening: {error}", file=sys.stderr)
        return 0
    if track and not track.get("track"):
        track = None
    if track:
        write(track)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
