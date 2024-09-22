import sys

from src.state import State
from src.settings import *
from src.utils import parse
from src.chess import ChessMenu
from src.config_manager import config


class WelcomeScreen(State):
    def __init__(self):
        super().__init__()
        self.structure = parse(config.get_layout("Welcome"))
        self.s_time = pg.time.get_ticks() / 1000
        self.switch = False

    def goto(self):
        self.exit()
        self.switch = True

    def update(self, mos_pos, dt):
        if pg.time.get_ticks() / 1000 - self.s_time > 0.5:
            self.goto()

    def change(self):
        if not self.switch: return self
        next_state = MainMenu()
        next_state.enter(other=self)
        return next_state

    def render(self, screen):
        for img in self.structure["imgs"].values():
            pos = img["pos"]
            scaleby = img["scaleby"]
            picture = pg.transform.scale_by(img["img"], scaleby)
            pos = WIN_WIDTH * pos[0] - picture.get_width() // 2, WIN_HEIGHT * pos[1] - picture.get_height() // 2
            screen.blit(picture, pos)


class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.tag = "MainMenu"
        self.structure = parse(config.get_layout("MainMenu"))
        self.transition_screen.input_img(pg.display.get_surface().copy())
        self.event = []

    def handle_events(self, event):
        self.event = self.structure["stack"].listen(event, self.tag)

    def update(self, mos_pos, dt):
        if "stack" in self.structure: self.structure["stack"].update(mos_pos)
        self.transition = self.transition_screen.update(dt, self.transition)

    def change(self):
        if not self.event: return self
        if self.event[0] == "PlayMenu":
            return self.call(PlayMenu)
        elif self.event[0] == "Quit":
            pg.quit()
            sys.exit()
        return self

    def render(self, screen):
        for img in self.structure["imgs"].values():
            pos = img["pos"]
            pos = WIN_WIDTH * pos[0] - img["img"].get_width() // 2, WIN_HEIGHT * pos[1] - img["img"].get_height() // 2
            screen.blit(img["img"], pos)
        self.structure["stack"].render(screen, config.get_setting("button", "gap"), config.get_setting("button", "shape"))
        self.transition_screen.render(screen)


class PlayMenu(State):
    def __init__(self):
        super().__init__()
        self.tag = "PlayMenu"
        self.structure = parse(config.get_layout("PlayMenu"))
        self.transition_screen.input_img(pg.display.get_surface().copy())
        self.event = []

    def change(self):
        if not self.event: return self
        if self.event[0] == "Back":
            return self.call(MainMenu)
        elif self.event[0] == "Hum_vs_Hum":
            return self.call(ChessMenu)
        return self

    def handle_events(self, event):
        self.event = self.structure["stack"].listen(event, self.tag)

    def update(self, mos_pos, dt):
        if "stack" in self.structure: self.structure["stack"].update(mos_pos)
        self.transition = self.transition_screen.update(dt, self.transition)

    def render(self, screen):
        for img in self.structure["imgs"].values():
            pos = img["pos"]
            pos = WIN_WIDTH * pos[0] - img["img"].get_width() // 2, WIN_HEIGHT * pos[1] - img["img"].get_height() // 2
            screen.blit(img["img"], pos)
        self.structure["stack"].render(screen, config.get_setting("button", "gap"), config.get_setting("button", "shape"))
        self.transition_screen.render(screen)
