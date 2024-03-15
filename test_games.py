import re
from functools import reduce
from chess import Chess
from chess_values import Color, Figure

def extract_start_square(move_str):
    if move_str.endswith('+') or move_str.endswith('#'):
        move_str = move_str[:-3]
    else:
        move_str = move_str[:-2]

    if move_str.endswith("x"):
        move_str = move_str[:-1]

    return move_str[1:]



#with open("games.pgn") as file:
#    lines = enumerate(file.readlines())

#lines = list(filter(lambda x: x[1][0] == "1", lines))

with open("games.pgn") as file:
    read_lines = file.readlines()
    lines_index = read_lines.index("<start>\n")
    lines = read_lines[lines_index:]
    print(len(lines))
    lines = enumerate(lines)


lines = list(filter(lambda x: x[1][0] == "1", lines))

for game_num, game in lines:
    moves = list(map(lambda x: x.split(), re.split(r" ?[0-9]+\. ", game)[1:]))
    moves = reduce(lambda moves_list_a, moves_list_b: moves_list_a + moves_list_b, moves)
    print(game_num, moves)
    chess = Chess()
    chess.reset_board()
    for move in moves:
        print(chess.turn)
        print(move)
        if move.startswith('{'):
            break
        curr_player = chess.turn
        piece_map = {
            'B': 'bishop',
            'N': 'knight',
            'R': 'rook',
            'Q': 'queen',
            'K': 'king',
        }
        possible_moves = chess.get_moves_figs(chess.turn)
        move = move.replace("=Q", "")
        # print(possible_moves)
        if move[0] in piece_map:
            piece = piece_map[move[0]]
            fig_location = list(filter(lambda x:  x[0][0].piece == piece, possible_moves))
            if re.match(r'^[BNRQK][a-h]?[1-8]?x?[a-h][1-8]$', move):
                target = Chess.get_cords(move[-2:])
            elif re.match(r'^[BNRQK][a-h]?[1-8]?x?[a-h][1-8][+#]$', move):
                target = Chess.get_cords(move[-3:-1])
            else:
                raise Exception(f"Unrecognised {piece} move, move: {move}, game_id: {game_num}")

            start_square = extract_start_square(move)
            print(fig_location)
            if start_square:
                if len(start_square) == 2:
                    fig_location = list(filter(lambda x: x[0][1] == chess.get_cords(start_square), fig_location))
                elif start_square.isnumeric():
                    fig_location = list(filter(lambda x: Chess.get_notation(x[0][1])[1] == start_square[0], fig_location))
                else:
                    fig_location = list(filter(lambda x: Chess.get_notation(x[0][1])[0] == start_square[0], fig_location))

            print(fig_location)
            for fig in fig_location:
                if target in fig[1]:
                    if chess.is_move_valid(*fig[0][1], *target):
                        chess.move_piece(*fig[0][1], *target, update_status=True)
                        break
                    else:
                        raise Exception(f"Validation Failed: Matching {piece} move not found, move: {move}, game_id: {game_num}")
            else:
                raise Exception(f"Matching {piece} move not found, move: {move}, game_id: {game_num}")

        elif move.startswith("O"):
            fig_location = list(filter(lambda x:  x[0][0].piece == Figure.king, possible_moves))
            if chess.turn:
                if move.count("O") == 2 and chess.get_cords("g1") in fig_location[0][1]:
                    if chess.is_move_valid(*chess.get_cords("e1"), *chess.get_cords("g1")):
                        chess.move_piece(*chess.get_cords("e1"), *chess.get_cords("g1"), update_status=True)
                    else:
                        raise Exception(f"Validation failed: Matching move not found, move: {move}, game_id: {game_num}")

                elif move.count("O") == 3 and chess.get_cords("c1") in fig_location[0][1]:
                    if chess.is_move_valid(*chess.get_cords("e1"), *chess.get_cords("c1")):
                        chess.move_piece(*chess.get_cords("e1"), *chess.get_cords("c1"), update_status=True)
                    else:
                        raise Exception(f"Validation failed: Matching move not found, move: {move}, game_id: {game_num}")
                else:
                    raise Exception(f"Matching move not found, move: {move}, game_id: {game_num}")
            else:
                if move.count("O") == 2 and chess.get_cords("g8") in fig_location[0][1]:
                    if chess.is_move_valid(*chess.get_cords("e8"), *chess.get_cords("g8")):
                        chess.move_piece(*chess.get_cords("e8"), *chess.get_cords("g8"), update_status=True)
                    else:
                        raise Exception(f"Validation failed: Matching move not found, move: {move}, game_id: {game_num}")
                elif move.count("O") == 3 and chess.get_cords("c8") in fig_location[0][1]:
                    if chess.is_move_valid(*chess.get_cords("e8"), *chess.get_cords("c8")):
                        chess.move_piece(*chess.get_cords("e8"), *chess.get_cords("c8"), update_status=True)
                    else:
                        raise Exception(f"Validation failed: Matching move not found, move: {move}, game_id: {game_num}")
                else:
                    raise Exception(f"Matching move not found, move: {move}, game_id: {game_num}")

        else:
            if re.match(r'^[a-h][1-8][+#]?$', move):
                fig_location = list(filter(lambda x: Chess.get_notation(x[0][1])[0] == move[0]
                                                     and x[0][0].piece == Figure.pawn, possible_moves))
                target = Chess.get_cords(move)
                for fig in fig_location:
                    if target in fig[1]:
                        if chess.is_move_valid(*fig[0][1], *target):
                            chess.move_piece(*fig[0][1], *target, update_status=True)
                            break
                        else:
                            raise Exception(f"Validation Failed: Matching pawn not found, move: {move}, game_id: {game_num}")
                else:
                    raise Exception(f"Matching pawn not found, move: {move}, game_id: {game_num}")

            elif re.match(r'^[a-h]x[a-h][1-8][+#]?$', move):
                fig_location = list(filter(lambda x: x[0][0].piece == Figure.pawn
                                                     and chess.get_notation(x[0][1])[0] == move[0], possible_moves))
                target = Chess.get_cords(move[-2:] if "+" not in move and "#" not in move else move[-3:-1])
                for fig in fig_location:
                    if target in fig[1]:
                        if chess.is_move_valid(*fig[0][1], *target):
                            chess.move_piece(*fig[0][1], *target, update_status=True)
                            break
                        else:
                            raise Exception(
                                f"Validation Failed: Matching pawn for diagonal move not found, move: {move}, game_id: {game_num}")
                else:
                    print(target)
                    print(fig_location)
                    raise Exception(f"Matching pawn for diagonal move not found, move: {move}, game_id: {game_num}")
            else:
                raise Exception(f'Unrecognised pawn move: {move}, game_id: {game_num}')

