from src.pieces import Queen
from src.board import Board
from src.settings import *
from src.resource_manager import res_manager
from src.chess_abc import ChessAbc
from src.utils import log


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
    def __init__(self, rel_pos, org=True):
        self.curr_player = None
        self.rel_pos = rel_pos
        self.board = Board()
        self.selected = -1
        self.w_threat = {i: 0 for i in range(64)}
        self.b_threat = {i: 0 for i in range(64)}
        self.history = []
        self.cal = True
        self.register_move = None
        self.curr_player = self.board.load_fnn("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w")
        self.history = [self.board.get_fnn(self.curr_player)]
        self.mvt_history = [0] * 64
        if org:
            self.update_mvt()

    def copy(self):
        other = ChessEng(self.rel_pos, org=False)
        other.curr_player = self.curr_player
        other.rel_pos = self.rel_pos
        other.board = self.board.copy()
        other.selected = self.selected
        other.w_threat = self.w_threat.copy()
        other.b_threat = self.b_threat.copy()
        other.history = self.history.copy()
        other.cal = self.cal
        other.curr_player = self.curr_player
        return other

    def is_king_checked(self, color):
        king_pos = self.find_king(color)
        if king_pos is None: return False
        oppsing_color = WH if color == BL else BL
        return self.is_square_under_attack(king_pos, oppsing_color)

    def zero_move(self, color):
        for i in range(64):
            piece = self.board.get_piece(i)
            if piece and piece.get_type() == color:
                if piece.all_legal_moves: return False
        return True

    def is_checkmate(self, color):
        return self.is_king_checked(color) and self.zero_move(color)

    def is_stalemate(self, color):
        return (not self.is_king_checked(color)) and self.zero_move(color)

    def handle_events(self, event):
        mos_pos = self.get_mos_pos()
        t_square = mos_pos[0] // SQUA + (mos_pos[1] // SQUA) * 8  # target square
        if mos_pos[0] < 0 or mos_pos[1] < 0: t_square = -1
        if mos_pos[0] > 8 * SQUA or mos_pos[1] > 8 * SQUA: t_square = -1
        piece = self.board.get_piece(t_square)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                print(f"command:{self.board.get_fnn(self.curr_player)}")
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.selected == -1 and piece and self.is_my_turn(piece):
                    self.select(t_square)
                elif self.selected > -1:
                    current = self.board.get_piece(self.selected)
                    for mv in current.all_legal_moves:
                        if mv.end == t_square:
                            self.make_move(mv)
                            break
                    self.unselect()

    def cal_threat(self, color):
        threat = self.w_threat if color == WH else self.b_threat
        for i in range(64):
            threat[i] = 0
        for i in range(64):
            piece = self.board.get_piece(i)
            if piece and piece.get_type() == color : piece.apply_threat(threat, i)

    def is_square_under_attack(self, square, attacking_color):
        threat = self.w_threat if attacking_color == WH else self.b_threat
        return bool(threat[square])

    def find_king(self, color):
        fen = "K" if color == WH else "k"
        for i in range(64):
            piece = self.board.get_piece(i)
            if piece and piece.fen == fen: return i

    def is_my_turn(self, piece):
        return piece.get_type() == self.curr_player

    def is_cap(self, pos):
        return bool(self.board.get_piece(pos))

    def unselect(self):
        self.selected = -1

    def select(self, t_square):
        self.selected = t_square
        res_manager.get_resource("move").play()

    def get_mos_pos(self):
        mos_pos = pg.mouse.get_pos()
        mos_pos = mos_pos[0] - self.rel_pos[0], mos_pos[1] - self.rel_pos[1]
        return mos_pos

    def update(self, dt):
        return
        if self.is_checkmate(self.curr_player):
            res_manager.get_resource("check_mate").play()
            print("#"*40)
            if self.curr_player == WH: print("Black win")
            else: print("White wins")
            print("#"*40)
        if self.is_stalemate(self.curr_player):
            res_manager.get_resource("check_mate").play()
            print("#"*40)
            print("DRAW, DRAW DRAW")
            print("#"*40)


    def is_move_valid(self, move):
        color = self.curr_player
        temp = self.copy()
        temp.make_move(move, real=False)
        return not temp.is_king_checked(color)

    def get_all_legal_moves(self, me, moves, real=True):
        hall = []
        curr = self.board.get_piece(me)
        for m in moves:
            peice = self.board.get_piece(m)

            #add castling
            if curr and curr.fen.lower() == "k" and real:
                if curr.castling[0]:
                    do_it = True
                    for s in range(1, 4):
                        ct_s =  me - s  # castling target square
                        if self.board.get_piece(ct_s): do_it = False
                    if do_it:
                        if self.is_move_valid(Move(me, me - 2, False)): hall.append(Move(me, me - 2, False))
                if curr.castling[1]:
                    do_it = True
                    for s in range(1, 3):
                        ct_s =  me + s  # castling target square
                        if self.board.get_piece(ct_s): do_it = False
                    if do_it:
                        if self.is_move_valid(Move(me, me + 2, False)): hall.append(Move(me, me + 2, False))

            if curr.fen.lower() == "p":
                if m % 8 == me % 8:
                    if peice: continue
                    if abs(m // 8 - me // 8) == 2:
                        sign = 1 if curr.get_type() == WH else -1
                        if self.board.get_piece(m + sign * 8): continue
                else:
                    if not peice: continue
            if peice and peice.is_friend(curr): continue
            if real:
                if self.is_move_valid(Move(me, m, self.is_cap(m))): hall.append(Move(me, m, self.is_cap(m)))
            else:
                hall.append(Move(me, m, self.is_cap(m)))
        return hall

    def make_move(self, move, real=True):
        # getting the piece before making the move
        piece = self.board.get_piece(move.start)
        # playing the sound
        if real:
            if move.is_capture:
                res_manager.get_resource("capture").play()
            else:
                res_manager.get_resource("move").play()
        # actually making the move on the board
        self.board.move_piece(move.start, move.end)
        self.board.del_piece(move.start)

        # checking if rook as moved and ihabinting the castling on that side
        if real and piece and piece.fen.lower() == "r":
            mon_king = self.board.get_piece(self.find_king(piece.get_type()))
            if move.start % 8 == 0:
                mon_king.castling[0] = False
            elif move.start % 8 == 7:
                mon_king.castling[1] = False

        # checking if the move is castling and moving the rook aproparietly
        if real and piece and piece.fen.lower() == "k":
            if abs(move.start - move.end) == 2:
                rook_pos = (move.start // 8) * 8 if move.end % 8 == 2 else (move.start // 8) * 8 + 7
                end_pos = move.start - 1 if move.end % 8 == 2 else move.start + 1
                rook = self.board.get_piece(rook_pos)
                if rook:
                    self.board.move_piece(rook_pos, end_pos)
                    self.board.del_piece(rook_pos)
                    piece.castling = [False, False]
            else:
                # if the move is not castling the king loses all right to future castling
                piece.castling = [False, False]

        # checking for promotion
        if piece and piece.fen.lower() == "p" and move.end // 8 in {0, 7}:
            if real: res_manager.get_resource("promote").play()
            self.board.in_board[move.end] = Queen("Q" if piece.get_type() == WH else "q")

        # chaging the current palyer and updating the history and the possible mvt and threat for every piece
        self.curr_player = WH if self.curr_player == BL else BL
        self.history.append(self.board.get_fnn(self.curr_player))
        self.update_mvt(real=real)
        self.cal_threat(WH)
        self.cal_threat(BL)
        # checking if the move made the king in danger and playing the sound
        if self.is_king_checked(self.curr_player):
            if real: res_manager.get_resource("check").play()

    def undo_move(self):
        last = self.history.pop()
        self.curr_player = self.board.load_fnn(self.history[-1])
        self.update_mvt()
        self.cal_threat(WH)
        self.cal_threat(BL)
        return last

    def update_mvt(self, real=True):
        for i in range(64):
            piece = self.board.get_piece(i)
            if not piece: continue
            piece.all_moves = piece.get_moves(self.board, i)
            piece.all_legal_moves = self.get_all_legal_moves(i, piece.all_moves, real=real)

    def draw_threat(self, screen):
        threat = self.w_threat if self.curr_player == BL else self.b_threat
        for square in threat:
            if threat[square]:
                pg.draw.rect(screen, (255, 0, 0), ((square % 8) * SQUA, (square // 8) * SQUA, SQUA, SQUA))

    def render(self, screen):
        self.board.blit_board(screen)
        #self.draw_threat(screen)
        self.board.draw_pieces(screen, self.selected)
        #self.board.draw_pos(screen)
        if self.selected > -1:
            self.board.mark_moves(screen, self.board.get_piece(self.selected))
            self.board.draw_selected(screen, self.board.get_piece(self.selected), self.get_mos_pos())
