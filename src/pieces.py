from src.settings import *
from src.resource_manager import res_manager


class Piece:
    def __init__(self, fen):
        self.fen = fen
        self.img = res_manager.get_resource(self.fen)
        self.all_moves = []
        self.all_legal_moves = []
        self.dirs = {}

    def apply_threat(self, threat):
        for sqaure in self.all_moves:
            threat[sqaure] += 1

    def get_moves(self, board, pos):
        return []

    def is_friend(self, other):
        return self.get_type() == other.get_type()

    def get_type(self):
        if self.fen.lower() == self.fen: return BL
        else: return WH

class Slider(Piece):
    def __init__(self, fen):
        super().__init__(fen)

    def get_moves(self, board, pos):
        current = board.get_piece(pos)
        all_moves = []
        lazers = board.lazers.copy()
        #print(f"pos: {pos} | dirs: {lazers[pos]}")
        for dir in lazers[pos]:
            if dir not in self.dirs: continue
            for step in range(1, lazers[pos][dir] + 1):
                t_square = pos + step * dir
                piece = board.get_piece(t_square)
                if piece:
                    all_moves.append(t_square)
                    break
                else:
                    all_moves.append(t_square)
                if self.fen.lower() == "k": break
        #print(f"all: {all_moves}")
        return all_moves


class King(Slider):
    def __init__(self, fen):
        super().__init__(fen)
        self.dirs = {-1, 1, -8, 8, -7, 7, -9, 9}

    def get_moves(self, board, pos):
        return super().get_moves(board, pos)


class Queen(Slider):
    def __init__(self, fen):
        super().__init__(fen)
        self.dirs = {-1, 1, -8, 8, -7, 7, -9, 9}

    def get_moves(self, board, pos):
        return super().get_moves(board, pos)


class Bishop(Slider):
    def __init__(self, fen):
        super().__init__(fen)
        self.dirs = {-7, 7, -9, 9}

    def get_moves(self, board, pos):
        return super().get_moves(board, pos)


class Rook(Slider):
    def __init__(self, fen):
        super().__init__(fen)
        self.dirs = {-1, 1, -8, 8}

    def get_moves(self, board, pos):
        return super().get_moves(board, pos)


class Knight(Piece):
    def __init__(self, fen):
        super().__init__(fen)
        self.dirs = {-17, -15, -10, -6, 6, 10, 15, 17}

    def get_moves(self, board, pos):
        all_moves = []
        for dir in self.dirs:
            t_square = pos + dir
            if not (0 <= t_square <= 63): continue
            me_x, me_y, t_x, t_y = pos % 8, pos // 8, t_square % 8, t_square // 8
            if (t_x - me_x) ** 2 + (t_y - me_y) ** 2 != 5: continue
            all_moves.append(t_square)
        return all_moves


class Pawn(Piece):
    def __init__(self, fen):
        super().__init__(fen)

    def get_moves(self, board, pos):
        all_moves = []
        self.dirs = {8, 7, 9} if self.get_type() == BL else {-8, -7, -9}
        if self.get_type() == WH and pos // 8 == 6: self.dirs.add(-16)
        if self.get_type() == BL and pos // 8 == 1: self.dirs.add(16)

        for dir in self.dirs:
            t_square = pos + dir
            if not (0 <= t_square <= 63): continue
            me_x, me_y, t_x, t_y = pos % 8, pos // 8, t_square % 8, t_square // 8
            if (t_x - me_x) ** 2 + (t_y - me_y) ** 2 > 4: continue
            all_moves.append(t_square)
        return all_moves
