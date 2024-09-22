import sys

from src.settings import *
from src.menu import WelcomeScreen
from src.utils import log
from src.config_manager import config


class UiEngine:
    def __init__(self):
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pg.time.Clock()
        self.state = WelcomeScreen()
        self.dt = 0
        log("Start:", "w")

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.state.handle_events(event)

    def update(self):
        mos_pos = pg.mouse.get_pos()
        self.state.update(mos_pos, self.dt)
        self.state = self.state.change()

    def render(self):
        self.screen.fill(config.get_theme("background"))
        self.state.render(self.screen)

    def run(self):
        while True:
            pg.display.set_caption(f"FPS: {self.clock.get_fps() // 1}")
            self.handle_events()
            self.update()
            self.render()
            pg.display.flip()
            self.dt = self.clock.tick(40)


if __name__ == "__main__":
    UiEngine().run()
