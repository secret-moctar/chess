import sys

from src.settings import *
from src.state import State
from src.config_manager import config
from src.utils import parse
from src.state_manager import state_manager


class PlayMenu(State):
    def __init__(self):
        super().__init__()
        self.tag = "PlayMenu"
        self.transition_screen = self.custom_transition()

    def process_event(self, event):
        if not self.transition_screen.is_finished(): return
        if event.data["id"] == "Back":
            self.call("MainMenu", tweak=True, direction="right")
        elif event.data["id"] == "Hum_vs_Hum":
            self.call("ChessMenu", form="pixel")

    @State.check_render_transition
    def render(self, screen):
        super().render(screen)

state_manager.register("PlayMenu", PlayMenu)
