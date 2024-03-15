import numpy as np
import tensorflow as tf

from keras.models import load_model

import engine.chess as chess
from engine.chess_values import Color

bot1 = "value_nn_20240305181141.keras"
bot2 = "20240301220159.keras"
current_white = bot1
bot1_wins = 0
bot2_wins = 0
draw = 0


def harmonic_criterion(arr):

    new_array = np.zeros((8*8*8*8, 5))

    for pos_row in range(8):
        for pos_col in range(8):
            for mov_row in range(8):
                for mov_col in range(8):
                    harmonic_mean = ((2*arr[0][pos_row][pos_col]*arr[1][mov_row][mov_col]) /
                                     (arr[0][pos_row][pos_col] + arr[1][mov_row][mov_col]))
                    new_array[(pos_row*8 + pos_col)*64 + 8*mov_row + mov_col] = \
                        [pos_row, pos_col, mov_row, mov_col, harmonic_mean]

    sorted_moves = new_array[np.argsort(new_array[:, 4])[::-1]]

    return sorted_moves[:, :-1].astype(int)


def max_criterion(arr):
    positions = np.transpose(np.unravel_index(np.argsort(arr[0], axis=None)[::-1], arr[0].shape))
    moves = np.transpose(np.unravel_index(np.argsort(arr[1], axis=None)[::-1], arr[1].shape))

    positions = np.repeat(positions, 64, axis=0)
    moves = np.tile(moves, (64, 1))
    res = np.hstack((positions, moves))
    return res


def bot1_move(model, game, color):
    coded_board = game.code_board(1 - color)
    prediction = model.predict(coded_board.reshape(1, 12, 8, 8), verbose=0)[0]
    predicted_moves = max_criterion(prediction)
    for row_index, move_numbers in enumerate(predicted_moves):
        if (game.board[move_numbers[0]][move_numbers[1]].color == 1-color and
                game.is_move_valid(*move_numbers)):
            game.move_piece(*move_numbers, update_status=True)
            break


def weighted_mse(y_true, y_pred):
    weights = (y_true * 62) + 1
    squared_difference = tf.math.multiply(weights, tf.square(y_true - y_pred))
    return tf.reduce_mean(squared_difference)


def bot2_move(model, game, color):

    possible_moves = game.get_moves_figs(1 - color)
    moves = None
    max_pred = -2
    for piece, targets in possible_moves:
        for target in targets:
            game_copy = game.copy_game()
            game_copy.move_piece(piece[1][0], piece[1][1], target[0], target[1])
            coded_board = game_copy.code_board(1 - color)
            prediction = model.predict(coded_board.reshape(1, 12, 8, 8), verbose=0)[0]
            if prediction > max_pred:
                moves = (piece[1][0], piece[1][1], target[0], target[1])
                max_pred = prediction

    if not moves:
        raise Exception("Valid moves not found")

    game.move_piece(*moves, update_status=True)


model1 = load_model("20240301220159.keras", custom_objects={"weighted_mse": weighted_mse})
model2 = load_model("value_nn_20240305181141.keras", custom_objects={"weighted_mse": weighted_mse})

while True:
    print(bot1_wins, draw, bot2_wins)
    game = chess.Chess()
    game.reset_board()
    current_player = current_white
    bot1_color = Color.white if current_white == bot1 else Color.black
    bot2_color = 1 - bot1_color
    move = 0
    while game.status == 2:
        if move % 20 == 0:
            print(move, bot1_wins, draw, bot2_wins)
            game.print_board()
        if current_player == bot1:
            bot1_move(model1, game, bot1_color)
            current_player = bot2
        else:
            bot2_move(model2, game, bot2_color)
            current_player = bot1
        move += 1

    bot1_wins += 1 * (bot1_color == game.status)
    bot2_wins += 1 * (bot2_color == game.status)

    current_white = bot1 if current_white == bot2 else bot2
