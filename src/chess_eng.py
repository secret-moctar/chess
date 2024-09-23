from src.board import Board
from src.settings import *
from src.resource_manager import res_manager
from src.chess_abc import ChessAbc


class Move:
    def __init__(self, start,  end, cap):
        self.start = start
        self.end = end
        self.is_capture = cap

    def __eq__(self, other):
        if isinstance(other, Move):
            return other == self
        return self.end == other


class ChessEng(ChessAbc):
    def __init__(self, rel_pos):
        self.curr_player = None
        self.rel_pos = rel_pos
        self.board = Board()
        self.selected = -1
        self.history = []
        self.cal = True
        # self.curr_player = self.board.load_fnn("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w")
        self.curr_player = self.board.load_fnn("8/8/8/3Qq3/8/8/8/8 w")
        self.history = [self.board.get_fnn(self.curr_player)]
        print(self.board.get_fnn(WH))
        print(self.curr_player)

    def make_move(self, move):
        self.board.move_piece(move.start, move.end)
        self.board.del_piece(move.start)
        self.curr_player = WH if self.curr_player == BL else BL
        self.cal = True
        self.history.append(self.board.get_fnn(self.curr_player))

    def undo_move(self):
        return self.history.pop()

    def is_checkmate(self): return False
    def is_stalemate(self): return False

    def is_move_valid(self, move):
        return True

    def handle_events(self, event):
        mos_pos = self.get_mos_pos()
        t_square = mos_pos[0] // SQUA + (mos_pos[1] // SQUA) * 8  # target square
        piece = self.board.get_piece(t_square)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.selected == -1 and piece and self.is_my_turn(piece):
                    self.select(t_square)
                elif self.selected > -1:
                    current = self.board.get_piece(self.selected)
                    for mv in current.all_legal_moves:
                        if mv.end == t_square: self.make_move(mv)
                    else: self.unselect()

    def is_my_turn(self, piece):
        return piece.get_type() == self.curr_player

    def is_cap(self, pos):
        return bool(self.board.get_piece(pos))

    def get_all_legal_moves(self, me, moves):
        hall = []
        for m in moves:
            if self.is_move_valid(Move(me, m, self.is_cap(m))): hall.append(Move(me, m, self.is_cap(m)))
        return hall

    def unselect(self):
        self.selected = -1

    def select(self, t_square):
        self.selected = t_square
        print(self.board.get_piece(self.selected).all_moves)
        print(self.board.get_piece(self.selected).all_legal_moves)

    def get_mos_pos(self):
        mos_pos = pg.mouse.get_pos()
        mos_pos = mos_pos[0] - self.rel_pos[0], mos_pos[1] - self.rel_pos[1]
        return mos_pos

    def update(self, dt):
        if self.cal:
            for i in range(64):
                piece = self.board.get_piece(i)
                if not piece: continue
                piece.get_moves()
                piece.all_legal_moves = self.get_all_legal_moves(i, piece.all_moves)
            self.cal = False

    def render(self, screen):
        self.board.blit_board(screen)
        self.board.draw_pieces(screen, self.selected)
        if self.selected > -1:
            self.board.mark_moves(screen, self.board.get_piece(self.selected))
            self.board.draw_selected(screen, self.board.get_piece(self.selected), self.get_mos_pos())
