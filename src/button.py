from src.settings import *
from src.resource_manager import res_manager
from src.eventer import event_queue, GameEvent, EventType


class Button:
    def __init__(self, id, text, font, tcolor, bcolor, s_bcolor, event):
        pg.init()
        self.id = id
        self.text = text
        self.font = font
        self.tcolor = tcolor
        self.img = self.draw()
        self.rect = self.img.get_rect(topleft=(0, 0)).inflate(30, 10)  # need to add these values to config
        self.bcolor = bcolor
        self.s_bcolor = s_bcolor
        self.highlight = False
        self.event = event

    def draw(self):
        return self.font.render(self.text, True, self.tcolor)

    def is_on(self, pos):
        return self.rect.collidepoint(*pos)

    def on_click(self, event):
        data = event.data.copy()
        print(f"button: {self.event}, high: {self.highlight}")
        if self.is_on(data["pos"]) and data["button"] == 1:
            res_manager.get_resource("button").play()
            event_queue.push(GameEvent(EventType.UiButtonClick, "UiButton", data={"id": self.event}))
            return True
        return False

    def update(self, mos_pos):
        if self.is_on(mos_pos):
            self.highlight = True
        else:
            self.highlight = False


class CompButton(Button):
    def __init__(self, id, text, font, tcolor, bcolor, s_bcolor, tabs, paths, event):
        self.t_gap = 5
        self.tabs = tabs  # list containing the space between two images on the button
        self.paths = paths  # list of paths to the image in the button
        super().__init__(id, text, font, tcolor, bcolor, s_bcolor, event)
        # self.imgs = self.load_imgs()

    def update(self, mos_pos):
        super().update(mos_pos)

    def load_imgs(self):
        imgs = []
        for path in self.paths:
            if path in os.listdir(ICONDIR):
                # im not scaling them by the way but if i need to i will figure some way to do it.
                imgs.append(pg.transform.scale_by(res_manager.get_pres(os.path.join("icons", path)).convert_alpha(), 1))
            else:
                imgs.append(self.font.render(self.text, True, self.tcolor))
        return imgs

    def render(self, screen, rel_pos):
        width = sum(map(lambda x: x.get_width(), self.imgs)) + sum(self.tabs)
        height = max(self.imgs, key=lambda x: x.get_height()).get_height() + 2 * self.t_gap
        x, y = self.tabs[0], height // 2
        for i in range(len(self.imgs)):
            screen.blit(self.imgs[i], (rel_pos[0] + x, rel_pos[1] + y - self.imgs[i].get_height() // 2))
            x += self.imgs[i].get_width() + self.tabs[i + 1]

    def draw(self):
        self.imgs = self.load_imgs()
        """Depecracated, but due to the principle of if it's works don't touch it i din't dorp it
            it is nessary cause in the parent class(Button) we use this function to get the rect and after that
            use rect.inflate(x, y) to have thes beautifull outline
        """
        width, height = sum(map(lambda x: x.get_width(), self.imgs)) + sum(self.tabs), max(self.imgs, key=lambda x: x.get_height()).get_height() + 2 * self.t_gap
        img = pg.Surface((width, height))
        # img.fill((1, 2, 3))
        img.set_colorkey((0, 0, 0))
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
        """This will come handy when we start to implement pop up screen and stuff that dynamicaly get called"""
        self.pos[0] += x
        self.pos[1] += y

    def moveto(self, x, y):
        """the same goes for this one also"""
        self.pos = [x, y]

    def push(self, button):
        """push any thing that follow the listen, update, also and render structure if you support these three function you can be added to the stack no problem"""
        self.stack.append(button)

    def get_button_clicked(self, pos):
        for button in self.stack:
            if button.is_clicked(pos):
                return button.event

    def get_buttons(self):
        return self.stack

    def update(self, mos_pos):
        for button in self.stack:
            button.update(mos_pos)

    def listen(self, user_event, tag):
        mon_event = []
        for button in self.stack:
            if button.event.b_type == user_event.type and button.event.b_key == user_event.button:
                if button.highlight:
                    res_manager.get_resource("button").play()
                    mon_event.append(button.event.event_id)
        return mon_event

    def render(self, screen, gap, shape):
        acc = 0
        for i in range(len(self.stack)):
            roundness = 0
            if shape == "rounded": roundness = 7
            button = self.stack[i]
            bcolor = self.bcolor if button.bcolor == "theme" else button.bcolor
            s_bcolor = self.s_bcolor if button.s_bcolor == "theme" else button.s_bcolor
            bcolor, inflame = (bcolor, (30, 10)) if not button.highlight else (s_bcolor, (40, 15))

            button.rect = button.img.get_rect(center=(self.pos[0], self.pos[1] + acc)).inflate(*inflame)
            pg.draw.rect(screen, bcolor, button.rect, border_radius=roundness)
            if isinstance(button, CompButton):
                button.render(screen, (button.rect.centerx - button.img.get_width() // 2, button.rect.centery - button.img.get_height() // 2))
            else:
                screen.blit(button.img, (button.rect.centerx - button.img.get_width() // 2, button.rect.centery - button.img.get_height() // 2))
            acc += button.img.get_height() + gap
