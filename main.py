import json
import pickSix
import players

averages = pickSix.get_player_totals(players.baseball_heroes_test)
print(averages)

game_counts = pickSix.get_team_games("20240618", "20240624")
print(game_counts)

for player, avg in averages.items():
    player_line = players.baseball_heroes_test[player][3]
    est_total_points = avg * game_counts[players.baseball_heroes_test[player][1]]
    print(f"{player} is estimated to score {est_total_points} points this week with a line of {player_line}.")
    print(f"{player} has a {est_total_points/player_line} chance of hitting the line.")