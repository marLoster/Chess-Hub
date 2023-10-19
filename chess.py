from functools import reduce

from piece import Piece


class Chess:

    def __init__(self):
        self.board = [[Piece("empty") for _ in range(8)] for _ in range(8)]
        self.en_passant = []
        self.turn = 1
        self.curr_piece = None
        self.status = "going"

    def place_piece(self, piece, square):
        self.board[Chess.get_cords(square)[0]][Chess.get_cords(square)[1]] = piece

    def reset_board(self):
        self.place_piece(Piece("rook", 0), "a8")
        self.place_piece(Piece("knight", 0), "b8")
        self.place_piece(Piece("bishop", 0), "c8")
        self.place_piece(Piece("queen", 0), "d8")
        self.place_piece(Piece("king", 0), "e8")
        self.place_piece(Piece("bishop", 0), "f8")
        self.place_piece(Piece("knight", 0), "g8")
        self.place_piece(Piece("rook", 0), "h8")

        self.place_piece(Piece("pawn", 0), "a7")
        self.place_piece(Piece("pawn", 0), "b7")
        self.place_piece(Piece("pawn", 0), "c7")
        self.place_piece(Piece("pawn", 0), "d7")
        self.place_piece(Piece("pawn", 0), "e7")
        self.place_piece(Piece("pawn", 0), "f7")
        self.place_piece(Piece("pawn", 0), "g7")
        self.place_piece(Piece("pawn", 0), "h7")

        self.place_piece(Piece("rook", 1), "a1")
        self.place_piece(Piece("knight", 1), "b1")
        self.place_piece(Piece("bishop", 1), "c1")
        self.place_piece(Piece("queen", 1), "d1")
        self.place_piece(Piece("king", 1), "e1")
        self.place_piece(Piece("bishop", 1), "f1")
        self.place_piece(Piece("knight", 1), "g1")
        self.place_piece(Piece("rook", 1), "h1")

        self.place_piece(Piece("pawn", 1), "a2")
        self.place_piece(Piece("pawn", 1), "b2")
        self.place_piece(Piece("pawn", 1), "c2")
        self.place_piece(Piece("pawn", 1), "d2")
        self.place_piece(Piece("pawn", 1), "e2")
        self.place_piece(Piece("pawn", 1), "f2")
        self.place_piece(Piece("pawn", 1), "g2")
        self.place_piece(Piece("pawn", 1), "h2")

    def move_piece(self, row, col, new_row, new_col, update_status=False):
        #print(f"attempted move: {new_row}, {new_col}")
        if abs(col-new_col) == 2 and self.board[row][col].piece == "king":
            if new_col > col:
                self.board[row][(col+new_col)//2] = self.board[row][7]
                self.board[row][7] = Piece("empty")
                self.board[row][7].moved = True
            else:
                self.board[row][(col+new_col)//2] = self.board[row][0]
                self.board[row][0] = Piece("empty")
                self.board[row][0].moved = True

        self.board[new_row][new_col] = self.board[row][col]
        self.board[row][col] = Piece("empty")
        self.board[new_row][new_col].moved = True
        if (new_row == 0 or new_row == 7) and self.board[new_row][new_col].piece == "pawn":
            self.board[new_row][new_col].piece = "queen"
        if (self.en_passant and new_row == self.en_passant[0] and
                new_col == self.en_passant[1] and self.board[new_row][new_col].piece == "pawn"):
            self.board[row][new_col] = Piece("empty")
        if abs(row-new_row) == 2 and self.board[new_row][new_col].piece=="pawn":
            self.en_passant = ((new_row+row)//2, col)
        else:
            self.en_passant = False

        if update_status:

            self.turn = 1 - self.turn

            print(self.get_moves_figs(self.turn))
            moves = map(lambda x: x[1], self.get_moves_figs(self.turn))
            combined_moves = reduce(lambda moves_list_a, moves_list_b: moves_list_a + moves_list_b, moves)
            if len(combined_moves) == 0:
                own_pieces = self.locate_pieces(self.turn)
                king = next(filter(lambda x: x[0].piece == "king", own_pieces))[1]
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

    def get_moves(self, row, col, check_pins=True):
        piece = self.board[row][col]
        own_pieces = self.locate_pieces(piece.color)
        other_pieces = self.locate_pieces(1 - piece.color)
        king = next(filter(lambda x: x[0].piece == "king", own_pieces))[1]
        moves = []

        #print(f"{'' if check_pins else '    '}getting moves for {piece.piece} on ({row},{col})")

        match piece.piece:

            case "king":
                other_pieces_without_king = list(filter(lambda piece: piece[0].piece != "king", other_pieces))
                danger_points = list(map(lambda piece: self.get_moves(piece[1][0], piece[1][1], check_pins=False), other_pieces_without_king))
                danger_points = reduce(lambda moves_list_a, moves_list_b: moves_list_a + moves_list_b, danger_points)

                other_king = next(filter(lambda x: x[0].piece == "king", other_pieces))[1]
                for offset_row in (-1, 0, 1):
                    for offset_col in (-1, 0, 1):
                        danger_points.append((other_king[0] + offset_row, other_king[1] + offset_col))

                for offset_row in (-1, 0, 1):
                    for offset_col in (-1, 0, 1):
                        #print(f'checking {offset_row}, {offset_col}')
                        if offset_col or offset_row:
                            #print('actual move')
                            try:
                                if (row+offset_row < 0 or col+offset_col < 0 or
                                        self.board[row+offset_row][col+offset_col].color == piece.color):
                                    #or (row+offset_row, col+offset_col) in danger_points):
                                    #print('failed first check')
                                    continue
                                else:
                                    game_copy = self.copy_game()
                                    game_copy.move_piece(row, col, row+offset_row, col+offset_col)
                                    other_pieces_curr = game_copy.locate_pieces(1 - piece.color)
                                    other_pieces_without_king = list(
                                        filter(lambda fig: fig[0].piece != "king",
                                               other_pieces_curr))
                                    danger_points_curr = list(
                                        map(lambda fig: game_copy.get_moves(fig[1][0], fig[1][1], check_pins=False),
                                            other_pieces_without_king))
                                    danger_points_curr = reduce(
                                        lambda moves_list_a, moves_list_b: moves_list_a + moves_list_b,
                                        danger_points_curr)
                                   # print(danger_points_curr)
                                    if (row+offset_row, col+offset_col) not in danger_points_curr:
                                        moves.append((row+offset_row, col+offset_col))
                                    #print('move puts king in danger')
                            except IndexError:
                                #print('index error')
                                continue

                if (row == 0 and piece.color == 0) or (row == 7 and piece.color == 1):
                    if not self.board[row][col].moved and not self.board[row][0].moved\
                        and (row, 1) not in danger_points and (row, 2) not in danger_points and (row, 3) not in danger_points\
                        and (row,col) not in danger_points and self.board[row][1].piece == "empty"\
                        and self.board[row][2].piece == "empty" and self.board[row][3].piece == "empty":
                        moves.append((row, 2))

                    if not self.board[row][col].moved and not self.board[row][7].moved\
                        and (row, 6) not in danger_points and (row, 5) not in danger_points and (row, col) not in danger_points\
                        and self.board[row][6].piece == "empty" and self.board[row][5].piece == "empty":
                        moves.append((row, 6))


            case "queen":

                # horizontal and vertical
                for new_row in range(row+1, 8):
                    if self.board[new_row][col].color == piece.color:
                        break

                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, new_row, col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((new_row, col))
                    if self.board[new_row][col].color == 1 - piece.color:
                        break

                for new_row in list(range(0, row))[::-1]:
                    if self.board[new_row][col].color == piece.color:
                        break

                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, new_row, col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((new_row, col))
                    if self.board[new_row][col].color == 1 - piece.color:
                        break

                for new_col in range(col + 1, 8):
                    if self.board[row][new_col].color == piece.color:
                        break

                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, row, new_col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((row, new_col))
                    if self.board[row][new_col].color == 1 - piece.color:
                        break

                for new_col in list(range(0, col))[::-1]:
                    if self.board[row][new_col].color == piece.color:
                        break

                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, row, new_col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((row, new_col))
                    if self.board[row][new_col].color == 1 - piece.color:
                        break

                # diagonal
                for offset in range(1, 8):
                    new_row = row + offset
                    new_col = col + offset


                    if new_row < 0 or new_col < 0 or new_col > 7 or new_row > 7 or\
                            self.board[new_row][new_col].color == piece.color:
                        break


                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, new_row, new_col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((new_row, new_col))
                    if self.board[new_row][new_col].color == 1 - piece.color:
                        break

                for offset in range(1, 8):
                    new_row = row + offset
                    new_col = col - offset

                    if new_row < 0 or new_col < 0 or new_col > 7 or new_row > 7 or\
                            self.board[new_row][new_col].color == piece.color:
                        break


                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, new_row, new_col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((new_row, new_col))
                    if self.board[new_row][new_col].color == 1 - piece.color:
                        break

                for offset in range(1, 8):
                    new_row = row - offset
                    new_col = col + offset

                    if new_row < 0 or new_col < 0 or new_col > 7 or new_row > 7 or\
                            self.board[new_row][new_col].color == piece.color:
                        break


                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, new_row, new_col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((new_row, new_col))
                    if self.board[new_row][new_col].color == 1 - piece.color:
                        break

                for offset in range(1, 8):
                    new_row = row - offset
                    new_col = col - offset

                    if new_row < 0 or new_col < 0 or new_col > 7 or new_row > 7 or\
                            self.board[new_row][new_col].color == piece.color:
                        break


                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, new_row, new_col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((new_row, new_col))
                    if self.board[new_row][new_col].color == 1 - piece.color:
                        break

            case "rook":

                for new_row in range(row + 1, 8):
                    if self.board[new_row][col].color == piece.color:
                        break

                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, new_row, col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((new_row, col))
                    if self.board[new_row][col].color == 1 - piece.color:
                        break

                for new_row in list(range(0, row))[::-1]:
                    if self.board[new_row][col].color == piece.color:
                        break

                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, new_row, col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((new_row, col))
                    if self.board[new_row][col].color == 1 - piece.color:
                        break

                for new_col in range(col + 1, 8):
                    if self.board[row][new_col].color == piece.color:
                        break

                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, row, new_col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((row, new_col))
                    if self.board[row][new_col].color == 1 - piece.color:
                        break

                for new_col in list(range(0, col))[::-1]:
                    if self.board[row][new_col].color == piece.color:
                        break

                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, row, new_col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((row, new_col))
                    if self.board[row][new_col].color == 1 - piece.color:
                        break

            case "bishop":
                for offset in range(1, 8):
                    new_row = row + offset
                    new_col = col + offset

                    if new_row < 0 or new_col < 0 or new_col > 7 or new_row > 7 or\
                            self.board[new_row][new_col].color == piece.color:
                        break


                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, new_row, new_col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((new_row, new_col))
                    if self.board[new_row][new_col].color == 1 - piece.color:
                        break

                for offset in range(1, 8):
                    new_row = row + offset
                    new_col = col - offset

                    if new_row < 0 or new_col < 0 or new_col > 7 or new_row > 7 or\
                            self.board[new_row][new_col].color == piece.color:
                        break


                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, new_row, new_col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((new_row, new_col))
                    if self.board[new_row][new_col].color == 1 - piece.color:
                        break

                for offset in range(1, 8):
                    new_row = row - offset
                    new_col = col + offset

                    if new_row < 0 or new_col < 0 or new_col > 7 or new_row > 7 or\
                            self.board[new_row][new_col].color == piece.color:
                        break


                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, new_row, new_col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((new_row, new_col))
                    if self.board[new_row][new_col].color == 1 - piece.color:
                        break

                for offset in range(1, 8):
                    new_row = row - offset
                    new_col = col - offset

                    if new_row < 0 or new_col < 0 or new_col > 7 or new_row > 7 or\
                            self.board[new_row][new_col].color == piece.color:
                        break


                    if check_pins:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, new_row, new_col)
                        if king in game_copy.get_all_moves(1 - piece.color):
                            break

                    moves.append((new_row, new_col))
                    if self.board[new_row][new_col].color == 1 - piece.color:
                        break
            case "knight":
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

            case "pawn":
                #print(row, col)
                if not piece.color:

                    if self.board[row+1][col].piece == "empty":
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, row+1, col)
                        if (not check_pins or king not in game_copy.get_all_moves(1 - piece.color)):
                            moves.append((row+1, col))

                        try:
                            if not piece.moved and self.board[row+2][col].piece == "empty":
                                game_copy = self.copy_game()
                                game_copy.move_piece(row, col, row + 2, col)
                                if (not check_pins or king not in game_copy.get_all_moves(1 - piece.color)):
                                    moves.append((row + 2, col))

                        except IndexError:
                            pass

                    try:
                        if self.board[row+1][col+1].color == 1 - piece.color:
                            game_copy = self.copy_game()
                            game_copy.move_piece(row, col, row + 1, col+1)
                            if (not check_pins or king not in game_copy.get_all_moves(1 - piece.color)):
                                moves.append((row + 1, col + 1))

                    except IndexError:
                        pass

                    try:
                        if self.board[row+1][col-1].color == 1 - piece.color:
                            game_copy = self.copy_game()
                            game_copy.move_piece(row, col, row+1, col-1)
                            if (not check_pins or king not in game_copy.get_all_moves(1 - piece.color)):
                                moves.append((row + 1, col - 1))

                    except IndexError:
                        pass

                    if self.en_passant and self.en_passant[0] - row == 1 and abs(self.en_passant[1]-col) == 1:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, self.en_passant[0], self.en_passant[1])
                        if (not check_pins or king not in game_copy.get_all_moves(1 - piece.color)):
                            moves.append((self.en_passant[0], self.en_passant[1]))
                else:

                    if self.board[row - 1][col].piece == "empty":
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, row - 1, col)
                        if (not check_pins or king not in game_copy.get_all_moves(1 - piece.color)):
                            moves.append((row - 1, col))

                        try:
                            if not piece.moved and self.board[row - 2][col].piece == "empty":
                                game_copy = self.copy_game()
                                game_copy.move_piece(row, col, row - 2, col)
                                if (not check_pins or king not in game_copy.get_all_moves(1 - piece.color)):
                                    moves.append((row - 2, col))
                        except IndexError:
                            pass

                    try:
                        if self.board[row - 1][col + 1].color == 1 - piece.color:
                            game_copy = self.copy_game()
                            game_copy.move_piece(row, col, row - 1, col + 1)
                            if (not check_pins or king not in game_copy.get_all_moves(1 - piece.color)):
                                moves.append((row - 1, col + 1))

                    except IndexError:
                        pass

                    try:
                        if self.board[row - 1][col - 1].color == 1 - piece.color:
                            game_copy = self.copy_game()
                            game_copy.move_piece(row, col, row - 1, col - 1)
                            if (not check_pins or king not in game_copy.get_all_moves(1 - piece.color)):
                                moves.append((row - 1, col - 1))

                    except IndexError:
                        pass

                    if self.en_passant and self.en_passant[0] - row == -1 and abs(self.en_passant[1] - col) == 1:
                        game_copy = self.copy_game()
                        game_copy.move_piece(row, col, self.en_passant[0], self.en_passant[1])
                        if (not check_pins or king not in game_copy.get_all_moves(1 - piece.color)):
                            moves.append((self.en_passant[0], self.en_passant[1]))
        return moves

    def get_all_moves(self, color):
        pieces = self.locate_pieces(color)
        moves = list(map(lambda piece: self.get_moves(piece[1][0], piece[1][1], check_pins=False), pieces))
        #print(moves)
        moves = reduce(lambda moves_list_a, moves_list_b: moves_list_a+moves_list_b, moves)
        return moves

    def get_moves_figs(self, color):
        #print(f'getting all the moves for color: {color}')
        pieces = self.locate_pieces(color)
        #print(f'player {color} locations: {pieces}')
        moves = list(map(lambda piece: (piece, self.get_moves(piece[1][0], piece[1][1])), pieces))
        return moves

    def copy_game(self):
        new_game = Chess()

        for row in range(8):
            for col in range(8):
                new_game.board[row][col] = self.board[row][col].copy()

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