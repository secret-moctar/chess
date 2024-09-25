from src.settings import*
from src.pieces import King, Piece, Queen, Knight, Rook, Bishop, Pawn
from src.config_manager import config
from src.resource_manager import res_manager


class Board():
    def __init__(self):
        self.in_board = [0] * 64
        self.hash_fnn = {
            "k": King,
            "q": Queen,
            "n": Knight,
            "b": Bishop,
            "r": Rook,
            "p": Pawn,
        }
        self.lazers = self.shoot_lazer()

    def copy_in(self):
        in_board = [0] * 64
        for i in range(64):
            piece = self.get_piece(i)
            if piece:
                c_piece = self.hash_fnn[piece.fen.lower()](piece.fen)
                c_piece.all_moves = piece.all_moves.copy()
                c_piece.all_legal_moves =piece.all_legal_moves.copy()
                c_piece.dirs = piece.dirs.copy()
                if c_piece.fen.lower() == "k": c_piece.castling = piece.castling.copy()
                in_board[i] = c_piece
        return in_board

    def copy(self):
        other = Board()
        other.in_board = self.copy_in()
        other.hash_fnn = {
            "k": King,
            "q": Queen,
            "n": Knight,
            "b": Bishop,
            "r": Rook,
            "p": Pawn,
        }
        other.lazers = self.lazers.copy()

        return other

    def shoot_lazer(self):
        lazers = []
        for i in range(len(self.in_board)):
            west = i % 8
            east = 8 - west - 1
            north = i // 8
            south = 8 - north - 1
            north_west = min(north, west)
            south_west = min(south, west)
            south_east = min(south, east)
            north_east = min(north, east)
            dir = {
                -1: west,
                1: east,
                -8: north,
                8: south,
                -9: north_west,
                7: south_west,
                9: south_east,
                -7: north_east
            }
            lazers.append(dir)
        return lazers

    def move_piece(self, start, end):
        self.in_board[end] = self.in_board[start]

    def del_piece(self, pos):
        self.in_board[pos] = 0

    def load_fnn(self, squence):
        self.in_board = [0] * 64
        file = 0
        rank = 0
        for char in squence.split()[0]:
            if char.lower() in self.hash_fnn:
                target_square = rank * 8 + file
                self.in_board[target_square] = self.hash_fnn[char.lower()](char)
                file += 1
            elif char == "/":
                rank += 1
                file = 0
            else:
                num = int(char)
                file += num
        return squence.split()[1]

    def get_fnn(self, curr_player):
        fen = ""
        empty = 0
        for square in range(len(self.in_board)):
            piece = self.in_board[square]
            if piece:
                if square % 8 == 0 and square != 0:
                    if empty:
                        fen += str(empty)
                        empty = 0
                    fen += "/"
                if empty: fen += str(empty)
                empty = 0
                fen += piece.fen
            else:
                if square % 8 == 0 and square != 0:
                    if empty:
                        fen += str(empty)
                    fen += "/"
                    empty = 0
                empty += 1
        if empty: fen += f"{empty}"
        fen += f" {curr_player[0].lower()}"
        return fen

    def get_piece(self, position):
        return self.in_board[position] if 0 <= position <= 63 else 0

    def blit_board(self, screen, a_color=(150, 177, 34), b_color=(238, 220, 151)):
        for i in range(8):
            for j in range(8, -1, -1):
                color = b_color if (i + j) % 2 == 0 else a_color
                pg.draw.rect(screen, color, (i * SQUA, j * SQUA, SQUA, SQUA))

    def mark_moves(self, screen, piece: Piece):
        for move in piece.all_legal_moves:
            rad = SQUA // 4
            x, y = (move.end % 8) * SQUA, (move.end // 8) * SQUA
            if move.is_capture:
                screen.blit(res_manager.get_resource("red_circle"), (x + SQUA // 2 - 24, y + SQUA // 2 - 24))
            else:
                screen.blit(res_manager.get_resource("blue_circle"), (x + SQUA // 2 - 15, y + SQUA // 2 - 15))

    def draw_selected(self, screen, piece, pos):
        s_pos = list(pos)
        width = piece.img.get_width() // 2
        height = piece.img.get_height() // 2
        if s_pos[0] < width: s_pos[0] = width
        if s_pos[1] < height: s_pos[1] = height
        if s_pos[0] > SQUA * 8 - width: s_pos[0] = SQUA * 8 - width
        if s_pos[1] > SQUA * 8 - height: s_pos[1] = SQUA * 8 - height
        screen.blit(piece.img, (s_pos[0] - piece.img.get_width() // 2, s_pos[1] - piece.img.get_height() // 2))

    def draw_pos(self, screen):
        for i in range(64):
            x, y = (i % 8) * SQUA, (i // 8) * SQUA
            screen.blit(config.get_theme("font").render(f"{i}", True, config.get_theme("tcolor")), (x, y))

    def draw_pieces(self, screen, selected):
        for i in range(64):
            if not self.in_board[i]: continue
            piece = self.in_board[i]
            if i == selected: continue
            x, y = (i % 8) * SQUA, (i // 8) * SQUA
            screen.blit(piece.img, (x, y))
