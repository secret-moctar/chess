import os
import sys
import json

import pygame as pg

FONTDIR = os.path.join("data", "fonts")
ICONDIR = os.path.join("data", "icons")

WIN_WIDTH = 800 
WIN_HEIGHT = 600

class Button:
    def __init__(self, text, font, tcolor):
        self.text = text
        self.img = font.render(self.text, True, tcolor)
        self.rect = self.img.get_rect(topleft=(0, 0)).inflate(30, 10)
        self.hightlight = False

    def set_color(tcolor):
        self.img = font.render(self.text, True, tcolor)

    def update(self, mos_pos):
        if self.rect.collidepoint(*mos_pos):
            self.hightlight = True
        else:
            self.hightlight = False


class CompButton:
    def __init__(self, text, font, tcolor, bcolor):
        self.text = text
        self.t_gap = 5
        self.cmps = []
        self.img = None
        self.surf = self.compose()

    def add_component(self, path):
        self.cmps.add(pg.image.load(path).convert())

    def compose(self):
        width, height = self.t_gap, self.t_gap
        for cmp in self.cmps:
            width += cmp.get_width() + self.t_gap
        height += max(self.cmps, key=lambda x:x.get_height()).get_height() + self.t_gap
        return pg.Surface((width, height))

class StackButton:
    def __init__(self, pos, tcolor, bcolor, s_bcolor):
        self.pos = list(pos)
        self.stack = []
        self.bcolor = bcolor
        self.tcolor = tcolor
        self.s_bcolor = s_bcolor

    def moveby(self, x, y):
        self.pos[0] += x
        self.pos[1] += y

    def moveto(self, x, y):
        self.pos = [x, y]

    def push(self, button):
        self.stack.append(button)

    def update(self, mos_pos):
        self.check_collide(mos_pos)

    def check_collide(self, mos_pos):
        for button in self.stack:
            button.update(mos_pos)

    def render(self, screen, gap, shape):
        acc = 0
        for i in range(len(self.stack)):
            roundness = 0
            if shape == "rounded": roundness = 7
            button = self.stack[i]
            bcolor, inflame = (self.bcolor, (30, 10)) if not button.hightlight else (self.s_bcolor, (40, 15))
            button.rect = button.img.get_rect(center=(self.pos[0], self.pos[1] + acc)).inflate(*inflame)
            pg.draw.rect(screen, bcolor, button.rect, border_radius=roundness)
            screen.blit(button.img, (button.rect.centerx - button.img.get_width() // 2, button.rect.centery - button.img.get_height() // 2))
            acc += button.img.get_height() + gap

class UiEngine:
    def __init__(self):
        pg.init()
        self.layout_info = self.load_config("layout.json")
        self.font = pg.font.Font(f"{FONTDIR}/FiraCode-SemiBold.ttf", 20)
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pg.time.Clock()
        self.options = self.load_config("settings.json")
        self.offsetX = 0
        self.offsetY = 0
        self.tcolor = self.options["button"]["text"]
        self.bcolor = self.options["button"]["background"]
        self.s_bcolor = self.options["button"]["sbackground"]
        self.strcutre = self.parse("Welcome")

    def parse(self, menu):
        structure = {"imgs": {}, "stack": {}}
        for key in self.layout_info[menu]:
            if key == "imgs":
                for img in self.layout_info[menu][key]:
                    path = os.path.join(ICONDIR, self.layout_info[menu][key][img]["path"])
                    pos = self.layout_info[menu][key][img]["pos"]
                    structure["imgs"][img] = {"img":pg.image.load(path).convert_alpha(), "pos":pos}
            if key == "stack":
                pos = self.layout_info[menu][key]["pos"]
                pos = WIN_WIDTH * pos[0], WIN_HEIGHT * pos[1]
                structure["stack"] = StackButton(pos, self.tcolor, self.bcolor, self.s_bcolor)
                for button in self.layout_info[menu][key]["buttons"]:
                    structure["stack"].push(Button(button, self.font, self.tcolor))
        return structure
        

    def load_config(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_j: self.offsetY += 10
                if event.key == pg.K_k: self.offsetY -= 10
                if event.key == pg.K_h: self.offsetX -= 10
                if event.key == pg.K_l: self.offsetX += 10

    def update(self):
        mos_pos = pg.mouse.get_pos()
        self.strcutre["stack"].update(mos_pos)

    def img_mat(self):
        accY = 0
        j = 0
        while True:
            max_accY = 0
            accX = 0
            for i in range(3):
                index = j * 3 + i
                if index >= len(self.imgs): return
                img = self.imgs[index]
                gap = self.options["button"]["gap"]
                self.screen.blit(img, (-self.offsetX + accX , -self.offsetY + accY))
                accX += img.get_width() + gap
                max_accY = max(max_accY, img.get_height())
            accY += max_accY + gap
            j += 1

    def render(self):
        self.screen.fill(self.options["theme"]["background"])
        for img in self.strcutre["imgs"].values():
            pos = img["pos"]
            pos = WIN_WIDTH * pos[0] - img["img"].get_width() // 2, WIN_HEIGHT * pos[1] - img["img"].get_height() // 2
            self.screen.blit(img["img"], pos)
        self.strcutre["stack"].render(self.screen, self.options["button"]["gap"], self.options["button"]["shape"])

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            pg.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    UiEngine().run()
