from src.settings import *
from src.resource_manager import res_manager
from src.config_manager import config


class Clock:
    def __init__(self, sand=180, team=WH, rel_pos=(0, 0)):
        self.sand = sand * 1000  # in min converting to milliseconds
        self.last = pg.time.get_ticks()
        print(f"time.start: {self.last}")
        pg.time.get_ticks()
        self.team = team
        self.offset = 20
        self.img = res_manager.get_pres(os.path.join("icons", "icons8-clock-48.png"))
        self.pos = [rel_pos[0], rel_pos[1] - 20 - self.img.get_height()]
        if self.team == WH: self.pos[1] = rel_pos[1] + 20 + SQUA * 8
        self.is_flip = self.team == WH
        self.color = "white"

    def on(self):
        self.is_flip = True

    def off(self):
        self.is_flip = False

    def update(self):
        if self.is_flip:
            self.sand -= pg.time.get_ticks() - self.last
        self.last = pg.time.get_ticks()
        if self.sand <= 0: self.sand = 0

        if 0 < self.sand // 1000 <= 10:
            self.color = "red"

    def over(self):
        return self.sand <= 0

    def render(self, screen):
        screen.blit(self.img, self.pos)
        min = str(self.sand // (1000 * 60))
        sec = str((self.sand // 1000) % 60)
        if len(min) == 1: min = "0" + min
        if len(sec) == 1: sec = "0" + sec
        screen.blit(config.get_theme("font").render(f"{min}:{sec}", True, self.color), (self.pos[0] + 50, self.pos[1] + 10))
