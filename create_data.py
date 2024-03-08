import numpy as np

import chess

with open("res2.txt") as f:
    games = f.readlines()

games_train = games[:int(len(games)*0.8)]
games_test = games[int(len(games)*0.8):]


def code_games(games_list):
    x = []
    y = []

    for i, game in enumerate(games_list):
        color = i % 2
        chess_game = chess.Chess()
        chess_game.reset_board()
        print(i)

        for j, move in enumerate(game.split(",")):
            move = move.replace("\n","")
            coded_move = chess_game.move_notation_to_digits(move)
            if j % 2 != color:
                board = chess_game.code_board(color).reshape((1,12,8,8))
                current_move = chess_game.code_move(*coded_move).reshape((1,2,8,8))

                x = board if not len(x) else np.concatenate((x, board))
                y = current_move if not len(y) else np.concatenate((y, current_move))

            chess_game.move_piece(*coded_move)
            chess_game.turn = 1 - chess_game.turn
    return x, y


x_train, y_train = code_games(games_train)
x_test, y_test = code_games(games_test)

np.save("x_train.npy", x_train)
np.save("y_train.npy", y_train)
np.save("x_test.npy", x_test)
np.save("y_test.npy", y_test)
