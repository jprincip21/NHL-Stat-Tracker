import requests
from datetime import date
import pytz

def get_games_by_date():
    
    today = date.today()
    #print(today)
    
    url = f"https://api-web.nhle.com/v1/schedule/{today}"

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
        
        home_team_name = game["homeTeam"]["commonName"]["default"]
        if home_team_name is None:
            home_team_name = "Unknown Home Team"
        
        away_team_name = game["awayTeam"]["commonName"]["default"]
        if away_team_name is None:
            away_team_name = "Unknown Away Team"

        venue = game["venue"]["default"]
        if venue is None:
            venue = "Unknown Venue"

        game_time = game["startTimeUTC"]
        if game_time is None:
            game_time = "Unknown Time"

        print(f"{away_team_name} @ {home_team_name}")
        print(f"Venue: {venue}")
        print(f"Start Time (UTC): {game_time}")
        print("-" * 30)
    