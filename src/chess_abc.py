from abc import ABC, abstractmethod


class ChessAbc(ABC):
    @abstractmethod
    def __init__(self, rel_pos, w_clock, b_clock, org=True): ...

    @abstractmethod
    def make_move(self, move, real=True): ...

    @abstractmethod
    def undo_move(self) -> str: ...

    @abstractmethod
    def is_checkmate(self, color) -> bool: ...

    @abstractmethod
    def is_stalemate(self, color) -> bool: ...

    @abstractmethod
    def is_move_valid(self, move) -> bool: ...

    @abstractmethod
    def update(self, dt): ...

    @abstractmethod
    def render(self, screen): ...
