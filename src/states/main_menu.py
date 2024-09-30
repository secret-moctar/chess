from src.settings import *
from src.state import State
from src.config_manager import config
from src.utils import parse
from src.state_manager import state_manager
from src.blender import SlideTransition
from src.eventer import event_queue, GameEvent, EventType


class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.tag = "MainMenu"
        self.transition_screen = self.custom_transition()

    def process_event(self, event: GameEvent):
        if not self.transition_screen.is_finished(): return
        print(f"proccess: {event}")
        if event.data["id"] == "PlayMenu":
            self.call("PlayMenu")
        elif event.data["id"] == "Quit":
            event_queue.push(GameEvent(EventType.QuitGame, "UiButton", data={}))

    @State.check_render_transition
    def render(self, screen):
        super().render(screen)


state_manager.register("MainMenu", MainMenu)
