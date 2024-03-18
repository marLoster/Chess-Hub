import numpy as np
import tensorflow as tf

from keras.models import load_model

import engine.chess as chess
from AI.board_models.model_Henry import HenryBot
from AI.board_models.model_Max import MaxBot
from AI.board_models.model_Rachel import RachelBot
from engine.chess_values import Color


def main():
    bot_1 = RachelBot("../AI/board_models/models/20240301220159.keras")
    bot_1_id = 1
    bot_2 = RachelBot("../AI/board_models/models/20240301220159.keras")
    bot_2_id = 2

    current_white = bot_1_id
    bot1_wins = 0
    bot2_wins = 0
    draw = 0

    while True:
        print(bot1_wins, draw, bot2_wins)
        game = chess.Chess()
        game.reset_board()
        current_player = current_white
        bot1_color = Color.white if current_white == bot_1_id else Color.black
        bot2_color = 1 - bot1_color
        move = 0
        while game.status == 2:
            if move % 20 == 0:
                print(move, bot1_wins, draw, bot2_wins)
                game.print_board()
            if current_player == bot_1_id:
                current_move = bot_1.get_move(game.code_board(bot1_color), bot1_color)
                game.move_piece(*current_move, update_status=True)
                current_player = bot_2_id
            else:
                current_move = bot_2.get_move(game.code_board(bot2_color), bot2_color)
                game.move_piece(*current_move, update_status=True)
                current_player = bot_1_id
            move += 1

            if move == 250:
                game.status = -1
                break

        bot1_wins += 1 * (bot1_color == game.status)
        bot2_wins += 1 * (bot2_color == game.status)
        if game.status == -1:
            draw += 1

        current_white = bot_1_id if current_white == bot_2_id else bot_2_id


if __name__ == "__main__":
    main()
