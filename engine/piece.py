from engine.chess_values import Color, Figure


class Piece:

    def __init__(self, piece, color=-1, moved=False):
        self.piece = piece
        self.color = color
        self.moved = False

    def to_unicode(self):
        if self.color:
            unicodes = {Figure.king: "♔", Figure.queen: "♕", Figure.rook: "♖", Figure.bishop: "♗", Figure.knight: "♘", Figure.pawn: "♙", Figure.empty: ""}
        else:
            unicodes = {Figure.king: "♚", Figure.queen: "♛", Figure.rook: "♜", Figure.bishop: "♝", Figure.knight: "♞", Figure.pawn: "♟", Figure.empty: ""}
        return unicodes[self.piece]

    def copy(self):
        return Piece(self.piece, self.color, self.moved)
