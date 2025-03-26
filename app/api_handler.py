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

    api_date = week_data[0]['date']
    print(api_date)

    if str(today) == api_date:
        games = week_data[0]['games']

    print(games)

    if not games:
        print("No games scheduled for today.")
        return
    
    print("Todays NHL games:\n")
    for game in games:
        home = game["homeTeam"]["commonName"]["default"]
        away = game["awayTeam"]["commonName"]["default"]
        venue = game.get("venue", {}).get("default", "Unknown Venue")
        game_time = game.get("startTimeUTC", "Unknown Time")

        print(f"{away} @ {home}")
        print(f"Venue: {venue}")
        print(f"Start Time (UTC): {game_time}")
        print("-" * 30)
    