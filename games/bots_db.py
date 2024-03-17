import random
from datetime import datetime

import numpy as np
import tensorflow as tf

from keras.models import load_model

import engine.chess as chess
from engine.chess_values import Color
from database import connection
from AI.board_models.model_Rachel import RachelBot
from AI.board_models.model_Max import MaxBot
from AI.board_models.model_Henry import HenryBot
from AI.value_models.model_Victor import VictorBot

bot_1 = VictorBot("../AI/value_models/models/value_nn_20240305181141.keras")
bot_1_id = 5

bot_1 = HenryBot("../AI/board_models/models/20240301220159.keras")
bot_1_id = 1
bot_2 = MaxBot("../AI/board_models/models/20240301220159.keras")
bot_2_id = 2

white = bot_1_id if random.random() < 0.5 else bot_2_id
black = bot_1_id if white == bot_2_id else bot_2_id

game = chess.Chess()
game.reset_board()
bot1_color = Color.white if white == bot_1_id else Color.black
bot2_color = 1 - bot1_color
current_player = white
move = 0

while game.status == 2:
    if move % 20 == 0:
        print(move)
        game.print_board()
    if current_player == bot_1_id:
        current_move = bot_1.get_move(game.code_board(bot1_color), bot1_color)
        game.move_piece(*current_move, update_status=True)
    else:
        current_move = bot_2.get_move(game.code_board(bot2_color), bot2_color)
        game.move_piece(*current_move, update_status=True)
    move += 1

    if move == 40:
        game.status = -1
        break

    current_player = white if current_player == black else black

formatted_datetime = datetime.now().strftime("%Y%m%d%H%M")
con = connection.DBconnection()
con.execute("INSERT INTO games (white, black, winner, date) VALUES (%s, %s, %s, %s)",
            (white, black, game.status, formatted_datetime))
