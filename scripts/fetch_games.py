#!/usr/bin/env python3
"""Hämtar kommande V85/V75/V86/GS75/V64/V5-omgångar från ATG:s kalender-API
(server-sidan, ingen CORS-begränsning här) och skriver en liten
data/games.json som index.html läser via ett vanligt same-origin fetch() på
GitHub Pages.

GS75/V64/V5 är, till skillnad från V85/V75/V86, inte travexklusiva spelformer
— de kan gå på galoppbanor. Travreda hanterar bara travdata (inga skor-/
kusk-fält för galopp), så alla omgångar filtreras på travets egen
tracks[].sport-fält innan de tas med, oavsett speltyp."""

import json
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone

API_BASE = "https://www.atg.se/services/racinginfo/v1/api"
BET_TYPES = ["V85", "V75", "V86", "GS75", "V64", "V5"]
DAYS_AHEAD = 10
OUT_PATH = "data/games.json"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "travreda-fetch-games/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    today = date.today()
    games = []

    for offset in range(DAYS_AHEAD):
        day = today + timedelta(days=offset)
        date_str = day.isoformat()
        try:
            data = fetch_json(f"{API_BASE}/calendar/day/{date_str}")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                continue
            print(f"WARN: {date_str}: HTTP {exc.code}", file=sys.stderr)
            continue
        except Exception as exc:
            print(f"WARN: {date_str}: {exc}", file=sys.stderr)
            continue

        track_names = {t["id"]: t["name"] for t in data.get("tracks", [])}
        track_sports = {t["id"]: t.get("sport") for t in data.get("tracks", [])}
        day_games = data.get("games", {})

        for bet_type in BET_TYPES:
            for game in day_games.get(bet_type, []):
                if not game.get("id"):
                    # ATG listar ibland kommande omgångar innan spel-id:t
                    # är tilldelat. Inget vi kan göra med förrän det finns.
                    continue
                tracks = game.get("tracks") or []
                track_id = tracks[0] if tracks else None
                if track_sports.get(track_id) != "trot":
                    # Travreda hanterar bara trav — hoppar över galoppomgångar
                    # (förekommer för GS75/V64/V5, aldrig för V85/V75/V86).
                    continue
                # Bankoden som faktiskt skickas till ATG (trackcode i
                # exportfilen) hämtas ur spel-id:ts egen inbäddade
                # bankodskomponent ({TYP}_{datum}_{bankod}_{avdelning}) —
                # INTE ur kalenderns "tracks"-lista (bara sorterad på
                # bankod, inte avdelningsordning). Ett tidigare antagande om
                # att avdelning 1:s fysiska bana var rätt bankod visade sig
                # felaktigt: V86 körs numera alltid över två banor (Solvalla
                # + en av Åby/Jägersro/Bergsåker), och ATG identifierar hela
                # den kombinerade omgången med en reserverad specialbankod
                # (40) — exakt det som redan står i id-strängen. Bekräftat
                # mot tre oberoende källor, se CLAUDE.md avsnitt 5.
                game_id = game.get("id")
                id_parts = game_id.split("_")
                id_track_id = int(id_parts[2]) if len(id_parts) == 4 and id_parts[2].isdigit() else None
                is_multi_track = len(tracks) > 1
                games.append(
                    {
                        "type": bet_type,
                        "id": game_id,
                        "date": date_str,
                        "startTime": game.get("startTime"),
                        "status": game.get("status"),
                        "trackId": id_track_id if id_track_id is not None else track_id,
                        "trackName": "Flera banor" if is_multi_track else track_names.get(track_id),
                    }
                )

        time.sleep(0.3)

    games.sort(key=lambda g: (g["startTime"] or "", g["type"]))

    out = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "games": games,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(games)} games to {OUT_PATH}")


if __name__ == "__main__":
    main()
