import sys

from src.settings import *
from src.utils import parse
from src.state import State
from src.chess_eng import ChessEng
from src.config_manager import config
from src.resource_manager import res_manager


class Clock:
    def __init__(self, sand=15, team=WH, rel_pos=(0, 0)):
        self.sand = sand * 1000  # in min converting to milliseconds
        self.last = pg.time.get_ticks()
        print(f"time.start: {self.last}")
        pg.time.get_ticks()
        self.team = team
        self.offset = 20
        self.img = res_manager.get_pres(os.path.join("icons", "icons8-clock-48.png"))
        self.pos = [rel_pos[0], rel_pos[1] - 20 - self.img.get_height()]
        if self.team == WH: self.pos[1] = rel_pos[1] + 20 + SQUA * 8
        self.is_flip = self.team == WH
        self.color = "white"

    def on(self):
        self.is_flip = True

    def off(self):
        self.is_flip = False

    def update(self):
        if self.is_flip:
            self.sand -= pg.time.get_ticks() - self.last
        self.last = pg.time.get_ticks()
        if self.sand <= 0: self.sand = 0

        if 0 < self.sand // 1000 <= 10:
            self.color = "red"

    def over(self):
        return self.sand <= 0

    def render(self, screen):
        screen.blit(self.img, self.pos)
        min = str(self.sand // (1000 * 60))
        sec = str((self.sand // 1000) % 60)
        if len(min) == 1: min = "0" + min
        if len(sec) == 1: sec = "0" + sec
        screen.blit(config.get_theme("font").render(f"{min}:{sec}", True, self.color), (self.pos[0] + 50, self.pos[1] + 10))


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
        self.clock_b = Clock(team=BL, rel_pos=self.board_pos)
        self.chess_engine = ChessEng(self.board_pos, self.clock_w, self.clock_b)

    def handle_events(self, event):
        self.event = self.structure["stack"].listen(event, self.tag)
        self.chess_engine.handle_events(event)

    def update(self, mos_pos, dt):
        self.clock_w.update()
        self.clock_b.update()
        if "stack" in self.structure: self.structure["stack"].update(mos_pos)
        self.chess_engine.update(dt)
        self.transition = self.transition_screen.update(dt, self.transition)

    def change(self):
        if not self.event: return self
        if self.event[0] == "Quit":
            pg.time.delay(500)
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
        # rendering the chess engine / borad and pieces
        self.chess_engine.render(self.board)
        screen.blit(self.board, self.board_pos)
        self.clock_w.render(screen)
        self.clock_b.render(screen)
        self.transition_screen.render(screen)
