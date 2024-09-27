import sys

from src.settings import *
from src.utils import log
from src.config_manager import config
from src.resource_manager import res_manager
from src.state_manager import state_manager
import src.loader  # this is important don't delete it imtalking to the future me


class UiEngine:
    def __init__(self):
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pg.display.set_icon(res_manager.get_resource("chess_title"))
        self.clock = pg.time.Clock()
        state_manager.change_state("WelcomeScreen")
        self.dt = 0
        log("Start:", "w")

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            state_manager.current_state.handle_events(event)

    def update(self):
        mos_pos = pg.mouse.get_pos()
        state_manager.current_state.update(mos_pos, self.dt)

    def render(self):
        self.screen.fill(config.get_theme("background"))
        state_manager.current_state.render(self.screen)

    def run(self):
        while True:
            pg.display.set_caption(f"FPS: {self.clock.get_fps() // 1}")
            self.handle_events()
            self.update()
            self.render()
            pg.display.flip()
            self.dt = self.clock.tick(FPS) / 1000 # to seconds


if __name__ == "__main__":
    UiEngine().run()
