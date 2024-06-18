import players
from datetime import datetime, timedelta
import http.client
import os
import json
from dotenv import load_dotenv
from collections import Counter

load_dotenv()
conn = http.client.HTTPSConnection("tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com")

headers = {
    'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
    'x-rapidapi-host': os.getenv('RAPIDAPI_HOST')
}

def calculate_game_score(stat_line):
    score = 0
    score += int(stat_line["2B"])*players.baseball_scoring["double"]
    score += int(stat_line["3B"])*players.baseball_scoring["triple"]
    score += int(stat_line["HR"])*players.baseball_scoring["home run"]
    score += int(stat_line["RBI"])*players.baseball_scoring["rbi"]
    score += int(stat_line["R"])*players.baseball_scoring["run"]
    score += int(stat_line["BB"])*players.baseball_scoring["bb"]
    score += int(stat_line["IBB"])*players.baseball_scoring["bb"]
    score += int(stat_line["HBP"])*players.baseball_scoring["hbp"]
    score += int(stat_line["SB"])*players.baseball_scoring["sb"]
    singles = int(stat_line["H"])-int(stat_line["2B"])-int(stat_line["3B"])-int(stat_line["HR"])
    score += singles*players.baseball_scoring["single"]
    return score

def calculate_weekly_score(stat_line):
    score = 0
    for line in stat_line.values():
        hitting = line["Hitting"]
        running = line["BaseRunning"]
        hitting["SB"] = running["SB"]
        score += calculate_game_score(hitting)
    return score

def get_player_totals(player_dict):
    player_avg = {}
    for player in player_dict:
        player_id = player_dict[player][2]
        conn.request("GET", f"/getMLBGamesForPlayer?playerID={player_id}&numberOfGames=10&season=2024", headers=headers)
        res = conn.getresponse()
        data = res.read()
        data_str = data.decode("utf-8")
        data_dict = json.loads(data_str)
        player_avg[player] = calculate_weekly_score(data_dict['body'])/10
    return player_avg

def get_team_games(start_date, end_date):
    start = datetime.strptime(start_date, '%Y%m%d').date()
    end = datetime.strptime(end_date, '%Y%m%d').date()

    # Loop from start to end date
    cur_date = start
    team_games = []
    while cur_date <= end:
        cur_date_str = cur_date.strftime('%Y%m%d')
        conn.request("GET", f"/getMLBGamesForDate?gameDate={cur_date_str}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        data_str = data.decode("utf-8")
        data_dict = json.loads(data_str)
        game_dict = data_dict['body']
        for game in game_dict:
            team_games.append(game['away'])
            team_games.append(game['home'])
        # Increment the date by one day
        cur_date += timedelta(days=1)
    game_count = Counter(team_games)
    return game_count
