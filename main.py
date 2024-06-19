import json
import pickSix
import players

averages = pickSix.get_player_totals(players.baseball_heroes)
print(averages)

game_counts = pickSix.get_team_games("20240620", "20240624")
print(game_counts)

projections = pickSix.get_player_projections()
print(projections)

outcome_dict = {}

for player, avg in averages.items():
    player_line = players.baseball_heroes[player][3]
    est_total_points = avg * game_counts[players.baseball_heroes[player][1]]
    outcome_dict[player] = est_total_points/player_line

sorted_outcome = sorted(outcome_dict.items(), key=lambda x: x[1], reverse=True)
# Convert the sorted list of tuples back to a dictionary if needed
sorted_outcome = dict(sorted_outcome)
# Printing the sorted dictionary
for player, score in sorted_outcome.items():
    print(f"{player}: {score}")