from src.settings import *
from src.state import State
from src.utils import parse
from src.config_manager import config
from src.state_manager import state_manager


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
        if pg.time.get_ticks() / 1000 - self.s_time > 0.8:
            self.goto()
        self.change()

    def change(self):
        if not self.switch: return
        self.call("MainMenu", form="zoom")

    def render(self, screen):
        for img in self.structure["imgs"].values():
            pos = img["pos"]
            scaleby = img["scaleby"]
            picture = pg.transform.scale_by(img["img"], scaleby)
            pos = WIN_WIDTH * pos[0] - picture.get_width() // 2, WIN_HEIGHT * pos[1] - picture.get_height() // 2
            screen.blit(picture, pos)

state_manager.register("WelcomeScreen", WelcomeScreen)
