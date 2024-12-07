import sys

from src.settings import *
from src.utils import log
from src.config_manager import config
from src.resource_manager import res_manager
from src.state_manager import state_manager
import src.loader  # this is important don't delete it imtalking to the future me
from src.eventer import event_queue, event_dispatcher, EventType, GameEvent


class UiEngine:
    def __init__(self):
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pg.display.set_icon(res_manager.get_resource("chess_title"))
        self.clock = pg.time.Clock()
        state_manager.change_state("WelcomeScreen")
        self.dt = 0
        event_dispatcher.register(EventType.QuitGame, self.quit)
        log("Start:", "w")

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                event_queue.push(GameEvent(EventType.QuitGame, "PYGAME", data={}))
            if event.type == pg.MOUSEBUTTONDOWN:
                event_queue.push(
                    GameEvent(
                        EventType.MouseDown,
                        "PYGAME",
                        data={"pos": event.pos, "button": event.button},
                    )
                )
            if event.type == pg.MOUSEBUTTONUP:
                event_queue.push(
                    GameEvent(
                        EventType.MouseUp,
                        "PYGAME",
                        data={"pos": event.pos, "button": event.button},
                    )
                )
            if event.type == pg.KEYDOWN:
                event_queue.push(
                    GameEvent(EventType.KeyDown, "PYGAME", data={"key": event.key})
                )
                if event.key == pg.K_SPACE:
                    print("#" * 40)
                    event_dispatcher.display()
                    print("#" * 40)

    def proccess_events(self):
        if not event_queue.is_empty():
            print("#" * 40)
            print("event_queue:", end="\t")
            event_queue.display()
            print("#" * 40)
        while True:
            event = event_queue.pop()
            if not event:
                break
            event_dispatcher.dispatch(event)

    def quit(self, event):
        pg.time.delay(500)
        sys.exit()
        pg.quit()

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
            self.proccess_events()
            self.update()
            self.render()
            pg.display.flip()
            self.dt = self.clock.tick(FPS) / 1000  # to seconds


if __name__ == "__main__":
    UiEngine().run()
