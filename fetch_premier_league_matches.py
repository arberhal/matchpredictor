import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_KEY:
    raise ValueError("API_FOOTBALL_KEY not found")

BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

LEAGUE_ID = 39  # Premier League
SEASONS = [2022, 2023, 2024]


def fetch_fixtures(season: int) -> list:
    r = requests.get(
        f"{BASE_URL}/fixtures",
        headers=HEADERS,
        params={"league": LEAGUE_ID, "season": season}
    )
    r.raise_for_status()
    return r.json()["response"]


def fetch_statistics(fixture_id: int) -> list:
    r = requests.get(
        f"{BASE_URL}/fixtures/statistics",
        headers=HEADERS,
        params={"fixture": fixture_id}
    )
    r.raise_for_status()
    return r.json()["response"]


def parse_statistics(stats_response: list, fixture_id: int) -> dict:
    row = {"fixture_id": fixture_id}

    for i, team_block in enumerate(stats_response):
        side = "home" if i == 0 else "away"

        for stat in team_block["statistics"]:
            key = stat["type"].lower().replace(" ", "_")
            value = stat["value"]

            if isinstance(value, str) and "%" in value:
                value = float(value.replace("%", ""))

            row[f"{side}_{key}"] = value

    return row


matches = []

for season in SEASONS:
    print(f"Fetching fixtures for season {season}...")
    fixtures = fetch_fixtures(season)

    for f in fixtures:
        if f["fixture"]["status"]["short"] != "FT":
            continue

        matches.append({
            "fixture_id": f["fixture"]["id"],
            "date": f["fixture"]["date"],
            "season": f["league"]["season"],
            "home_team": f["teams"]["home"]["name"],
            "away_team": f["teams"]["away"]["name"],
            "home_goals": f["goals"]["home"],
            "away_goals": f["goals"]["away"],
            "venue": f["fixture"]["venue"]["name"]
        })

print(f"Total matches fetched: {len(matches)}")

df_matches = pd.DataFrame(matches)


stats_rows = []

for i, fixture_id in enumerate(df_matches["fixture_id"], start=1):
    print(f"Fetching statistics {i}/{len(df_matches)}")

    stats = fetch_statistics(fixture_id)
    if stats:
        stats_rows.append(parse_statistics(stats, fixture_id))

    time.sleep(0.4)  # API rate limit protection

df_stats = pd.DataFrame(stats_rows)


df_full = df_matches.merge(df_stats, on="fixture_id", how="left")

os.makedirs("data/raw", exist_ok=True)
df_full.to_csv(
    "data/raw/premier_league_matches_with_stats_3_seasons.csv",
    index=False
)

print("Saved: data/raw/premier_league_matches_with_stats_3_seasons.csv")
print("Final shape:", df_full.shape)