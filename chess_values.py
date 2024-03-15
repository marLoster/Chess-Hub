from enum import IntEnum, StrEnum


class Color(IntEnum):
    white = 1
    black = 0


class Figure(StrEnum):
    king = "king"
    queen = "queen"
    rook = "rook"
    bishop = "bishop"
    knight = "knight"
    pawn = "pawn"
    empty = "empty"
