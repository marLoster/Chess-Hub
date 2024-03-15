import random

from keras.models import load_model

import engine.chess as chess
import engine.chess_bot as chess_bot


class RachelBot(chess_bot.ChessBot):
    def __init__(self, model_location):
        super().__init__(model_location)
        self.model = load_model(model_location)

    def get_move(self, board, color):
        game = chess.Chess()
        game.load_board(board, color)
        possible_moves = game.get_moves_figs(color)
        possible_moves = list(filter(lambda x: x[1], possible_moves))
        piece = 0 if len(possible_moves) == 1 else random.randint(0, len(possible_moves)-1)
        print(possible_moves[piece])
        move = 0 if len(possible_moves[piece][1]) == 1 else random.randint(0, len(possible_moves[piece][1])-1)
        print(move)

        return (possible_moves[piece][0][1][0],
                possible_moves[piece][0][1][1],
                possible_moves[piece][1][move][0],
                possible_moves[piece][1][move][1])
