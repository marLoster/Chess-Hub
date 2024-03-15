import tkinter as tk

from chess import Chess
from chess_values import Color, Figure


# Initialize the main application window
root = tk.Tk()
root.title("Chessboard")

# Create a canvas to display the chessboard
canvas = tk.Canvas(root, width=400, height=400)
canvas.grid(row=0, column=0, padx=10, pady=10)

# Create a frame for buttons and dropdown menus
control_frame = tk.Frame(root)
control_frame.grid(row=0, column=1, padx=10, pady=10)

# Define the chessboard colors
colors = ["#0bb38b", "#327fe3"]

def draw_board():
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            canvas.create_rectangle(
                col * 50,
                row * 50,
                (col + 1) * 50,
                (row + 1) * 50,
                fill=color,
            )


# Function to place a chess piece.py
def place_piece(piece, row, col, color):
    canvas.create_text(
        col * 50 + 25,
        row * 50 + 25,
        text=piece,
        font=("Helvetica", 24),
        fill=color,
    )


def draw_game(game: Chess):
    draw_board()
    for row in range(8):
        for col in range(8):
            if game.board[row][col].piece != Figure.empty:
                place_piece(game.board[row][col].to_unicode(),
                            row,
                            col,
                            "white" if game.board[row][col].color else "black")


piece_dropdown = tk.StringVar(root)
piece_dropdown.set("♙")  # Default piece.py
piece_menu = tk.OptionMenu(control_frame, piece_dropdown, "♙", "♘")
piece_menu.grid(row=0, column=0, padx=5, pady=5)

move_dropdown = tk.StringVar(root)
move_dropdown.set("...")  # Default move
move_menu = tk.OptionMenu(control_frame, move_dropdown, "...")
move_menu.grid(row=2, column=0, padx=5, pady=5)

status_label = tk.Label(root, text="Game is ready")
status_label.grid(row=0, column=3, padx=5, pady=5)


# Function to handle the "Place Piece" button click
def fun_piece_button():
    piece = piece_dropdown.get()
    row, col = Chess.get_cords(piece.split()[1])
    game.curr_piece = (row, col)
    moves = game.get_moves(row, col)
    move_menu = tk.OptionMenu(control_frame, move_dropdown, *list(map(lambda x: Chess.get_notation(x), moves)))
    move_menu.grid(row=2, column=0, padx=5, pady=5)
    piece_button["state"] = "disabled"
    piece_menu["state"] = "disabled"
    move_button["state"] = "normal"
    move_menu["state"] = "normal"

# Function to handle the "Move Piece" button click
def fun_move_button():
    move = move_dropdown.get()
    game.move_piece(*game.curr_piece, *Chess.get_cords(move), update_status=True)
    piece_button["state"] = "normal"
    move_button["state"] = "disabled"
    move_menu["state"] = "disabled"
    # game.turn = 1 - game.turn
    draw_game(game)
    if isinstance(game.status, str):
        print("str", game.status)
        status_label.config( text=f"Player {game.turn} plays now")
        moves_figs = list(filter(lambda x: len(x[1]), game.get_moves_figs(game.turn)))
        figs = list(map(lambda x: x[0][0].to_unicode() + " " + Chess.get_notation(x[0][1]), moves_figs))
        print(figs)
        piece_menu = tk.OptionMenu(control_frame, piece_dropdown, *figs)
        piece_menu.grid(row=0, column=0, padx=5, pady=5)
        piece_menu["state"] = "normal"
    else:
        print("non str", game.status)
        if game.status == -1:
            status_label.config( text=f"Draw")
        else:
            status_label.config(text=f"Player {game.status} wins")

def clear_board():
    piece_button["state"] = "disabled"
    piece_menu["state"] = "disabled"


# Create buttons
piece_button = tk.Button(control_frame, text="Place Piece", command=fun_piece_button)
move_button = tk.Button(control_frame, text="Move Piece", command=fun_move_button)
clear_button = tk.Button(control_frame, text="Clear Board", command=clear_board)

piece_button.grid(row=1, column=0, padx=5, pady=5)
move_button.grid(row=3, column=0, padx=5, pady=5)
clear_button.grid(row=4, column=0, padx=5, pady=5)

game = Chess()
game.reset_board()
draw_game(game)

moves_figs = list(filter(lambda x: len(x[1]), game.get_moves_figs(game.turn)))
figs = list(map(lambda x: x[0][0].to_unicode() + " " + Chess.get_notation(x[0][1]), moves_figs))
piece_menu = tk.OptionMenu(control_frame, piece_dropdown, *figs)
piece_menu.grid(row=0, column=0, padx=5, pady=5)

# Start the main loop
root.mainloop()
