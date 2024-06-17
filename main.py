import json
import pickSix
import players

#averages = pickSix.get_player_totals(players.baseball_heroes_test)
#print(averages)

game_counts = pickSix.get_team_games("20240618", "20240624")
print(game_counts)