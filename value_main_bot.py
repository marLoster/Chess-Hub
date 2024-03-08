import tkinter as tk
import numpy as np
import tensorflow as tf

from keras.models import load_model

import chess

class gameController:
    def __init__(self, model):
        self.game: chess.Chess = chess.Chess()
        self.game.reset_board()
        self.select_piece = False
        self.select_move = False
        self.bot_move = False
        self.player = None
        self.move_start = None
        self.moves = None
        self.model = model

    def set_player(self, color):
        self.player = color

    def set_select_piece(self):
        self.select_piece = True
        self.select_move = False
        self.bot_move = False

    def set_select_move(self):
        self.select_piece = False
        self.select_move = True
        self.bot_move = False

    def set_bot_move(self):
        self.select_piece = False
        self.select_move = False
        self.bot_move = True

def play_white(game, buttons):
    game.player = 1
    game.set_select_piece()
    buttons[0].config(state=tk.DISABLED)
    buttons[1].config(state=tk.DISABLED)

def play_black(game, buttons):
    game.player = 0
    buttons[0].config(state=tk.DISABLED)
    buttons[1].config(state=tk.DISABLED)
    game.set_bot_move()


def bot_move(buttons, game: gameController):
    if game.bot_move:

        possible_moves = game.game.get_moves_figs(1 - game.player)
        print(possible_moves)
        moves = None
        max_pred = -2
        for piece, targets in possible_moves:
            for target in targets:
                game_copy = game.game.copy_game()
                game_copy.move_piece(piece[1][0], piece[1][1], target[0], target[1])
                coded_board = game_copy.code_board(1 - game.player)
                prediction = game.model.predict(coded_board.reshape(1, 12, 8, 8))[0]
                print(prediction)
                if prediction > max_pred:
                    moves = (piece[1][0], piece[1][1], target[0], target[1])
                    max_pred = prediction

        if not moves:
            raise Exception("Valid moves not found")

        game.game.move_piece(*moves, update_status=True)

        write_in_squares(buttons, game)
        game.set_select_piece()

def write_in_squares(buttons, game: gameController):
    for i in range(8):
        for j in range(8):
            color = "white" if game.game.board[i][j].color == 1 else "black"
            buttons[i][j].config(text=game.game.board[i][j].to_unicode(), fg=color)

def reset_buttons_color(buttons):
    for i in range(8):
        for j in range(8):
            color = "#4ae5e8" if (i + j) % 2 == 0 else "#33de33"
            buttons[i][j].config(bg=color)
def click_square(buttons, game: gameController, row: int, col: int):
    # case 1: select piece
    if game.select_piece:
        # case 1a: correct piece
        if game.game.board[row][col].color == game.player:
            game.move_start = (row, col)
            game.moves = game.game.get_moves(row, col)

            buttons[row][col].config(bg="red")
            for move in game.moves:
                buttons[move[0]][move[1]].config(bg="#c20cb0")
            game.set_select_move()
        #case 1b: not correct piece
            # do nothing
    # case 2: select move
    elif game.select_move:
        # case 2a: cancel piece
        if (row, col) == game.move_start:
            reset_buttons_color(buttons)
            game.set_select_piece()

        # case 2b: move piece
        elif (row, col) in game.moves:
            game.game.move_piece(*game.move_start, row, col, update_status=True)
            reset_buttons_color(buttons)
            write_in_squares(buttons, game)
            game.set_bot_move()

def create_board(root, game, buttons):
    board_frame = tk.Frame(root)
    board_frame.pack(side=tk.LEFT)

    for i in range(8):
        for j in range(8):
            color = "#4ae5e8" if (i + j) % 2 == 0 else "#33de33"
            buttons[i][j] = tk.Button(board_frame, bg=color, width=5, height=2, font=("Arial", 24),
                                       command=lambda i=i, j=j: click_square(buttons, game, i, j))
            buttons[i][j].grid(row=i, column=j)

    write_in_squares(buttons, game)

    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.RIGHT)

    disable_buttons = []

    white_button = tk.Button(button_frame, text="Play white", command=lambda: play_white(game, disable_buttons))
    white_button.pack()

    black_button = tk.Button(button_frame, text="Play black", command=lambda: play_black(game, disable_buttons))
    black_button.pack()

    disable_buttons.append(white_button)
    disable_buttons.append(black_button)

    hello_button = tk.Button(button_frame, text="Bot Move", command=lambda: bot_move(buttons, game))
    hello_button.pack()


def weighted_mse(y_true, y_pred):
    weights = (y_true * 62) + 1
    squared_difference = tf.math.multiply(weights, tf.square(y_true - y_pred))
    return tf.reduce_mean(squared_difference)

def main():
    root = tk.Tk()
    root.title("Chess App")
    model = load_model("value_nn_20240305181141.keras",
                       custom_objects={"weighted_mse": weighted_mse})
    game = gameController(model)
    buttons = [[None] * 8 for _ in range(8)]
    create_board(root, game, buttons)
    root.mainloop()

if __name__ == "__main__":
    main()
