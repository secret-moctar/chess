import sys

from src.settings import *
from src.state import State
from src.config_manager import config
from src.utils import parse
from src.state_manager import state_manager
from src.blender import SlideTransition


class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.tag = "MainMenu"
        self.structure = parse(config.get_layout("MainMenu"))
        self.transition_screen = self.custom_transition()
        self.event = []

    def handle_events(self, event):
        if not self.transition_screen.is_finished(): return
        self.event = []
        if "stacks" in self.structure:
            for stack in self.structure["stacks"].values():
                events = stack.listen(event, self.tag)
                for even in events: self.event.append(even)

    def update(self, mos_pos, dt):
        if self.transition_screen.is_finished():
            if "stacks" in self.structure:
                for stack in self.structure["stacks"].values():
                    stack.update(mos_pos)
        else:
            self.transition_screen.update(dt)
        self.change()

    def change(self):
        if not self.event: return
        if self.event[0] == "PlayMenu":
            self.call("PlayMenu")
        elif self.event[0] == "Quit":
            pg.time.delay(500)
            pg.quit()
            sys.exit()

    def render(self, screen):
        if self.transition: screen = self.get_new_window()
        if self.transition_screen.is_finished():
            for img in self.structure["imgs"].values():
                pos = img["pos"]
                pos = WIN_WIDTH * pos[0] - img["img"].get_width() // 2, WIN_HEIGHT * pos[1] - img["img"].get_height() // 2
                screen.blit(img["img"], pos)
            if "stacks" in self.structure:
                for stack in self.structure["stacks"].values():
                    stack.render(screen, config.get_setting("button", "gap"), config.get_setting("button", "shape"))
            if self.transition:
                self.transition_screen.start(screen)
                self.transition = False
        else:
            self.transition_screen.render(screen)

state_manager.register("MainMenu", MainMenu)
