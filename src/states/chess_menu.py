import sys

from src.settings import *
from src.utils import parse
from src.state import State
from src.chess_eng import ChessEng
from src.config_manager import config
from src.resource_manager import res_manager
from src.clock import Clock
from src.state_manager import state_manager
from src.eventer import event_queue, GameEvent, EventType


class ChessMenu(State):
    def __init__(self):
        super().__init__()
        self.transition_screen = self.custom_transition(form="pixel")
        self.tag = "ChessMenu"
        self.event = []
        self.surf_board = pg.Surface((SQUA * 8, SQUA * 8))
        self.board_pos = (WIN_WIDTH // 2 + 50 - self.surf_board.get_width() // 2, WIN_HEIGHT // 2 - self.surf_board.get_height() // 2)
        self.clock_w = Clock(rel_pos=self.board_pos)
        self.clock_b = Clock(team=BL, rel_pos=self.board_pos)
        self.chess_engine = ChessEng(self.board_pos, self.clock_w, self.clock_b)
        for event_type in self.chess_engine._handlers:
            for handler in self.chess_engine._handlers[event_type]:
                self._handlers[event_type].add(handler)

    def update(self, mos_pos, dt):
        super().update(mos_pos, dt)
        if self.transition_screen.is_finished():
            self.chess_engine.update(dt)
            self.clock_w.update()
            self.clock_b.update()

    def process_event(self, event):
        if not self.transition_screen.is_finished(): return
        if event.data["id"] == "Quit":
            event_queue.push(GameEvent(EventType.QuitGame, "ChessMenu", data={}))
        if event.data["id"] == "Pause":
            self.clock_w.off()
            self.clock_b.off()
        if event.data["id"] == "Back":
            self.call("PlayMenu", tweak=True, direction="right")

    @State.check_render_transition
    def render(self, screen):
        super().render(screen)
        if self.transition_screen.is_finished():
            # rendering the chess engine / borad and pieces
            self.chess_engine.render(self.surf_board)
            self.clock_w.render(screen)
            self.clock_b.render(screen)
            screen.blit(self.surf_board, self.board_pos)


state_manager.register("ChessMenu", ChessMenu)
