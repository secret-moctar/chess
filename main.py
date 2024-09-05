import os
import sys
import json

import pygame as pg

FONTDIR = os.path.join("data", "fonts")
ICONDIR = os.path.join("data", "icons")

WIN_WIDTH = 800 
WIN_HEIGHT = 600

class Button:
    def __init__(self, text, font, tcolor, bcolor, s_bcolor):
        self.text = text
        self.font = font
        self.tcolor = tcolor
        self.img = self.draw()
        self.rect = self.img.get_rect(topleft=(0, 0)).inflate(30, 10)
        self.bcolor = bcolor
        self.s_bcolor = s_bcolor
        self.hightlight = False

    def draw(self):
        return self.font.render(self.text, True, self.tcolor)

    def update(self, mos_pos):
        if self.rect.collidepoint(*mos_pos):
            self.hightlight = True
        else:
            self.hightlight = False


class CompButton(Button):
    def __init__(self, text, font, tcolor, bcolor, s_bcolor, tabs, paths):
        self.t_gap = 5
        self.tabs = tabs
        self.paths = paths
        super().__init__(text, font, tcolor, bcolor, s_bcolor)

    def update(self, mos_pos):
        super().update(mos_pos)

    def load_imgs(self):
        imgs = []
        for path in self.paths:
            if path in os.listdir(ICONDIR): 
                imgs.append(pg.transform.scale_by(pg.image.load(os.path.join(ICONDIR, path)).convert_alpha(), 0.5))
            else:
                imgs.append(self.font.render(self.text, True, self.tcolor))
        return imgs

    def draw(self):
        self.imgs = self.load_imgs()
        width, height = sum(map(lambda x:x.get_width(), self.imgs)) + sum(self.tabs), max(self.imgs, key=lambda x:x.get_height()).get_height() + 2 * self.t_gap
        img = pg.Surface((width, height))
        img.fill((100, 100, 100))
        img.set_colorkey((100, 100, 100))
        x, y = self.tabs[0], height // 2
        for i in range(len(self.imgs)):
            img.blit(self.imgs[i], (x, y - self.imgs[i].get_height() // 2))
            x += self.imgs[i].get_width() + self.tabs[i + 1]
        return img

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
            bcolor = self.bcolor if button.bcolor == "theme" else button.bcolor
            s_bcolor = self.s_bcolor if button.s_bcolor == "theme" else button.s_bcolor
            bcolor, inflame = (bcolor, (30, 10)) if not button.hightlight else (s_bcolor, (40, 15))

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
                for but_tex in self.layout_info[menu][key]["buttons"]:
                    button = self.layout_info[menu][key]["buttons"][but_tex]
                    if button["type"] == "simple":
                        structure["stack"].push(Button(but_tex, self.font, self.tcolor, button["bcolor"], button["s_bcolor"]))
                    elif button["type"] == "complex": 
                        structure["stack"].push(CompButton(but_tex, self.font, self.tcolor, button["bcolor"], button["s_bcolor"], button["tabs"], button["paths"]))
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
