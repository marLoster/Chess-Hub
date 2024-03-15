from enum import IntEnum, Enum


class Color(IntEnum):
    white = 1
    black = 0

    def other(self):
        return Color.black if self == Color.white else Color.white


class Figure(str, Enum):
    king = "king"
    queen = "queen"
    rook = "rook"
    bishop = "bishop"
    knight = "knight"
    pawn = "pawn"
    empty = "empty"
