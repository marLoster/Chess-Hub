import re

with open("games.pgn") as file:
    lines = enumerate(file.readlines())

lines = list(filter(lambda x: x[1][0] == "1", lines))

for game_num, game in lines:
    moves = re.split(r" ?[0-9]+\. ", game)[1:]
    print(moves)
    break