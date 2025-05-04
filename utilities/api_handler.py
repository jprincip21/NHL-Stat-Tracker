import requests
from datetime import date, datetime
import pytz

def get_games_by_date():
    """Function which calls NHLS api to pull game information for the user selected date"""
    
    today = date.today()
    #print(today)
    
    url = f"https://api-web.nhle.com/v1/schedule/{today}"

    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch data")
        return "Failed to fetch data"   
    

    data = response.json()
    week_data = data.get("gameWeek", {})

    todays_games = []

    for day in week_data:
        if day.get("date") == str(today):
            todays_games = day.get("games", [])
            break

    if not todays_games:
        print("No games scheduled for today")
        return "No games scheduled for today"
    
    games_data = {}
    print("Todays NHL games:\n")
    for i, game in enumerate(todays_games):
        
        home_team_name = game["homeTeam"]["abbrev"] + " " + game["homeTeam"]["commonName"]["default"]
        if home_team_name is None:
            home_team_name = "Unknown Home Team"
        
        home_team_logo = game["homeTeam"]["logo"]
        if home_team_logo is None:
            home_team_logo = "Unknown Logo"
        
        away_team_name = game["awayTeam"]["abbrev"] + " " + game["awayTeam"]["commonName"]["default"]
        if away_team_name is None:
            away_team_name = "Unknown Away Team"

        away_team_logo = game["awayTeam"]["logo"]
        if away_team_logo is None:
            away_team_logo = "Unknown Logo"

        venue = game["venue"]["default"]
        if venue is None:
            venue = "Unknown Venue"

        game_time = game["startTimeUTC"]
        if game_time is None:
            game_time = "Unknown Time"
        
        #Convert UTC to Current Machines Timezone
        utc_time = datetime.strptime(game_time, "%Y-%m-%dT%H:%M:%SZ")
        utc_time = utc_time.replace(tzinfo=pytz.UTC)
        local_time = utc_time.astimezone()
        formatted_time = local_time.strftime("%I:%M %p")



        
        games_data[i] = {
            "home_team_name" : home_team_name,
            "home_team_logo" : home_team_logo,
            "away_team_name" : away_team_name,
            "away_team_logo" : away_team_logo,
            "venue": venue,
            "game_time": formatted_time
        }
        

        print(f"{games_data[i]["away_team_name"]} @ {games_data[i]["home_team_name"]}")
        print(f"{games_data[i]["venue"]}")
        print(f"{games_data[i]["game_time"]}")
        print("-" * 30)

    #Example Usage Of games_data Varible

    # for i, game in enumerate(games_data):
    #     print(f"{game[i]["away_team_name"]} @ {game[i]["home_team_name"]}")
    #     print(f"{game[i]["home_team_logo"]}")
    #     print(f"{game[i]["away_team_logo"]}")
    #     print(f"{game[i]["venue"]}")
    #     print(f"{game[i]["game_time"]}")
    #     print("-" * 30)

    return games_data # Return Games data