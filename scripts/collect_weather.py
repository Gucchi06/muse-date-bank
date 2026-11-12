#!/usr/bin/env python3
"""Daily weather snapshot collector.

Fetches the day's forecast from Open-Meteo (no API key) for a few
locations relevant to JRA racecourses and appends one JSON line per
location to data/weather_daily.jsonl. Stdlib only.
"""
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

LOCATIONS = [
    {"name": "osaka_kyoto_racecourse_area", "lat": 34.90, "lon": 135.71},  # near Kyoto racecourse
    {"name": "tokyo_fuchu", "lat": 35.67, "lon": 139.48},                  # Tokyo racecourse (Fuchu)
    {"name": "nakayama_funabashi", "lat": 35.72, "lon": 139.96},           # Nakayama racecourse
]

API = (
    "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
    "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max"
    "&timezone=Asia%2FTokyo&forecast_days=3"
)

OUT = Path(__file__).resolve().parent.parent / "data" / "weather_daily.jsonl"


def fetch(loc: dict) -> dict:
    url = API.format(lat=loc["lat"], lon=loc["lon"])
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)
    daily = data.get("daily", {})
    return {
        "collected_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "location": loc["name"],
        "daily": daily,
    }


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for loc in LOCATIONS:
        try:
            lines.append(json.dumps(fetch(loc), ensure_ascii=False))
        except Exception as e:  # keep going if one location fails
            lines.append(json.dumps({
                "collected_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "location": loc["name"],
                "error": str(e),
            }, ensure_ascii=False))
    with OUT.open("a", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    print(f"Appended {len(lines)} records to {OUT}")


if __name__ == "__main__":
    main()
