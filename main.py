from src.settings import*
from src.button import Button, CompButton, StackButton


class UiEngine:
    def __init__(self):
        pg.init()
        self.font = pg.font.Font(f"{FONTDIR}/FiraCode-SemiBold.ttf", 20)
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pg.time.Clock()
        self.options = OPTIONS 
        self.offsetX = 0
        self.offsetY = 0
        self.tcolor = self.options["button"]["text"]
        self.bcolor = self.options["button"]["background"]
        self.s_bcolor = self.options["button"]["sbackground"]
        self.strcutre = self.parse(LAYOUT_INFO["Welcome"])

    def parse(self, menu):
        structure = {"imgs": {}, "stack": {}}
        for key in menu:
            if key == "imgs":
                for img in menu[key]:
                    path = os.path.join(ICONDIR, menu[key][img]["path"])
                    pos = menu[key][img]["pos"]
                    structure["imgs"][img] = {"img":pg.image.load(path).convert_alpha(), "pos":pos}
            if key == "stack":
                pos = menu[key]["pos"]
                pos = WIN_WIDTH * pos[0], WIN_HEIGHT * pos[1]
                structure["stack"] = StackButton(pos, self.tcolor, self.bcolor, self.s_bcolor)
                for but_tex in menu[key]["buttons"]:
                    button = menu[key]["buttons"][but_tex]
                    if button["type"] == "simple":
                        structure["stack"].push(Button(button["id"], but_tex, self.font, self.tcolor, button["bcolor"], button["s_bcolor"]))
                    elif button["type"] == "complex": 
                        structure["stack"].push(CompButton(button["id"], but_tex, self.font, self.tcolor, button["bcolor"], button["s_bcolor"], button["tabs"], button["paths"]))
        return structure

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
            self.strcutre["stack"].listen(event)

    def update(self):
        mos_pos = pg.mouse.get_pos()
        self.strcutre["stack"].update(mos_pos)

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
