from collections import defaultdict

from pygame.surface import Surface
from src.settings import *
from src.blender import SlideTransition, PixelateTransition, ZoomTransition
from src.state_manager import state_manager
from src.config_manager import config
from src.utils import parse, log
from src.eventer import event_dispatcher, EventType


class State:
    def __init__(self):
        self.transition_screen = None
        self.transition = True
        self.structure = parse(config.get_layout(self.__class__.__name__))
        self._handlers = defaultdict(set)

        buttons = self.get_all_buttons()
        for button in buttons:
            self._handlers[EventType.MouseDown].add(button.on_click)
        self._handlers[EventType.UiButtonClick].add(self.process_event)

    def process_event(self, event): ...
    def change(self): ...
    def goto(self): ...

    def get_all_buttons(self):
        if "stacks" in self.structure:
            all_buttons = set()
            for stack in self.structure["stacks"].values():
                for button in stack.get_buttons():
                    all_buttons.add(button)
            return all_buttons
        return set()

    def enter(self):
        for event_type in self._handlers:
            for handler in self._handlers[event_type]:
                event_dispatcher.register(event_type, handler)

    def exit(self):
        for event_type in self._handlers:
            for handler in self._handlers[event_type]:
                event_dispatcher.unregister(event_type, handler)

    def set_transition_screen(self, transition_screen):
        self.transition_screen = transition_screen

    def get_new_window(self):
        window = pg.Surface((WIN_WIDTH, WIN_HEIGHT))
        window.fill(config.get_theme("background"))
        return window

    def call(self, obj_id, **kwargs):
        state_manager.change_state(obj_id)
        state_manager.current_state.enter()
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
                    return PixelateTransition(surface, **kwargs)
                if kv["form"] == "zoom":
                    return ZoomTransition(surface, **kwargs)

            else:
                return SlideTransition(surface, **kwargs)
        return SlideTransition(surface)

    def update(self, mos_pos, dt):
        if self.transition_screen.is_finished():
            if "stacks" in self.structure:
                for stack in self.structure["stacks"].values():
                    stack.update(mos_pos)
        else:
            self.transition_screen.update(dt)

    def check_render_transition(func):
        def wrapper_function(self, screen):
            if self.transition: screen = self.get_new_window()
            if self.transition_screen.is_finished():
                func(self, screen)
                if self.transition:
                    self.transition_screen.start(screen)
                    self.transition = False
            else:
                self.transition_screen.render(screen)
        return wrapper_function

    def draw_images(self, screen):
        for img in self.structure["imgs"].values():
            pos = img["pos"]
            pos = WIN_WIDTH * pos[0] - img["img"].get_width() // 2, WIN_HEIGHT * pos[1] - img["img"].get_height() // 2
            screen.blit(img["img"], pos)

    def render_stacks(self, screen):
        for stack in self.structure["stacks"].values():
            stack.render(screen, config.get_setting("button", "gap"), config.get_setting("button", "shape"))

    def render(self, screen):
        if "imgs" in self.structure:
            self.draw_images(screen)
        if "stacks" in self.structure:
            self.render_stacks(screen)
