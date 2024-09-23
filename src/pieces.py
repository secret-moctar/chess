from src.settings import *
from src.resource_manager import res_manager


class Piece:
    def __init__(self, fen):
        self.fen = fen
        self.img = res_manager.get_resource(self.fen)
        self.all_moves = []
        self.all_legal_moves = []

    def get_moves(self):
        self.all_moves = [4, 5, 6, 8]

    def get_type(self):
        if self.fen.lower() == self.fen: return BL
        else: return WH

class Slider(Piece):
    def __init__(self, fen):
        super().__init__(fen)


class King(Slider):
    def __init__(self, fen):
        super().__init__(fen)


class Queen(Slider):
    def __init__(self, fen):
        super().__init__(fen)


class Bishop(Slider):
    def __init__(self, fen):
        super().__init__(fen)


class Rook(Slider):
    def __init__(self, fen):
        super().__init__(fen)


class Knight(Piece):
    def __init__(self, fen):
        super().__init__(fen)


class Pawn(Piece):
    def __init__(self, fen):
        super().__init__(fen)
