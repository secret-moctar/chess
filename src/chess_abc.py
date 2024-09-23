from abc import ABC, abstractmethod


class ChessAbc(ABC):
    @abstractmethod
    def make_move(self, move): ...

    @abstractmethod
    def undo_move(self) -> str: ...

    @abstractmethod
    def is_checkmate(self) -> bool: ...

    @abstractmethod
    def is_stalemate(self) -> bool: ...

    @abstractmethod
    def is_move_valid(self, move) -> bool: ...

    @abstractmethod
    def handle_events(self, event): ...

    @abstractmethod
    def update(self, dt): ...

    @abstractmethod
    def render(self, screen): ...
