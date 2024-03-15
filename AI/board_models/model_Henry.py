import numpy as np
import tensorflow as tf

from keras.models import load_model

import engine.chess as chess
import engine.chess_bot as chess_bot


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


def weighted_mse(y_true, y_pred):
    weights = (y_true * 62) + 1
    squared_difference = tf.math.multiply(weights, tf.square(y_true - y_pred))
    return tf.reduce_mean(squared_difference)


class HenryBot(chess_bot.ChessBot):
    def __init__(self, model_location):
        super().__init__(model_location)
        self.model = load_model(model_location, custom_objects={"weighted_mse": weighted_mse})

    def get_move(self, board, color):
        game = chess.Chess()
        game.load_board(board, color)
        prediction = self.model.predict(board.reshape(1, 12, 8, 8))[0]
        predicted_moves = harmonic_criterion(prediction)
        for row_index, move_numbers in enumerate(predicted_moves):
            if (game.board[move_numbers[0]][move_numbers[1]].color == color and
                    game.is_move_valid(*move_numbers)):
                return move_numbers
