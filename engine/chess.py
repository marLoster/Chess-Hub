from functools import reduce
import re

import numpy as np

from engine.piece import Piece
from engine.chess_values import Color, Figure


class Chess:

    def __init__(self):
        self.board = [[Piece(Figure.empty) for _ in range(8)] for _ in range(8)]
        self.en_passant = []
        self.turn = Color.white
        self.curr_piece = None
        self.status = 2

    def place_piece(self, piece, square):
        self.board[Chess.get_cords(square)[0]][Chess.get_cords(square)[1]] = piece

    def reset_board(self):

        for i in range(8):
            for j in range(8):
                self.board[i][j] = Piece(Figure.empty)

        self.place_piece(Piece(Figure.rook, Color.black), "a8")
        self.place_piece(Piece(Figure.knight, Color.black), "b8")
        self.place_piece(Piece(Figure.bishop, Color.black), "c8")
        self.place_piece(Piece(Figure.queen, Color.black), "d8")
        self.place_piece(Piece(Figure.king, Color.black), "e8")
        self.place_piece(Piece(Figure.bishop, Color.black), "f8")
        self.place_piece(Piece(Figure.knight, Color.black), "g8")
        self.place_piece(Piece(Figure.rook, Color.black), "h8")

        self.place_piece(Piece(Figure.pawn, Color.black), "a7")
        self.place_piece(Piece(Figure.pawn, Color.black), "b7")
        self.place_piece(Piece(Figure.pawn, Color.black), "c7")
        self.place_piece(Piece(Figure.pawn, Color.black), "d7")
        self.place_piece(Piece(Figure.pawn, Color.black), "e7")
        self.place_piece(Piece(Figure.pawn, Color.black), "f7")
        self.place_piece(Piece(Figure.pawn, Color.black), "g7")
        self.place_piece(Piece(Figure.pawn, Color.black), "h7")

        self.place_piece(Piece(Figure.rook, Color.white), "a1")
        self.place_piece(Piece(Figure.knight, Color.white), "b1")
        self.place_piece(Piece(Figure.bishop, Color.white), "c1")
        self.place_piece(Piece(Figure.queen, Color.white), "d1")
        self.place_piece(Piece(Figure.king, Color.white), "e1")
        self.place_piece(Piece(Figure.bishop, Color.white), "f1")
        self.place_piece(Piece(Figure.knight, Color.white), "g1")
        self.place_piece(Piece(Figure.rook, Color.white), "h1")

        self.place_piece(Piece(Figure.pawn, Color.white), "a2")
        self.place_piece(Piece(Figure.pawn, Color.white), "b2")
        self.place_piece(Piece(Figure.pawn, Color.white), "c2")
        self.place_piece(Piece(Figure.pawn, Color.white), "d2")
        self.place_piece(Piece(Figure.pawn, Color.white), "e2")
        self.place_piece(Piece(Figure.pawn, Color.white), "f2")
        self.place_piece(Piece(Figure.pawn, Color.white), "g2")
        self.place_piece(Piece(Figure.pawn, Color.white), "h2")

    def move_piece(self, row, col, new_row, new_col, update_status=False):
        if abs(col-new_col) == 2 and self.board[row][col].piece == Figure.king:
            if new_col > col:
                self.board[row][(col+new_col)//2] = self.board[row][7]
                self.board[row][7] = Piece(Figure.empty)
                self.board[row][7].moved = True
            else:
                self.board[row][(col+new_col)//2] = self.board[row][0]
                self.board[row][0] = Piece(Figure.empty)
                self.board[row][0].moved = True

        self.board[new_row][new_col] = self.board[row][col]
        self.board[row][col] = Piece(Figure.empty)
        self.board[new_row][new_col].moved = True
        if (new_row == 0 or new_row == 7) and self.board[new_row][new_col].piece == Figure.pawn:
            self.board[new_row][new_col].piece = Figure.queen
        if (self.en_passant and new_row == self.en_passant[0] and
                new_col == self.en_passant[1] and self.board[new_row][new_col].piece == Figure.pawn):
            self.board[row][new_col] = Piece(Figure.empty)
        if abs(row-new_row) == 2 and self.board[new_row][new_col].piece == Figure.pawn:
            self.en_passant = ((new_row+row) // 2, col)
        else:
            self.en_passant = False

        if update_status:

            self.turn = 1 - self.turn

            moves = map(lambda x: x[1], self.get_moves_figs(self.turn))
            combined_moves = reduce(lambda moves_list_a, moves_list_b: moves_list_a + moves_list_b, moves)
            if len(combined_moves) == 0:
                own_pieces = self.locate_pieces(self.turn)
                king = next(filter(lambda x: x[0].piece == Figure.king, own_pieces))[1]
                if king in self.get_all_moves(1 - self.turn):
                    self.status = 1 - self.turn
                else:
                    self.status = -1

    def locate_pieces(self, color):
        pieces_locations = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col].color == color:
                    pieces_locations.append((self.board[row][col], (row, col)))

        return pieces_locations

    def _straight_move(self, row, col,  check_pins, piece, king, new_row, new_col, moves):
        if new_row < 0 or new_col < 0 or new_col > 7 or new_row > 7 or \
                self.board[new_row][new_col].color == piece.color:
            return True

        if check_pins:
            game_copy = self.copy_game()
            game_copy.move_piece(row, col, new_row, new_col)
            if king in game_copy.get_all_moves(1 - piece.color):
                if self.board[new_row][new_col].color == 1 - piece.color:
                    return True
                return False

        moves.append((new_row, new_col))
        if self.board[new_row][new_col].color == 1 - piece.color:
            return True

        return False

    def _bishop_moves(self, row, col, check_pins, piece, king):
        moves = []

        for offset in range(1, 8):
            new_row = row + offset
            new_col = col + offset
            if self._straight_move(row, col, check_pins, piece, king, new_row, new_col, moves):
                break

        for offset in range(1, 8):
            new_row = row + offset
            new_col = col - offset
            if self._straight_move(row, col, check_pins, piece, king, new_row, new_col, moves):
                break

        for offset in range(1, 8):
            new_row = row - offset
            new_col = col + offset
            if self._straight_move(row, col, check_pins, piece, king, new_row, new_col, moves):
                break

        for offset in range(1, 8):
            new_row = row - offset
            new_col = col - offset
            if self._straight_move(row, col, check_pins, piece, king, new_row, new_col, moves):
                break

        return moves

    def _rook_moves(self, row, col, check_pins, piece, king):
        moves = []

        for new_row in range(row + 1, 8):
            if self._straight_move(row, col, check_pins, piece, king, new_row, col, moves):
                break

        for new_row in list(range(0, row))[::-1]:
            if self._straight_move(row, col, check_pins, piece, king, new_row, col, moves):
                break

        for new_col in range(col + 1, 8):
            if self._straight_move(row, col, check_pins, piece, king, row, new_col, moves):
                break

        for new_col in list(range(0, col))[::-1]:
            if self._straight_move(row, col, check_pins, piece, king, row, new_col, moves):
                break

        return moves

    def _pawn_king_check(self, row, col, new_row, new_col, check_pins, king, piece):
        game_copy = self.copy_game()
        game_copy.move_piece(row, col, new_row, new_col)
        return not check_pins or king not in game_copy.get_all_moves(1 - piece.color)

    def get_moves(self, row, col, check_pins=True):
        piece = self.board[row][col]
        own_pieces = self.locate_pieces(piece.color)
        other_pieces = self.locate_pieces(1 - piece.color)
        king = next(filter(lambda x: x[0].piece == Figure.king, own_pieces))[1]
        moves = []

        match piece.piece:

            case Figure.king:
                danger_points = []

                other_king = next(filter(lambda x: x[0].piece == Figure.king, other_pieces))[1]
                for offset_row in (-1, 0, 1):
                    for offset_col in (-1, 0, 1):
                        danger_points.append((other_king[0] + offset_row, other_king[1] + offset_col))

                for offset_row in (-1, 0, 1):
                    for offset_col in (-1, 0, 1):
                        if offset_col or offset_row:
                            try:
                                if row+offset_row < 0 or col+offset_col < 0 or\
                                        self.board[row+offset_row][col+offset_col].color == piece.color\
                                        or (row+offset_row, col+offset_col) in danger_points:
                                    continue
                                else:
                                    game_copy = self.copy_game()
                                    game_copy.move_piece(row, col, row+offset_row, col+offset_col)
                                    other_pieces_curr = game_copy.locate_pieces(1 - piece.color)
                                    other_pieces_without_king = list(
                                        filter(lambda fig: fig[0].piece != Figure.king,
                                               other_pieces_curr))
                                    if other_pieces_without_king:
                                        danger_points_curr = list(
                                            map(lambda fig: game_copy.get_moves(fig[1][0], fig[1][1], check_pins=False),
                                                other_pieces_without_king))
                                        danger_points_curr = reduce(
                                            lambda moves_list_a, moves_list_b: moves_list_a + moves_list_b,
                                            danger_points_curr)
                                        if (row+offset_row, col+offset_col) not in danger_points_curr:
                                            moves.append((row+offset_row, col+offset_col))
                                    else:
                                        moves.append((row + offset_row, col + offset_col))
                            except IndexError:
                                continue

                other_pieces_without_king = list(filter(lambda x: x[0].piece != Figure.king, other_pieces))
                if other_pieces_without_king:
                    other_danger_points = list(map(lambda x: self.get_moves(x[1][0],
                                                                            x[1][1],
                                                                            check_pins=False),
                                                   other_pieces_without_king))
                    other_danger_points = reduce(lambda moves_list_a, moves_list_b: moves_list_a + moves_list_b,
                                                 other_danger_points)
                    danger_points.extend(other_danger_points)

                if (row == 0 and piece.color == 0) or (row == 7 and piece.color == 1):
                    if (not self.board[row][col].moved and not self.board[row][0].moved
                            and (row, 2) not in danger_points
                            and (row, 3) not in danger_points
                            and (row, col) not in danger_points
                            and self.board[row][1].piece == Figure.empty
                            and self.board[row][2].piece == Figure.empty
                            and self.board[row][3].piece == Figure.empty):
                        moves.append((row, 2))

                    if (not self.board[row][col].moved and not self.board[row][7].moved
                            and (row, 6) not in danger_points
                            and (row, 5) not in danger_points
                            and (row, col) not in danger_points
                            and self.board[row][6].piece == Figure.empty and self.board[row][5].piece == Figure.empty):
                        moves.append((row, 6))

            case Figure.queen:

                moves.extend(self._rook_moves(row, col, check_pins, piece, king))
                moves.extend(self._bishop_moves(row, col, check_pins, piece, king))

            case Figure.rook:

                moves.extend(self._rook_moves(row, col, check_pins, piece, king))

            case Figure.bishop:

                moves.extend(self._bishop_moves(row, col, check_pins, piece, king))

            case Figure.knight:
                possible_moves = [(row+2, col+1),
                                  (row+2, col-1),
                                  (row-2, col+1),
                                  (row-2, col-1),
                                  (row+1, col+2),
                                  (row-1, col+2),
                                  (row+1, col-2),
                                  (row-1, col-2)]

                for move in possible_moves.copy():
                    if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                        possible_moves.remove(move)
                        continue

                    game_copy = self.copy_game()
                    game_copy.move_piece(row, col, move[0], move[1])
                    if (self.board[move[0]][move[1]].color == piece.color or
                            (check_pins and king in game_copy.get_all_moves(1 - piece.color))):
                        possible_moves.remove(move)
                        continue

                return possible_moves

            case Figure.pawn:

                direction = 1 if piece.color == Color.black else -1

                if self.board[row+1*direction][col].piece == Figure.empty:
                    if self._pawn_king_check(row, col, row+1*direction, col, check_pins, king, piece):
                        moves.append((row+1*direction, col))

                    try:
                        if not piece.moved and self.board[row+2*direction][col].piece == Figure.empty:
                            if self._pawn_king_check(row, col, row + 2*direction, col, check_pins, king, piece):
                                moves.append((row + 2*direction, col))

                    except IndexError:
                        pass

                try:
                    if self.board[row+1*direction][col+1].color == 1 - piece.color:
                        if self._pawn_king_check(row, col, row + 1*direction, col + 1, check_pins, king, piece):
                            moves.append((row + 1*direction, col + 1))

                except IndexError:
                    pass

                try:
                    if col > 0 and self.board[row+1*direction][col-1].color == 1 - piece.color:
                        if self._pawn_king_check(row, col, row + 1*direction, col - 1, check_pins, king, piece):
                            moves.append((row + 1*direction, col - 1))

                except IndexError:
                    pass

                if self.en_passant and self.en_passant[0] - row == 1*direction and abs(self.en_passant[1]-col) == 1\
                        and self.board[row][self.en_passant[1]].color == 1 - piece.color:
                    if self._pawn_king_check(row, col, self.en_passant[0], self.en_passant[1], check_pins, king, piece):
                        moves.append((self.en_passant[0], self.en_passant[1]))

        return moves

    def get_all_moves(self, color):
        pieces = self.locate_pieces(color)
        moves = list(map(lambda piece: self.get_moves(piece[1][0], piece[1][1], check_pins=False), pieces))
        moves = reduce(lambda moves_list_a, moves_list_b: moves_list_a+moves_list_b, moves)
        return moves

    def get_moves_figs(self, color):
        pieces = self.locate_pieces(color)
        moves = list(map(lambda piece: (piece, self.get_moves(piece[1][0], piece[1][1])), pieces))
        return moves

    def copy_game(self):
        new_game = Chess()

        for row in range(8):
            for col in range(8):
                new_game.board[row][col] = self.board[row][col].copy()

        new_game.en_passant = self.en_passant
        new_game.turn = self.turn
        new_game.curr_piece = self.curr_piece
        new_game.status = self.status

        return new_game

    @staticmethod
    def get_cords(square):
        row = 8 - int(square[1])
        col = ord(square.lower()[0]) - ord('a')
        return row, col

    @staticmethod
    def get_notation(square):
        num = str(8 - square[0])
        letter = chr(ord('a') + square[1])
        return letter + num

    def is_move_valid(self, row, col, new_row, new_col):
        game_copy = self.copy_game()
        piece = game_copy.board[row][col]

        if (piece.piece == Figure.empty
                or self.turn == game_copy.board[new_row][new_col].color
                or game_copy.board[new_row][new_col].piece == Figure.king
                or self.turn != game_copy.board[row][col].color):
            return False

        if (new_row, new_col) in game_copy.get_moves(row, col, check_pins=False):
            game_copy.move_piece(row, col, new_row, new_col)
            own_pieces = game_copy.locate_pieces(piece.color)
            king = next(filter(lambda x: x[0].piece == Figure.king, own_pieces))[1]
            return king not in game_copy.get_all_moves(1 - piece.color)

        return False

    def code_board(self, turn=None):
        turn = turn if turn else self.turn
        res = np.zeros((12, 8, 8))

        turn_dict = {
            turn: 0,
            1 - turn: 6
        }
        figure_type_dict = {
            Figure.king: 0,
            Figure.queen: 1,
            Figure.rook: 2,
            Figure.bishop: 3,
            Figure.knight: 4,
            Figure.pawn: 5
        }

        for i, _ in enumerate(self.board):
            for j, _ in enumerate(self.board[i]):
                current_piece = self.board[i][j]
                if current_piece.piece != Figure.empty:
                    res[turn_dict[current_piece.color] + figure_type_dict[current_piece.piece]][i][j] = 1

        return res

    def load_board(self, arr, turn):
        figure_type_dict = {
            0: Figure.king,
            1: Figure.queen,
            2: Figure.rook,
            3: Figure.bishop,
            4: Figure.knight,
            5: Figure.pawn
        }

        for i, _ in enumerate(self.board):
            for j, _ in enumerate(self.board[i]):
                self.board[i][j] = Piece(Figure.empty)

        locations = np.transpose(np.nonzero(arr))
        for piece_type, row, col in locations:
            curr_piece = Piece(figure_type_dict[piece_type % 6], turn if piece_type//6 == 0 else 1 - turn)
            self.board[row][col] = curr_piece

        self.turn = turn

    @staticmethod
    def code_move(row, col, new_row, new_col):
        res = np.zeros((2, 8, 8))
        res[0][row][col] = 1
        res[1][new_row][new_col] = 1

        return res

    def move_notation_to_digits(self, move):
        def extract_start_square(move_str):
            if move_str.endswith('+') or move_str.endswith('#'):
                move_str = move_str[:-3]
            else:
                move_str = move_str[:-2]

            if move_str.endswith("x"):
                move_str = move_str[:-1]

            return move_str[1:]

        piece_map = {
            'B': 'bishop',
            'N': 'knight',
            'R': 'rook',
            'Q': 'queen',
            'K': 'king',
        }
        possible_moves = self.locate_pieces(self.turn)
        move = move.replace("=Q", "")
        if move[0] in piece_map:
            piece = piece_map[move[0]]
            fig_location = list(filter(lambda x: x[0].piece == piece, possible_moves))
            if re.match(r'^[BNRQK][a-h]?[1-8]?x?[a-h][1-8]$', move):
                target = Chess.get_cords(move[-2:])
            elif re.match(r'^[BNRQK][a-h]?[1-8]?x?[a-h][1-8][+#]$', move):
                target = Chess.get_cords(move[-3:-1])
            else:
                raise Exception(f"Unrecognised {piece} move, move: {move}")

            start_square = extract_start_square(move)

            if start_square:
                if len(start_square) == 2:
                    fig_location = list(filter(lambda x: x[1] == self.get_cords(start_square), fig_location))
                elif start_square.isnumeric():
                    fig_location = list(
                        filter(lambda x: Chess.get_notation(x[1])[1] == start_square[0], fig_location))
                else:
                    fig_location = list(
                        filter(lambda x: Chess.get_notation(x[1])[0] == start_square[0], fig_location))

            for fig in fig_location:
                if target in self.get_moves(*fig[1], check_pins=True):
                    return *fig[1], *target
            else:
                raise Exception(f"Matching {piece} move not found, move: {move}")

        elif move.startswith("O"):
            fig_location = list(filter(lambda x: x[0].piece == Figure.king, possible_moves))
            if self.turn:
                if move.count("O") == 2 and self.get_cords("g1") in self.get_moves(*fig_location[0][1],
                                                                                   check_pins=True):
                    return *self.get_cords("e1"), *self.get_cords("g1")

                elif move.count("O") == 3 and self.get_cords("c1") in self.get_moves(*fig_location[0][1],
                                                                                     check_pins=True):
                    return *self.get_cords("e1"), *self.get_cords("c1")
                else:
                    raise Exception(f"Matching move not found, move: {move}")
            else:
                if move.count("O") == 2 and self.get_cords("g8") in self.get_moves(*fig_location[0][1],
                                                                                   check_pins=True):
                    return *self.get_cords("e8"), *self.get_cords("g8")
                elif move.count("O") == 3 and self.get_cords("c8") in self.get_moves(*fig_location[0][1],
                                                                                     check_pins=True):
                    return *self.get_cords("e8"), *self.get_cords("c8")
                else:
                    raise Exception(f"Matching move not found, move: {move}")

        else:
            if re.match(r'^[a-h][1-8][+#]?$', move):
                fig_location = list(
                    filter(lambda x: Chess.get_notation(x[1])[0] == move[0] and x[0].piece == Figure.pawn,
                           possible_moves))
                target = Chess.get_cords(move)
                for fig in fig_location:
                    if target in self.get_moves(*fig[1], check_pins=True):
                        return *fig[1], *target
                else:
                    raise Exception(f"Matching pawn not found, move: {move}")

            elif re.match(r'^[a-h]x[a-h][1-8][+#]?$', move):
                fig_location = list(
                    filter(lambda x: x[0].piece == Figure.pawn and self.get_notation(x[1])[0] == move[0],
                           possible_moves))
                target = Chess.get_cords(move[-2:] if "+" not in move and "#" not in move else move[-3:-1])
                for fig in fig_location:
                    if target in self.get_moves(*fig[1], check_pins=True):
                        return *fig[1], *target
                else:
                    raise Exception(f"Matching pawn for diagonal move not found, move: {move}")
            else:
                raise Exception(f'Unrecognised pawn move: {move}')

    def print_board(self):
        for row in self.board:
            print(*map(lambda x: x.to_unicode(), row))
