from typing import Optional

from pygame.surface import Surface
from src.settings import *
from src.blender import SlideTransition, PixelateTransition, ZoomTransition
from src.state_manager import state_manager
from src.config_manager import config
from src.utils import log


class State:
    def __init__(self):
        self.transition_screen = None
        self.transition = True

    def enter(self, other=None): ...

    def set_transition_screen(self, transition_screen):
        self.transition_screen = transition_screen

    def get_new_window(self):
        window = pg.Surface((WIN_WIDTH, WIN_HEIGHT))
        window.fill(config.get_theme("background"))
        return window

    def call(self, obj_id, **kwargs):
        self.event = []
        state_manager.change_state(obj_id)
        state_manager.current_state.enter(other=self)
        transition_screen = self.custom_transition(**kwargs)
        state_manager.current_state.set_transition_screen(transition_screen)

    def custom_transition(self, **kwargs):
        surface = pg.display.get_surface()
        kv = dict(kwargs.items())
        if kv:
            if "form" in kv:
                if kv["form"] == "slider":
                    return SlideTransition(surface, **kwargs)
                if kv["form"] == "pixel":
                    print("THast me asffffffffff")
                    return PixelateTransition(surface, **kwargs)
                if kv["form"] == "zoom":
                    return ZoomTransition(surface, **kwargs)

            else:
                return SlideTransition(surface, **kwargs)
        return SlideTransition(surface)


    def recall(self):
        self.prev_state.enter()
        return self.prev_state

    def handle_events(self, event): ...
    def change(self): ...
    def exit(self): ...
    def update(self, mos_pos, dt): ...
    def render(self, screen): ...
    def goto(self): ...
