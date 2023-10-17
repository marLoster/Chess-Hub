class Piece:

    def __init__(self, piece, color=-1, moved=False):
        self.piece = piece
        self.color = color
        self.moved = False

    def to_unicode(self):
        if self.color:
            unicodes = {"king": "♚", "queen": "♛", "rook": "♜", "bishop": "♝", "knight": "♞", "pawn": "♟"}
        else:
            unicodes = {"king": "♔", "queen": "♕", "rook": "♖", "bishop": "♗", "knight": "♘", "pawn": "♙"}
        return unicodes[self.piece]

    def copy(self):
        return Piece(self.piece, self.color, self.moved)
