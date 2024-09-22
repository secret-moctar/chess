import sys

from src.settings import *
from src.utils import parse
from src.state import State
from src.config_manager import config
from src.resource_manager import res_manager


class Clock:
    def __init__(self, sand=10, team="white", rel_pos=(0, 0)):
        self.sand = sand  # in min
        self.start = pg.time.get_ticks()
        self.team = team
        self.offset = 20
        self.img = res_manager.get_pres(os.path.join("icons", "icons8-clock-48.png"))
        self.pos = [rel_pos[0], rel_pos[1] - 20 - self.img.get_height()]
        if self.team == "B": self.pos[1] = rel_pos[1] + 20 + SQUA * 8

    def on(self): ...
    def off(self): ...

    def render(self, screen):
        screen.blit(self.img, self.pos)
        screen.blit(config.get_theme("font").render(f"{self.sand}:00", True, "white"), (self.pos[0] + 50, self.pos[1] + 10))


class ChessMenu(State):
    def __init__(self):
        super().__init__()
        self.tag = "ChessMenu"
        self.structure = parse(config.get_layout(self.tag))
        print(self.structure)
        self.transition_screen.input_img(pg.display.get_surface().copy())
        self.event = []
        self.chess_engine = None
        self.board = pg.Surface((SQUA * 8, SQUA * 8))
        self.board_pos = (WIN_WIDTH // 2 + 50 - self.board.get_width() // 2, WIN_HEIGHT // 2 - self.board.get_height() // 2)
        self.clock_w = Clock(rel_pos=self.board_pos)
        self.clock_b = Clock(team="B", rel_pos=self.board_pos)
        self.chess_engine = ChessEng()

    def handle_events(self, event):
        self.event = self.structure["stack"].listen(event, self.tag)
        self.chess_engine.handle_events()

    def update(self, mos_pos, dt):
        if "stack" in self.structure: self.structure["stack"].update(mos_pos)
        self.chess_engine.update(mos_pos, dt)
        self.transition = self.transition_screen.update(dt, self.transition)

    def change(self):
        if not self.event: return self
        if self.event[0] == "Quit":
            pg.quit()
            sys.exit()
        return self

    def render(self, screen):
        for img in self.structure["imgs"].values():
            pos = img["pos"]
            pic = img["img"]
            if "scaleby" in img: pic = pg.transform.scale_by(img["img"], img["scaleby"])
            pos = WIN_WIDTH * pos[0] - pic.get_width() // 2, WIN_HEIGHT * pos[1] - pic.get_height() // 2
            screen.blit(pic, pos)
        self.structure["stack"].render(screen, config.get_setting("button", "gap"), config.get_setting("button", "shape"))
        screen.blit(self.board, self.board_pos)
        # rendering the chess engine / borad and pieces
        self.chess_engine.render(self.board)
        self.clock_w.render(screen)
        self.clock_b.render(screen)
        self.transition_screen.render(screen)


class ChessEng:
    def __init__(self):
        self.in_board = [0] * 64
        self.turn = WH
        self.hash_fnn = {
            "K": res_manager.get_pres(os.path.join("chess-pieces", "Chess_klt60.png")),
            "k": res_manager.get_pres(os.path.join("chess-pieces", "Chess_kdt60.png")),
            "Q": res_manager.get_pres(os.path.join("chess-pieces", "Chess_qlt60.png")),
            "q": res_manager.get_pres(os.path.join("chess-pieces", "Chess_qdt60.png")),
            "N": res_manager.get_pres(os.path.join("chess-pieces", "Chess_nlt60.png")),
            "n": res_manager.get_pres(os.path.join("chess-pieces", "Chess_ndt60.png")),
            "B": res_manager.get_pres(os.path.join("chess-pieces", "Chess_blt60.png")),
            "b": res_manager.get_pres(os.path.join("chess-pieces", "Chess_bdt60.png")),
            "R": res_manager.get_pres(os.path.join("chess-pieces", "Chess_rlt60.png")),
            "r": res_manager.get_pres(os.path.join("chess-pieces", "Chess_rdt60.png")),
            "P": res_manager.get_pres(os.path.join("chess-pieces", "Chess_plt60.png")),
            "p": res_manager.get_pres(os.path.join("chess-pieces", "Chess_pdt60.png")),
        }
        self.fnn_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", WH)

    def fnn_board(self, squence, turn):
        self.turn = turn
        board = self.in_board
        file = 0
        rank = 0
        for char in squence:
            if char in self.hash_fnn:
                target_square = rank * 8 + file
                board[target_square] = self.hash_fnn[char]
                file += 1
            elif char == "/":
                rank += 1
                file = 0
            else:
                num = int(char)
                file += num

    def handle_events(self, mos_pos=[0, 0]): ...
    def update(self, mos_pos, dt): ...

    def blit_board(self, screen, a_color=(150, 177, 34), b_color=(238, 220, 151)):
        for i in range(8):
            for j in range(8, -1, -1):
                color = b_color if (i + j) % 2 == 0 else a_color
                pg.draw.rect(screen, color, (i * SQUA, j * SQUA, SQUA, SQUA))

    def render(self, screen):
        self.blit_board(screen)
        for i in range(len(self.in_board)):
            if not self.in_board[i]: continue
            square = i % 8, i // 8
            sq_pos = square[0] * SQUA, square[1] * SQUA
            screen.blit(self.in_board[i], sq_pos)
