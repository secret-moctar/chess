import sys

from src.settings import *
from src.utils import parse
from src.state import State


class ChessMenu(State):
    def __init__(self):
        super().__init__()
        self.tag = "ChessMenu"
        self.structure = parse(LAYOUT_INFO[self.tag])
        print(self.structure)
        self.transition_screen.input_img(pg.display.get_surface().copy())
        self.event = []
        self.chess_engine = None
        self.board = pg.Surface((64 * 8, 64 * 8))
        self.board_pos = (WIN_WIDTH // 2 + 50, WIN_HEIGHT // 2)

    def handle_events(self, event):
        self.event = self.structure["stack"].listen(event, self.tag)

    def update(self, mos_pos, dt):
        if "stack" in self.structure: self.structure["stack"].update(mos_pos)
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
        self.structure["stack"].render(screen, OPTIONS["button"]["gap"], OPTIONS["button"]["shape"])
        screen.blit(self.board, (self.board_pos[0] - self.board.get_width() // 2, self.board_pos[1] - self.board.get_height() // 2))
        self.transition_screen.render(screen)
