from math import sqrt

import numpy as np

import chess

with open("res2_end.txt") as f:
    games = f.readlines()

games_train = games[:int(len(games)*0.8)]
games_test = games[int(len(games)*0.8):]


def code_games(games_list):
    x = []
    y = []

    for i, game in enumerate(games_list):
        winner = game.split(",")[0]
        game_length = len(game.split(","))-1
        chess_game = chess.Chess()
        chess_game.reset_board()

        if game_length == 1:
            continue

        for j, move in enumerate(game.split(",")[1:]):
            move = move.replace("\n","")
            coded_move = chess_game.move_notation_to_digits(move)

            board = chess_game.code_board(1 - j%2).reshape((1,12,8,8))
            if winner == "0-1":
                sign = 2*(j%2) - 1
            elif winner == "1-0":
                sign = -2*(j%2) + 1
            else:
                sign = 0

            checkmate_bonus = 0.1 if "#" in move else 0

            current_evaluation = np.array([[sign * (-sqrt(-(j/(game_length-1)) + 1) + 1) + checkmate_bonus]])

            x = board if not len(x) else np.concatenate((x, board))
            y = current_evaluation if not len(y) else np.concatenate((y, current_evaluation))

            chess_game.move_piece(*coded_move)
            chess_game.turn = 1 - chess_game.turn
    return x, y


x_train, y_train = code_games(games_train)
x_test, y_test = code_games(games_test)

np.save("x_train2.npy", x_train)
np.save("y_train2.npy", y_train)
np.save("x_test2.npy", x_test)
np.save("y_test2.npy", y_test)
