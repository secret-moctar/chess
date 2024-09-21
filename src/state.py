from src.settings import *
from src.utils import log


class State:
    def __init__(self):
        self.prev_state = None
        self.transition_screen = BlendMenu()
        self.transition = True

    def enter(self, other=None):
        self.prev_state = other
        log(f"{self.prev_state}")

    def call(self, obj):
        self.event = []
        next_state = obj()
        next_state.enter(other=self)
        return next_state

    def recall(self):
        self.prev_state.enter()
        return self.prev_state

    def handle_events(self, event): ...
    def change(self): ...
    def exit(self): ...
    def update(self, mos_pos, dt): ...
    def render(self, screen): ...
    def goto(self): ...


class BlendMenu:
    def __init__(self):
        self.img = pg.Surface((WIN_WIDTH, WIN_HEIGHT))
        self.alpha = 255  # opacity
        self.offsetX = 0
        self.offsetY = 0
        self.fade_in = 1
        self.size = [WIN_WIDTH, WIN_HEIGHT]

    def input_alpha(self, alpha):
        self.alpha = alpha

    def input_img(self, img):
        self.img = img

    def update(self, dt, transition):
        if transition:
            self.alpha -= self.fade_in * dt
            self.offsetX -= self.fade_in * dt * (WIN_WIDTH / WIN_HEIGHT)
            self.offsetY -= self.fade_in * dt
            self.size[1] -= self.fade_in * dt * 2
            self.size[0] -= self.fade_in * dt * (WIN_WIDTH / WIN_HEIGHT) * 2
        if self.size[0] < 0 or self.size[1] < 0: self.size = [0, 0]
        if self.offsetX < -WIN_WIDTH: transition = False
        self.alpha = max(0, self.alpha)
        self.img.set_alpha(self.alpha)
        return transition

    def render(self, screen):
        screen.blit(pg.transform.scale(self.img, self.size), (self.offsetX, self.offsetY))
