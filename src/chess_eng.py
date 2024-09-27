from src.settings import *
from src.config_manager import config
from src.pieces import Queen, Rook, Knight, Bishop
from src.board import Board
from src.moves import Move
from src.resource_manager import res_manager
from src.chess_abc import ChessAbc


class ChessEng(ChessAbc):
    def __init__(self, rel_pos, w_clock, b_clock, org=True):
        self.rel_pos = rel_pos
        self.w_clock = w_clock
        self.b_clock = b_clock
        self.curr_player = None
        self.board = Board()
        self.selected = -1
        self.w_threat = {i: 0 for i in range(64)}
        self.b_threat = {i: 0 for i in range(64)}
        self.half_clock = 0
        self.full_clock = 0
        self.last_move = None
        if org: self.load_fnn("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w QKqk - 0 0")
        self.first_to_move = self.curr_player
        if org: self.history = [self.get_fnn()]
        if org:
            self.update_mvt()
            self.update_threat(WH)
            self.update_threat(BL)

    def get_fnn(self):
        w_k = self.board.get_piece(self.find_king(WH))
        b_k = self.board.get_piece(self.find_king(BL))
        return self.board.get_fnn(self.curr_player, w_k, b_k, self.last_move, self.half_clock, self.full_clock)

    def load_fnn(self, squence):
        turn, c_w, c_b, last_move, hc, fc = self.board.load_fnn(squence, debug=True)
        self.curr_player =  turn
        w_k = self.board.get_piece(self.find_king(WH))
        b_k = self.board.get_piece(self.find_king(BL))
        print(f"undo_cw: {c_w}")
        print(f"undo_cb: {c_b}")
        w_k.castling = c_w
        b_k.castling = c_b
        self.last_move = last_move
        self.half_clock = hc
        self.full_clock = fc

    def copy(self):
        other = ChessEng(self.rel_pos, self.w_clock, self.b_clock, org=False)
        other.curr_player = self.curr_player
        other.rel_pos = self.rel_pos
        other.board = self.board.copy()
        other.selected = self.selected
        other.w_threat = self.w_threat.copy()
        other.b_threat = self.b_threat.copy()
        other.history = self.history.copy()
        other.last_move = self.last_move
        other.curr_player = self.curr_player
        other.half_clock = self.half_clock
        other.full_clock = self.full_clock
        return other

    def is_king_checked(self, color):
        king_pos = self.find_king(color)
        if king_pos is None: return False
        oppsing_color = WH if color == BL else BL
        return self.is_square_under_attack(king_pos, oppsing_color)

    def is_zero_move(self, color):
        for i in range(64):
            piece = self.board.get_piece(i)
            if piece and piece.get_type() == color:
                if piece.all_legal_moves: return False
        return True

    def is_checkmate(self, color):
        return self.is_king_checked(color) and self.is_zero_move(color)

    def is_stalemate(self, color):
        return (not self.is_king_checked(color)) and self.is_zero_move(color)

    def update_threat(self, color):
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

    def handle_events(self, event):
        mos_pos = self.get_mos_pos()
        t_square = mos_pos[0] // SQUA + (mos_pos[1] // SQUA) * 8  # target square
        if mos_pos[0] < 0 or mos_pos[1] < 0: t_square = -1
        if mos_pos[0] > 8 * SQUA or mos_pos[1] > 8 * SQUA: t_square = -1
        piece = self.board.get_piece(t_square)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                print(f"command:{self.get_fnn()}")
                if self.last_move: print(f"last move: {self.last_move.start} -> {self.last_move.end}")
                print(f"time: {pg.time.get_ticks()}")
                w_k = self.board.get_piece(self.find_king(WH))
                w_b = self.board.get_piece(self.find_king(BL))
                print(f"cas_w:{w_k.castling}")
                print(f"cas_b:{w_b.castling}")
            if event.key == pg.K_BACKSPACE: self.undo_move()
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

    def update(self, dt):
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
        if self.half_clock >= 100:
            print("##################")
            print("CAN DRAW")
            print("##################")
        if self.w_clock.over():
            print("#"*40)
            print("Black wins")
            print("#"*40)
        if self.b_clock.over():
            print("#"*40)
            print("White wins")
            print("#"*40)


    def is_move_valid(self, move):
        color = self.curr_player
        temp = self.copy()

        # Special check for en passant
        piece = temp.board.get_piece(move.start)
        if piece and piece.fen.lower() == 'p' and move.start % 8 != move.end % 8 and not temp.board.get_piece(move.end):
            # Ensure it's a valid en passant move
            if temp.last_move and abs(temp.last_move.start - temp.last_move.end) == 16:
                captured_pawn_pos = move.end + 8 if piece.get_type() == WH else move.end - 8
                if temp.last_move.end == captured_pawn_pos:
                    # Remove the captured pawn for this validation
                    temp.board.del_piece(captured_pawn_pos)
        temp.make_move(move, real=False)
        return not temp.is_king_checked(color)

    def handle_castling(self, me, curr, piece, hall, real=True):
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

    def handle_en_passant(self, me, curr, hall):
        if curr.fen.lower() == "p" and self.last_move and abs(self.last_move.start - self.last_move.end) == 16:  # Two-square pawn move
            if curr.get_type() == WH and me // 8 == 3:  # White pawn on 5th rank
                if me % 8 != 0 and self.last_move.end == me - 1:  # Left side
                    if self.is_move_valid(Move(me, me - 9, True)): hall.append(Move(me, me - 9, True))
                if me % 8 != 7 and self.last_move.end == me + 1:  # Right side
                    if self.is_move_valid(Move(me, me - 7, True)): hall.append(Move(me, me - 7, True))
            elif curr.get_type() == BL and me // 8 == 4:  # Black pawn on 4th rank
                if me % 8 != 0 and self.last_move.end == me - 1:  # Left side
                    if self.is_move_valid(Move(me, me + 7, True)): hall.append(Move(me, me + 7, True))
                if me % 8 != 7 and self.last_move.end == me + 1:  # Right side
                    if self.is_move_valid(Move(me, me + 9, True)): hall.append(Move(me, me + 9, True))

    def get_all_legal_moves(self, me, moves, real=True):
        hall = []
        curr = self.board.get_piece(me)
        for m in moves:
            peice = self.board.get_piece(m)
            #add castling
            self.handle_castling(me, curr, peice, hall, real=real)
            # pawn moves and en-passant
            self.handle_en_passant(me, curr, hall)

            # filtering the pawn movement
            if curr.fen.lower() == "p":
                if m % 8 == me % 8:
                    if peice: continue
                    if abs(m // 8 - me // 8) == 2:
                        sign = 1 if curr.get_type() == WH else -1
                        if self.board.get_piece(m + sign * 8): continue
                else:
                    if not peice: continue

            # preveting friendly fire
            if peice and peice.is_friend(curr): continue
            if real:
                if self.is_move_valid(Move(me, m, self.is_cap(m))): hall.append(Move(me, m, self.is_cap(m)))
            else:
                hall.append(Move(me, m, self.is_cap(m)))
        return hall

    def castling_special_move(self, move, piece, real=True):
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
                    res_manager.get_resource("promote").play()
                    piece.castling = [False, False]
            else:
                # if the move is not castling the king loses all right to future castling
                piece.castling = [False, False]

    def pawn_special_move(self, move, piece, real=True):
        if piece and piece.fen.lower() == 'p' and move.start % 8 != move.end % 8 and not self.board.get_piece(move.end):
            # Remove the captured pawn
            captured_pawn_pos = move.end + 8 if piece.get_type() == WH else move.end - 8
            self.board.del_piece(captured_pawn_pos)
            move.is_capture = True

    def pawn_promotion(self, move, piece, real=True):
        if piece and piece.fen.lower() == "p" and move.end // 8 in {0, 7}:
            if real: res_manager.get_resource("promote").play()
            self.board.in_board[move.end] = Queen("Q" if piece.get_type() == WH else "q")

    def make_move(self, move, real=True):
        # getting the piece before making the move
        piece = self.board.get_piece(move.start)
        # playing the sound
        if real:
            if move.is_capture:
                res_manager.get_resource("capture").play()
            else:
                res_manager.get_resource("move").play()

        # Handle en passant capture
        self.pawn_special_move(move, piece, real=real)

        # actually making the move on the board
        self.board.move_piece(move.start, move.end)
        self.board.del_piece(move.start)
        # read the name of the method
        self.castling_special_move(move, piece, real=real)
        # checking for promotion
        self.pawn_promotion(move, piece, real=real)

        # chaging the current palyer and updating the history and the possible mvt and threat for every piece
        self.curr_player = WH if self.curr_player == BL else BL
        if real and piece and piece.fen.lower() == "p" and abs(move.end - move.start) == 16:
            self.last_move = move
        else:
            self.last_move = None
        # recalculating the mvt after the new move
        self.update_mvt(real=real)
        # updating the thret
        self.update_threat(WH)
        self.update_threat(BL)
        # checking if the move made the king in danger and playing the sound
        if self.is_king_checked(self.curr_player):
            if real: res_manager.get_resource("check").play()
        # updating the half-move and full-move clocks
        if real and piece and piece.fen.lower() == "p" or move.is_capture:
            self.half_clock = 0
        else:
            self.half_clock += 1

        if real and piece and piece.get_type() != self.first_to_move:
            self.full_clock += 1

        # updating the state of the real clocks
        if real and piece.get_type() == WH:
            self.w_clock.off()
            self.b_clock.on()
        elif real:
            self.b_clock.off()
            self.w_clock.on()

        # updating the history with this last move
        if real: self.history.append(self.get_fnn())
        if real:
            if self.last_move: print(f"last: {self.last_move.start} -> {self.last_move.end} ")
            else: print("last: None")
            print(f"hist: {self.history[-1]}")

    def undo_move(self):
        if len(self.history) > 1: last = self.history.pop()
        else: return ""
        res_manager.get_resource("move").play()
        self.load_fnn(self.history[-1])
        self.update_mvt(debug=False, real=False)
        self.update_threat(WH)
        self.update_threat(BL)
        return last

    def update_mvt(self, real=True, debug=False):
        for i in range(64):
            piece = self.board.get_piece(i)
            if not piece: continue
            piece.all_moves = piece.get_moves(self.board, i)
            piece.all_legal_moves = self.get_all_legal_moves(i, piece.all_moves, real=real)
        if debug:
            self.show_legal_moves(self.curr_player)

    def show_legal_moves(self, color):
        for i in range(64):
            piece = self.board.get_piece(i)
            if piece and piece.get_type() == color:
                print(f"{piece.fen}{i}: {piece.all_legal_moves}")

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
        self.board.draw_labels(screen)
        if self.selected > -1:
            self.board.mark_moves(screen, self.board.get_piece(self.selected))
            self.board.draw_selected(screen, self.board.get_piece(self.selected), self.get_mos_pos())
