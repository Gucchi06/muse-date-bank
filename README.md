# muse-data-bank

Automated, unattended data collection run by GitHub Actions.
Public datasets only — no personal data is stored here.

## What runs

- Workflow: `.github/workflows/collect.yml`
  - Schedule: daily 09:05 JST (`5 0 * * *` UTC), plus manual `workflow_dispatch`
- Script: `scripts/collect_weather.py`
  - Fetches Open-Meteo daily forecasts (no API key) for areas near
    Kyoto / Tokyo / Nakayama racecourses and appends JSON lines.

## Data layout

- `data/weather_daily.jsonl` — one JSON object per location per run,
  with `collected_at_utc`, `location`, and the Open-Meteo `daily` block.

## Notes

- Weather history is an input for horse-racing going (track condition)
  analysis in the racing databank project.
- Collection jobs must respect each source's terms and rate limits.
