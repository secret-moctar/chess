from src.settings import*


class ButtonEvent:
    def __init__(self, b_type=pg.MOUSEBUTTONDOWN, b_key = 1):
        self.b_type = b_type
        self.b_key = b_key

class Button:
    def __init__(self, id, text, font, tcolor, bcolor, s_bcolor):
        pg.init()
        self.id = id
        self.text = text
        self.font = font
        self.tcolor = tcolor
        self.img = self.draw()
        self.rect = self.img.get_rect(topleft=(0, 0)).inflate(30, 10)
        self.bcolor = bcolor
        self.s_bcolor = s_bcolor
        self.hightlight = False
        self.event = ButtonEvent()

    def draw(self):
        return self.font.render(self.text, True, self.tcolor)

    def update(self, mos_pos):
        if self.rect.collidepoint(*mos_pos):
            self.hightlight = True
        else:
            self.hightlight = False


class CompButton(Button):
    def __init__(self, id, text, font, tcolor, bcolor, s_bcolor, tabs, paths):
        self.t_gap = 5
        self.tabs = tabs
        self.paths = paths
        super().__init__(id, text, font, tcolor, bcolor, s_bcolor)

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
        self.s_event = []

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

    def listen(self, user_event):
        for button in self.stack:
                if button.event.b_type == user_event.type and button.event.b_key == user_event.button:
                    if button.hightlight:
                        print("action")
                        self.broadcast(button.id)

    def broadcast(self, id):
        self.s_event.append(ID_ACTION[id])
        print(self.s_event)


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
