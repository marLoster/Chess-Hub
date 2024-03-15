import numpy as np
import tensorflow as tf

from keras.models import load_model

import engine.chess as chess
import engine.chess_bot as chess_bot


def max_criterion(arr):
    positions = np.transpose(np.unravel_index(np.argsort(arr[0], axis=None)[::-1], arr[0].shape))
    moves = np.transpose(np.unravel_index(np.argsort(arr[1], axis=None)[::-1], arr[1].shape))

    positions = np.repeat(positions, 64, axis=0)
    moves = np.tile(moves, (64, 1))
    res = np.hstack((positions, moves))
    return res


def weighted_mse(y_true, y_pred):
    weights = (y_true * 62) + 1
    squared_difference = tf.math.multiply(weights, tf.square(y_true - y_pred))
    return tf.reduce_mean(squared_difference)


class MaxBot(chess_bot.ChessBot):
    def __init__(self, model_location):
        super().__init__(model_location)
        self.model = load_model(model_location, custom_objects={"weighted_mse": weighted_mse})

    def get_move(self, board, color):
        game = chess.Chess()
        game.load_board(board, color)
        prediction = self.model.predict(board.reshape(1, 12, 8, 8))[0]
        predicted_moves = max_criterion(prediction)
        for row_index, move_numbers in enumerate(predicted_moves):
            if (game.board[move_numbers[0]][move_numbers[1]].color == color and
                    game.is_move_valid(*move_numbers)):
                return move_numbers
