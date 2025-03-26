import requests
import json
from datetime import date

def get_todays_games():
    
    today = date.today()
    print(today)
    
    url = "https://api-web.nhle.com/v1/schedule/now"

    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch data")
        return
    
    data = response.json()
    week_data = data.get("gameWeek", {})

    todays_games = []

    for day in week_data:
        if day.get("date") == str(today):
            todays_games = day.get("games", [])
            break

    if not todays_games:
        print("No games scheduled for today")
        return
    
    print("Todays NHL games:\n")
    for game in todays_games:
        home = game["homeTeam"]["commonName"]["default"]
        away = game["awayTeam"]["commonName"]["default"]
        venue = game.get("venue", {}).get("default", "Unknown Venue")
        game_time = game.get("startTimeUTC", "Unknown Time")

        print(f"{away} @ {home}")
        print(f"Venue: {venue}")
        print(f"Start Time (UTC): {game_time}")
        print("-" * 30)
    