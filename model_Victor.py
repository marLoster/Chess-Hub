import numpy as np
import tensorflow as tf

from keras.models import load_model

import chess
import chess_bot


class VictorBot(chess_bot.ChessBot):
    def __init__(self, model_location):
        super().__init__(model_location)
        self.model = load_model(model_location)

    def get_move(self, board, color):
        game = chess.Chess()
        game.load_board(board, color)
        possible_moves = game.get_moves_figs(color)
        moves = None
        max_pred = -2
        for piece, targets in possible_moves:
            for target in targets:
                game_copy = game.copy_game()
                game_copy.move_piece(piece[1][0], piece[1][1], target[0], target[1])
                coded_board = game_copy.code_board(color)
                prediction = self.model.predict(coded_board.reshape(1, 12, 8, 8), verbose=0)[0]
                if prediction > max_pred:
                    moves = (piece[1][0], piece[1][1], target[0], target[1])
                    max_pred = prediction

        return moves
