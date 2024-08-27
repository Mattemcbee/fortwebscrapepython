import requests
import json
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define your list of players
playerDict = [
    {"name": "Aaron", "playerTag": "Savage Gibson12","accountType":"epic"},
    {"name": "Panna", "playerTag": "puhnuh18","accountType":"epic"},
    {"name": "Andrew", "playerTag": "2ndlunch","accountType":"epic"},
    {"name": "Nick", "playerTag": "TheOGNickTSB","accountType":"epic"},
    {"name": "Matt", "playerTag": "69hogcranker69","accountType":"epic"},
    {"name": "Josh", "playerTag": "bodaciousbunny22","accountType":"psn"},
    {"name": "Tommy", "playerTag": "theartoftom","accountType":"epic"}
]

# Function to fetch player stats
def fetch_player_stats(player):
    api_url = f"https://fortnite-api.com/v2/stats/br/v2?name={player['playerTag']}&timeWindow=season&accountType={player['accountType']}"
    headers = {"Authorization": "60729e20-c6f7-4b8c-83fc-d1f2b7e1a265"}  # Replace YOUR_API_KEY with your actual API key
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        level = data.get("data", {}).get("battlePass", {}).get("level", "N/A")
        kd = data.get("data", {}).get("stats", {}).get("all", {}).get("overall", {}).get("kd", "N/A")
        kills = data.get("data", {}).get("stats", {}).get("all", {}).get("overall", {}).get("kills", "N/A")
        wins = data.get("data", {}).get("stats", {}).get("all", {}).get("overall", {}).get("wins", "N/A")
        minutesPlayed = data.get("data", {}).get("stats", {}).get("all", {}).get("overall", {}).get("minutesPlayed", "N/A")
        matches = data.get("data", {}).get("stats", {}).get("all", {}).get("overall", {}).get("matches", "N/A")
        scorePerMatch = data.get("data", {}).get("stats", {}).get("all", {}).get("overall", {}).get("scorePerMatch", "N/A")
        top3 = data.get("data", {}).get("stats", {}).get("all", {}).get("overall", {}).get("top3", "N/A")
        

        '''          const matches = overallStats.matches ? overallStats.matches : 'N/A';
          const scorePerMatch = overallStats.scorePerMatch ? overallStats.scorePerMatch : 'N/A';
          const top3 = overallStats.top3 ? overallStats.top3 : 'N/A';
          const top3per = (top3 / matches * 100).toFixed(1);

'''
        
        return {"name": player["name"], "level": level, "kd": kd, "kills": kills, "wins": wins, "minutesPlayed": minutesPlayed, "matches": matches, "top3": top3, "scorePerMatch": scorePerMatch  }
    else:
        print(f"Failed to fetch player stats for {player['name']}. Status code: {response.status_code}")
        return None

# Function to store player stats to Google Sheets
def store_player_stats_to_sheets(stats):
    # Authenticate with Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet
    spreadsheet = client.open('fortniteData')
    worksheet = spreadsheet.get_worksheet(0)  # Assuming data is in the first worksheet

    # Get current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append data to the spreadsheet including the timestamp
    worksheet.append_row([current_time, stats['name'], stats['level'], stats['kd'], stats['kills'], stats['wins'],  stats['matches']])

#stats['minutesPlayed'],stats['top3'], stats['scorePerMatch']
# Handler function to fetch, store, and view stats for all players
def lambda_handler(event, context):
    for player in playerDict:
        stats = fetch_player_stats(player)
        if stats:
            store_player_stats_to_sheets(stats)

# If you want to test your function locally, you can call lambda_handler() directly
if __name__ == "__main__":
    lambda_handler(None, None)
