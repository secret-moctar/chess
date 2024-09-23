from src.settings import*
from src.pieces import King, Piece, Queen, Knight, Rook, Bishop, Pawn
from src.config_manager import config
from src.resource_manager import res_manager


class Board():
    def __init__(self):
        self.in_board = [0] * 64
        self.threat_map = set()
        self.hash_fnn = {
            "k": King,
            "q": Queen,
            "n": Knight,
            "b": Bishop,
            "r": Rook,
            "p": Pawn,
        }

    def move_piece(self, start, end):
        self.in_board[end] = self.in_board[start]

    def del_piece(self, pos):
        self.in_board[pos] = 0

    def load_fnn(self, squence):
        board = self.in_board
        file = 0
        rank = 0
        for char in squence.split()[0]:
            if char.lower() in self.hash_fnn:
                target_square = rank * 8 + file
                board[target_square] = self.hash_fnn[char.lower()](char)
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

    def draw_pieces(self, screen, selected):
        for i in range(64):
            if not self.in_board[i]: continue
            piece = self.in_board[i]
            if i == selected: continue
            x, y = (i % 8) * SQUA, (i // 8) * SQUA
            screen.blit(piece.img, (x, y))
