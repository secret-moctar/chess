import sys

from src.settings import *
from src.utils import parse
from src.state import State
from src.chess_eng import ChessEng
from src.config_manager import config
from src.resource_manager import res_manager
from src.clock import Clock
from src.state_manager import state_manager


class ChessMenu(State):
    def __init__(self):
        super().__init__()
        self.transition_screen = self.custom_transition(form="pixel")
        self.tag = "ChessMenu"
        self.structure = parse(config.get_layout(self.tag))
        print(self.structure)
        self.event = []
        self.chess_engine = None
        self.board = pg.Surface((SQUA * 8, SQUA * 8))
        self.board_pos = (WIN_WIDTH // 2 + 50 - self.board.get_width() // 2, WIN_HEIGHT // 2 - self.board.get_height() // 2)
        self.clock_w = Clock(rel_pos=self.board_pos)
        self.clock_b = Clock(team=BL, rel_pos=self.board_pos)
        self.chess_engine = ChessEng(self.board_pos, self.clock_w, self.clock_b)

    def handle_events(self, event):
        self.event = []
        if self.transition_screen.is_finished():
            if "stacks" in self.structure:
                for stack in self.structure["stacks"].values():
                    events = stack.listen(event, self.tag)
                    for even in events: self.event.append(even)
            self.chess_engine.handle_events(event)

    def update(self, mos_pos, dt):
        if self.transition_screen.is_finished():
            self.clock_w.update()
            self.clock_b.update()
            if "stacks" in self.structure:
                for stack in self.structure["stacks"].values():
                    stack.update(mos_pos)
            self.chess_engine.update(dt)
        else:
            self.transition_screen.update(dt)
        self.change()

    def change(self):
        if not self.event: return
        if self.event[0] == "Quit":
            pg.time.delay(500)
            pg.quit()
            sys.exit()
        if self.event[0] == "Pause":
            self.clock_w.off()
            self.clock_b.off()
        if self.event[0] == "Back":
            self.call("PlayMenu", tweak=True, direction="right")

    def render(self, screen):
        if self.transition: screen = self.get_new_window()
        if self.transition_screen.is_finished():
            for img in self.structure["imgs"].values():
                pos = img["pos"]
                pic = img["img"]
                if "scaleby" in img: pic = pg.transform.scale_by(img["img"], img["scaleby"])
                pos = WIN_WIDTH * pos[0] - pic.get_width() // 2, WIN_HEIGHT * pos[1] - pic.get_height() // 2
                screen.blit(pic, pos)
            if "stacks" in self.structure:
                for stack in self.structure["stacks"].values():
                    stack.render(screen, config.get_setting("button", "gap"), config.get_setting("button", "shape"))
            # rendering the chess engine / borad and pieces
            self.chess_engine.render(self.board)
            screen.blit(self.board, self.board_pos)
            self.clock_w.render(screen)
            self.clock_b.render(screen)
            if self.transition:
                self.transition_screen.start(screen)
                self.transition = False
        else:
            self.transition_screen.render(screen)

state_manager.register("ChessMenu", ChessMenu)
