from abc import ABC, abstractmethod

from src.settings import *


class BlendABC(ABC):
    @abstractmethod
    def update(self, dt): ...

    @abstractmethod
    def render(self, screen): ...

    @abstractmethod
    def start(self, to_surface): ...

    @abstractmethod
    def is_finished(self) -> bool: ...


class SlideTransition(BlendABC):
    def __init__(self, from_surface, duration=0.3, direction="left", **kwargs):
        self.duration = duration
        self.direction = direction
        self.progress = 0
        self.from_surface = from_surface.copy()
        self.to_surface = None

    def start(self, to_surface):
        self.to_surface = to_surface.copy()
        self.progress = 0.0001

    def update(self, dt):
        self.progress += dt / self.duration
        self.progress = min(1.0, self.progress)

    def render(self, screen):
        width, height = screen.get_size()
        if self.direction == "left":
            screen.blit(self.from_surface, (width * -self.progress, 0))
            screen.blit(self.to_surface, (width * (1 - self.progress), 0))
        elif self.direction == "right":
            screen.blit(self.from_surface, (width * self.progress, 0))
            screen.blit(self.to_surface, (width * (self.progress - 1), 0))
        # Add more directions as needed

    def is_finished(self):
        return self.progress >= 1.0 or self.progress == 0


class PixelateTransition(BlendABC):
    def __init__(self, from_surface, duration=1.0, max_pixel_size=32, **kwargs):
        self.duration = duration
        self.max_pixel_size = max_pixel_size
        self.progress = 0
        self.from_surface = from_surface.copy()
        self.to_surface = None

    def start(self, to_surface):
        self.to_surface = to_surface.copy()
        self.progress = 0.0001

    def update(self, dt):
        self.progress += dt / self.duration
        self.progress = min(1.0, self.progress)

    def render(self, screen):
        width, height = screen.get_size()
        if self.progress < 0.5:
            pixel_size = int(self.max_pixel_size * (self.progress * 2))
            if not pixel_size: pixel_size = 1
            small = pg.transform.scale(self.from_surface, (width // pixel_size, height // pixel_size))
            pixelated = pg.transform.scale(small, (width, height))
            screen.blit(pixelated, (0, 0))
        else:
            pixel_size = int(self.max_pixel_size * ((1 - self.progress) * 2))
            if not pixel_size: pixel_size = 1
            small = pg.transform.scale(self.to_surface, (width // pixel_size, height // pixel_size))
            pixelated = pg.transform.scale(small, (width, height))
            screen.blit(pixelated, (0, 0))
        del small
        del pixelated

    def is_finished(self):
        return self.progress >= 1.0 or self.progress == 0


class ZoomTransition(BlendABC):
    def __init__(self, from_surface, duration=1.0, **kwargs):
        self.duration = duration
        self.progress = 0
        self.from_surface = from_surface.copy()
        self.to_surface = None

    def start(self, to_surface):
        self.to_surface = to_surface.copy()
        self.progress = 0.0001

    def update(self, dt):
        self.progress += dt / self.duration
        self.progress = min(1.0, self.progress)

    def render(self, screen):
        width, height = screen.get_size()
        if self.progress < 0.5:
            scale = 1 - self.progress * 2
            scaled = pg.transform.scale(self.from_surface, (int(width * scale), int(height * scale)))
            screen.blit(scaled, ((width - scaled.get_width()) // 2, (height - scaled.get_height()) // 2))
        else:
            scale = (self.progress - 0.5) * 2
            scaled = pg.transform.scale(self.to_surface, (int(width * scale), int(height * scale)))
            screen.blit(scaled, ((width - scaled.get_width()) // 2, (height - scaled.get_height()) // 2))

    def is_finished(self):
        return self.progress >= 1.0 or self.progress == 0
