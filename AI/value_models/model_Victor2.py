import random

from keras.models import load_model

import engine.chess as chess
import engine.chess_bot as chess_bot
from engine.chess_values import Color, Figure


class VictorBot2(chess_bot.ChessBot):
    def __init__(self, model_location):
        super().__init__(model_location)
        self.model = load_model(model_location)

    def get_move(self, board, color):
        game = chess.Chess()
        game.load_board(board, color)
        possible_moves = game.get_moves_figs(color)
        moves = None
        max_pred = -2
        moves_check = None
        max_pred_check = -2
        for piece, targets in possible_moves:
            for target in targets:
                game_copy = game.copy_game()
                game_copy.move_piece(piece[1][0], piece[1][1], target[0], target[1], update_status=True)
                if game_copy.status == color:
                    return piece[1][0], piece[1][1], target[0], target[1]
                coded_board = game_copy.code_board(color)
                prediction = self.model.predict(coded_board.reshape(1, 12, 8, 8), verbose=0)[0]
                opponent_pieces = game_copy.locate_pieces(1 - color)
                king = next(filter(lambda x: x[0].piece == Figure.king, opponent_pieces))[1]

                if king in game_copy.get_all_moves(color) and prediction > max_pred_check:
                    moves_check = (piece[1][0], piece[1][1], target[0], target[1])
                    max_pred_check = prediction

                if prediction > max_pred:
                    moves = (piece[1][0], piece[1][1], target[0], target[1])
                    max_pred = prediction

        if moves_check is None:
            return moves

        return moves_check if random.random() < 0.9 else moves
